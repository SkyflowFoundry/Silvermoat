"""
API integration tests.
"""
import pytest
import requests
import uuid
from decimal import Decimal


@pytest.mark.api
def test_api_root_endpoint(api_base_url):
    """Test that API root endpoint responds."""
    response = requests.get(api_base_url)
    assert response.status_code == 200

    # API should return list of available endpoints
    data = response.json()
    assert isinstance(data, dict) or isinstance(data, list)


@pytest.mark.api
def test_api_cors_headers(api_base_url):
    """Test that API returns CORS headers."""
    response = requests.get(api_base_url)
    assert "Access-Control-Allow-Origin" in response.headers
    assert response.headers["Access-Control-Allow-Origin"] == "*"


@pytest.mark.api
def test_create_quote(api_base_url):
    """Test creating a new quote via POST /quote."""
    quote_data = {
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "coverage_type": "auto",
        "coverage_amount": 100000,
        "annual_premium_cents": 50000,
    }

    response = requests.post(f"{api_base_url}/quote", json=quote_data)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["customer_name"] == "Test User"
    assert data["coverage_type"] == "auto"

    # Return quote ID for other tests
    return data["id"]


@pytest.mark.api
def test_get_quote(api_base_url):
    """Test retrieving a quote via GET /quote/{id}."""
    # First create a quote
    quote_id = test_create_quote(api_base_url)

    # Then retrieve it
    response = requests.get(f"{api_base_url}/quote/{quote_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == quote_id
    assert "customer_name" in data


@pytest.mark.api
def test_create_policy(api_base_url):
    """Test creating a new policy via POST /policy."""
    policy_data = {
        "customer_name": "Test User",
        "policy_number": f"POL-{uuid.uuid4().hex[:8].upper()}",
        "coverage_type": "auto",
        "status": "active",
        "annual_premium_cents": 50000,
    }

    response = requests.post(f"{api_base_url}/policy", json=policy_data)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["policy_number"] == policy_data["policy_number"]


@pytest.mark.api
def test_create_claim(api_base_url):
    """Test creating a new claim via POST /claim."""
    claim_data = {
        "policy_id": f"pol-{uuid.uuid4().hex[:8]}",
        "claim_number": f"CLM-{uuid.uuid4().hex[:8].upper()}",
        "claim_type": "auto",
        "status": "submitted",
        "amount_cents": 25000,
        "description": "Test claim",
    }

    response = requests.post(f"{api_base_url}/claim", json=claim_data)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["claim_number"] == claim_data["claim_number"]


@pytest.mark.api
def test_create_payment(api_base_url):
    """Test creating a new payment via POST /payment."""
    payment_data = {
        "policy_id": f"pol-{uuid.uuid4().hex[:8]}",
        "amount_cents": 50000,
        "payment_method": "credit_card",
        "status": "completed",
    }

    response = requests.post(f"{api_base_url}/payment", json=payment_data)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["amount_cents"] == payment_data["amount_cents"]


@pytest.mark.api
def test_api_error_handling(api_base_url):
    """Test that API returns proper error responses."""
    # Try to get non-existent quote
    response = requests.get(f"{api_base_url}/quote/nonexistent-id")
    assert response.status_code in [404, 500]  # Either is acceptable

    # Try invalid POST data (missing required fields)
    response = requests.post(f"{api_base_url}/quote", json={})
    assert response.status_code in [400, 500]


@pytest.mark.api
def test_api_response_format(api_base_url):
    """Test that API responses are properly formatted JSON."""
    response = requests.get(api_base_url)
    assert response.headers["Content-Type"].startswith("application/json")

    # Should be valid JSON
    try:
        data = response.json()
    except ValueError:
        pytest.fail("API response is not valid JSON")
