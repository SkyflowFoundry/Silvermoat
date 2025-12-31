"""
Customer Portal API Contract Tests

Tests for customer-facing API endpoints including authentication,
policy viewing, claim submission, and payment viewing.
"""

import pytest


@pytest.mark.api
@pytest.mark.customer
def test_customer_auth_success(api_client):
    """Test customer authentication with valid policy number and ZIP"""
    # First, create a policy to authenticate against
    policy_data = {
        "policyNumber": "POL-2024-TEST001",
        "holderName": "John Doe",
        "zip": "12345",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 150000,
    }
    create_response = api_client.api_request('POST', '/policy', json=policy_data)
    assert create_response.status_code == 201

    # Authenticate as customer
    auth_data = {
        "policyNumber": "POL-2024-TEST001",
        "zip": "12345"
    }
    auth_response = api_client.api_request('POST', '/customer/auth', json=auth_data)

    assert auth_response.status_code == 200
    data = auth_response.json()
    assert data['authenticated'] is True
    assert data['policyNumber'] == "POL-2024-TEST001"
    assert data['holderName'] == "John Doe"
    assert 'policyId' in data


@pytest.mark.api
@pytest.mark.customer
def test_customer_auth_invalid_zip(api_client):
    """Test customer authentication with invalid ZIP code"""
    # First, create a policy
    policy_data = {
        "policyNumber": "POL-2024-TEST002",
        "holderName": "Jane Smith",
        "zip": "54321",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 150000,
    }
    create_response = api_client.api_request('POST', '/policy', json=policy_data)
    assert create_response.status_code == 201

    # Try to authenticate with wrong ZIP
    auth_data = {
        "policyNumber": "POL-2024-TEST002",
        "zip": "99999"
    }
    auth_response = api_client.api_request('POST', '/customer/auth', json=auth_data)

    assert auth_response.status_code == 401


@pytest.mark.api
@pytest.mark.customer
def test_customer_auth_missing_credentials(api_client):
    """Test customer authentication with missing credentials"""
    auth_data = {
        "policyNumber": "POL-2024-TEST003"
        # Missing zip
    }
    auth_response = api_client.api_request('POST', '/customer/auth', json=auth_data)

    assert auth_response.status_code == 400


@pytest.mark.api
@pytest.mark.customer
def test_customer_get_policies(api_client):
    """Test customer can view their policies"""
    # Create a policy
    policy_data = {
        "policyNumber": "POL-2024-TEST004",
        "holderName": "Bob Johnson",
        "zip": "11111",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 200000,
    }
    create_response = api_client.api_request('POST', '/policy', json=policy_data)
    assert create_response.status_code == 201

    # Get policies for customer
    get_response = api_client.api_request('GET', '/customer/policies?policyNumber=POL-2024-TEST004')

    assert get_response.status_code == 200
    data = get_response.json()
    assert 'policies' in data
    assert 'count' in data
    assert data['count'] >= 1
    assert any(p['data']['policyNumber'] == 'POL-2024-TEST004' for p in data['policies'])


@pytest.mark.api
@pytest.mark.customer
def test_customer_get_policy_by_id(api_client):
    """Test customer can view specific policy by ID"""
    # Create a policy
    policy_data = {
        "policyNumber": "POL-2024-TEST005",
        "holderName": "Alice Brown",
        "zip": "22222",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 180000,
    }
    create_response = api_client.api_request('POST', '/policy', json=policy_data)
    assert create_response.status_code == 201
    policy_id = create_response.json()['id']

    # Get policy by ID
    get_response = api_client.api_request('GET', f'/customer/policies/{policy_id}')

    assert get_response.status_code == 200
    policy = get_response.json()
    assert policy['id'] == policy_id
    assert policy['data']['policyNumber'] == 'POL-2024-TEST005'


@pytest.mark.api
@pytest.mark.customer
def test_customer_submit_claim(api_client):
    """Test customer can submit a new claim"""
    # First, create a policy
    policy_data = {
        "policyNumber": "POL-2024-TEST006",
        "holderName": "Charlie Wilson",
        "zip": "33333",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 250000,
    }
    policy_response = api_client.api_request('POST', '/policy', json=policy_data)
    assert policy_response.status_code == 201

    # Submit a claim
    claim_data = {
        "policyNumber": "POL-2024-TEST006",
        "claimantName": "Charlie Wilson",
        "incidentDate": "2024-12-15",
        "description": "Vehicle collision on highway, rear-end accident with minor damage to bumper",
        "estimatedAmount_cents": 150000,
    }
    claim_response = api_client.api_request('POST', '/customer/claims', json=claim_data)

    assert claim_response.status_code == 201
    data = claim_response.json()
    assert 'id' in data
    assert 'claim' in data
    assert data['claim']['status'] == 'PENDING'


@pytest.mark.api
@pytest.mark.customer
def test_customer_submit_claim_missing_fields(api_client):
    """Test claim submission with missing required fields"""
    claim_data = {
        "policyNumber": "POL-2024-TEST007",
        # Missing claimantName, incidentDate, description
    }
    claim_response = api_client.api_request('POST', '/customer/claims', json=claim_data)

    assert claim_response.status_code == 400


@pytest.mark.api
@pytest.mark.customer
def test_customer_get_claims(api_client):
    """Test customer can view their claims"""
    # Create policy
    policy_data = {
        "policyNumber": "POL-2024-TEST008",
        "holderName": "Diana Prince",
        "zip": "44444",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 200000,
    }
    policy_response = api_client.api_request('POST', '/policy', json=policy_data)
    assert policy_response.status_code == 201
    policy_id = policy_response.json()['id']

    # Create a claim linked to policy
    claim_data = {
        "policyId": policy_id,
        "claimNumber": "CLM-2024-TEST008",
        "claimantName": "Diana Prince",
        "incidentDate": "2024-12-10",
        "description": "Water damage from burst pipe",
        "estimatedAmount_cents": 300000,
    }
    claim_response = api_client.api_request('POST', '/claim', json=claim_data)
    assert claim_response.status_code == 201

    # Get claims for customer
    get_response = api_client.api_request('GET', '/customer/claims?policyNumber=POL-2024-TEST008')

    assert get_response.status_code == 200
    data = get_response.json()
    assert 'claims' in data
    assert 'count' in data
    assert data['count'] >= 1


@pytest.mark.api
@pytest.mark.customer
def test_customer_get_payments(api_client):
    """Test customer can view their payments"""
    # Create policy
    policy_data = {
        "policyNumber": "POL-2024-TEST009",
        "holderName": "Edward Miller",
        "zip": "55555",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 175000,
    }
    policy_response = api_client.api_request('POST', '/policy', json=policy_data)
    assert policy_response.status_code == 201
    policy_id = policy_response.json()['id']

    # Create a payment linked to policy
    payment_data = {
        "policyId": policy_id,
        "paymentNumber": "PAY-2024-TEST009",
        "amount_cents": 87500,
        "paymentMethod": "CREDIT_CARD",
        "status": "COMPLETED",
        "paymentDate": "2024-12-01",
    }
    payment_response = api_client.api_request('POST', '/payment', json=payment_data)
    assert payment_response.status_code == 201

    # Get payments for customer
    get_response = api_client.api_request('GET', '/customer/payments?policyNumber=POL-2024-TEST009')

    assert get_response.status_code == 200
    data = get_response.json()
    assert 'payments' in data
    assert 'count' in data
    assert data['count'] >= 1


@pytest.mark.api
@pytest.mark.customer
def test_customer_upload_claim_document(api_client):
    """Test customer can upload document to claim"""
    # Create policy and claim
    policy_data = {
        "policyNumber": "POL-2024-TEST010",
        "holderName": "Frank Davis",
        "zip": "66666",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 190000,
    }
    policy_response = api_client.api_request('POST', '/policy', json=policy_data)
    assert policy_response.status_code == 201

    claim_data = {
        "policyNumber": "POL-2024-TEST010",
        "claimantName": "Frank Davis",
        "incidentDate": "2024-12-01",
        "description": "Auto glass damage from road debris",
        "estimatedAmount_cents": 50000,
    }
    claim_response = api_client.api_request('POST', '/customer/claims', json=claim_data)
    assert claim_response.status_code == 201
    claim_id = claim_response.json()['id']

    # Upload document
    doc_data = {
        "filename": "damage-photo.txt",
        "content": "Photo evidence of glass damage",
        "contentType": "text/plain"
    }
    upload_response = api_client.api_request('POST', f'/customer/claims/{claim_id}/doc', json=doc_data)

    assert upload_response.status_code == 200
    data = upload_response.json()
    assert data['id'] == claim_id
    assert 's3Key' in data
    assert data['uploaded'] is True
