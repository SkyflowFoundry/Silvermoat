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
