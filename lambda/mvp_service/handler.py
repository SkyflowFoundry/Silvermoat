"""
DEPRECATED: This handler is being replaced by vertical-specific handlers.

In the new multi-vertical architecture:
- /lambda/insurance/handler.py - Insurance vertical API
- /lambda/retail/handler.py - Retail vertical API

Each vertical gets its own Lambda function and API Gateway.
This file is kept temporarily for backward compatibility during migration.
"""
import os
import json
import boto3
from shared.responses import _resp
from shared.events import _emit
from shared.storage import DynamoDBBackend
from shared.vertical_detector import detect_vertical


# Initialize storage backend
storage = DynamoDBBackend()

# S3 client for document uploads
s3 = boto3.client("s3")
DOCS_BUCKET = os.environ.get("DOCS_BUCKET", "")


def handler(event, context):
    """
    Legacy unified handler - will be replaced by vertical-specific Lambda functions.
    Returns deprecation notice.
    """
    return _resp(200, {
        "message": "This endpoint is deprecated. Use vertical-specific endpoints.",
        "verticals": {
            "insurance": "Deploy insurance vertical Lambda",
            "retail": "Deploy retail vertical Lambda"
        },
        "migration_status": "in_progress"
    })
