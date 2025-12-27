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


@pytest.mark.api
@pytest.mark.policies
def test_get_policy_by_id(api_client, sample_policy_data):
    """Test that created policy can be retrieved by ID"""
    # Create policy
    create_response = api_client.api_request('POST', '/policy', json=sample_policy_data)
    assert create_response.status_code == 201
    policy_id = create_response.json()['id']

    # Retrieve policy
    get_response = api_client.api_request('GET', f'/policy/{policy_id}')

    assert get_response.status_code == 200
    policy = get_response.json()

    # Validate policy structure (data is nested under 'data' key)
    assert policy['id'] == policy_id
    assert 'customer_name' in policy['data']
    assert 'coverage_amount' in policy['data']
    # Status may be at top level or in data
    assert 'status' in policy or 'status' in policy.get('data', {})


@pytest.mark.api
@pytest.mark.policies
def test_get_policy_not_found(api_client):
    """Test that requesting non-existent policy returns 404"""
    response = api_client.api_request('GET', '/policy/non-existent-999')

    assert response.status_code == 404


@pytest.mark.api
@pytest.mark.policies
def test_policy_status_field(api_client, sample_policy_data):
    """Test that policy includes status field"""
    # Create policy
    create_response = api_client.api_request('POST', '/policy', json=sample_policy_data)
    assert create_response.status_code == 201
    policy_id = create_response.json()['id']

    # Retrieve policy
    get_response = api_client.api_request('GET', f'/policy/{policy_id}')
    policy = get_response.json()

    # Status should be present and valid (may be at top level or in data)
    status = policy.get('status') or policy.get('data', {}).get('status')
    assert status is not None, "Policy should have a status field"
    # Status values vary by implementation - just verify it exists
    assert isinstance(status, str)
