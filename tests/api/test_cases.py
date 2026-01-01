"""
Case API Contract Tests

Infrastructure-agnostic tests validating case API behavior.
"""

import pytest


@pytest.mark.api
@pytest.mark.cases
def test_create_case_success(api_client, sample_case_data):
    """Test that valid case creation returns 201 with case ID"""
    response = api_client.api_request('POST', '/case', json=sample_case_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    data = response.json()

    # Validate response structure
    assert 'id' in data, "Response should contain case ID"
    assert isinstance(data['id'], str), "Case ID should be a string"
    assert len(data['id']) > 0, "Case ID should not be empty"


@pytest.mark.api
@pytest.mark.cases
def test_get_case_by_id(api_client, sample_case_data):
    """Test that created case can be retrieved by ID"""
    # Create a case first
    create_response = api_client.api_request('POST', '/case', json=sample_case_data)
    assert create_response.status_code == 201
    case_id = create_response.json()['id']

    # Retrieve the case
    get_response = api_client.api_request('GET', f'/case/{case_id}')

    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
    case = get_response.json()

    # Validate case structure (data is nested under 'data' key)
    assert case['id'] == case_id
    assert 'title' in case['data']
    assert 'description' in case['data']
    assert 'relatedEntityType' in case['data']
    assert 'relatedEntityId' in case['data']
    assert 'assignee' in case['data']
    assert 'priority' in case['data']
    # Status may be at top level or in data
    assert 'status' in case or 'status' in case.get('data', {})


@pytest.mark.api
@pytest.mark.cases
def test_get_case_not_found(api_client):
    """Test that requesting non-existent case returns 404"""
    non_existent_id = 'case-does-not-exist-999999'

    response = api_client.api_request('GET', f'/case/{non_existent_id}')

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


@pytest.mark.api
@pytest.mark.cases
def test_case_data_persistence(api_client, sample_case_data):
    """Test that case data persists correctly (create then retrieve)"""
    # Create case
    create_response = api_client.api_request('POST', '/case', json=sample_case_data)
    assert create_response.status_code == 201
    case_id = create_response.json()['id']

    # Retrieve case
    get_response = api_client.api_request('GET', f'/case/{case_id}')
    assert get_response.status_code == 200
    case = get_response.json()

    # Verify data matches what was submitted (data is nested under 'data' key)
    assert case['data']['title'] == sample_case_data['title']
    assert case['data']['description'] == sample_case_data['description']
    assert case['data']['relatedEntityType'] == sample_case_data['relatedEntityType']
    assert case['data']['relatedEntityId'] == sample_case_data['relatedEntityId']
    assert case['data']['assignee'] == sample_case_data['assignee']
    assert case['data']['priority'] == sample_case_data['priority']


@pytest.mark.api
@pytest.mark.cases
def test_case_default_status(api_client, sample_case_data):
    """Test that newly created cases have default OPEN status"""
    response = api_client.api_request('POST', '/case', json=sample_case_data)
    assert response.status_code == 201

    data = response.json()
    case_id = data['id']

    # Retrieve to verify status
    get_response = api_client.api_request('GET', f'/case/{case_id}')
    assert get_response.status_code == 200
    case = get_response.json()

    # Default status should be OPEN (from Lambda line 387)
    status = case.get('status') or case.get('data', {}).get('status')
    assert status == 'OPEN', f"Default status should be OPEN, got {status}"


@pytest.mark.api
@pytest.mark.cases
def test_case_cors_headers(api_client, sample_case_data):
    """Test that case endpoints return CORS headers"""
    response = api_client.api_request('POST', '/case', json=sample_case_data)

    # Should have CORS headers in actual responses
    assert 'Access-Control-Allow-Origin' in response.headers, "Missing CORS origin header"


# DELETE Tests

@pytest.mark.api
@pytest.mark.cases
def test_delete_case_success(api_client, sample_case_data):
    """Test that case can be deleted successfully"""
    # Create a case first
    create_response = api_client.api_request('POST', '/case', json=sample_case_data)
    assert create_response.status_code == 201
    case_id = create_response.json()['id']

    # Delete the case
    delete_response = api_client.api_request('DELETE', f'/case/{case_id}')
    assert delete_response.status_code in [200, 204], f"Expected 200 or 204, got {delete_response.status_code}"

    # Verify case no longer exists
    get_response = api_client.api_request('GET', f'/case/{case_id}')
    assert get_response.status_code == 404, "Deleted case should return 404"


@pytest.mark.api
@pytest.mark.cases
def test_delete_case_not_found(api_client):
    """Test that deleting non-existent case succeeds (idempotent DELETE)"""
    non_existent_id = 'case-does-not-exist-999999'

    response = api_client.api_request('DELETE', f'/case/{non_existent_id}')

    # DELETE is idempotent - both 200 and 404 are acceptable
    assert response.status_code in [200, 204, 404], f"Expected 200, 204, or 404, got {response.status_code}"


# Negative Tests

@pytest.mark.api
@pytest.mark.cases
@pytest.mark.negative
def test_create_case_missing_required_fields(api_client):
    """Test that creating case without required fields returns 400"""
    invalid_data = {
        "title": "Test Case"
        # Missing description, relatedEntityType, relatedEntityId, etc.
    }

    response = api_client.api_request('POST', '/case', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.cases
@pytest.mark.negative
def test_create_case_invalid_json(api_client):
    """Test that invalid JSON returns 400"""
    response = api_client.api_request(
        'POST',
        '/case',
        data='{"invalid": json syntax}',  # Invalid JSON
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.cases
@pytest.mark.negative
def test_create_case_invalid_data_types(api_client):
    """Test that invalid data types return 400"""
    invalid_data = {
        "title": "Test Case",
        "description": "Test Description",
        "relatedEntityType": "claim",
        "relatedEntityId": "claim-123",
        "assignee": 12345,  # Should be string
        "priority": "not-a-valid-priority"  # Should be valid enum value
    }

    response = api_client.api_request('POST', '/case', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.cases
@pytest.mark.negative
def test_create_case_empty_payload(api_client):
    """Test that empty payload returns 400"""
    response = api_client.api_request('POST', '/case', json={})

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.cases
@pytest.mark.negative
def test_get_case_invalid_id_format(api_client):
    """Test that invalid ID format returns 400 or 404"""
    invalid_id = ""  # Empty ID

    response = api_client.api_request('GET', f'/case/{invalid_id}')

    # Accept either 400 (bad request) or 404 (not found) as valid
    assert response.status_code in [400, 404], f"Expected 400 or 404, got {response.status_code}"


@pytest.mark.api
@pytest.mark.cases
@pytest.mark.negative
def test_create_case_invalid_related_entity_type(api_client):
    """Test that invalid related entity type returns 400"""
    invalid_data = {
        "title": "Test Case",
        "description": "Test Description",
        "relatedEntityType": "invalid_entity_type",  # Should be quote, policy, claim, or payment
        "relatedEntityId": "test-123",
        "assignee": "agent@example.com",
        "priority": "high"
    }

    response = api_client.api_request('POST', '/case', json=invalid_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
