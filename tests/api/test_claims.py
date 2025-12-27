"""
Claims API Contract Tests

Infrastructure-agnostic tests validating claims API behavior.
"""

import pytest
import io


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

    # Validate claim structure
    assert claim['id'] == claim_id
    assert 'policy_id' in claim
    assert 'claim_type' in claim
    assert 'status' in claim


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

    # Verify status changed
    get_response = api_client.api_request('GET', f'/claim/{claim_id}')
    claim = get_response.json()
    assert claim['status'] == 'under_review'


@pytest.mark.api
@pytest.mark.claims
@pytest.mark.slow
def test_upload_claim_document(api_client, sample_claim_data):
    """Test that document can be uploaded to claim"""
    # Create claim
    create_response = api_client.api_request('POST', '/claim', json=sample_claim_data)
    assert create_response.status_code == 201
    claim_id = create_response.json()['id']

    # Create a test file
    test_file = io.BytesIO(b"Test document content")
    files = {'file': ('test_document.pdf', test_file, 'application/pdf')}

    # Upload document
    upload_response = api_client.api_request('POST', f'/claim/{claim_id}/doc', files=files)

    assert upload_response.status_code == 200, f"Expected 200, got {upload_response.status_code}"
    upload_data = upload_response.json()

    # Response should include document info (don't care if it's S3 URL or doc ID)
    assert 'doc_url' in upload_data or 'doc_id' in upload_data or 'document_id' in upload_data


@pytest.mark.api
@pytest.mark.claims
@pytest.mark.slow
def test_claim_includes_uploaded_documents(api_client, sample_claim_data):
    """Test that claim retrieval includes uploaded document metadata"""
    # Create claim
    create_response = api_client.api_request('POST', '/claim', json=sample_claim_data)
    claim_id = create_response.json()['id']

    # Upload document
    test_file = io.BytesIO(b"Test document content")
    files = {'file': ('evidence.pdf', test_file, 'application/pdf')}
    api_client.api_request('POST', f'/claim/{claim_id}/doc', files=files)

    # Retrieve claim
    get_response = api_client.api_request('GET', f'/claim/{claim_id}')
    claim = get_response.json()

    # Should include document metadata (not testing S3 bucket structure)
    assert 'documents' in claim or 'attachments' in claim or 'files' in claim
