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
            "endpoints": ["/quote", "/policy", "/claim", "/payment", "/case", "/chat"]
        })

    domain = parts[0]

    # Parse request body (needed by all endpoints)
    body = {}
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except Exception:
            body = {"raw": event["body"]}

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
