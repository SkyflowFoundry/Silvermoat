"""
AI Handler - Manages AI chatbot operations.

Routes:
- POST /chat (internal chatbot)
- POST /customer-chat (customer chatbot)
"""
from shared.responses import _resp
from shared.storage import DynamoDBBackend
from chatbot import handle_chat
from customer_chatbot import handle_customer_chat


# Initialize storage backend
storage = DynamoDBBackend()


def handler(event, context):
    """Handler for AI chatbot operations"""
    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    # POST /chat -> internal chatbot endpoint
    if path == "chat" and method == "POST":
        return handle_chat(event, storage)

    # POST /customer-chat -> customer chatbot endpoint
    if path == "customer-chat" and method == "POST":
        return handle_customer_chat(event, storage)

    return _resp(404, {"error": "not_found", "path": event.get("path")})
