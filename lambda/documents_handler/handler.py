"""
Documents Handler - Manages document uploads to S3.

Routes:
- POST /claim/{id}/doc
"""
import os
import json
import boto3
from shared.responses import _resp
from shared.events import _emit
from shared.storage import DynamoDBBackend


# Initialize clients
storage = DynamoDBBackend()
s3 = boto3.client("s3")
DOCS_BUCKET = os.environ["DOCS_BUCKET"]


def handler(event, context):
    """Handler for document upload operations"""
    path = (event.get("path") or "/").strip("/")
    method = (event.get("httpMethod") or "GET").upper()

    # Handle CORS preflight
    if method == "OPTIONS":
        return _resp(200, {"message": "CORS preflight"})

    parts = [p for p in path.split("/") if p]

    # Parse request body
    body = {}
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except Exception:
            body = {"raw": event["body"]}

    # POST /claim/{id}/doc -> attach document to S3
    if len(parts) == 3 and parts[0] == "claim" and parts[2] == "doc" and method == "POST":
        item_id = parts[1]

        # Verify claim exists
        claim = storage.get("claim", item_id)
        if not claim:
            return _resp(404, {"error": "claim_not_found", "id": item_id})

        # Upload document to S3
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

    return _resp(404, {"error": "not_found", "path": event.get("path")})
