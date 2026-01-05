"""
Customer Handler - Manages customer and quote operations.

Routes:
- GET / (root health check)
- GET/POST/DELETE /customer
- GET/POST/DELETE /quote
"""
import json
from shared.responses import _resp
from shared.events import _emit
from shared.storage import DynamoDBBackend
from shared.domain_logic import upsert_customer_for_quote


# Initialize storage backend
storage = DynamoDBBackend()


def handler(event, context):
    """Handler for customer and quote operations"""
    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    parts = [p for p in path.split("/") if p]

    # Root endpoint - list available endpoints
    if not parts:
        return _resp(200, {
            "name": "Silvermoat MVP",
            "endpoints": ["/customer", "/quote", "/policy", "/claim", "/payment", "/case", "/chat", "/customer-chat"]
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
    valid_domains = ["customer", "quote"]
    if domain not in valid_domains:
        return _resp(404, {"error": "unknown_domain", "domain": domain})

    # GET /{domain} -> list all items
    if method == "GET" and len(parts) == 1:
        query_params = event.get("queryStringParameters") or {}
        customer_email = query_params.get("customerEmail")
        limit = query_params.get("limit")

        # Filter by customerEmail if provided
        if customer_email:
            customers = storage.query_by_email("customer", customer_email)
            if not customers:
                return _resp(200, {"items": [], "count": 0})

            customer_id = customers[0]["id"]
            if domain == "quote":
                items = storage.query_by_customer_id(domain, customer_id)
                return _resp(200, {"items": items, "count": len(items)})

        # Get all items
        items = storage.list(domain)

        # Apply limit if specified
        if limit:
            try:
                limit_int = int(limit)
                items = items[:limit_int]
            except ValueError:
                pass

        return _resp(200, {"items": items, "count": len(items)})

    # POST /{domain} -> create
    if method == "POST" and len(parts) == 1:
        default_status = {
            "customer": "ACTIVE",
            "quote": "PENDING"
        }.get(domain, "PENDING")

        # Handle customer creation/upsert
        if domain == "customer":
            customer_email = body.get("email")
            if customer_email:
                item = storage.upsert_customer(customer_email, body)
            else:
                item = storage.create(domain, body, default_status)

        # Handle customer upsert for quote
        elif domain == "quote":
            customer_id = upsert_customer_for_quote(storage, body)
            top_level_fields = {}
            if customer_id:
                body["customerId"] = customer_id
                top_level_fields["customerId"] = customer_id
            item = storage.create(domain, body, default_status, top_level_fields)

        _emit(f"{domain}.created", {"id": item["id"], "data": body, "status": default_status})
        return _resp(201, {"id": item["id"], "item": item})

    # GET /{domain}/{id} -> read
    if method == "GET" and len(parts) == 2:
        item_id = parts[1]
        item = storage.get(domain, item_id)
        if not item:
            return _resp(404, {"error": "not_found", "id": item_id})
        return _resp(200, item)

    # DELETE /{domain}/{id} -> delete single item
    if method == "DELETE" and len(parts) == 2:
        item_id = parts[1]
        storage.delete(domain, item_id)
        _emit(f"{domain}.deleted", {"id": item_id})
        return _resp(200, {"id": item_id, "deleted": True})

    # DELETE /{domain} -> delete all items
    if method == "DELETE" and len(parts) == 1:
        deleted_count = storage.delete_all(domain)
        _emit(f"{domain}.bulk_deleted", {"count": deleted_count})
        return _resp(200, {"deleted": deleted_count, "domain": domain})

    return _resp(400, {"error": "unsupported_operation", "path": event.get("path"), "method": method})
