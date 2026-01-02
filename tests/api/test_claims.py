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

    # Cleanup
    api_client.api_request('DELETE', f'/claim/{data["id"]}')


@pytest.mark.api
@pytest.mark.claims
def test_get_claim_by_id(api_client, created_claim):
    """Test that created claim can be retrieved by ID (self-contained with cleanup)"""
    # Retrieve claim
    get_response = api_client.api_request('GET', f'/claim/{created_claim}')

    assert get_response.status_code == 200
    claim = get_response.json()

    # Validate claim structure (data is nested under 'data' key)
    assert claim['id'] == created_claim
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

    try:
        # Update status
        status_update = {"status": "under_review"}
        update_response = api_client.api_request('POST', f'/claim/{claim_id}/status', json=status_update)

        assert update_response.status_code == 200, f"Expected 200, got {update_response.status_code}"

        # Verify status changed (Lambda uppercases status values)
        get_response = api_client.api_request('GET', f'/claim/{claim_id}')
        claim = get_response.json()
        assert claim['status'] == 'UNDER_REVIEW'
    finally:
        # Cleanup
        api_client.api_request('DELETE', f'/claim/{claim_id}')


@pytest.mark.api
@pytest.mark.claims
def test_get_claim_not_found(api_client):
    """Test that requesting non-existent claim returns 404"""
    response = api_client.api_request('GET', '/claim/non-existent-999')

    assert response.status_code == 404


# DELETE Tests

@pytest.mark.api
@pytest.mark.claims
def test_delete_claim_success(api_client, sample_claim_data):
    """Test that claim can be deleted successfully"""
    # Create a claim first
    create_response = api_client.api_request('POST', '/claim', json=sample_claim_data)
    assert create_response.status_code == 201
    claim_id = create_response.json()['id']

    # Delete the claim
    delete_response = api_client.api_request('DELETE', f'/claim/{claim_id}')
    assert delete_response.status_code in [200, 204], f"Expected 200 or 204, got {delete_response.status_code}"

    # Verify claim no longer exists
    get_response = api_client.api_request('GET', f'/claim/{claim_id}')
    assert get_response.status_code == 404, "Deleted claim should return 404"


@pytest.mark.api
@pytest.mark.claims
def test_delete_claim_not_found(api_client):
    """Test that deleting non-existent claim succeeds (idempotent DELETE)"""
    non_existent_id = 'claim-does-not-exist-999999'

    response = api_client.api_request('DELETE', f'/claim/{non_existent_id}')

    # DELETE is idempotent - both 200 and 404 are acceptable
    assert response.status_code in [200, 204, 404], f"Expected 200, 204, or 404, got {response.status_code}"


# Negative Tests

@pytest.mark.api
@pytest.mark.claims
@pytest.mark.negative
def test_create_claim_missing_required_fields(api_client):
    """Test that creating claim without required fields returns 400"""
    invalid_data = {
        "policy_id": "policy-123"
        # Missing claim_type, claim_date, etc.
    }

    response = api_client.api_request('POST', '/claim', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.claims
@pytest.mark.negative
def test_create_claim_invalid_json(api_client):
    """Test that invalid JSON returns 400"""
    response = api_client.api_request(
        'POST',
        '/claim',
        data='{"invalid": json syntax}',  # Invalid JSON
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.claims
@pytest.mark.negative
def test_create_claim_invalid_data_types(api_client):
    """Test that invalid data types return 400"""
    invalid_data = {
        "policy_id": "policy-123",
        "claim_type": "water_damage",
        "claim_date": "not-a-date",  # Should be valid date format
        "claim_amount": "not-a-number"  # Should be numeric
    }

    response = api_client.api_request('POST', '/claim', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.claims
@pytest.mark.negative
def test_create_claim_empty_payload(api_client):
    """Test that empty payload returns 400"""
    response = api_client.api_request('POST', '/claim', json={})

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.claims
@pytest.mark.negative
def test_get_claim_invalid_id_format(api_client):
    """Test that invalid ID format returns 400 or 404"""
    invalid_id = ""  # Empty ID

    response = api_client.api_request('GET', f'/claim/{invalid_id}')

    # Accept either 400 (bad request) or 404 (not found) as valid
    assert response.status_code in [400, 404], f"Expected 400 or 404, got {response.status_code}"


@pytest.mark.api
@pytest.mark.claims
@pytest.mark.negative
def test_update_claim_status_invalid(api_client, sample_claim_data):
    """Test that updating claim with invalid status returns 400"""
    # Create claim
    create_response = api_client.api_request('POST', '/claim', json=sample_claim_data)
    assert create_response.status_code == 201
    claim_id = create_response.json()['id']

    try:
        # Attempt invalid status update
        invalid_status = {"status": "invalid_status_value"}
        response = api_client.api_request('POST', f'/claim/{claim_id}/status', json=invalid_status)

        # Should reject invalid status values
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
    finally:
        # Cleanup
        api_client.api_request('DELETE', f'/claim/{claim_id}')
