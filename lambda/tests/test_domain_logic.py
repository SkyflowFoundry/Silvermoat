"""
Unit tests for shared.domain_logic - business logic utilities.

Tests:
- upsert_customer_for_quote() - Customer upsert from quote data
- upsert_customer_for_policy() - Customer upsert from policy data
- get_customer_id_from_policy() - Customer ID extraction from policy
"""
import pytest
from shared.domain_logic import (
    upsert_customer_for_quote,
    upsert_customer_for_policy,
    get_customer_id_from_policy,
)


class TestQuoteCustomerUpsert:
    """Tests for upsert_customer_for_quote()"""

    def test_upsert_creates_customer_from_quote(self, storage_backend):
        """Should create customer from quote data"""
        body = {
            "customerName": "John Doe",
            "customerEmail": "john@example.com",
            "coverageType": "AUTO",
            "premium": 1200,
        }

        customer_id = upsert_customer_for_quote(storage_backend, body)

        assert customer_id is not None
        # Verify customer was created
        customer = storage_backend.get("customer", customer_id)
        assert customer is not None
        assert customer["email"] == "john@example.com"

    def test_upsert_removes_customer_fields_from_body(self, storage_backend):
        """Should remove customerName and customerEmail from body"""
        body = {
            "customerName": "John Doe",
            "customerEmail": "john@example.com",
            "coverageType": "AUTO",
        }

        upsert_customer_for_quote(storage_backend, body)

        # Customer fields should be removed
        assert "customerName" not in body
        assert "customerEmail" not in body
        # Other fields should remain
        assert "coverageType" in body

    def test_upsert_returns_existing_customer_id(self, storage_backend):
        """Should return existing customer ID if email already exists"""
        # Create customer first
        storage_backend.upsert_customer("john@example.com", {"name": "John Doe"})

        # Try to create quote with same email
        body = {
            "customerName": "John Doe",
            "customerEmail": "john@example.com",
            "coverageType": "AUTO",
        }

        customer_id = upsert_customer_for_quote(storage_backend, body)

        # Should return existing customer ID
        assert customer_id is not None
        customers = storage_backend.query_by_email("customer", "john@example.com")
        assert len(customers) == 1
        assert customers[0]["id"] == customer_id

    def test_upsert_returns_none_without_email(self, storage_backend):
        """Should return None if no customerEmail provided"""
        body = {
            "customerName": "John Doe",
            "coverageType": "AUTO",
        }

        customer_id = upsert_customer_for_quote(storage_backend, body)

        assert customer_id is None


class TestPolicyCustomerUpsert:
    """Tests for upsert_customer_for_policy()"""

    def test_upsert_creates_customer_from_policy(self, storage_backend):
        """Should create customer from policy data with holderEmail"""
        body = {
            "holderName": "Jane Smith",
            "holderEmail": "jane@example.com",
            "policyNumber": "POL-123",
        }

        customer_id = upsert_customer_for_policy(storage_backend, body)

        assert customer_id is not None
        customer = storage_backend.get("customer", customer_id)
        assert customer["email"] == "jane@example.com"

    def test_upsert_uses_customer_email_fallback(self, storage_backend):
        """Should use customer_email if holderEmail not provided"""
        body = {
            "holderName": "Jane Smith",
            "customer_email": "jane@example.com",
            "policyNumber": "POL-123",
        }

        customer_id = upsert_customer_for_policy(storage_backend, body)

        assert customer_id is not None
        customer = storage_backend.get("customer", customer_id)
        assert customer["email"] == "jane@example.com"

    def test_upsert_removes_policy_fields_from_body(self, storage_backend):
        """Should remove holderName, holderEmail, customer_email from body"""
        body = {
            "holderName": "Jane Smith",
            "holderEmail": "jane@example.com",
            "customer_email": "backup@example.com",
            "policyNumber": "POL-123",
        }

        upsert_customer_for_policy(storage_backend, body)

        # Customer fields should be removed
        assert "holderName" not in body
        assert "holderEmail" not in body
        assert "customer_email" not in body
        # Other fields should remain
        assert "policyNumber" in body

    def test_upsert_returns_existing_customer(self, storage_backend):
        """Should return existing customer ID if email exists"""
        # Create customer first
        storage_backend.upsert_customer("jane@example.com", {"name": "Jane Smith"})

        body = {
            "holderName": "Jane Smith",
            "holderEmail": "jane@example.com",
            "policyNumber": "POL-123",
        }

        customer_id = upsert_customer_for_policy(storage_backend, body)

        # Should return existing customer ID
        customers = storage_backend.query_by_email("customer", "jane@example.com")
        assert len(customers) == 1
        assert customers[0]["id"] == customer_id

    def test_upsert_returns_none_without_email(self, storage_backend):
        """Should return None if no email provided"""
        body = {
            "holderName": "Jane Smith",
            "policyNumber": "POL-123",
        }

        customer_id = upsert_customer_for_policy(storage_backend, body)

        assert customer_id is None


class TestGetCustomerIdFromPolicy:
    """Tests for get_customer_id_from_policy()"""

    def test_get_customer_id_from_existing_policy(self, storage_backend):
        """Should extract customerId from existing policy"""
        # Create policy with customerId
        policy_data = {
            "customerId": "cust-123",
            "policyNumber": "POL-456",
        }
        policy = storage_backend.create("policy", policy_data, "ACTIVE", {"customerId": "cust-123"})
        policy_id = policy["id"]

        customer_id = get_customer_id_from_policy(storage_backend, policy_id)

        assert customer_id == "cust-123"

    def test_get_customer_id_returns_none_for_nonexistent_policy(self, storage_backend):
        """Should return None if policy doesn't exist"""
        customer_id = get_customer_id_from_policy(storage_backend, "nonexistent-policy-id")

        assert customer_id is None

    def test_get_customer_id_returns_none_for_none_policy_id(self, storage_backend):
        """Should return None if policy_id is None"""
        customer_id = get_customer_id_from_policy(storage_backend, None)

        assert customer_id is None

    def test_get_customer_id_returns_none_for_empty_policy_id(self, storage_backend):
        """Should return None if policy_id is empty string"""
        customer_id = get_customer_id_from_policy(storage_backend, "")

        assert customer_id is None

    def test_get_customer_id_returns_none_if_policy_has_no_customer_id(self, storage_backend):
        """Should return None if policy exists but has no customerId"""
        # Create policy without customerId
        policy = storage_backend.create("policy", {"policyNumber": "POL-789"}, "ACTIVE")
        policy_id = policy["id"]

        customer_id = get_customer_id_from_policy(storage_backend, policy_id)

        assert customer_id is None
