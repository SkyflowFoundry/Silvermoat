import os
import json
import boto3
import urllib.request
import urllib.error

s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb")


def send(event, status, data, phys_id, reason=None):
    if reason is None:
        reason = "See CloudWatch logs for details"

    response_body = {
        "Status": status,
        "Reason": reason,
        "PhysicalResourceId": phys_id,
        "StackId": event["StackId"],
        "RequestId": event["RequestId"],
        "LogicalResourceId": event["LogicalResourceId"],
        "Data": data,
    }

    body = json.dumps(response_body).encode("utf-8")
    response_url = event.get("ResponseURL")

    if not response_url:
        raise ValueError("ResponseURL is missing from event")

    print(f"Sending {status} response to CloudFormation")
    print(f"ResponseURL: {response_url[:100]}...")  # Log partial URL for security

    req = urllib.request.Request(
        response_url,
        data=body,
        method="PUT",
        headers={
            "content-type": "",
            "content-length": str(len(body)),
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            response_code = response.getcode()
            print(f"Response sent successfully. HTTP {response_code}")
            if response_code != 200:
                print(f"Warning: Expected 200, got {response_code}")
    except urllib.error.HTTPError as e:
        error_msg = f"HTTP error sending response: {e.code} {e.reason}"
        print(error_msg)
        try:
            error_body = e.read().decode("utf-8")
            print(f"Error response body: {error_body}")
        except Exception:
            pass
        raise Exception(f"Could not send response to CloudFormation: {error_msg}")
    except Exception as e:
        error_msg = f"Failed to send response: {type(e).__name__}: {str(e)}"
        print(error_msg)
        print(f"Body length: {len(body)}")
        print(f"Response body preview: {body[:200]}")
        raise Exception(f"Could not send response to CloudFormation: {error_msg}")


def empty_bucket(bucket):
    print(f"Emptying bucket: {bucket}")
    deleted_count = 0

    # Delete all object versions + delete markers (works for versioned and non-versioned buckets)
    try:
        paginator = s3.get_paginator("list_object_versions")
        for page in paginator.paginate(Bucket=bucket):
            to_delete = []

            for v in page.get("Versions", []):
                to_delete.append({"Key": v["Key"], "VersionId": v["VersionId"]})

            for m in page.get("DeleteMarkers", []):
                to_delete.append({"Key": m["Key"], "VersionId": m["VersionId"]})

            if to_delete:
                for i in range(0, len(to_delete), 1000):
                    batch = to_delete[i : i + 1000]
                    s3.delete_objects(Bucket=bucket, Delete={"Objects": batch})
                    deleted_count += len(batch)
                    print(f"Deleted {len(batch)} object versions/markers from {bucket}")
    except s3.exceptions.NoSuchBucket:
        print(f"Bucket {bucket} does not exist, skipping")
        return
    except Exception as e:
        # If bucket is not versioned or API is restricted, fall back to non-versioned deletion
        error_name = type(e).__name__
        if "NoSuchBucket" in error_name or "404" in str(e):
            print(f"Bucket {bucket} does not exist, skipping")
            return
        print(f"list_object_versions failed or not applicable for {bucket}: {error_name}: {e}")

    # Delete current objects (covers non-versioned and any remaining current keys)
    token = None
    while True:
        kwargs = {"Bucket": bucket}
        if token:
            kwargs["ContinuationToken"] = token
        try:
            r = s3.list_objects_v2(**kwargs)
            objs = [{"Key": o["Key"]} for o in r.get("Contents", [])]
            if objs:
                for i in range(0, len(objs), 1000):
                    batch = objs[i : i + 1000]
                    s3.delete_objects(Bucket=bucket, Delete={"Objects": batch})
                    deleted_count += len(batch)
                    print(f"Deleted {len(batch)} objects from {bucket}")
            if r.get("IsTruncated"):
                token = r.get("NextContinuationToken")
            else:
                break
        except s3.exceptions.NoSuchBucket:
            print(f"Bucket {bucket} does not exist, skipping")
            return
        except Exception as e:
            error_name = type(e).__name__
            if "NoSuchBucket" in error_name or "404" in str(e):
                print(f"Bucket {bucket} does not exist, skipping")
                return
            raise

    if deleted_count == 0:
        print(f"Bucket {bucket} was already empty")
    else:
        print(f"Bucket {bucket} emptied successfully ({deleted_count} items deleted)")


def wipe_table(name):
    t = ddb.Table(name)
    start_key = None
    while True:
        kwargs = {"ProjectionExpression": "id"}
        if start_key:
            kwargs["ExclusiveStartKey"] = start_key
        r = t.scan(**kwargs)
        for it in r.get("Items", []):
            t.delete_item(Key={"id": it["id"]})
        start_key = r.get("LastEvaluatedKey")
        if not start_key:
            break


def handler(event, context):
    print(f"Custom Resource Handler invoked. RequestType: {event.get('RequestType')}")
    print(f"Event keys: {list(event.keys())}")

    props = event.get("ResourceProperties", {})
    mode = props.get("Mode", "seed")
    request_type = event.get("RequestType", "Create")

    print(f"Mode: {mode}")
    print(f"Processing RequestType: {request_type}, Mode: {mode}")

    phys_id = f"silvermoat-{mode}-{event.get('StackId','').split('/')[-1]}"

    try:
        ui_bucket = os.environ["UI_BUCKET"]
        docs_bucket = os.environ["DOCS_BUCKET"]
        tables = [
            os.environ["QUOTES_TABLE"],
            os.environ["POLICIES_TABLE"],
            os.environ["CLAIMS_TABLE"],
            os.environ["PAYMENTS_TABLE"],
            os.environ["CASES_TABLE"],
        ]
        api = os.environ.get("API_BASE", "")
        web = os.environ.get("WEB_BASE", "")

        print(f"UI_BUCKET: {ui_bucket}")
        print(f"DOCS_BUCKET: {docs_bucket}")
        print(f"API_BASE: {api}")
        print(f"WEB_BASE: {web}")

        # -------------------------
        # Cleanup mode
        # -------------------------
        if mode == "cleanup":
            if request_type == "Delete":
                print("Starting cleanup...")
                for tn in tables:
                    print(f"Wiping table: {tn}")
                    wipe_table(tn)

                print(f"Emptying bucket: {ui_bucket}")
                empty_bucket(ui_bucket)

                print(f"Emptying bucket: {docs_bucket}")
                empty_bucket(docs_bucket)

                send(event, "SUCCESS", {"message": "cleaned"}, phys_id, "Cleanup completed successfully")
            else:
                # Create/Update: no-op
                print("Cleanup mode: Create/Update - no action needed")
                send(event, "SUCCESS", {"message": "cleanup resource ready"}, phys_id, "Cleanup resource initialized")
            return

        # -------------------------
        # Seed mode
        # -------------------------
        if mode == "seed":
            if request_type == "Delete":
                # Delete: no-op (cleanup is handled by CleanupCustomResource)
                print("Seed mode: Delete - no action needed")
                send(event, "SUCCESS", {"message": "seed resource deleted"}, phys_id, "Seed resource deleted")
                return

            if request_type in ["Create", "Update"]:
                print("Starting seeding process...")

                # Seed UI (only if UiSeedingMode is "seeded")
                ui_seeding_mode = props.get("UiSeedingMode", "seeded")
                print(f"UiSeedingMode: {ui_seeding_mode}")

                if ui_seeding_mode == "seeded":
                    print(f"Uploading index.html to {ui_bucket}")
                    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Silvermoat Insurance Demo</title></head>
<body style="font-family:Arial;padding:24px">
  <h1>Silvermoat Insurance</h1>
  <p>One-shot CloudFormation MVP (S3 Website Hosting)</p>
  <ul>
    <li>API Base: <code>{api}</code></li>
    <li>Web Base: <code>{web}</code></li>
  </ul>
  <button id="btn">Create Quote</button>
  <pre id="out" style="margin-top:16px;background:#f7f7f7;padding:12px;border-radius:8px;"></pre>
  <script>
    const out = document.getElementById("out");
    document.getElementById("btn").onclick = async () => {{
      const r = await fetch("{api}/quote", {{
        method:"POST",
        headers:{{"content-type":"application/json"}},
        body: JSON.stringify({{"name":"Jane Doe","zip":"33431"}})
      }});
      out.textContent = await r.text();
    }};
  </script>
</body></html>"""

                    s3.put_object(
                        Bucket=ui_bucket,
                        Key="index.html",
                        Body=html.encode("utf-8"),
                        ContentType="text/html",
                    )
                    print("index.html uploaded successfully")
                else:
                    print(f"UiSeedingMode is '{ui_seeding_mode}' - skipping index.html upload (UI should be deployed externally)")

                # Seed DynamoDB
                print("Seeding DynamoDB tables with rich demo data...")

                import time
                from random import choice, randint, random

                def put(table, item):
                    ddb.Table(table).put_item(Item=item)

                # Helper functions for generating realistic data
                def random_name():
                    firsts = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Jessica", "William", "Jennifer", "James", "Linda", "Richard", "Patricia", "Joseph", "Mary", "Thomas", "Barbara", "Charles", "Elizabeth"]
                    lasts = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
                    return f"{choice(firsts)} {choice(lasts)}"

                def random_email(name):
                    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com"]
                    safe_name = name.lower().replace(" ", ".")
                    return f"{safe_name}{randint(1,999)}@{choice(domains)}"

                def random_phone():
                    return f"{randint(200,999)}{randint(200,999)}{randint(1000,9999)}"

                def random_address():
                    streets = ["Main St", "Oak Ave", "Maple Dr", "Park Blvd", "Lake Rd", "Hill Ct", "Pine St", "Cedar Ln", "Elm Dr", "Washington St"]
                    return f"{randint(100,9999)} {choice(streets)}"

                def random_city_state():
                    cities = [
                        ("Miami", "FL"), ("Tampa", "FL"), ("Orlando", "FL"), ("Atlanta", "GA"), ("Charlotte", "NC"),
                        ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"), ("Houston", "TX"), ("Phoenix", "AZ"),
                        ("Philadelphia", "PA"), ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"), ("Austin", "TX")
                    ]
                    return choice(cities)

                def random_zip():
                    return f"{randint(10000,99999)}"

                def random_dob():
                    year = randint(1950, 2000)
                    month = randint(1, 12)
                    day = randint(1, 28)
                    return f"{year}-{month:02d}-{day:02d}"

                def random_date_recent(days_ago):
                    now = int(time.time())
                    return now - randint(0, days_ago * 86400)

                def random_date_string(days_ago):
                    ts = random_date_recent(days_ago)
                    import datetime
                    dt = datetime.datetime.fromtimestamp(ts)
                    return dt.strftime("%Y-%m-%d")

                def random_date_future(days_ahead):
                    now = int(time.time())
                    return now + randint(0, days_ahead * 86400)

                def random_date_string_future(days_ahead):
                    ts = random_date_future(days_ahead)
                    import datetime
                    dt = datetime.datetime.fromtimestamp(ts)
                    return dt.strftime("%Y-%m-%d")

                def random_currency(min_cents, max_cents):
                    return randint(min_cents, max_cents)

                def random_vin():
                    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
                    return "".join(choice(chars) for _ in range(17))

                # Generate 80 quotes
                print("Generating 80 quotes...")
                coverage_types = ["AUTO", "HOME", "LIFE", "HEALTH"]
                quote_statuses = ["PENDING", "ACCEPTED", "DECLINED", "EXPIRED"]

                for i in range(1, 81):
                    name = random_name()
                    coverage = choice(coverage_types) if random() < 0.4 else choice(coverage_types[1:]) if random() < 0.5 else choice(coverage_types[2:]) if random() < 0.67 else coverage_types[3]
                    city, state = random_city_state()
                    created = random_date_recent(3650)

                    quote = {
                        "id": f"q-{i:04d}",
                        "createdAt": created,
                        "data": {
                            "name": name,
                            "email": random_email(name),
                            "phone": random_phone(),
                            "address": random_address(),
                            "city": city,
                            "state": state,
                            "zip": random_zip(),
                            "dateOfBirth": random_dob(),
                            "premium_cents": random_currency(50000, 300000),
                            "coverageType": coverage,
                            "coverageLimit_cents": random_currency(10000000, 100000000),
                            "deductible_cents": choice([50000, 100000, 250000, 500000]),
                            "quoteNumber": f"Q-2024-{i:06d}",
                            "status": choice(quote_statuses) if random() < 0.25 else "PENDING",
                            "expiresAt": created + (10 * 86400)
                        }
                    }

                    if coverage == "AUTO":
                        makes = ["Honda", "Toyota", "Ford", "Chevrolet", "Nissan", "BMW", "Mercedes", "Audi", "Lexus", "Mazda"]
                        models = ["Civic", "Accord", "Camry", "Corolla", "F-150", "Silverado", "Altima", "Maxima", "3 Series", "C-Class"]
                        quote["data"]["vehicleInfo"] = {
                            "year": randint(2015, 2024),
                            "make": choice(makes),
                            "model": choice(models),
                            "vin": random_vin()
                        }

                    put(tables[0], quote)

                print(f"Seeded {tables[0]} with 80 quotes")

                # Generate 60 policies (75% of quotes accepted)
                print("Generating 60 policies...")
                policy_statuses = ["ACTIVE", "EXPIRED", "CANCELLED", "SUSPENDED"]
                payment_schedules = ["MONTHLY", "QUARTERLY", "ANNUAL"]

                policy_ids = []
                for i in range(1, 61):
                    quote_id = f"q-{i:04d}"
                    created = random_date_recent(3650)
                    policy_id = f"p-{i:04d}"
                    policy_ids.append(policy_id)

                    policy = {
                        "id": policy_id,
                        "createdAt": created,
                        "data": {
                            "quoteId": quote_id,
                            "policyNumber": f"POL-2024-{i:06d}",
                            "status": choice(policy_statuses) if random() < 0.2 else "ACTIVE",
                            "holderName": random_name(),
                            "zip": random_zip(),
                            "effectiveDate": random_date_string(3650),
                            "expiryDate": random_date_string_future(300),
                            "renewalDate": random_date_string_future(15),
                            "premium_cents": random_currency(100000, 400000),
                            "paymentSchedule": choice(payment_schedules),
                            "coverageLimit_cents": random_currency(25000000, 100000000),
                            "deductible_cents": choice([50000, 100000, 250000, 500000]),
                            "coverageType": choice(coverage_types),
                            "coverageDetails": {
                                "liability": random_currency(10000000, 50000000),
                                "collision": random_currency(25000000, 100000000),
                                "comprehensive": random_currency(25000000, 100000000)
                            }
                        }
                    }
                    put(tables[1], policy)

                print(f"Seeded {tables[1]} with 60 policies")

                # Generate 40 claims (67% of policies have claims)
                print("Generating 40 claims...")
                claim_statuses = ["INTAKE", "PENDING", "REVIEW", "APPROVED", "DENIED", "CLOSED"]
                loss_types = ["AUTO_COLLISION", "AUTO_GLASS", "AUTO_THEFT", "PROPERTY_DAMAGE", "WATER_DAMAGE", "FIRE", "THEFT", "VANDALISM"]
                adjuster_names = ["Bob Smith", "Alice Johnson", "Charlie Brown", "Diana Prince", "Eve Adams"]

                for i in range(1, 41):
                    policy_id = choice(policy_ids)
                    created = random_date_recent(3650)
                    status_dist = random()
                    if status_dist < 0.3:
                        status = "INTAKE"
                    elif status_dist < 0.55:
                        status = "PENDING"
                    elif status_dist < 0.75:
                        status = "APPROVED"
                    elif status_dist < 0.9:
                        status = "REVIEW"
                    else:
                        status = "DENIED"

                    estimated = random_currency(10000, 5000000)
                    approved = int(estimated * (0.8 + random() * 0.2)) if status in ["APPROVED", "CLOSED"] else None

                    claim = {
                        "id": f"c-{i:04d}",
                        "createdAt": created,
                        "status": status,
                        "updatedAt": created + randint(3600, 86400 * 5),
                        "data": {
                            "policyId": policy_id,
                            "claimNumber": f"CLM-2024-{i:06d}",
                            "claimantName": random_name(),
                            "loss": f"{choice(loss_types).replace('_', ' ').title()} incident",
                            "lossType": choice(loss_types),
                            "incidentDate": random_date_string(3650),
                            "reportedDate": random_date_string(3650),
                            "estimatedAmount_cents": estimated,
                            "approvedAmount_cents": approved,
                            "deductible_cents": choice([0, 50000, 100000, 250000]),
                            "paidAmount_cents": approved if status == "CLOSED" and approved else None,
                            "description": f"Claim for {choice(loss_types).replace('_', ' ').lower()} with estimated damage",
                            "location": choice(["I-95 northbound", "I-75 southbound", "US-1", "Downtown", "Residential area", "Parking lot"]),
                            "adjusterName": choice(adjuster_names),
                            "adjusterNotes": "Under review" if status in ["PENDING", "REVIEW"] else "Claim processed"
                        }
                    }
                    put(tables[2], claim)

                print(f"Seeded {tables[2]} with 40 claims")

                # Generate 180 payments (~3 per policy)
                print("Generating 180 payments...")
                payment_statuses = ["PENDING", "COMPLETED", "FAILED", "REFUNDED"]
                payment_methods = ["CREDIT_CARD", "ACH", "CHECK", "WIRE"]
                payment_types = ["PREMIUM", "CLAIM", "REFUND"]

                for i in range(1, 181):
                    policy_id = choice(policy_ids)
                    created = random_date_recent(3650)

                    payment = {
                        "id": f"pay-{i:04d}",
                        "createdAt": created,
                        "data": {
                            "policyId": policy_id,
                            "paymentNumber": f"PAY-2024-{i:06d}",
                            "amount_cents": random_currency(5000, 50000),
                            "status": choice(payment_statuses) if random() < 0.15 else "COMPLETED",
                            "paymentMethod": choice(payment_methods),
                            "paymentType": choice(payment_types) if random() < 0.1 else "PREMIUM",
                            "transactionId": f"txn_{randint(100000,999999)}",
                            "dueDate": random_date_string(3650),
                            "paidDate": random_date_string(3650) if random() < 0.85 else None,
                            "description": f"Payment for policy {policy_id}",
                            "lastFourDigits": f"{randint(1000,9999)}"
                        }
                    }
                    put(tables[3], payment)

                print(f"Seeded {tables[3]} with 180 payments")

                # Generate 50 cases
                print("Generating 50 cases...")
                case_topics = ["POLICY_CHANGE", "CLAIM_INQUIRY", "BILLING", "COMPLAINT", "COVERAGE_QUESTION", "CANCELLATION"]
                case_statuses = ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]
                priorities = ["LOW", "MEDIUM", "HIGH", "URGENT"]
                assignees = ["Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince", "Eve Adams", "Frank Miller"]
                departments = ["CUSTOMER_SERVICE", "CLAIMS", "BILLING", "UNDERWRITING"]

                for i in range(1, 51):
                    created = random_date_recent(3650)

                    case = {
                        "id": f"case-{i:04d}",
                        "createdAt": created,
                        "data": {
                            "caseNumber": f"CS-2024-{i:06d}",
                            "title": f"{choice(case_topics).replace('_', ' ').title()} - Case {i}",
                            "topic": choice(case_topics),
                            "status": choice(case_statuses) if random() < 0.4 else "OPEN",
                            "priority": choice(priorities) if random() < 0.3 else "MEDIUM",
                            "assignee": choice(assignees),
                            "department": choice(departments),
                            "customerName": random_name(),
                            "policyId": choice(policy_ids) if random() < 0.7 else None,
                            "description": f"Customer inquiry regarding {choice(case_topics).replace('_', ' ').lower()}",
                            "resolution": None,
                            "dueDate": random_date_string_future(10),
                            "resolvedDate": random_date_string(3650) if random() < 0.3 else None
                        }
                    }
                    put(tables[4], case)

                print(f"Seeded {tables[4]} with 50 cases")

                # Seed one doc
                print(f"Uploading sample doc to {docs_bucket}")
                s3.put_object(
                    Bucket=docs_bucket,
                    Key="docs/sample.txt",
                    Body=b"Silvermoat demo document",
                    ContentType="text/plain",
                )
                print("Sample doc uploaded successfully")

                print("Seeding completed successfully")
                send(event, "SUCCESS", {"web": web, "api": api}, phys_id, "Seeding completed successfully")
                return

            raise ValueError(f"Unknown RequestType in seed mode: {request_type}")

        raise ValueError(f"Unknown Mode: {mode}")

    except Exception as e:
        error_msg = f"Error in Custom Resource handler: {str(e)}"
        print(error_msg)
        import traceback
        print(traceback.format_exc())
        try:
            send(event, "FAILED", {"error": str(e)}, phys_id, error_msg)
        except Exception as send_error:
            print(f"CRITICAL: Failed to send FAILED response: {send_error}")
            raise
