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

    # Validate payment structure
    assert payment['id'] == payment_id
    assert 'policy_id' in payment
    assert 'amount' in payment
    assert 'status' in payment


@pytest.mark.api
@pytest.mark.payments
def test_payment_includes_confirmation(api_client, sample_payment_data):
    """Test that payment response includes confirmation details"""
    response = api_client.api_request('POST', '/payment', json=sample_payment_data)
    assert response.status_code == 201

    payment = response.json()

    # Should include some form of confirmation (don't care about exact format)
    assert payment.get('status') in ['completed', 'pending', 'success', 'approved']
