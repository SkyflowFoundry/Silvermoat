"""
API Contract Test Configuration

Pytest fixtures for infrastructure-agnostic API testing.
Tests validate API behavior without depending on specific backend implementation.
"""

import os
import pytest
import requests
from faker import Faker

fake = Faker()


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
def sample_quote_data():
    """Sample quote data for testing using Faker"""
    return {
        "customer_name": fake.name(),
        "customer_email": fake.email(),
        "property_address": fake.address(),
        "coverage_amount": fake.random_int(min=100000, max=1000000, step=50000),
        "property_type": "single_family",
        "year_built": fake.random_int(min=1950, max=2024)
    }


@pytest.fixture
def sample_policy_data():
    """Sample policy data for testing using Faker"""
    return {
        "quote_id": "test-quote-123",
        "customer_name": fake.name(),
        "customer_email": fake.email(),
        "property_address": fake.address(),
        "coverage_amount": fake.random_int(min=100000, max=1000000, step=50000),
        "premium_annual": fake.random_int(min=1000, max=5000, step=50) + fake.random.random(),
        "effective_date": fake.date_between(start_date='-30d', end_date='today').strftime("%Y-%m-%d"),
        "expiration_date": fake.date_between(start_date='+335d', end_date='+365d').strftime("%Y-%m-%d")
    }


@pytest.fixture
def sample_claim_data():
    """Sample claim data for testing using Faker"""
    return {
        "policy_id": "test-policy-456",
        "claim_type": fake.random_element(elements=('water_damage', 'fire', 'theft', 'vandalism')),
        "description": f"{fake.sentence()} causing damage to property",
        "claim_amount": fake.random_int(min=1000, max=50000, step=100),
        "date_of_loss": fake.date_between(start_date='-90d', end_date='today').strftime("%Y-%m-%d")
    }


@pytest.fixture
def sample_payment_data():
    """Sample payment data for testing using Faker"""
    return {
        "policy_id": "test-policy-789",
        "amount": fake.random_int(min=100, max=2000, step=25) + fake.random.random(),
        "payment_method": fake.random_element(elements=('credit_card', 'ach', 'check')),
        "card_last_four": fake.credit_card_number()[-4:]
    }


@pytest.fixture
def sample_case_data():
    """Sample case data for testing using Faker"""
    topics = ['Policy Change Request', 'Claim Inquiry', 'Billing Question', 'Coverage Question', 'General Inquiry']
    return {
        "title": fake.random_element(elements=topics),
        "description": f"Customer requesting {fake.sentence().lower()}",
        "relatedEntityType": "policy",
        "relatedEntityId": "test-policy-123",
        "assignee": fake.name(),
        "priority": fake.random_element(elements=('LOW', 'MEDIUM', 'HIGH'))
    }
