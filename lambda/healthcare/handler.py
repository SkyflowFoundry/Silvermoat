"""Healthcare vertical API handler - Complete standalone Lambda function"""
import os
import json
from shared.responses import _resp
from shared.events import _emit
from shared.storage import DynamoDBBackend
from entities import (
    upsert_patient_for_appointment,
    upsert_patient_for_medical_record,
    get_patient_id_from_medical_record
)
from chatbot import handle_chat as handle_healthcare_chat
from customer_chatbot import handle_customer_chat as handle_healthcare_customer_chat


# Healthcare domain mapping: healthcare entity names -> environment variable names
# Healthcare reuses insurance table env vars but with different semantics:
# - CUSTOMERS_TABLE -> patients
# - QUOTES_TABLE -> appointments
# - POLICIES_TABLE -> medical_records
# - CLAIMS_TABLE -> prescriptions
HEALTHCARE_DOMAIN_MAPPING = {
    "patient": "CUSTOMERS_TABLE",
    "appointment": "QUOTES_TABLE",       # Healthcare appointments stored in quotes table
    "medical_record": "POLICIES_TABLE",  # Healthcare medical records stored in policies table
    "prescription": "CLAIMS_TABLE",      # Healthcare prescriptions stored in claims table
    "billing": "PAYMENTS_TABLE",
    "case": "CASES_TABLE"
}

# Initialize storage backend with healthcare domain mapping
storage = DynamoDBBackend(domain_mapping=HEALTHCARE_DOMAIN_MAPPING)


# Healthcare entities (domains)
HEALTHCARE_ENTITIES = ["patient", "appointment", "medical_record", "prescription", "billing", "case"]


def handler(event, context):
    """Main Lambda handler for Healthcare vertical API"""
    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    # POST /chat -> chatbot endpoint
    if path == "chat" and method == "POST":
        return handle_healthcare_chat(event, storage)

    # POST /customer-chat -> customer chatbot endpoint (patient chat)
    if path == "customer-chat" and method == "POST":
        return handle_healthcare_customer_chat(event, storage)

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
            "name": "Silvermoat Healthcare",
            "vertical": "healthcare",
            "endpoints": [f"/{e}" for e in HEALTHCARE_ENTITIES] + ["/chat", "/customer-chat"]
        })

    domain = parts[0]

    # Validate domain
    if domain not in HEALTHCARE_ENTITIES:
        return _resp(404, {"error": "unknown_domain", "domain": domain})

    # GET /{domain} -> list all items (with optional query params)
    if method == "GET" and len(parts) == 1:
        # Parse query string parameters
        query_params = event.get("queryStringParameters") or {}
        patient_email = query_params.get("patientEmail")
        limit = query_params.get("limit")

        # Filter by patientEmail for medical_record, prescription, billing
        if patient_email and domain in ["medical_record", "prescription", "billing"]:
            # Get patient by email to find patientId
            patients = storage.query_by_email("patient", patient_email)
            if not patients:
                return _resp(200, {"items": [], "count": 0})

            patient_id = patients[0]["id"]

            # Query by patientId using GSI (customerId is the GSI field name)
            if domain in ["medical_record", "prescription"]:
                # These domains have customerId GSI
                items = storage.query_by_customer_id(domain, patient_id)
            elif domain == "billing":
                # For billing, get medical records first, then filter billing
                medical_records = storage.query_by_customer_id("medical_record", patient_id)
                medical_record_ids = [mr["id"] for mr in medical_records]
                all_billing = storage.scan("billing")
                items = [b for b in all_billing if b.get("data", {}).get("medicalRecordId") in medical_record_ids]

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
            "patient": "ACTIVE",
            "appointment": "SCHEDULED",
            "medical_record": "ACTIVE",
            "prescription": "ACTIVE",
            "billing": "PENDING",
            "case": "OPEN"
        }.get(domain, "PENDING")

        # Handle patient creation/upsert
        if domain == "patient":
            # Use upsert_customer for proper email indexing
            patient_email = body.get("email")
            if patient_email:
                item = storage.upsert_customer(patient_email, body)
            else:
                item = storage.create(domain, body, default_status)

        # Handle patient upsert for appointment
        elif domain == "appointment":
            patient_id = upsert_patient_for_appointment(storage, body)
            if patient_id:
                body["patientId"] = patient_id
            item = storage.create(domain, body, default_status)

        # Handle patient upsert for medical_record
        elif domain == "medical_record":
            patient_id = upsert_patient_for_medical_record(storage, body)
            top_level_fields = {}
            if patient_id:
                body["patientId"] = patient_id
                top_level_fields["customerId"] = patient_id  # GSI field name
            item = storage.create(domain, body, default_status, top_level_fields)

        # Handle prescription with patient denormalization
        elif domain == "prescription":
            # Denormalize patientId from medical_record
            medical_record_id = body.get("medicalRecordId")
            top_level_fields = {}
            if medical_record_id:
                patient_id = get_patient_id_from_medical_record(storage, medical_record_id)
                if patient_id:
                    body["patientId"] = patient_id
                    top_level_fields["customerId"] = patient_id  # GSI field name
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

    # POST /prescription/{id}/status -> simple state update demo
    if domain == "prescription" and method == "POST" and len(parts) == 3 and parts[2] == "status":
        item_id = parts[1]
        new_status = (body.get("status") or "ACTIVE").upper()
        storage.update_status(domain, item_id, new_status)
        _emit("prescription.status_changed", {"id": item_id, "status": new_status})
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
