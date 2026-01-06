"""
AI Handler - Manages AI chatbot operations via Lambda Function URL with response streaming.

Routes (via Function URL):
- POST / or /chat (internal chatbot)
- POST /customer-chat (customer chatbot)

Uses NDJSON format for real-time streaming of status messages and responses.
"""
import json
import sys
from io import TextIOWrapper
from shared.storage import DynamoDBBackend
from shared.streaming import write_error_chunk
from chatbot import handle_chat_streaming
from customer_chatbot import handle_customer_chat_streaming


# Initialize storage backend
storage = DynamoDBBackend()


def handler(event, context):
    """
    Streaming handler for Lambda Function URL invocations.

    This handler is invoked when the Lambda is called via Function URL
    with InvokeMode=RESPONSE_STREAM. It supports real-time streaming
    of status messages and responses using NDJSON format.
    """
    try:
        # Parse Function URL event structure
        request_context = event.get("requestContext", {})
        http = request_context.get("http", {})
        method = http.get("method", "GET").upper()
        path = http.get("path", "/").strip("/")

        # Parse request body
        body_str = event.get("body", "{}")
        if event.get("isBase64Encoded"):
            import base64
            body_str = base64.b64decode(body_str).decode("utf-8")

        body = json.loads(body_str)

        # Get response stream (Lambda provides this for streaming responses)
        # When invoked with RESPONSE_STREAM, stdout is the response stream
        response_stream = TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

        # Route to appropriate handler
        if path in ["", "chat"] and method == "POST":
            handle_chat_streaming(body, storage, response_stream)
        elif path == "customer-chat" and method == "POST":
            handle_customer_chat_streaming(body, storage, response_stream)
        else:
            write_error_chunk(response_stream, "not_found", f"Path not found: /{path}")

        # Flush and return (response already streamed)
        response_stream.flush()
        return None  # Response already written to stream

    except json.JSONDecodeError as e:
        response_stream = TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
        write_error_chunk(response_stream, "invalid_json", f"Invalid JSON in request body: {str(e)}")
        response_stream.flush()
        return None

    except Exception as e:
        response_stream = TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
        write_error_chunk(response_stream, "internal_error", f"Internal server error: {str(e)}")
        response_stream.flush()
        return None
