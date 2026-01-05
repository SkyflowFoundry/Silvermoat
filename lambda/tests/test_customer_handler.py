"""
Unit tests for customer_handler - customer and quote operations.

Tests all routes:
- GET / (root health check)
- GET/POST/DELETE /customer
- GET/POST/DELETE /quote
- Query filters (customerEmail, limit)
- Error cases (404, 400, invalid JSON)
"""
import json
import pytest
from customer_handler.handler import handler


class TestRootEndpoint:
    """Tests for GET / root health check"""

    def test_root_returns_endpoint_list(self, api_gateway_event, lambda_context, dynamodb_tables):
        """Root endpoint should return list of available endpoints"""
        event = api_gateway_event(method="GET", path="/")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["name"] == "Silvermoat MVP"
        assert "endpoints" in body
        assert "/customer" in body["endpoints"]
        assert "/quote" in body["endpoints"]

    def test_cors_preflight(self, api_gateway_event, lambda_context, dynamodb_tables):
        """OPTIONS requests should return 200 for CORS preflight"""
        event = api_gateway_event(method="OPTIONS", path="/customer")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["message"] == "CORS preflight"


class TestCustomerEndpoints:
    """Tests for /customer CRUD operations"""

    def test_create_customer(self, api_gateway_event, lambda_context, storage_backend, sample_customer_data):
        """POST /customer should create a new customer"""
        event = api_gateway_event(method="POST", path="/customer", body=sample_customer_data)
        response = handler(event, lambda_context)

        assert response["statusCode"] == 201
        body = json.loads(response["body"])
        assert "id" in body
        assert "item" in body
        assert body["item"]["status"] == "ACTIVE"
        assert body["item"]["email"] == sample_customer_data["email"]

    def test_create_customer_upserts_by_email(
        self, api_gateway_event, lambda_context, storage_backend, sample_customer_data
    ):
        """POST /customer with existing email should return existing customer"""
        # Create first customer
        event1 = api_gateway_event(method="POST", path="/customer", body=sample_customer_data)
        response1 = handler(event1, lambda_context)
        body1 = json.loads(response1["body"])
        customer_id = body1["id"]

        # Create second customer with same email
        event2 = api_gateway_event(method="POST", path="/customer", body=sample_customer_data)
        response2 = handler(event2, lambda_context)
        body2 = json.loads(response2["body"])

        # Should return same customer ID (upsert behavior)
        assert body2["id"] == customer_id

    def test_get_customer_by_id(self, api_gateway_event, lambda_context, storage_backend, sample_customer_data):
        """GET /customer/{id} should return customer by ID"""
        # Create customer
        create_event = api_gateway_event(method="POST", path="/customer", body=sample_customer_data)
        create_response = handler(create_event, lambda_context)
        customer_id = json.loads(create_response["body"])["id"]

        # Get customer
        get_event = api_gateway_event(method="GET", path=f"/customer/{customer_id}")
        get_response = handler(get_event, lambda_context)

        assert get_response["statusCode"] == 200
        body = json.loads(get_response["body"])
        assert body["id"] == customer_id
        assert body["email"] == sample_customer_data["email"]

    def test_get_customer_not_found(self, api_gateway_event, lambda_context, dynamodb_tables):
        """GET /customer/{id} with non-existent ID should return 404"""
        event = api_gateway_event(method="GET", path="/customer/nonexistent-id")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 404
        body = json.loads(response["body"])
        assert body["error"] == "not_found"
        assert body["id"] == "nonexistent-id"

    def test_list_customers(self, api_gateway_event, lambda_context, storage_backend, sample_customer_data):
        """GET /customer should list all customers"""
        # Create two customers
        data1 = dict(sample_customer_data, email="customer1@example.com")
        data2 = dict(sample_customer_data, email="customer2@example.com")
        handler(api_gateway_event(method="POST", path="/customer", body=data1), lambda_context)
        handler(api_gateway_event(method="POST", path="/customer", body=data2), lambda_context)

        # List customers
        event = api_gateway_event(method="GET", path="/customer")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["count"] == 2
        assert len(body["items"]) == 2

    def test_list_customers_with_limit(self, api_gateway_event, lambda_context, storage_backend, sample_customer_data):
        """GET /customer?limit=1 should limit results"""
        # Create two customers
        data1 = dict(sample_customer_data, email="customer1@example.com")
        data2 = dict(sample_customer_data, email="customer2@example.com")
        handler(api_gateway_event(method="POST", path="/customer", body=data1), lambda_context)
        handler(api_gateway_event(method="POST", path="/customer", body=data2), lambda_context)

        # List with limit
        event = api_gateway_event(method="GET", path="/customer", query_params={"limit": "1"})
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert len(body["items"]) == 1

    def test_delete_customer(self, api_gateway_event, lambda_context, storage_backend, sample_customer_data):
        """DELETE /customer/{id} should delete customer"""
        # Create customer
        create_event = api_gateway_event(method="POST", path="/customer", body=sample_customer_data)
        create_response = handler(create_event, lambda_context)
        customer_id = json.loads(create_response["body"])["id"]

        # Delete customer
        delete_event = api_gateway_event(method="DELETE", path=f"/customer/{customer_id}")
        delete_response = handler(delete_event, lambda_context)

        assert delete_response["statusCode"] == 200
        body = json.loads(delete_response["body"])
        assert body["deleted"] is True
        assert body["id"] == customer_id

    def test_delete_all_customers(self, api_gateway_event, lambda_context, storage_backend, sample_customer_data):
        """DELETE /customer should delete all customers"""
        # Create two customers
        data1 = dict(sample_customer_data, email="customer1@example.com")
        data2 = dict(sample_customer_data, email="customer2@example.com")
        handler(api_gateway_event(method="POST", path="/customer", body=data1), lambda_context)
        handler(api_gateway_event(method="POST", path="/customer", body=data2), lambda_context)

        # Delete all
        event = api_gateway_event(method="DELETE", path="/customer")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["deleted"] == 2
        assert body["domain"] == "customer"


class TestQuoteEndpoints:
    """Tests for /quote CRUD operations"""

    def test_create_quote_with_existing_customer(
        self, api_gateway_event, lambda_context, storage_backend, sample_customer_data, sample_quote_data
    ):
        """POST /quote should create quote and link to existing customer"""
        # Create customer first
        customer_event = api_gateway_event(method="POST", path="/customer", body=sample_customer_data)
        customer_response = handler(customer_event, lambda_context)
        customer_id = json.loads(customer_response["body"])["id"]

        # Create quote
        quote_event = api_gateway_event(method="POST", path="/quote", body=sample_quote_data)
        quote_response = handler(quote_event, lambda_context)

        assert quote_response["statusCode"] == 201
        body = json.loads(quote_response["body"])
        assert "id" in body
        assert body["item"]["status"] == "PENDING"
        assert body["item"]["data"]["coverageType"] == "AUTO"
        # Should have customerId from upserted customer
        assert "customerId" in body["item"]["data"]

    def test_create_quote_creates_new_customer(
        self, api_gateway_event, lambda_context, storage_backend, sample_quote_data
    ):
        """POST /quote should create new customer if email doesn't exist"""
        # Create quote without pre-existing customer
        quote_event = api_gateway_event(method="POST", path="/quote", body=sample_quote_data)
        quote_response = handler(quote_event, lambda_context)

        assert quote_response["statusCode"] == 201
        body = json.loads(quote_response["body"])
        assert "id" in body
        assert "customerId" in body["item"]["data"]

    def test_get_quote_by_id(self, api_gateway_event, lambda_context, storage_backend, sample_quote_data):
        """GET /quote/{id} should return quote by ID"""
        # Create quote
        create_event = api_gateway_event(method="POST", path="/quote", body=sample_quote_data)
        create_response = handler(create_event, lambda_context)
        quote_id = json.loads(create_response["body"])["id"]

        # Get quote
        get_event = api_gateway_event(method="GET", path=f"/quote/{quote_id}")
        get_response = handler(get_event, lambda_context)

        assert get_response["statusCode"] == 200
        body = json.loads(get_response["body"])
        assert body["id"] == quote_id
        assert body["data"]["coverageType"] == "AUTO"

    def test_list_quotes_by_customer_email(
        self, api_gateway_event, lambda_context, storage_backend, sample_customer_data, sample_quote_data
    ):
        """GET /quote?customerEmail=... should filter quotes by customer"""
        # Create customer and quote
        customer_email = "test@example.com"
        customer_data = dict(sample_customer_data, email=customer_email)
        handler(api_gateway_event(method="POST", path="/customer", body=customer_data), lambda_context)
        handler(api_gateway_event(method="POST", path="/quote", body=sample_quote_data), lambda_context)

        # List quotes by customer email
        event = api_gateway_event(method="GET", path="/quote", query_params={"customerEmail": customer_email})
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["count"] >= 1

    def test_list_quotes_by_nonexistent_customer_returns_empty(
        self, api_gateway_event, lambda_context, dynamodb_tables
    ):
        """GET /quote?customerEmail=nonexistent should return empty list"""
        event = api_gateway_event(method="GET", path="/quote", query_params={"customerEmail": "nonexistent@example.com"})
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["count"] == 0
        assert body["items"] == []

    def test_delete_quote(self, api_gateway_event, lambda_context, storage_backend, sample_quote_data):
        """DELETE /quote/{id} should delete quote"""
        # Create quote
        create_event = api_gateway_event(method="POST", path="/quote", body=sample_quote_data)
        create_response = handler(create_event, lambda_context)
        quote_id = json.loads(create_response["body"])["id"]

        # Delete quote
        delete_event = api_gateway_event(method="DELETE", path=f"/quote/{quote_id}")
        delete_response = handler(delete_event, lambda_context)

        assert delete_response["statusCode"] == 200
        body = json.loads(delete_response["body"])
        assert body["deleted"] is True


class TestErrorHandling:
    """Tests for error cases and edge conditions"""

    def test_invalid_domain_returns_404(self, api_gateway_event, lambda_context, dynamodb_tables):
        """Request to invalid domain should return 404"""
        event = api_gateway_event(method="GET", path="/invalid-domain")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 404
        body = json.loads(response["body"])
        assert body["error"] == "unknown_domain"
        assert body["domain"] == "invalid-domain"

    def test_unsupported_operation_returns_400(self, api_gateway_event, lambda_context, dynamodb_tables):
        """Unsupported HTTP method should return 400"""
        event = api_gateway_event(method="PATCH", path="/customer")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert body["error"] == "unsupported_operation"

    def test_malformed_json_body(self, api_gateway_event, lambda_context, dynamodb_tables):
        """Malformed JSON body should be handled gracefully"""
        event = api_gateway_event(method="POST", path="/customer", body="{invalid json}")
        response = handler(event, lambda_context)

        # Handler should process without crashing (body wrapped in {"raw": ...})
        assert response["statusCode"] in [201, 400, 500]
