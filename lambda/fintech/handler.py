"""Fintech vertical API handler - Complete standalone Lambda function"""
import os
import json
from shared.responses import _resp
from shared.events import _emit
from shared.storage import DynamoDBBackend
from entities import (
    upsert_customer_for_account,
    upsert_customer_for_transaction,
    get_customer_id_from_account
)
from chatbot import handle_chat as handle_fintech_chat
from customer_chatbot import handle_customer_chat as handle_fintech_customer_chat


# Fintech domain mapping: fintech entity names -> environment variable names
# Fintech reuses insurance table env vars but with different semantics:
# - CUSTOMERS_TABLE -> customers
# - QUOTES_TABLE -> accounts
# - POLICIES_TABLE -> transactions
# - CLAIMS_TABLE -> loans
# - PAYMENTS_TABLE -> cards
FINTECH_DOMAIN_MAPPING = {
    "customer": "CUSTOMERS_TABLE",
    "account": "QUOTES_TABLE",        # Fintech accounts stored in quotes table
    "transaction": "POLICIES_TABLE",  # Fintech transactions stored in policies table
    "loan": "CLAIMS_TABLE",           # Fintech loans stored in claims table
    "card": "PAYMENTS_TABLE",         # Fintech cards stored in payments table
    "case": "CASES_TABLE"
}

# Initialize storage backend with fintech domain mapping
storage = DynamoDBBackend(domain_mapping=FINTECH_DOMAIN_MAPPING)


# Fintech entities (domains)
FINTECH_ENTITIES = ["customer", "account", "transaction", "loan", "card", "case"]


def handler(event, context):
    """Main Lambda handler for Fintech vertical API"""
    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    # POST /chat -> chatbot endpoint
    if path == "chat" and method == "POST":
        return handle_fintech_chat(event, storage)

    # POST /customer-chat -> customer chatbot endpoint
    if path == "customer-chat" and method == "POST":
        return handle_fintech_customer_chat(event, storage)

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
            "name": "Silvermoat Fintech",
            "vertical": "fintech",
            "endpoints": [f"/{e}" for e in FINTECH_ENTITIES] + ["/chat", "/customer-chat"]
        })

    domain = parts[0]

    # Validate domain
    if domain not in FINTECH_ENTITIES:
        return _resp(404, {"error": "unknown_domain", "domain": domain})

    # GET /{domain} -> list all items (with optional query params)
    if method == "GET" and len(parts) == 1:
        # Parse query string parameters
        query_params = event.get("queryStringParameters") or {}
        customer_email = query_params.get("customerEmail")
        limit = query_params.get("limit")

        # Filter by customerEmail for account, transaction, loan, card
        if customer_email and domain in ["account", "transaction", "loan", "card"]:
            # Get customer by email to find customerId
            customers = storage.query_by_email("customer", customer_email)
            if not customers:
                return _resp(200, {"items": [], "count": 0})

            customer_id = customers[0]["id"]

            # Query by customerId using GSI
            if domain in ["account", "transaction", "loan"]:
                # These domains have customerId GSI
                items = storage.query_by_customer_id(domain, customer_id)
            elif domain == "card":
                # For cards, get accounts first, then filter cards
                accounts = storage.query_by_customer_id("account", customer_id)
                account_ids = [acc["id"] for acc in accounts]
                all_cards = storage.scan("card")
                items = [c for c in all_cards if c.get("data", {}).get("accountId") in account_ids]

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
            "account": "ACTIVE",
            "transaction": "COMPLETED",
            "loan": "ACTIVE",
            "card": "ACTIVE",
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

        # Handle customer upsert for account
        elif domain == "account":
            customer_id = upsert_customer_for_account(storage, body)
            top_level_fields = {}
            if customer_id:
                body["customerId"] = customer_id
                top_level_fields["customerId"] = customer_id  # GSI field name
            item = storage.create(domain, body, default_status, top_level_fields)

        # Handle customer upsert for transaction
        elif domain == "transaction":
            customer_id = upsert_customer_for_transaction(storage, body)
            top_level_fields = {}
            if customer_id:
                body["customerId"] = customer_id
                top_level_fields["customerId"] = customer_id  # GSI field name
            item = storage.create(domain, body, default_status, top_level_fields)

        # Handle loan with customer denormalization
        elif domain == "loan":
            # Denormalize customerId from account
            account_id = body.get("accountId")
            top_level_fields = {}
            if account_id:
                customer_id = get_customer_id_from_account(storage, account_id)
                if customer_id:
                    body["customerId"] = customer_id
                    top_level_fields["customerId"] = customer_id  # GSI field name
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

    # POST /loan/{id}/status -> simple state update demo
    if domain == "loan" and method == "POST" and len(parts) == 3 and parts[2] == "status":
        item_id = parts[1]
        new_status = (body.get("status") or "ACTIVE").upper()
        storage.update_status(domain, item_id, new_status)
        _emit("loan.status_changed", {"id": item_id, "status": new_status})
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
