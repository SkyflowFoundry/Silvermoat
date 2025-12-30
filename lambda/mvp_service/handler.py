import os
import json
import uuid
import time
from decimal import Decimal
import boto3

# Import database modules for PostgreSQL
try:
    from .db import initialize_schema
    from . import customers
    DB_AVAILABLE = True
except ImportError as e:
    print(f"Warning: PostgreSQL modules not available: {e}")
    DB_AVAILABLE = False

ddb = boto3.resource("dynamodb")
s3 = boto3.client("s3")
eb = boto3.client("events")
sns = boto3.client("sns")
bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("BEDROCK_REGION", "us-east-1"))

T = {
    "quote": ddb.Table(os.environ["QUOTES_TABLE"]),
    "policy": ddb.Table(os.environ["POLICIES_TABLE"]),
    "claim": ddb.Table(os.environ["CLAIMS_TABLE"]),
    "payment": ddb.Table(os.environ["PAYMENTS_TABLE"]),
    "case": ddb.Table(os.environ["CASES_TABLE"]),
}
DOCS_BUCKET = os.environ["DOCS_BUCKET"]
TOPIC = os.environ["SNS_TOPIC_ARN"]
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

TOOLS = [
    {
        "name": "search_quotes",
        "description": "Search insurance quotes by customer name or ZIP code",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Customer name to search for"},
                "zip": {"type": "string", "description": "ZIP code to search for"}
            }
        }
    },
    {
        "name": "search_policies",
        "description": "Search insurance policies by policy number, holder name, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "policy_number": {"type": "string", "description": "Policy number"},
                "holder_name": {"type": "string", "description": "Policy holder name"},
                "status": {"type": "string", "enum": ["ACTIVE", "EXPIRED", "CANCELLED"]}
            }
        }
    },
    {
        "name": "search_claims",
        "description": "Search insurance claims by claim number, claimant name, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "claim_number": {"type": "string", "description": "Claim number"},
                "claimant_name": {"type": "string", "description": "Claimant name"},
                "status": {"type": "string", "enum": ["PENDING", "REVIEW", "APPROVED", "DENIED"]}
            }
        }
    },
    {
        "name": "search_payments",
        "description": "Search payments by policy ID or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "policy_id": {"type": "string", "description": "Related policy ID"},
                "status": {"type": "string", "enum": ["PENDING", "COMPLETED", "FAILED"]}
            }
        }
    },
    {
        "name": "search_cases",
        "description": "Search cases by title, assignee, priority, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Case title keywords"},
                "assignee": {"type": "string", "description": "Assigned employee name"},
                "priority": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
                "status": {"type": "string", "enum": ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]}
            }
        }
    },
    {
        "name": "get_entity_details",
        "description": "Get full details of a specific quote, policy, claim, payment, or case by ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "entity_type": {"type": "string", "enum": ["quote", "policy", "claim", "payment", "case"]},
                "entity_id": {"type": "string", "description": "The unique ID of the entity"}
            },
            "required": ["entity_type", "entity_id"]
        }
    }
]


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError


def convert_floats_to_decimal(obj):
    """Recursively convert floats to Decimal for DynamoDB compatibility"""
    if isinstance(obj, list):
        return [convert_floats_to_decimal(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_floats_to_decimal(value) for key, value in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))
    return obj


def _resp(code, body):
    return {
        "statusCode": code,
        "headers": {
            "content-type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(body, default=decimal_default),
    }


def _emit(detail_type, detail):
    # Best-effort: events + demo notifications
    try:
        eb.put_events(Entries=[{
            "Source": "silvermoat.mvp",
            "DetailType": detail_type,
            "Detail": json.dumps(detail, default=decimal_default)
        }])
    except Exception:
        pass
    try:
        sns.publish(TopicArn=TOPIC, Subject=detail_type, Message=json.dumps(detail, default=decimal_default))
    except Exception:
        pass


def execute_tool(tool_name, tool_input):
    """Execute a tool call and return results"""

    if tool_name == "search_quotes":
        table = T["quote"]
        response = table.scan()
        items = response.get("Items", [])

        # Filter by name or zip if provided
        if tool_input.get("name"):
            name_lower = tool_input["name"].lower()
            items = [i for i in items if name_lower in i.get("data", {}).get("name", "").lower()]
        if tool_input.get("zip"):
            items = [i for i in items if tool_input["zip"] == i.get("data", {}).get("zip")]

        return {"quotes": items[:10], "count": len(items)}

    elif tool_name == "search_policies":
        table = T["policy"]
        response = table.scan()
        items = response.get("Items", [])

        # Filter by criteria
        if tool_input.get("policy_number"):
            pn = tool_input["policy_number"].lower()
            items = [i for i in items if pn in i.get("data", {}).get("policyNumber", "").lower()]
        if tool_input.get("holder_name"):
            hn = tool_input["holder_name"].lower()
            items = [i for i in items if hn in i.get("data", {}).get("holderName", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("data", {}).get("status")]

        return {"policies": items[:10], "count": len(items)}

    elif tool_name == "search_claims":
        table = T["claim"]
        response = table.scan()
        items = response.get("Items", [])

        # Filter by criteria
        if tool_input.get("claim_number"):
            cn = tool_input["claim_number"].lower()
            items = [i for i in items if cn in i.get("data", {}).get("claimNumber", "").lower()]
        if tool_input.get("claimant_name"):
            cn = tool_input["claimant_name"].lower()
            items = [i for i in items if cn in i.get("data", {}).get("claimantName", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"claims": items[:10], "count": len(items)}

    elif tool_name == "search_payments":
        table = T["payment"]
        response = table.scan()
        items = response.get("Items", [])

        # Filter by criteria
        if tool_input.get("policy_id"):
            items = [i for i in items if tool_input["policy_id"] == i.get("data", {}).get("policyId")]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("data", {}).get("status")]

        return {"payments": items[:10], "count": len(items)}

    elif tool_name == "search_cases":
        table = T["case"]
        response = table.scan()
        items = response.get("Items", [])

        # Filter by criteria
        if tool_input.get("title"):
            title = tool_input["title"].lower()
            items = [i for i in items if title in i.get("data", {}).get("title", "").lower()]
        if tool_input.get("assignee"):
            assignee = tool_input["assignee"].lower()
            items = [i for i in items if assignee in i.get("data", {}).get("assignee", "").lower()]
        if tool_input.get("priority"):
            items = [i for i in items if tool_input["priority"] == i.get("data", {}).get("priority")]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("data", {}).get("status")]

        return {"cases": items[:10], "count": len(items)}

    elif tool_name == "get_entity_details":
        entity_type = tool_input["entity_type"]
        entity_id = tool_input["entity_id"]

        if entity_type not in T:
            return {"error": f"Unknown entity type: {entity_type}"}

        table = T[entity_type]
        response = table.get_item(Key={"id": entity_id})

        if "Item" not in response:
            return {"error": f"{entity_type} not found"}

        return {entity_type: response["Item"]}

    return {"error": "Unknown tool"}


def handle_customer_request(path, method, raw_body, parts):
    """Handle customer API requests (PostgreSQL backend)"""
    if not DB_AVAILABLE:
        return _resp(503, {"error": "database_unavailable", "message": "PostgreSQL modules not loaded"})

    try:
        # Parse body
        body = {}
        if raw_body:
            try:
                body = json.loads(raw_body)
            except Exception:
                body = {"raw": raw_body}

        # POST /customer - Create
        if method == "POST" and len(parts) == 1:
            customer = customers.create_customer(body)
            if customer:
                return _resp(201, {"id": customer['id'], "item": customer})
            return _resp(500, {"error": "failed_to_create"})

        # GET /customer - List all
        if method == "GET" and len(parts) == 1:
            items = customers.list_customers()
            return _resp(200, {"items": items, "count": len(items)})

        # GET /customer/{id} - Read
        if method == "GET" and len(parts) == 2:
            customer_id = parts[1]
            customer = customers.get_customer(customer_id)
            if customer:
                return _resp(200, customer)
            return _resp(404, {"error": "not_found", "id": customer_id})

        # PUT /customer/{id} - Update
        if method == "PUT" and len(parts) == 2:
            customer_id = parts[1]
            customer = customers.update_customer(customer_id, body)
            if customer:
                return _resp(200, customer)
            return _resp(404, {"error": "not_found", "id": customer_id})

        # DELETE /customer/{id} - Delete
        if method == "DELETE" and len(parts) == 2:
            customer_id = parts[1]
            success = customers.delete_customer(customer_id)
            if success:
                return _resp(200, {"id": customer_id, "deleted": True})
            return _resp(404, {"error": "not_found", "id": customer_id})

        # Unsupported operation
        return _resp(400, {"error": "unsupported_operation", "path": path, "method": method})

    except Exception as e:
        print(f"Error handling customer request: {e}")
        import traceback
        traceback.print_exc()
        return _resp(500, {"error": "internal_error", "message": str(e)})


def handler(event, context):
    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Initialize PostgreSQL schema on cold start
    if DB_AVAILABLE:
        try:
            initialize_schema()
        except Exception as e:
            print(f"Warning: Failed to initialize database schema: {e}")

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    # POST /chat -> chatbot endpoint (handle before domain check)
    if path == "chat" and method == "POST":
        try:
            body = json.loads(event.get("body", "{}"))
            user_message = body.get("message", "")
            conversation_history = body.get("history", [])

            if not user_message:
                return _resp(400, {"error": "message_required", "message": "Message is required"})

            # Build messages for Claude
            messages = conversation_history + [{"role": "user", "content": user_message}]

            # System prompt for insurance assistant
            system_prompt = "You are a helpful AI assistant for Silvermoat Insurance employees. You help employees search customer data, fill forms, and generate reports. When users ask about customers, policies, or claims, use the available tools to search the database. Be professional, concise, and accurate. Format data clearly for insurance context. When helping with forms, provide structured data that can pre-fill form fields."

            # Invoke Bedrock with tool use
            response = bedrock.invoke_model(
                modelId=BEDROCK_MODEL_ID,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4096,
                    "system": system_prompt,
                    "messages": messages,
                    "tools": TOOLS,
                    "temperature": 0.7
                })
            )

            response_body = json.loads(response["body"].read())

            # Handle tool use loop
            while response_body.get("stop_reason") == "tool_use":
                # Extract tool calls
                assistant_message = {
                    "role": "assistant",
                    "content": response_body["content"]
                }
                messages.append(assistant_message)

                # Execute tools
                tool_results = []
                for content_block in response_body["content"]:
                    if content_block["type"] == "tool_use":
                        tool_name = content_block["name"]
                        tool_input = content_block["input"]
                        tool_use_id = content_block["id"]

                        # Execute the tool
                        result = execute_tool(tool_name, tool_input)

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": json.dumps(result, default=decimal_default)
                        })

                # Send tool results back to Claude
                messages.append({
                    "role": "user",
                    "content": tool_results
                })

                # Continue conversation
                response = bedrock.invoke_model(
                    modelId=BEDROCK_MODEL_ID,
                    body=json.dumps({
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 4096,
                        "system": system_prompt,
                        "messages": messages,
                        "tools": TOOLS,
                        "temperature": 0.7
                    })
                )

                response_body = json.loads(response["body"].read())

            # Extract final response
            assistant_content = response_body["content"]
            text_content = next((block["text"] for block in assistant_content if block["type"] == "text"), "")

            return _resp(200, {
                "response": text_content,
                "usage": response_body.get("usage", {}),
                "conversation": messages + [{"role": "assistant", "content": assistant_content}]
            })

        except Exception as e:
            print(f"Chat error: {str(e)}")
            return _resp(500, {"error": "chat_error", "message": str(e)})

    parts = [p for p in path.split("/") if p]

    if not parts:
        return _resp(200, {
            "name": "Silvermoat MVP",
            "endpoints": ["/quote", "/policy", "/claim", "/payment", "/case", "/customer", "/chat"]
        })

    domain = parts[0]

    # Route to PostgreSQL for customer resource
    if domain == "customer":
        return handle_customer_request(path, method, event.get("body"), parts)

    if domain not in T:
        return _resp(404, {"error": "unknown_domain", "domain": domain})

    table = T[domain]
    body = {}
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except Exception:
            body = {"raw": event["body"]}

    # GET /{domain} -> list all items
    if method == "GET" and len(parts) == 1:
        response = table.scan()
        items = response.get("Items", [])
        # Sort by createdAt descending (most recent first)
        items.sort(key=lambda x: x.get("createdAt", 0), reverse=True)
        return _resp(200, {"items": items, "count": len(items)})

    # POST /{domain} -> create
    if method == "POST" and len(parts) == 1:
        _id = str(uuid.uuid4())
        # Convert floats to Decimal for DynamoDB compatibility
        clean_body = convert_floats_to_decimal(body)

        # Add default status based on domain type
        default_status = {
            "quote": "PENDING",
            "policy": "ACTIVE",
            "claim": "PENDING",
            "payment": "PENDING",
            "case": "OPEN"
        }.get(domain, "PENDING")

        item = {"id": _id, "createdAt": int(time.time()), "data": clean_body, "status": default_status}
        print(f"Creating {domain} with id={_id}, status={default_status}")
        table.put_item(Item=item)
        _emit(f"{domain}.created", {"id": _id, "data": clean_body, "status": default_status})
        return _resp(201, {"id": _id, "item": item})

    # GET /{domain}/{id} -> read
    if method == "GET" and len(parts) == 2:
        _id = parts[1]
        r = table.get_item(Key={"id": _id})
        if "Item" not in r:
            return _resp(404, {"error": "not_found", "id": _id})
        return _resp(200, r["Item"])

    # POST /claim/{id}/status -> simple state update demo
    if domain == "claim" and method == "POST" and len(parts) == 3 and parts[2] == "status":
        _id = parts[1]
        new_status = (body.get("status") or "REVIEW").upper()
        table.update_item(
            Key={"id": _id},
            UpdateExpression="SET #s = :s, updatedAt = :u",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":s": new_status, ":u": int(time.time())},
        )
        _emit("claim.status_changed", {"id": _id, "status": new_status})
        return _resp(200, {"id": _id, "status": new_status})

    # POST /claim/{id}/doc -> attach a tiny doc to S3 (demo)
    if domain == "claim" and method == "POST" and len(parts) == 3 and parts[2] == "doc":
        _id = parts[1]
        key = f"claims/{_id}/note.txt"
        content = (body.get("text") or "Demo claim note").encode("utf-8")
        s3.put_object(
            Bucket=DOCS_BUCKET,
            Key=key,
            Body=content,
            ContentType="text/plain"
        )
        _emit("claim.document_added", {"id": _id, "s3Key": key})
        return _resp(200, {"id": _id, "s3Key": key})

    # DELETE /{domain}/{id} -> delete single item
    if method == "DELETE" and len(parts) == 2:
        _id = parts[1]
        table.delete_item(Key={"id": _id})
        _emit(f"{domain}.deleted", {"id": _id})
        return _resp(200, {"id": _id, "deleted": True})

    # DELETE /{domain} -> delete all items in domain (bulk clear)
    if method == "DELETE" and len(parts) == 1:
        response = table.scan()
        items = response.get("Items", [])
        deleted_count = 0
        for item in items:
            table.delete_item(Key={"id": item["id"]})
            deleted_count += 1
        _emit(f"{domain}.bulk_deleted", {"count": deleted_count})
        return _resp(200, {"deleted": deleted_count, "domain": domain})

    return _resp(400, {"error": "unsupported_operation", "path": event.get("path"), "method": method})
