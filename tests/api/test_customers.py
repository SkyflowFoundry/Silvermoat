"""
Customer API Contract Tests

Infrastructure-agnostic tests validating customer API behavior.
Tests verify API contracts without depending on DynamoDB or other implementation details.
"""

import pytest


@pytest.mark.api
@pytest.mark.customers
def test_create_customer_success(api_client, sample_customer_data):
    """Test that valid customer creation returns 201 with customer ID"""
    response = api_client.api_request('POST', '/customer', json=sample_customer_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    data = response.json()

    # Validate response structure
    assert 'id' in data, "Response should contain customer ID"
    assert isinstance(data['id'], str), "Customer ID should be a string"
    assert len(data['id']) > 0, "Customer ID should not be empty"

    # Cleanup
    api_client.api_request('DELETE', f'/customer/{data["id"]}')


@pytest.mark.api
@pytest.mark.customers
def test_get_customer_by_id(api_client, created_customer):
    """Test that created customer can be retrieved by ID (self-contained with cleanup)"""
    # Retrieve the customer
    get_response = api_client.api_request('GET', f'/customer/{created_customer}')

    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
    customer = get_response.json()

    # Validate customer structure (email at top-level for GSI, other fields in data)
    assert customer['id'] == created_customer
    assert 'email' in customer  # GSI field at top level
    assert 'name' in customer['data']
    assert 'address' in customer['data']


@pytest.mark.api
@pytest.mark.customers
def test_get_customer_not_found(api_client):
    """Test that requesting non-existent customer returns 404"""
    non_existent_id = 'customer-does-not-exist-999999'

    response = api_client.api_request('GET', f'/customer/{non_existent_id}')

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


@pytest.mark.api
@pytest.mark.customers
def test_customer_data_persistence(api_client, created_customer, sample_customer_data):
    """Test that customer data persists correctly (self-contained with cleanup)"""
    # Retrieve customer
    get_response = api_client.api_request('GET', f'/customer/{created_customer}')
    assert get_response.status_code == 200
    customer = get_response.json()

    # Verify data matches what was submitted (email at top-level, other fields in data)
    assert customer['data']['name'] == sample_customer_data['name']
    assert customer['email'] == sample_customer_data['email']  # Email stored at top-level for GSI
    assert customer['data']['address'] == sample_customer_data['address']


@pytest.mark.api
@pytest.mark.customers
def test_customer_default_status(api_client, sample_customer_data):
    """Test that newly created customers have default ACTIVE status"""
    response = api_client.api_request('POST', '/customer', json=sample_customer_data)
    assert response.status_code == 201

    data = response.json()
    customer_id = data['id']

    try:
        # Retrieve to verify status
        get_response = api_client.api_request('GET', f'/customer/{customer_id}')
        assert get_response.status_code == 200
        customer = get_response.json()

        # Default status should be ACTIVE
        status = customer.get('status') or customer.get('data', {}).get('status')
        assert status == 'ACTIVE', f"Default status should be ACTIVE, got {status}"
    finally:
        # Cleanup
        api_client.api_request('DELETE', f'/customer/{customer_id}')


@pytest.mark.api
@pytest.mark.customers
def test_customer_cors_headers(api_client, sample_customer_data):
    """Test that customer endpoints return CORS headers"""
    response = api_client.api_request('POST', '/customer', json=sample_customer_data)

    # Should have CORS headers in actual responses
    assert 'Access-Control-Allow-Origin' in response.headers, "Missing CORS origin header"

    # Cleanup
    if response.status_code == 201:
        api_client.api_request('DELETE', f'/customer/{response.json()["id"]}')


# DELETE Tests

@pytest.mark.api
@pytest.mark.customers
def test_delete_customer_success(api_client, sample_customer_data):
    """Test that customer can be deleted successfully (creates own data)"""
    # Create a customer
    create_response = api_client.api_request('POST', '/customer', json=sample_customer_data)
    assert create_response.status_code == 201
    customer_id = create_response.json()['id']

    # Delete the customer
    delete_response = api_client.api_request('DELETE', f'/customer/{customer_id}')
    assert delete_response.status_code in [200, 204], f"Expected 200 or 204, got {delete_response.status_code}"

    # Verify customer no longer exists
    get_response = api_client.api_request('GET', f'/customer/{customer_id}')
    assert get_response.status_code == 404, "Deleted customer should return 404"


@pytest.mark.api
@pytest.mark.customers
def test_delete_customer_not_found(api_client):
    """Test that deleting non-existent customer succeeds (idempotent DELETE)"""
    non_existent_id = 'customer-does-not-exist-999999'

    response = api_client.api_request('DELETE', f'/customer/{non_existent_id}')

    # DELETE is idempotent - both 200 and 404 are acceptable
    assert response.status_code in [200, 204, 404], f"Expected 200, 204, or 404, got {response.status_code}"


# Negative Tests

@pytest.mark.api
@pytest.mark.customers
@pytest.mark.negative
def test_create_customer_missing_required_fields(api_client):
    """Test that creating customer without required fields returns 400"""
    invalid_data = {
        "name": "Test Customer"
        # Missing email, address, etc.
    }

    response = api_client.api_request('POST', '/customer', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.customers
@pytest.mark.negative
def test_create_customer_invalid_json(api_client):
    """Test that invalid JSON returns 400"""
    response = api_client.api_request(
        'POST',
        '/customer',
        data='{"invalid": json syntax}',  # Invalid JSON
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.customers
@pytest.mark.negative
def test_create_customer_invalid_data_types(api_client):
    """Test that invalid data types return 400"""
    invalid_data = {
        "name": 12345,  # Should be string
        "email": "invalid-email-format",  # Invalid email
        "address": ["should", "be", "string"],  # Should be string
        "phone": 5125550100  # Should be string
    }

    response = api_client.api_request('POST', '/customer', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.customers
@pytest.mark.negative
def test_create_customer_empty_payload(api_client):
    """Test that empty payload returns 400"""
    response = api_client.api_request('POST', '/customer', json={})

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.customers
@pytest.mark.negative
def test_get_customer_invalid_id_format(api_client):
    """Test that invalid ID format returns 400 or 404"""
    invalid_id = ""  # Empty ID

    response = api_client.api_request('GET', f'/customer/{invalid_id}')

    # Accept either 400 (bad request) or 404 (not found) as valid
    assert response.status_code in [400, 404], f"Expected 400 or 404, got {response.status_code}"
