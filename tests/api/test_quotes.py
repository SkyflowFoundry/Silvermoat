"""
Quote API Contract Tests

Infrastructure-agnostic tests validating quote API behavior.
Tests verify API contracts without depending on DynamoDB or other implementation details.
"""

import pytest


@pytest.mark.api
@pytest.mark.quotes
def test_create_quote_success(api_client, sample_quote_data):
    """Test that valid quote creation returns 201 with quote ID"""
    response = api_client.api_request('POST', '/quote', json=sample_quote_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    data = response.json()

    # Validate response structure
    assert 'id' in data, "Response should contain quote ID"
    assert isinstance(data['id'], str), "Quote ID should be a string"
    assert len(data['id']) > 0, "Quote ID should not be empty"


@pytest.mark.api
@pytest.mark.quotes
def test_get_quote_by_id(api_client, sample_quote_data):
    """Test that created quote can be retrieved by ID"""
    # Create a quote first
    create_response = api_client.api_request('POST', '/quote', json=sample_quote_data)
    assert create_response.status_code == 201
    quote_id = create_response.json()['id']

    # Retrieve the quote
    get_response = api_client.api_request('GET', f'/quote/{quote_id}')

    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
    quote = get_response.json()

    # Validate quote structure (data is nested under 'data' key)
    assert quote['id'] == quote_id
    assert 'customer_name' in quote['data']
    assert 'customer_email' in quote['data']
    assert 'property_address' in quote['data']
    assert 'coverage_amount' in quote['data']


@pytest.mark.api
@pytest.mark.quotes
def test_get_quote_not_found(api_client):
    """Test that requesting non-existent quote returns 404"""
    non_existent_id = 'quote-does-not-exist-999999'

    response = api_client.api_request('GET', f'/quote/{non_existent_id}')

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


@pytest.mark.api
@pytest.mark.quotes
def test_quote_data_persistence(api_client, sample_quote_data):
    """Test that quote data persists correctly (create then retrieve)"""
    # Create quote
    create_response = api_client.api_request('POST', '/quote', json=sample_quote_data)
    assert create_response.status_code == 201
    quote_id = create_response.json()['id']

    # Retrieve quote
    get_response = api_client.api_request('GET', f'/quote/{quote_id}')
    assert get_response.status_code == 200
    quote = get_response.json()

    # Verify data matches what was submitted (data is nested under 'data' key)
    assert quote['data']['customer_name'] == sample_quote_data['customer_name']
    assert quote['data']['customer_email'] == sample_quote_data['customer_email']
    assert quote['data']['property_address'] == sample_quote_data['property_address']
    assert quote['data']['coverage_amount'] == sample_quote_data['coverage_amount']


@pytest.mark.api
@pytest.mark.quotes
def test_quote_cors_headers(api_client, sample_quote_data):
    """Test that quote endpoints return CORS headers"""
    response = api_client.api_request('POST', '/quote', json=sample_quote_data)

    # Should have CORS headers in actual responses
    assert 'Access-Control-Allow-Origin' in response.headers, "Missing CORS origin header"


# DELETE Tests

@pytest.mark.api
@pytest.mark.quotes
def test_delete_quote_success(api_client, sample_quote_data):
    """Test that quote can be deleted successfully"""
    # Create a quote first
    create_response = api_client.api_request('POST', '/quote', json=sample_quote_data)
    assert create_response.status_code == 201
    quote_id = create_response.json()['id']

    # Delete the quote
    delete_response = api_client.api_request('DELETE', f'/quote/{quote_id}')
    assert delete_response.status_code in [200, 204], f"Expected 200 or 204, got {delete_response.status_code}"

    # Verify quote no longer exists
    get_response = api_client.api_request('GET', f'/quote/{quote_id}')
    assert get_response.status_code == 404, "Deleted quote should return 404"


@pytest.mark.api
@pytest.mark.quotes
def test_delete_quote_not_found(api_client):
    """Test that deleting non-existent quote succeeds (idempotent DELETE)"""
    non_existent_id = 'quote-does-not-exist-999999'

    response = api_client.api_request('DELETE', f'/quote/{non_existent_id}')

    # DELETE is idempotent - both 200 and 404 are acceptable
    assert response.status_code in [200, 204, 404], f"Expected 200, 204, or 404, got {response.status_code}"


# Negative Tests

@pytest.mark.api
@pytest.mark.quotes
@pytest.mark.negative
def test_create_quote_missing_required_fields(api_client):
    """Test that creating quote without required fields returns 400"""
    invalid_data = {
        "customer_name": "Test Customer"
        # Missing customer_email, property_address, coverage_amount, etc.
    }

    response = api_client.api_request('POST', '/quote', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.quotes
@pytest.mark.negative
def test_create_quote_invalid_json(api_client):
    """Test that invalid JSON returns 400"""
    response = api_client.api_request(
        'POST',
        '/quote',
        data='{"invalid": json syntax}',  # Invalid JSON
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.quotes
@pytest.mark.negative
def test_create_quote_invalid_data_types(api_client):
    """Test that invalid data types return 400"""
    invalid_data = {
        "customer_name": "Test Customer",
        "customer_email": "invalid-email",  # Invalid email format
        "property_address": "123 Test St",
        "coverage_amount": "not-a-number",  # Should be numeric
        "property_type": "single_family",
        "year_built": "not-a-year"  # Should be numeric
    }

    response = api_client.api_request('POST', '/quote', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.quotes
@pytest.mark.negative
def test_create_quote_empty_payload(api_client):
    """Test that empty payload returns 400"""
    response = api_client.api_request('POST', '/quote', json={})

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.quotes
@pytest.mark.negative
def test_get_quote_invalid_id_format(api_client):
    """Test that invalid ID format returns 400 or 404"""
    invalid_id = ""  # Empty ID

    response = api_client.api_request('GET', f'/quote/{invalid_id}')

    # Accept either 400 (bad request) or 404 (not found) as valid
    assert response.status_code in [400, 404], f"Expected 400 or 404, got {response.status_code}"
