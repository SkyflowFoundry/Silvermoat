"""
Policy API Contract Tests

Infrastructure-agnostic tests validating policy API behavior.
"""

import pytest


@pytest.mark.api
@pytest.mark.policies
def test_create_policy_success(api_client, sample_policy_data):
    """Test that valid policy creation returns 201 with policy ID"""
    response = api_client.api_request('POST', '/policy', json=sample_policy_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    data = response.json()

    assert 'id' in data, "Response should contain policy ID"
    assert isinstance(data['id'], str), "Policy ID should be a string"

    # Cleanup
    api_client.api_request('DELETE', f'/policy/{data["id"]}')


@pytest.mark.api
@pytest.mark.policies
def test_get_policy_by_id(api_client, created_policy):
    """Test that created policy can be retrieved by ID (self-contained with cleanup)"""
    # Retrieve policy
    get_response = api_client.api_request('GET', f'/policy/{created_policy}')

    assert get_response.status_code == 200
    policy = get_response.json()

    # Validate policy structure (data is nested under 'data' key)
    assert policy['id'] == created_policy
    assert 'customerId' in policy['data']
    assert 'coverageAmount' in policy['data']
    # Status is at top level
    assert 'status' in policy


@pytest.mark.api
@pytest.mark.policies
def test_get_policy_not_found(api_client):
    """Test that requesting non-existent policy returns 404"""
    response = api_client.api_request('GET', '/policy/non-existent-999')

    assert response.status_code == 404


@pytest.mark.api
@pytest.mark.policies
def test_policy_status_field(api_client, created_policy):
    """Test that policy includes status field (self-contained with cleanup)"""
    # Retrieve policy
    get_response = api_client.api_request('GET', f'/policy/{created_policy}')
    policy = get_response.json()

    # Status should be present and valid (may be at top level or in data)
    status = policy.get('status') or policy.get('data', {}).get('status')
    assert status is not None, "Policy should have a status field"
    # Status values vary by implementation - just verify it exists
    assert isinstance(status, str)


# DELETE Tests

@pytest.mark.api
@pytest.mark.policies
def test_delete_policy_success(api_client, sample_policy_data):
    """Test that policy can be deleted successfully"""
    # Create a policy first
    create_response = api_client.api_request('POST', '/policy', json=sample_policy_data)
    assert create_response.status_code == 201
    policy_id = create_response.json()['id']

    # Delete the policy
    delete_response = api_client.api_request('DELETE', f'/policy/{policy_id}')
    assert delete_response.status_code in [200, 204], f"Expected 200 or 204, got {delete_response.status_code}"

    # Verify policy no longer exists
    get_response = api_client.api_request('GET', f'/policy/{policy_id}')
    assert get_response.status_code == 404, "Deleted policy should return 404"


@pytest.mark.api
@pytest.mark.policies
def test_delete_policy_not_found(api_client):
    """Test that deleting non-existent policy succeeds (idempotent DELETE)"""
    non_existent_id = 'policy-does-not-exist-999999'

    response = api_client.api_request('DELETE', f'/policy/{non_existent_id}')

    # DELETE is idempotent - both 200 and 404 are acceptable
    assert response.status_code in [200, 204, 404], f"Expected 200, 204, or 404, got {response.status_code}"


# Negative Tests

@pytest.mark.api
@pytest.mark.policies
@pytest.mark.negative
def test_create_policy_missing_required_fields(api_client):
    """Test that creating policy without required fields returns 400"""
    invalid_data = {
        "customer_name": "Test Customer"
        # Missing customer_email, coverage_amount, etc.
    }

    response = api_client.api_request('POST', '/policy', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.policies
@pytest.mark.negative
def test_create_policy_invalid_json(api_client):
    """Test that invalid JSON returns 400"""
    response = api_client.api_request(
        'POST',
        '/policy',
        data='{"invalid": json syntax}',  # Invalid JSON
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.policies
@pytest.mark.negative
def test_create_policy_invalid_data_types(api_client):
    """Test that invalid data types return 400"""
    invalid_data = {
        "customer_name": "Test Customer",
        "customer_email": "invalid-email",  # Invalid email format
        "property_address": "123 Test St",
        "coverage_amount": "not-a-number",  # Should be numeric
        "property_type": "single_family",
        "year_built": "not-a-year"  # Should be numeric
    }

    response = api_client.api_request('POST', '/policy', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.policies
@pytest.mark.negative
def test_create_policy_empty_payload(api_client):
    """Test that empty payload returns 400"""
    response = api_client.api_request('POST', '/policy', json={})

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.policies
@pytest.mark.negative
def test_get_policy_invalid_id_format(api_client):
    """Test that invalid ID format returns 400 or 404"""
    invalid_id = ""  # Empty ID

    response = api_client.api_request('GET', f'/policy/{invalid_id}')

    # Accept either 400 (bad request) or 404 (not found) as valid
    assert response.status_code in [400, 404], f"Expected 400 or 404, got {response.status_code}"
