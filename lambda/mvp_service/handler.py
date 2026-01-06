"""Main Lambda handler for Silvermoat MVP API"""
import os
import json
import boto3
from shared.responses import _resp
from shared.events import _emit
from shared.storage import DynamoDBBackend
from shared.vertical_detector import detect_vertical
from chatbot import handle_chat
from customer_chatbot import handle_customer_chat


# Initialize storage backend
storage = DynamoDBBackend()

# S3 client for document uploads
s3 = boto3.client("s3")
DOCS_BUCKET = os.environ["DOCS_BUCKET"]


def handler(event, context):
    """Main Lambda handler for API Gateway proxy integration"""
    # Detect vertical from Host header
    headers = event.get("headers") or {}
    host_header = headers.get("Host") or headers.get("host") or ""
    vertical = detect_vertical(host_header)

    # Store vertical in event for downstream handlers
    event["vertical"] = vertical

    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    # Route to vertical-specific handlers
    if vertical == "insurance":
        from verticals.insurance.handler import handle_request as insurance_handler
        from verticals.insurance.chatbot import handle_chat as insurance_chat
        from verticals.insurance.customer_chatbot import handle_customer_chat as insurance_customer_chat

        # POST /chat -> insurance chatbot
        if path == "chat" and method == "POST":
            return insurance_chat(event, storage)

        # POST /customer-chat -> insurance customer chatbot
        if path == "customer-chat" and method == "POST":
            return insurance_customer_chat(event, storage)

        # All other requests -> insurance handler
        return insurance_handler(event, storage, vertical)

    elif vertical == "retail":
        from verticals.retail.handler import handle_request as retail_handler
        from verticals.retail.chatbot import handle_chat as retail_chat
        from verticals.retail.customer_chatbot import handle_customer_chat as retail_customer_chat

        # POST /chat -> retail chatbot
        if path == "chat" and method == "POST":
            return retail_chat(event, storage)

        # POST /customer-chat -> retail customer chatbot
        if path == "customer-chat" and method == "POST":
            return retail_customer_chat(event, storage)

        # All other requests -> retail handler
        return retail_handler(event, storage, vertical)

    # Fallback to insurance for unknown verticals
    from verticals.insurance.handler import handle_request as insurance_handler
    from verticals.insurance.chatbot import handle_chat as insurance_chat
    from verticals.insurance.customer_chatbot import handle_customer_chat as insurance_customer_chat

    if path == "chat" and method == "POST":
        return insurance_chat(event, storage)
    if path == "customer-chat" and method == "POST":
        return insurance_customer_chat(event, storage)
    return insurance_handler(event, storage, "insurance")

