"""
Unit tests for claims_handler - policy, claim, payment, and case operations.

Tests all routes:
- GET/POST/DELETE /policy
- GET/POST/DELETE /claim
- POST /claim/{id}/status
- GET/POST/DELETE /payment
- GET/POST/DELETE /case
- Query filters (customerEmail, limit)
"""
import json
import pytest
from claims_handler.handler import handler


@pytest.fixture
def sample_policy_data(sample_customer_data):
    """Sample policy data for testing"""
    return {
        "customer": sample_customer_data,
        "policyNumber": "POL-12345",
        "coverageType": "AUTO",
        "premium": 1200,
        "deductible": 500,
        "startDate": "2024-01-01",
        "endDate": "2025-01-01",
    }


@pytest.fixture
def sample_claim_data():
    """Sample claim data for testing"""
    return {
        "policyId": "test-policy-id",
        "claimNumber": "CLM-12345",
        "incidentDate": "2024-06-15",
        "description": "Vehicle accident",
        "claimAmount": 5000,
    }


@pytest.fixture
def sample_payment_data():
    """Sample payment data for testing"""
    return {
        "policyId": "test-policy-id",
        "amount": 1200,
        "paymentMethod": "CREDIT_CARD",
        "paymentDate": "2024-01-01",
    }


@pytest.fixture
def sample_case_data():
    """Sample case data for testing"""
    return {
        "customerId": "test-customer-id",
        "caseType": "INQUIRY",
        "subject": "Policy question",
        "description": "Question about coverage",
    }


class TestPolicyEndpoints:
    """Tests for /policy CRUD operations"""

    def test_create_policy_with_customer(
        self, api_gateway_event, lambda_context, storage_backend, sample_policy_data
    ):
        """POST /policy should create policy and upsert customer"""
        event = api_gateway_event(method="POST", path="/policy", body=sample_policy_data)
        response = handler(event, lambda_context)

        assert response["statusCode"] == 201
        body = json.loads(response["body"])
        assert "id" in body
        assert body["item"]["status"] == "ACTIVE"
        assert body["item"]["data"]["policyNumber"] == "POL-12345"
        # Should have customerId from upserted customer (at top level for GSI)
        assert "customerId" in body["item"]

    def test_get_policy_by_id(self, api_gateway_event, lambda_context, storage_backend, sample_policy_data):
        """GET /policy/{id} should return policy by ID"""
        # Create policy
        create_event = api_gateway_event(method="POST", path="/policy", body=sample_policy_data)
        create_response = handler(create_event, lambda_context)
        policy_id = json.loads(create_response["body"])["id"]

        # Get policy
        get_event = api_gateway_event(method="GET", path=f"/policy/{policy_id}")
        get_response = handler(get_event, lambda_context)

        assert get_response["statusCode"] == 200
        body = json.loads(get_response["body"])
        assert body["id"] == policy_id
        assert body["data"]["policyNumber"] == "POL-12345"

    def test_list_policies(self, api_gateway_event, lambda_context, storage_backend, sample_policy_data):
        """GET /policy should list all policies"""
        # Create two policies
        data1 = dict(sample_policy_data, policyNumber="POL-001")
        data2 = dict(sample_policy_data, policyNumber="POL-002")
        handler(api_gateway_event(method="POST", path="/policy", body=data1), lambda_context)
        handler(api_gateway_event(method="POST", path="/policy", body=data2), lambda_context)

        # List policies
        event = api_gateway_event(method="GET", path="/policy")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["count"] >= 2

    def test_list_policies_by_customer_email(
        self, api_gateway_event, lambda_context, storage_backend, sample_policy_data
    ):
        """GET /policy?customerEmail=... should filter by customer"""
        # Create policy with customer
        handler(api_gateway_event(method="POST", path="/policy", body=sample_policy_data), lambda_context)

        customer_email = sample_policy_data["customer"]["email"]
        event = api_gateway_event(method="GET", path="/policy", query_params={"customerEmail": customer_email})
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["count"] >= 1

    def test_delete_policy(self, api_gateway_event, lambda_context, storage_backend, sample_policy_data):
        """DELETE /policy/{id} should delete policy"""
        # Create policy
        create_event = api_gateway_event(method="POST", path="/policy", body=sample_policy_data)
        create_response = handler(create_event, lambda_context)
        policy_id = json.loads(create_response["body"])["id"]

        # Delete policy
        delete_event = api_gateway_event(method="DELETE", path=f"/policy/{policy_id}")
        delete_response = handler(delete_event, lambda_context)

        assert delete_response["statusCode"] == 200
        body = json.loads(delete_response["body"])
        assert body["deleted"] is True


class TestClaimEndpoints:
    """Tests for /claim CRUD operations"""

    def test_create_claim_with_policy(
        self, api_gateway_event, lambda_context, storage_backend, sample_policy_data, sample_claim_data
    ):
        """POST /claim should create claim and denormalize customerId from policy"""
        # Create policy first
        policy_event = api_gateway_event(method="POST", path="/policy", body=sample_policy_data)
        policy_response = handler(policy_event, lambda_context)
        policy_id = json.loads(policy_response["body"])["id"]

        # Create claim with policy ID
        claim_data = dict(sample_claim_data, policyId=policy_id)
        claim_event = api_gateway_event(method="POST", path="/claim", body=claim_data)
        claim_response = handler(claim_event, lambda_context)

        assert claim_response["statusCode"] == 201
        body = json.loads(claim_response["body"])
        assert "id" in body
        assert body["item"]["status"] == "PENDING"
        assert body["item"]["data"]["claimNumber"] == "CLM-12345"
        # Should have customerId denormalized from policy (at top level for GSI)
        assert "customerId" in body["item"]

    def test_get_claim_by_id(
        self, api_gateway_event, lambda_context, storage_backend, sample_policy_data, sample_claim_data
    ):
        """GET /claim/{id} should return claim by ID"""
        # Create policy and claim
        policy_event = api_gateway_event(method="POST", path="/policy", body=sample_policy_data)
        policy_response = handler(policy_event, lambda_context)
        policy_id = json.loads(policy_response["body"])["id"]

        claim_data = dict(sample_claim_data, policyId=policy_id)
        claim_event = api_gateway_event(method="POST", path="/claim", body=claim_data)
        claim_response = handler(claim_event, lambda_context)
        claim_id = json.loads(claim_response["body"])["id"]

        # Get claim
        get_event = api_gateway_event(method="GET", path=f"/claim/{claim_id}")
        get_response = handler(get_event, lambda_context)

        assert get_response["statusCode"] == 200
        body = json.loads(get_response["body"])
        assert body["id"] == claim_id

    def test_list_claims_by_customer_email(
        self, api_gateway_event, lambda_context, storage_backend, sample_policy_data, sample_claim_data
    ):
        """GET /claim?customerEmail=... should filter by customer"""
        # Create policy and claim
        policy_event = api_gateway_event(method="POST", path="/policy", body=sample_policy_data)
        policy_response = handler(policy_event, lambda_context)
        policy_id = json.loads(policy_response["body"])["id"]

        claim_data = dict(sample_claim_data, policyId=policy_id)
        handler(api_gateway_event(method="POST", path="/claim", body=claim_data), lambda_context)

        customer_email = sample_policy_data["customer"]["email"]
        event = api_gateway_event(method="GET", path="/claim", query_params={"customerEmail": customer_email})
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["count"] >= 1

    def test_update_claim_status(
        self, api_gateway_event, lambda_context, storage_backend, sample_policy_data, sample_claim_data
    ):
        """POST /claim/{id}/status should update claim status"""
        # Create policy and claim
        policy_event = api_gateway_event(method="POST", path="/policy", body=sample_policy_data)
        policy_response = handler(policy_event, lambda_context)
        policy_id = json.loads(policy_response["body"])["id"]

        claim_data = dict(sample_claim_data, policyId=policy_id)
        claim_event = api_gateway_event(method="POST", path="/claim", body=claim_data)
        claim_response = handler(claim_event, lambda_context)
        claim_id = json.loads(claim_response["body"])["id"]

        # Update status
        status_event = api_gateway_event(
            method="POST", path=f"/claim/{claim_id}/status", body={"status": "APPROVED"}
        )
        status_response = handler(status_event, lambda_context)

        assert status_response["statusCode"] == 200
        body = json.loads(status_response["body"])
        assert body["status"] == "APPROVED"
        assert body["id"] == claim_id

    def test_update_claim_status_defaults_to_review(
        self, api_gateway_event, lambda_context, storage_backend, sample_policy_data, sample_claim_data
    ):
        """POST /claim/{id}/status without status should default to REVIEW"""
        # Create policy and claim
        policy_event = api_gateway_event(method="POST", path="/policy", body=sample_policy_data)
        policy_response = handler(policy_event, lambda_context)
        policy_id = json.loads(policy_response["body"])["id"]

        claim_data = dict(sample_claim_data, policyId=policy_id)
        claim_event = api_gateway_event(method="POST", path="/claim", body=claim_data)
        claim_response = handler(claim_event, lambda_context)
        claim_id = json.loads(claim_response["body"])["id"]

        # Update without status
        status_event = api_gateway_event(method="POST", path=f"/claim/{claim_id}/status", body={})
        status_response = handler(status_event, lambda_context)

        assert status_response["statusCode"] == 200
        body = json.loads(status_response["body"])
        assert body["status"] == "REVIEW"

    def test_delete_claim(
        self, api_gateway_event, lambda_context, storage_backend, sample_policy_data, sample_claim_data
    ):
        """DELETE /claim/{id} should delete claim"""
        # Create policy and claim
        policy_event = api_gateway_event(method="POST", path="/policy", body=sample_policy_data)
        policy_response = handler(policy_event, lambda_context)
        policy_id = json.loads(policy_response["body"])["id"]

        claim_data = dict(sample_claim_data, policyId=policy_id)
        claim_event = api_gateway_event(method="POST", path="/claim", body=claim_data)
        claim_response = handler(claim_event, lambda_context)
        claim_id = json.loads(claim_response["body"])["id"]

        # Delete claim
        delete_event = api_gateway_event(method="DELETE", path=f"/claim/{claim_id}")
        delete_response = handler(delete_event, lambda_context)

        assert delete_response["statusCode"] == 200
        body = json.loads(delete_response["body"])
        assert body["deleted"] is True


class TestPaymentEndpoints:
    """Tests for /payment CRUD operations"""

    def test_create_payment(self, api_gateway_event, lambda_context, storage_backend, sample_payment_data):
        """POST /payment should create payment"""
        event = api_gateway_event(method="POST", path="/payment", body=sample_payment_data)
        response = handler(event, lambda_context)

        assert response["statusCode"] == 201
        body = json.loads(response["body"])
        assert "id" in body
        assert body["item"]["status"] == "PENDING"
        assert body["item"]["data"]["amount"] == 1200

    def test_get_payment_by_id(self, api_gateway_event, lambda_context, storage_backend, sample_payment_data):
        """GET /payment/{id} should return payment by ID"""
        # Create payment
        create_event = api_gateway_event(method="POST", path="/payment", body=sample_payment_data)
        create_response = handler(create_event, lambda_context)
        payment_id = json.loads(create_response["body"])["id"]

        # Get payment
        get_event = api_gateway_event(method="GET", path=f"/payment/{payment_id}")
        get_response = handler(get_event, lambda_context)

        assert get_response["statusCode"] == 200
        body = json.loads(get_response["body"])
        assert body["id"] == payment_id

    def test_list_payments(self, api_gateway_event, lambda_context, storage_backend, sample_payment_data):
        """GET /payment should list all payments"""
        # Create two payments
        handler(api_gateway_event(method="POST", path="/payment", body=sample_payment_data), lambda_context)
        handler(api_gateway_event(method="POST", path="/payment", body=sample_payment_data), lambda_context)

        # List payments
        event = api_gateway_event(method="GET", path="/payment")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["count"] >= 2

    def test_delete_payment(self, api_gateway_event, lambda_context, storage_backend, sample_payment_data):
        """DELETE /payment/{id} should delete payment"""
        # Create payment
        create_event = api_gateway_event(method="POST", path="/payment", body=sample_payment_data)
        create_response = handler(create_event, lambda_context)
        payment_id = json.loads(create_response["body"])["id"]

        # Delete payment
        delete_event = api_gateway_event(method="DELETE", path=f"/payment/{payment_id}")
        delete_response = handler(delete_event, lambda_context)

        assert delete_response["statusCode"] == 200
        body = json.loads(delete_response["body"])
        assert body["deleted"] is True


class TestCaseEndpoints:
    """Tests for /case CRUD operations"""

    def test_create_case(self, api_gateway_event, lambda_context, storage_backend, sample_case_data):
        """POST /case should create case"""
        event = api_gateway_event(method="POST", path="/case", body=sample_case_data)
        response = handler(event, lambda_context)

        assert response["statusCode"] == 201
        body = json.loads(response["body"])
        assert "id" in body
        assert body["item"]["status"] == "OPEN"
        assert body["item"]["data"]["subject"] == "Policy question"

    def test_get_case_by_id(self, api_gateway_event, lambda_context, storage_backend, sample_case_data):
        """GET /case/{id} should return case by ID"""
        # Create case
        create_event = api_gateway_event(method="POST", path="/case", body=sample_case_data)
        create_response = handler(create_event, lambda_context)
        case_id = json.loads(create_response["body"])["id"]

        # Get case
        get_event = api_gateway_event(method="GET", path=f"/case/{case_id}")
        get_response = handler(get_event, lambda_context)

        assert get_response["statusCode"] == 200
        body = json.loads(get_response["body"])
        assert body["id"] == case_id

    def test_list_cases(self, api_gateway_event, lambda_context, storage_backend, sample_case_data):
        """GET /case should list all cases"""
        # Create two cases
        handler(api_gateway_event(method="POST", path="/case", body=sample_case_data), lambda_context)
        handler(api_gateway_event(method="POST", path="/case", body=sample_case_data), lambda_context)

        # List cases
        event = api_gateway_event(method="GET", path="/case")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["count"] >= 2

    def test_delete_case(self, api_gateway_event, lambda_context, storage_backend, sample_case_data):
        """DELETE /case/{id} should delete case"""
        # Create case
        create_event = api_gateway_event(method="POST", path="/case", body=sample_case_data)
        create_response = handler(create_event, lambda_context)
        case_id = json.loads(create_response["body"])["id"]

        # Delete case
        delete_event = api_gateway_event(method="DELETE", path=f"/case/{case_id}")
        delete_response = handler(delete_event, lambda_context)

        assert delete_response["statusCode"] == 200
        body = json.loads(delete_response["body"])
        assert body["deleted"] is True


class TestErrorHandling:
    """Tests for error cases"""

    def test_root_path_returns_404(self, api_gateway_event, lambda_context, dynamodb_tables):
        """GET / should return 404 (no root endpoint)"""
        event = api_gateway_event(method="GET", path="/")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 404
        body = json.loads(response["body"])
        assert body["error"] == "not_found"

    def test_invalid_domain_returns_404(self, api_gateway_event, lambda_context, dynamodb_tables):
        """Request to invalid domain should return 404"""
        event = api_gateway_event(method="GET", path="/invalid")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 404
        body = json.loads(response["body"])
        assert body["error"] == "unknown_domain"

    def test_nonexistent_item_returns_404(self, api_gateway_event, lambda_context, dynamodb_tables):
        """GET with non-existent ID should return 404"""
        event = api_gateway_event(method="GET", path="/claim/nonexistent-id")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 404
        body = json.loads(response["body"])
        assert body["error"] == "not_found"

    def test_cors_preflight(self, api_gateway_event, lambda_context, dynamodb_tables):
        """OPTIONS requests should return 200 for CORS"""
        event = api_gateway_event(method="OPTIONS", path="/policy")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
