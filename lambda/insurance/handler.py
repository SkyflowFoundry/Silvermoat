"""Insurance vertical API handler - Complete standalone Lambda function"""
import os
import json
import boto3
from shared.responses import _resp
from shared.events import _emit
from shared.storage import DynamoDBBackend
from entities import (
    upsert_customer_for_quote,
    upsert_customer_for_policy,
    get_customer_id_from_policy
)
from chatbot import handle_chat as handle_insurance_chat
from customer_chatbot import handle_customer_chat as handle_insurance_customer_chat


# Initialize storage backend
storage = DynamoDBBackend()

# S3 client for document uploads
s3 = boto3.client("s3")
DOCS_BUCKET = os.environ["DOCS_BUCKET"]


# Insurance entities (domains)
INSURANCE_ENTITIES = ["customer", "quote", "policy", "claim", "payment", "case"]


def handler(event, context):
    """Main Lambda handler for Insurance vertical API"""
    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    # POST /chat -> chatbot endpoint
    if path == "chat" and method == "POST":
        return handle_insurance_chat(event, storage)

    # POST /customer-chat -> customer chatbot endpoint
    if path == "customer-chat" and method == "POST":
        return handle_insurance_customer_chat(event, storage)

    # Parse request body (needed by all endpoints)
    body = {}
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except Exception:
            body = {"raw": event["body"]}

    parts = [p for p in path.split("/") if p]

    # Root endpoint - list available endpoints
    if not parts:
        return _resp(200, {
            "name": "Silvermoat Insurance",
            "vertical": "insurance",
            "endpoints": [f"/{e}" for e in INSURANCE_ENTITIES] + ["/chat", "/customer-chat"]
        })

    domain = parts[0]

    # Validate domain
    if domain not in INSURANCE_ENTITIES:
        return _resp(404, {"error": "unknown_domain", "domain": domain})

    # GET /{domain} -> list all items (with optional query params)
    if method == "GET" and len(parts) == 1:
        # Parse query string parameters
        query_params = event.get("queryStringParameters") or {}
        customer_email = query_params.get("customerEmail")
        limit = query_params.get("limit")

        # Filter by customerEmail for policy, claim, payment
        if customer_email and domain in ["policy", "claim", "payment"]:
            # Get customer by email to find customerId
            customers = storage.query_by_email("customer", customer_email)
            if not customers:
                return _resp(200, {"items": [], "count": 0})

            customer_id = customers[0]["id"]

            # Query by customerId using GSI
            if domain in ["policy", "claim"]:
                items = storage.query_by_customer_id(domain, customer_id)
            elif domain == "payment":
                # For payments, get policies first, then filter payments
                policies = storage.query_by_customer_id("policy", customer_id)
                policy_ids = [p["id"] for p in policies]
                all_payments = storage.scan("payment")
                items = [p for p in all_payments if p.get("data", {}).get("policyId") in policy_ids]

            return _resp(200, {"items": items, "count": len(items)})

        # Get all items
        items = storage.list(domain)

        # Apply limit if specified
        if limit:
            try:
                limit_int = int(limit)
                items = items[:limit_int]
            except ValueError:
                pass  # Ignore invalid limit

        return _resp(200, {"items": items, "count": len(items)})

    # POST /{domain} -> create
    if method == "POST" and len(parts) == 1:
        # Add default status based on domain type
        default_status = {
            "customer": "ACTIVE",
            "quote": "PENDING",
            "policy": "ACTIVE",
            "claim": "PENDING",
            "payment": "PENDING",
            "case": "OPEN"
        }.get(domain, "PENDING")

        # Handle customer creation/upsert
        if domain == "customer":
            # Use upsert_customer for proper email indexing
            customer_email = body.get("email")
            if customer_email:
                item = storage.upsert_customer(customer_email, body)
            else:
                item = storage.create(domain, body, default_status)

        # Handle customer upsert for quote
        elif domain == "quote":
            customer_id = upsert_customer_for_quote(storage, body)
            if customer_id:
                body["customerId"] = customer_id
            item = storage.create(domain, body, default_status)

        # Handle customer upsert for policy
        elif domain == "policy":
            customer_id = upsert_customer_for_policy(storage, body)
            top_level_fields = {}
            if customer_id:
                body["customerId"] = customer_id
                top_level_fields["customerId"] = customer_id
            item = storage.create(domain, body, default_status, top_level_fields)

        # Handle claim with customer denormalization
        elif domain == "claim":
            # Denormalize customerId from policy
            policy_id = body.get("policyId")
            top_level_fields = {}
            if policy_id:
                customer_id = get_customer_id_from_policy(storage, policy_id)
                if customer_id:
                    body["customerId"] = customer_id
                    top_level_fields["customerId"] = customer_id
            item = storage.create(domain, body, default_status, top_level_fields)

        else:
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
