"""
Unit tests for documents_handler - document upload operations.

Tests all routes:
- POST /claim/{id}/doc
"""
import json
import pytest
import boto3
from documents_handler.handler import handler


class TestDocumentUpload:
    """Tests for document upload operations"""

    def test_upload_to_nonexistent_claim_returns_404(
        self, api_gateway_event, lambda_context, dynamodb_tables
    ):
        """POST /claim/{id}/doc with non-existent claim should return 404"""
        doc_event = api_gateway_event(method="POST", path="/claim/nonexistent-id/doc", body={"text": "Test"})
        doc_response = handler(doc_event, lambda_context)

        assert doc_response["statusCode"] == 404
        body = json.loads(doc_response["body"])
        assert body["error"] == "claim_not_found"
        assert body["id"] == "nonexistent-id"

    def test_cors_preflight(self, api_gateway_event, lambda_context, dynamodb_tables):
        """OPTIONS requests should return 200 for CORS"""
        event = api_gateway_event(method="OPTIONS", path="/claim/123/doc")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["message"] == "CORS preflight"

    def test_invalid_path_returns_404(self, api_gateway_event, lambda_context, dynamodb_tables):
        """Invalid paths should return 404"""
        event = api_gateway_event(method="POST", path="/invalid-path")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 404
        body = json.loads(response["body"])
        assert body["error"] == "not_found"
