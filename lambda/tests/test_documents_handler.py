"""
Unit tests for documents_handler - document upload operations.

Tests all routes:
- POST /claim/{id}/doc
"""
import os
import json
import pytest
from moto import mock_aws
import boto3
from documents_handler.handler import handler


@pytest.fixture
def s3_bucket(aws_credentials):
    """Create mocked S3 bucket"""
    with mock_aws():
        # Set environment variable
        os.environ["DOCS_BUCKET"] = "test-docs-bucket"

        # Create S3 bucket
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-docs-bucket")

        yield s3


class TestDocumentUpload:
    """Tests for document upload operations"""

    def test_upload_claim_document(
        self, api_gateway_event, lambda_context, storage_backend, s3_bucket, sample_policy_data, sample_claim_data
    ):
        """POST /claim/{id}/doc should upload document to S3"""
        # Import claims_handler to create claim
        from claims_handler.handler import handler as claims_handler

        # Create policy and claim
        policy_event = api_gateway_event(method="POST", path="/policy", body=sample_policy_data)
        policy_response = claims_handler(policy_event, lambda_context)
        policy_id = json.loads(policy_response["body"])["id"]

        claim_data = dict(sample_claim_data, policyId=policy_id)
        claim_event = api_gateway_event(method="POST", path="/claim", body=claim_data)
        claim_response = claims_handler(claim_event, lambda_context)
        claim_id = json.loads(claim_response["body"])["id"]

        # Upload document
        doc_data = {"text": "This is a test claim document"}
        doc_event = api_gateway_event(method="POST", path=f"/claim/{claim_id}/doc", body=doc_data)
        doc_response = handler(doc_event, lambda_context)

        assert doc_response["statusCode"] == 200
        body = json.loads(doc_response["body"])
        assert body["id"] == claim_id
        assert "s3Key" in body
        assert body["s3Key"] == f"claims/{claim_id}/note.txt"

        # Verify document exists in S3
        s3_object = s3_bucket.get_object(Bucket="test-docs-bucket", Key=body["s3Key"])
        content = s3_object["Body"].read().decode("utf-8")
        assert content == "This is a test claim document"

    def test_upload_claim_document_with_default_text(
        self, api_gateway_event, lambda_context, storage_backend, s3_bucket, sample_policy_data, sample_claim_data
    ):
        """POST /claim/{id}/doc without text should use default"""
        # Import claims_handler to create claim
        from claims_handler.handler import handler as claims_handler

        # Create policy and claim
        policy_event = api_gateway_event(method="POST", path="/policy", body=sample_policy_data)
        policy_response = claims_handler(policy_event, lambda_context)
        policy_id = json.loads(policy_response["body"])["id"]

        claim_data = dict(sample_claim_data, policyId=policy_id)
        claim_event = api_gateway_event(method="POST", path="/claim", body=claim_data)
        claim_response = claims_handler(claim_event, lambda_context)
        claim_id = json.loads(claim_response["body"])["id"]

        # Upload without text
        doc_event = api_gateway_event(method="POST", path=f"/claim/{claim_id}/doc", body={})
        doc_response = handler(doc_event, lambda_context)

        assert doc_response["statusCode"] == 200

        # Verify default content
        body = json.loads(doc_response["body"])
        s3_object = s3_bucket.get_object(Bucket="test-docs-bucket", Key=body["s3Key"])
        content = s3_object["Body"].read().decode("utf-8")
        assert content == "Demo claim note"

    def test_upload_to_nonexistent_claim_returns_404(
        self, api_gateway_event, lambda_context, dynamodb_tables, s3_bucket
    ):
        """POST /claim/{id}/doc with non-existent claim should return 404"""
        doc_event = api_gateway_event(method="POST", path="/claim/nonexistent-id/doc", body={"text": "Test"})
        doc_response = handler(doc_event, lambda_context)

        assert doc_response["statusCode"] == 404
        body = json.loads(doc_response["body"])
        assert body["error"] == "claim_not_found"
        assert body["id"] == "nonexistent-id"

    def test_cors_preflight(self, api_gateway_event, lambda_context, dynamodb_tables, s3_bucket):
        """OPTIONS requests should return 200 for CORS"""
        event = api_gateway_event(method="OPTIONS", path="/claim/123/doc")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["message"] == "CORS preflight"

    def test_invalid_path_returns_404(self, api_gateway_event, lambda_context, dynamodb_tables, s3_bucket):
        """Invalid paths should return 404"""
        event = api_gateway_event(method="POST", path="/invalid-path")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 404
        body = json.loads(response["body"])
        assert body["error"] == "not_found"
