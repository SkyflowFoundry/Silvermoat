"""
Claims API Contract Tests

Infrastructure-agnostic tests validating claims API behavior.
"""

import pytest


@pytest.mark.api
@pytest.mark.claims
def test_create_claim_success(api_client, sample_claim_data):
    """Test that valid claim creation returns 201 with claim ID"""
    response = api_client.api_request('POST', '/claim', json=sample_claim_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    data = response.json()

    assert 'id' in data, "Response should contain claim ID"
    assert isinstance(data['id'], str), "Claim ID should be a string"


@pytest.mark.api
@pytest.mark.claims
def test_get_claim_by_id(api_client, sample_claim_data):
    """Test that created claim can be retrieved by ID"""
    # Create claim
    create_response = api_client.api_request('POST', '/claim', json=sample_claim_data)
    assert create_response.status_code == 201
    claim_id = create_response.json()['id']

    # Retrieve claim
    get_response = api_client.api_request('GET', f'/claim/{claim_id}')

    assert get_response.status_code == 200
    claim = get_response.json()

    # Validate claim structure (data is nested under 'data' key)
    assert claim['id'] == claim_id
    assert 'policy_id' in claim['data']
    assert 'claim_type' in claim['data']
    assert 'status' in claim or 'status' in claim.get('data', {})


@pytest.mark.api
@pytest.mark.claims
def test_update_claim_status(api_client, sample_claim_data):
    """Test that claim status can be updated"""
    # Create claim
    create_response = api_client.api_request('POST', '/claim', json=sample_claim_data)
    assert create_response.status_code == 201
    claim_id = create_response.json()['id']

    # Update status
    status_update = {"status": "under_review"}
    update_response = api_client.api_request('POST', f'/claim/{claim_id}/status', json=status_update)

    assert update_response.status_code == 200, f"Expected 200, got {update_response.status_code}"

    # Verify status changed (Lambda uppercases status values)
    get_response = api_client.api_request('GET', f'/claim/{claim_id}')
    claim = get_response.json()
    assert claim['status'] == 'UNDER_REVIEW'
