"""Retail vertical API handler - Complete standalone Lambda function"""
import os
import json
from shared.responses import _resp
from shared.events import _emit
from shared.storage import DynamoDBBackend
from entities import upsert_customer_for_order, calculate_order_total
from chatbot import handle_chat as handle_retail_chat
from customer_chatbot import handle_customer_chat as handle_retail_customer_chat


# Retail domain mapping: retail entity names -> environment variable names
# Retail reuses insurance table env vars but with different semantics:
# - QUOTES_TABLE -> products
# - POLICIES_TABLE -> orders
# - CLAIMS_TABLE -> inventory
RETAIL_DOMAIN_MAPPING = {
    "customer": "CUSTOMERS_TABLE",
    "product": "QUOTES_TABLE",      # Retail products stored in quotes table
    "order": "POLICIES_TABLE",       # Retail orders stored in policies table
    "inventory": "CLAIMS_TABLE",     # Retail inventory stored in claims table
    "payment": "PAYMENTS_TABLE",
    "case": "CASES_TABLE"
}

# Initialize storage backend with retail domain mapping
storage = DynamoDBBackend(domain_mapping=RETAIL_DOMAIN_MAPPING)


# Retail entities (domains)
RETAIL_ENTITIES = ["customer", "product", "order", "inventory", "payment", "case"]


def handler(event, context):
    """Main Lambda handler for Retail vertical API"""
    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    # POST /chat -> chatbot endpoint
    if path == "chat" and method == "POST":
        return handle_retail_chat(event, storage)

    # POST /customer-chat -> customer chatbot endpoint
    if path == "customer-chat" and method == "POST":
        return handle_retail_customer_chat(event, storage)

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
            "name": "Silvermoat Retail",
            "vertical": "retail",
            "endpoints": [f"/{e}" for e in RETAIL_ENTITIES] + ["/chat", "/customer-chat"]
        })

    domain = parts[0]

    # Validate domain
    if domain not in RETAIL_ENTITIES:
        return _resp(404, {"error": "unknown_domain", "domain": domain})

    # GET /{domain} -> list all items (with optional query params)
    if method == "GET" and len(parts) == 1:
        # Parse query string parameters
        query_params = event.get("queryStringParameters") or {}
        customer_email = query_params.get("customerEmail")
        limit = query_params.get("limit")

        # Filter by customerEmail for orders and payments
        if customer_email and domain in ["order", "payment"]:
            # Get customer by email to find customerId
            customers = storage.query_by_email("customer", customer_email)
            if not customers:
                return _resp(200, {"items": [], "count": 0})

            customer_id = customers[0]["id"]

            # Query by customerId using GSI
            if domain == "order":
                items = storage.query_by_customer_id(domain, customer_id)
            elif domain == "payment":
                # For payments, get orders first, then filter payments
                orders = storage.query_by_customer_id("order", customer_id)
                order_ids = [o["id"] for o in orders]
                all_payments = storage.scan("payment")
                items = [p for p in all_payments if p.get("data", {}).get("orderId") in order_ids]

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
            "product": "ACTIVE",
            "order": "PENDING",
            "inventory": "IN_STOCK",
            "payment": "PENDING",
            "case": "OPEN"
        }.get(domain, "ACTIVE")

        # Handle customer creation/upsert
        if domain == "customer":
            customer_email = body.get("email")
            if customer_email:
                item = storage.upsert_customer(customer_email, body)
            else:
                item = storage.create(domain, body, default_status)

        # Handle order with customer upsert
        elif domain == "order":
            customer_id = upsert_customer_for_order(storage, body)
            top_level_fields = {}
            if customer_id:
                body["customerId"] = customer_id
                top_level_fields["customerId"] = customer_id

            # Calculate total if items provided
            if body.get("items"):
                body["totalAmount"] = calculate_order_total(body["items"])

            item = storage.create(domain, body, default_status, top_level_fields)

        # Handle product
        elif domain == "product":
            item = storage.create(domain, body, default_status)

        # Handle inventory
        elif domain == "inventory":
            item = storage.create(domain, body, default_status)

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

    # POST /order/{id}/status -> update order status
    if domain == "order" and method == "POST" and len(parts) == 3 and parts[2] == "status":
        item_id = parts[1]
        new_status = (body.get("status") or "PROCESSING").upper()
        storage.update_status(domain, item_id, new_status)
        _emit("order.status_changed", {"id": item_id, "status": new_status})
        return _resp(200, {"id": item_id, "status": new_status})

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
