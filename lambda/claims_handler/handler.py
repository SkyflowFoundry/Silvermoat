"""
Claims Handler - Manages policies, claims, payments, and cases.

Routes:
- GET/POST/DELETE /policy
- GET/POST/DELETE /claim
- POST /claim/{id}/status
- GET/POST/DELETE /payment
- GET/POST/DELETE /case
"""
import json
from shared.responses import _resp
from shared.events import _emit
from shared.storage import DynamoDBBackend
from shared.domain_logic import upsert_customer_for_policy, get_customer_id_from_policy


# Initialize storage backend
storage = DynamoDBBackend()


def handler(event, context):
    """Handler for policy, claim, payment, and case operations"""
    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    parts = [p for p in path.split("/") if p]

    # Validate we have a domain
    if not parts:
        return _resp(404, {"error": "not_found"})

    domain = parts[0]

    # Parse request body
    body = {}
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except Exception:
            body = {"raw": event["body"]}

    # Validate domain
    valid_domains = ["policy", "claim", "payment", "case"]
    if domain not in valid_domains:
        return _resp(404, {"error": "unknown_domain", "domain": domain})

    # GET /{domain} -> list all items
    if method == "GET" and len(parts) == 1:
        query_params = event.get("queryStringParameters") or {}
        customer_email = query_params.get("customerEmail")
        limit = query_params.get("limit")

        # Filter by customerEmail for policy, claim, payment
        if customer_email and domain in ["policy", "claim", "payment"]:
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
                pass

        return _resp(200, {"items": items, "count": len(items)})

    # POST /{domain} -> create
    if method == "POST" and len(parts) == 1:
        default_status = {
            "policy": "ACTIVE",
            "claim": "PENDING",
            "payment": "PENDING",
            "case": "OPEN"
        }.get(domain, "PENDING")

        top_level_fields = {}

        if domain == "policy":
            # Extract customer data from policy
            customer_id = upsert_customer_for_policy(storage, body)
            if customer_id:
                body["customerId"] = customer_id
                top_level_fields["customerId"] = customer_id
            item = storage.create(domain, body, default_status, top_level_fields)

        elif domain == "claim":
            # Denormalize customerId from policy
            policy_id = body.get("policyId")
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

    # POST /claim/{id}/status -> update claim status
    if domain == "claim" and method == "POST" and len(parts) == 3 and parts[2] == "status":
        item_id = parts[1]
        new_status = (body.get("status") or "REVIEW").upper()
        storage.update_status(domain, item_id, new_status)
        _emit("claim.status_changed", {"id": item_id, "status": new_status})
        return _resp(200, {"id": item_id, "status": new_status})

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
