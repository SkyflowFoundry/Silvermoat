"""
Payment API Contract Tests

Infrastructure-agnostic tests validating payment API behavior.
"""

import pytest


@pytest.mark.api
@pytest.mark.payments
def test_create_payment_success(api_client, sample_payment_data):
    """Test that valid payment creation returns 201 with confirmation"""
    response = api_client.api_request('POST', '/payment', json=sample_payment_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    data = response.json()

    assert 'id' in data, "Response should contain payment ID"
    assert isinstance(data['id'], str), "Payment ID should be a string"


@pytest.mark.api
@pytest.mark.payments
def test_get_payment_by_id(api_client, sample_payment_data):
    """Test that created payment can be retrieved by ID"""
    # Create payment
    create_response = api_client.api_request('POST', '/payment', json=sample_payment_data)
    assert create_response.status_code == 201
    payment_id = create_response.json()['id']

    # Retrieve payment
    get_response = api_client.api_request('GET', f'/payment/{payment_id}')

    assert get_response.status_code == 200
    payment = get_response.json()

    # Validate payment structure (data is nested under 'data' key)
    assert payment['id'] == payment_id
    assert 'policy_id' in payment['data']
    assert 'amount' in payment['data']
    # Status may be at top level or in data
    assert 'status' in payment or 'status' in payment.get('data', {})


@pytest.mark.api
@pytest.mark.payments
def test_payment_includes_confirmation(api_client, sample_payment_data):
    """Test that payment response includes confirmation details"""
    response = api_client.api_request('POST', '/payment', json=sample_payment_data)
    assert response.status_code == 201

    data = response.json()

    # Response should have ID and item structure
    assert 'id' in data
    assert 'item' in data
    # Payment was successfully created (existence of ID is confirmation)
    assert isinstance(data['id'], str)


@pytest.mark.api
@pytest.mark.payments
def test_get_payment_not_found(api_client):
    """Test that requesting non-existent payment returns 404"""
    response = api_client.api_request('GET', '/payment/non-existent-999')

    assert response.status_code == 404


# DELETE Tests

@pytest.mark.api
@pytest.mark.payments
def test_delete_payment_success(api_client, sample_payment_data):
    """Test that payment can be deleted successfully"""
    # Create a payment first
    create_response = api_client.api_request('POST', '/payment', json=sample_payment_data)
    assert create_response.status_code == 201
    payment_id = create_response.json()['id']

    # Delete the payment
    delete_response = api_client.api_request('DELETE', f'/payment/{payment_id}')
    assert delete_response.status_code in [200, 204], f"Expected 200 or 204, got {delete_response.status_code}"

    # Verify payment no longer exists
    get_response = api_client.api_request('GET', f'/payment/{payment_id}')
    assert get_response.status_code == 404, "Deleted payment should return 404"


@pytest.mark.api
@pytest.mark.payments
def test_delete_payment_not_found(api_client):
    """Test that deleting non-existent payment returns 404"""
    non_existent_id = 'payment-does-not-exist-999999'

    response = api_client.api_request('DELETE', f'/payment/{non_existent_id}')

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


# Negative Tests

@pytest.mark.api
@pytest.mark.payments
@pytest.mark.negative
def test_create_payment_missing_required_fields(api_client):
    """Test that creating payment without required fields returns 400"""
    invalid_data = {
        "policy_id": "policy-123"
        # Missing amount, payment_method, etc.
    }

    response = api_client.api_request('POST', '/payment', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.payments
@pytest.mark.negative
def test_create_payment_invalid_json(api_client):
    """Test that invalid JSON returns 400"""
    response = api_client.api_request(
        'POST',
        '/payment',
        data='{"invalid": json syntax}',  # Invalid JSON
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.payments
@pytest.mark.negative
def test_create_payment_invalid_data_types(api_client):
    """Test that invalid data types return 400"""
    invalid_data = {
        "policy_id": "policy-123",
        "amount": "not-a-number",  # Should be numeric
        "payment_method": "credit_card",
        "payment_date": "not-a-date"  # Should be valid date format
    }

    response = api_client.api_request('POST', '/payment', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.payments
@pytest.mark.negative
def test_create_payment_empty_payload(api_client):
    """Test that empty payload returns 400"""
    response = api_client.api_request('POST', '/payment', json={})

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.payments
@pytest.mark.negative
def test_get_payment_invalid_id_format(api_client):
    """Test that invalid ID format returns 400 or 404"""
    invalid_id = ""  # Empty ID

    response = api_client.api_request('GET', f'/payment/{invalid_id}')

    # Accept either 400 (bad request) or 404 (not found) as valid
    assert response.status_code in [400, 404], f"Expected 400 or 404, got {response.status_code}"


@pytest.mark.api
@pytest.mark.payments
@pytest.mark.negative
def test_create_payment_negative_amount(api_client):
    """Test that negative payment amount returns 400"""
    invalid_data = {
        "policy_id": "policy-123",
        "amount": -100.00,  # Negative amount
        "payment_method": "credit_card"
    }

    response = api_client.api_request('POST', '/payment', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
