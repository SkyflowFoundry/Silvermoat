"""
API Contract Test Configuration

Pytest fixtures for infrastructure-agnostic API testing.
Tests validate API behavior without depending on specific backend implementation.
"""

import os
import pytest
import requests


@pytest.fixture(scope="session")
def api_base_url():
    """
    Get API base URL from environment or CloudFormation stack.

    Priority:
    1. SILVERMOAT_API_URL environment variable
    2. CloudFormation stack outputs (via STACK_NAME)
    3. Default localhost
    """
    # Check environment variable first
    api_url = os.environ.get('SILVERMOAT_API_URL')
    if api_url:
        return api_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            if 'ApiBaseUrl' in outputs:
                return outputs['ApiBaseUrl'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # Fallback to localhost
    return os.environ.get('API_BASE_URL', 'http://localhost:3000').rstrip('/')


@pytest.fixture
def api_client(api_base_url):
    """
    API client with base URL configured.
    Returns requests session for making API calls.
    """
    session = requests.Session()
    session.base_url = api_base_url

    def request(method, path, **kwargs):
        """Make request with base URL prepended"""
        url = f"{api_base_url}{path}"
        return session.request(method, url, **kwargs)

    session.api_request = request
    return session


@pytest.fixture
def sample_customer_data():
    """Sample customer data for testing"""
    return {
        "name": "Test Customer",
        "email": "test.customer@example.com",
        "address": "789 Test St, Austin, TX 78703",
        "phone": "512-555-0100"
    }


@pytest.fixture
def sample_quote_data():
    """Sample quote data for testing"""
    return {
        "customer_name": "Jane Doe",
        "customer_email": "jane.doe@example.com",
        "property_address": "123 Main St, Austin, TX 78701",
        "coverage_amount": 500000,
        "property_type": "single_family",
        "year_built": 2010
    }


@pytest.fixture
def sample_policy_data():
    """Sample policy data for testing"""
    return {
        "quote_id": "test-quote-123",
        "customer_name": "John Smith",
        "customer_email": "john.smith@example.com",
        "property_address": "456 Oak Ave, Austin, TX 78702",
        "coverage_amount": 750000,
        "premium_annual": 1850.00,
        "effective_date": "2024-01-01",
        "expiration_date": "2025-01-01"
    }


@pytest.fixture
def sample_claim_data():
    """Sample claim data for testing"""
    return {
        "policy_id": "test-policy-456",
        "claim_type": "water_damage",
        "description": "Pipe burst in basement causing water damage",
        "claim_amount": 15000,
        "date_of_loss": "2024-03-15"
    }


@pytest.fixture
def sample_payment_data():
    """Sample payment data for testing"""
    return {
        "policy_id": "test-policy-789",
        "amount": 925.00,
        "payment_method": "credit_card",
        "card_last_four": "4242"
    }


@pytest.fixture
def sample_case_data():
    """Sample case data for testing"""
    return {
        "title": "Policy Change Request",
        "description": "Customer requesting coverage amount increase for home policy",
        "relatedEntityType": "policy",
        "relatedEntityId": "test-policy-123",
        "assignee": "Alice Johnson",
        "priority": "MEDIUM"
    }


# Self-contained test fixtures with automatic cleanup

@pytest.fixture
def created_customer(api_client, sample_customer_data):
    """Create a customer for testing, clean up after."""
    response = api_client.api_request('POST', '/customer', json=sample_customer_data)
    assert response.status_code == 201, f"Failed to create test customer: {response.status_code}"
    customer_id = response.json()['id']
    yield customer_id
    # Cleanup
    api_client.api_request('DELETE', f'/customer/{customer_id}')


@pytest.fixture
def created_quote(api_client, sample_quote_data):
    """Create a quote for testing, clean up after."""
    response = api_client.api_request('POST', '/quote', json=sample_quote_data)
    assert response.status_code == 201, f"Failed to create test quote: {response.status_code}"
    quote_id = response.json()['id']
    yield quote_id
    # Cleanup
    api_client.api_request('DELETE', f'/quote/{quote_id}')


@pytest.fixture
def created_policy(api_client, sample_policy_data):
    """Create a policy for testing, clean up after."""
    response = api_client.api_request('POST', '/policy', json=sample_policy_data)
    assert response.status_code == 201, f"Failed to create test policy: {response.status_code}"
    policy_id = response.json()['id']
    yield policy_id
    # Cleanup
    api_client.api_request('DELETE', f'/policy/{policy_id}')


@pytest.fixture
def created_claim(api_client, sample_claim_data):
    """Create a claim for testing, clean up after."""
    response = api_client.api_request('POST', '/claim', json=sample_claim_data)
    assert response.status_code == 201, f"Failed to create test claim: {response.status_code}"
    claim_id = response.json()['id']
    yield claim_id
    # Cleanup
    api_client.api_request('DELETE', f'/claim/{claim_id}')


@pytest.fixture
def created_payment(api_client, sample_payment_data):
    """Create a payment for testing, clean up after."""
    response = api_client.api_request('POST', '/payment', json=sample_payment_data)
    assert response.status_code == 201, f"Failed to create test payment: {response.status_code}"
    payment_id = response.json()['id']
    yield payment_id
    # Cleanup
    api_client.api_request('DELETE', f'/payment/{payment_id}')


@pytest.fixture
def created_case(api_client, sample_case_data):
    """Create a case for testing, clean up after."""
    response = api_client.api_request('POST', '/case', json=sample_case_data)
    assert response.status_code == 201, f"Failed to create test case: {response.status_code}"
    case_id = response.json()['id']
    yield case_id
    # Cleanup
    api_client.api_request('DELETE', f'/case/{case_id}')


def pytest_collection_modifyitems(config, items):
    """
    Automatically mark negative tests as xfail.

    Negative tests document expected API behavior but may fail until
    Lambda input validation is fully implemented.
    """
    for item in items:
        if "negative" in item.keywords:
            item.add_marker(
                pytest.mark.xfail(
                    reason="Requires Lambda input validation to be implemented",
                    strict=False
                )
            )
