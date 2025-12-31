"""Main Lambda handler for Silvermoat MVP API"""
import os
import json
import boto3
from shared.responses import _resp
from shared.events import _emit
from shared.storage import DynamoDBBackend
from chatbot import handle_chat


# Initialize storage backend
storage = DynamoDBBackend()

# S3 client for document uploads
s3 = boto3.client("s3")
DOCS_BUCKET = os.environ["DOCS_BUCKET"]


def handle_customer_request(parts, method, body, event, storage):
    """Handle customer portal API requests"""

    # POST /customer/auth -> authenticate customer with policy number + ZIP
    if method == "POST" and len(parts) == 2 and parts[1] == "auth":
        policy_number = body.get("policyNumber", "").strip()
        zip_code = body.get("zip", "").strip()

        if not policy_number or not zip_code:
            return _resp(400, {"error": "missing_credentials", "message": "Policy number and ZIP code required"})

        # Search for matching policy
        policies = storage.scan("policy")
        matching_policy = None

        for policy in policies:
            data = policy.get("data", {})
            if (data.get("policyNumber") == policy_number and
                data.get("zip") == zip_code):
                matching_policy = policy
                break

        if not matching_policy:
            return _resp(401, {"error": "invalid_credentials", "message": "Invalid policy number or ZIP code"})

        # Return minimal policy info for authenticated customer
        return _resp(200, {
            "authenticated": True,
            "policyId": matching_policy["id"],
            "policyNumber": policy_number,
            "holderName": matching_policy.get("data", {}).get("holderName", ""),
        })

    # GET /customer/policies?policyNumber=XXX -> list policies for customer
    if method == "GET" and len(parts) == 2 and parts[1] == "policies":
        query_params = event.get("queryStringParameters") or {}
        policy_number = query_params.get("policyNumber", "").strip()

        if not policy_number:
            return _resp(400, {"error": "missing_parameter", "message": "policyNumber query parameter required"})

        # Search for matching policies
        policies = storage.scan("policy")
        customer_policies = [
            p for p in policies
            if p.get("data", {}).get("policyNumber") == policy_number
        ]

        return _resp(200, {"policies": customer_policies, "count": len(customer_policies)})

    # GET /customer/policies/{id} -> get specific policy
    if method == "GET" and len(parts) == 3 and parts[1] == "policies":
        policy_id = parts[2]
        policy = storage.get("policy", policy_id)

        if not policy:
            return _resp(404, {"error": "not_found", "message": "Policy not found"})

        return _resp(200, policy)

    # GET /customer/claims?policyNumber=XXX -> list claims for customer
    if method == "GET" and len(parts) == 2 and parts[1] == "claims":
        query_params = event.get("queryStringParameters") or {}
        policy_number = query_params.get("policyNumber", "").strip()

        if not policy_number:
            return _resp(400, {"error": "missing_parameter", "message": "policyNumber query parameter required"})

        # Find policy IDs for this policy number
        policies = storage.scan("policy")
        policy_ids = [
            p["id"] for p in policies
            if p.get("data", {}).get("policyNumber") == policy_number
        ]

        if not policy_ids:
            return _resp(200, {"claims": [], "count": 0})

        # Search for claims matching these policy IDs
        claims = storage.scan("claim")
        customer_claims = [
            c for c in claims
            if c.get("data", {}).get("policyId") in policy_ids
        ]

        # Sort by creation date descending
        customer_claims.sort(key=lambda x: x.get("createdAt", 0), reverse=True)

        return _resp(200, {"claims": customer_claims, "count": len(customer_claims)})

    # POST /customer/claims -> submit new claim
    if method == "POST" and len(parts) == 2 and parts[1] == "claims":
        # Validate required fields
        required_fields = ["policyNumber", "claimantName", "incidentDate", "description"]
        missing_fields = [f for f in required_fields if not body.get(f)]

        if missing_fields:
            return _resp(400, {
                "error": "missing_fields",
                "message": f"Required fields missing: {', '.join(missing_fields)}"
            })

        # Create claim
        claim = storage.create("claim", body, "PENDING")
        _emit("claim.created", {"id": claim["id"], "data": body, "status": "PENDING"})

        return _resp(201, {"id": claim["id"], "claim": claim})

    # GET /customer/claims/{id} -> get specific claim
    if method == "GET" and len(parts) == 3 and parts[1] == "claims":
        claim_id = parts[2]
        claim = storage.get("claim", claim_id)

        if not claim:
            return _resp(404, {"error": "not_found", "message": "Claim not found"})

        return _resp(200, claim)

    # POST /customer/claims/{id}/doc -> upload claim document
    if method == "POST" and len(parts) == 4 and parts[1] == "claims" and parts[3] == "doc":
        claim_id = parts[2]

        # Verify claim exists
        claim = storage.get("claim", claim_id)
        if not claim:
            return _resp(404, {"error": "not_found", "message": "Claim not found"})

        # Upload document to S3
        key = f"claims/{claim_id}/{body.get('filename', 'document.txt')}"
        content = (body.get("text") or body.get("content") or "").encode("utf-8")

        s3.put_object(
            Bucket=DOCS_BUCKET,
            Key=key,
            Body=content,
            ContentType=body.get("contentType", "text/plain")
        )

        _emit("claim.document_added", {"id": claim_id, "s3Key": key})

        return _resp(200, {"id": claim_id, "s3Key": key, "uploaded": True})

    # GET /customer/payments?policyNumber=XXX -> list payments for customer
    if method == "GET" and len(parts) == 2 and parts[1] == "payments":
        query_params = event.get("queryStringParameters") or {}
        policy_number = query_params.get("policyNumber", "").strip()

        if not policy_number:
            return _resp(400, {"error": "missing_parameter", "message": "policyNumber query parameter required"})

        # Find policy IDs for this policy number
        policies = storage.scan("policy")
        policy_ids = [
            p["id"] for p in policies
            if p.get("data", {}).get("policyNumber") == policy_number
        ]

        if not policy_ids:
            return _resp(200, {"payments": [], "count": 0})

        # Search for payments matching these policy IDs
        payments = storage.scan("payment")
        customer_payments = [
            p for p in payments
            if p.get("data", {}).get("policyId") in policy_ids
        ]

        # Sort by payment date descending
        customer_payments.sort(key=lambda x: x.get("createdAt", 0), reverse=True)

        return _resp(200, {"payments": customer_payments, "count": len(customer_payments)})

    return _resp(404, {"error": "customer_endpoint_not_found", "path": f"/customer/{'/'.join(parts[1:])}"})


def handler(event, context):
    """Main Lambda handler for API Gateway proxy integration"""
    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    # POST /chat -> chatbot endpoint (handle before domain check)
    if path == "chat" and method == "POST":
        return handle_chat(event, storage)

    parts = [p for p in path.split("/") if p]

    # Root endpoint - list available endpoints
    if not parts:
        return _resp(200, {
            "name": "Silvermoat MVP",
            "endpoints": ["/quote", "/policy", "/claim", "/payment", "/case", "/chat", "/customer"]
        })

    domain = parts[0]

    # Parse request body (needed by all endpoints)
    body = {}
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except Exception:
            body = {"raw": event["body"]}

    # Customer portal endpoints (before domain validation)
    if domain == "customer":
        return handle_customer_request(parts, method, body, event, storage)

    # Validate domain
    valid_domains = ["quote", "policy", "claim", "payment", "case"]
    if domain not in valid_domains:
        return _resp(404, {"error": "unknown_domain", "domain": domain})

    # GET /{domain} -> list all items
    if method == "GET" and len(parts) == 1:
        items = storage.list(domain)
        return _resp(200, {"items": items, "count": len(items)})

    # POST /{domain} -> create
    if method == "POST" and len(parts) == 1:
        # Add default status based on domain type
        default_status = {
            "quote": "PENDING",
            "policy": "ACTIVE",
            "claim": "PENDING",
            "payment": "PENDING",
            "case": "OPEN"
        }.get(domain, "PENDING")

        item = storage.create(domain, body, default_status)
        _emit(f"{domain}.created", {"id": item["id"], "data": body, "status": default_status})
        return _resp(201, {"id": item["id"], "item": item})

    # GET /{domain}/{id} -> read
    if method == "GET" and len(parts) == 2:
        item_id = parts[1]
        item = storage.get(domain, item_id)
        if not item:
            return _resp(404, {"error": "not_found", "id": item_id})
        return _resp(200, item)

    # POST /claim/{id}/status -> simple state update demo
    if domain == "claim" and method == "POST" and len(parts) == 3 and parts[2] == "status":
        item_id = parts[1]
        new_status = (body.get("status") or "REVIEW").upper()
        storage.update_status(domain, item_id, new_status)
        _emit("claim.status_changed", {"id": item_id, "status": new_status})
        return _resp(200, {"id": item_id, "status": new_status})

    # POST /claim/{id}/doc -> attach a tiny doc to S3 (demo)
    if domain == "claim" and method == "POST" and len(parts) == 3 and parts[2] == "doc":
        item_id = parts[1]
        key = f"claims/{item_id}/note.txt"
        content = (body.get("text") or "Demo claim note").encode("utf-8")
        s3.put_object(
            Bucket=DOCS_BUCKET,
            Key=key,
            Body=content,
            ContentType="text/plain"
        )
        _emit("claim.document_added", {"id": item_id, "s3Key": key})
        return _resp(200, {"id": item_id, "s3Key": key})

    # DELETE /{domain}/{id} -> delete single item
    if method == "DELETE" and len(parts) == 2:
        item_id = parts[1]
        storage.delete(domain, item_id)
        _emit(f"{domain}.deleted", {"id": item_id})
        return _resp(200, {"id": item_id, "deleted": True})

    # DELETE /{domain} -> delete all items in domain (bulk clear)
    if method == "DELETE" and len(parts) == 1:
        deleted_count = storage.delete_all(domain)
        _emit(f"{domain}.bulk_deleted", {"count": deleted_count})
        return _resp(200, {"deleted": deleted_count, "domain": domain})

    return _resp(400, {"error": "unsupported_operation", "path": event.get("path"), "method": method})
