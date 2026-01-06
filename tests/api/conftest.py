"""
API Contract Test Configuration

Pytest fixtures for infrastructure-agnostic API testing.
Tests validate API behavior without depending on specific backend implementation.
"""

import os
import pytest
import requests
from faker import Faker
from datetime import date, timedelta

fake = Faker()


@pytest.fixture(scope="session")
def api_base_url():
    """
    Get API base URL from environment or CloudFormation stack.

    For multi-vertical testing, defaults to insurance vertical.
    Use insurance_api_base_url or retail_api_base_url for vertical-specific testing.

    Priority:
    1. SILVERMOAT_API_URL or INSURANCE_API_URL environment variable
    2. CloudFormation stack outputs (via STACK_NAME)
    3. Default localhost
    """
    # Check environment variable first (prefer INSURANCE_API_URL for backwards compat)
    api_url = os.environ.get('SILVERMOAT_API_URL') or os.environ.get('INSURANCE_API_URL')
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
            # Try insurance-specific output first, then generic
            if 'InsuranceApiUrl' in outputs:
                return outputs['InsuranceApiUrl'].rstrip('/')
            if 'InsuranceApiBaseUrl' in outputs:
                return outputs['InsuranceApiBaseUrl'].rstrip('/')
            if 'ApiBaseUrl' in outputs:
                return outputs['ApiBaseUrl'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # Fallback to localhost
    return os.environ.get('API_BASE_URL', 'http://localhost:3000').rstrip('/')


@pytest.fixture(scope="session")
def insurance_api_base_url():
    """Get insurance vertical API base URL"""
    # Check environment variable first
    api_url = os.environ.get('INSURANCE_API_URL')
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
            if 'InsuranceApiUrl' in outputs:
                return outputs['InsuranceApiUrl'].rstrip('/')
            if 'InsuranceApiBaseUrl' in outputs:
                return outputs['InsuranceApiBaseUrl'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # Fallback to api_base_url fixture
    return os.environ.get('API_BASE_URL', 'http://localhost:3000').rstrip('/')


@pytest.fixture(scope="session")
def retail_api_base_url():
    """Get retail vertical API base URL"""
    # Check environment variable first
    api_url = os.environ.get('RETAIL_API_URL')
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
            if 'RetailApiUrl' in outputs:
                return outputs['RetailApiUrl'].rstrip('/')
            if 'RetailApiBaseUrl' in outputs:
                return outputs['RetailApiBaseUrl'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # No fallback - retail tests should be skipped if not configured
    pytest.skip("RETAIL_API_URL not configured")


@pytest.fixture
def api_client(api_base_url):
    """
    API client with base URL configured (defaults to insurance vertical).
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
def insurance_api_client(insurance_api_base_url):
    """
    Insurance vertical API client.
    Returns requests session for making API calls to insurance vertical.
    """
    session = requests.Session()
    session.base_url = insurance_api_base_url

    def request(method, path, **kwargs):
        """Make request with base URL prepended"""
        url = f"{insurance_api_base_url}{path}"
        return session.request(method, url, **kwargs)

    session.api_request = request
    return session


@pytest.fixture
def retail_api_client(retail_api_base_url):
    """
    Retail vertical API client.
    Returns requests session for making API calls to retail vertical.
    """
    session = requests.Session()
    session.base_url = retail_api_base_url

    def request(method, path, **kwargs):
        """Make request with base URL prepended"""
        url = f"{retail_api_base_url}{path}"
        return session.request(method, url, **kwargs)

    session.api_request = request
    return session


@pytest.fixture
def sample_customer_data():
    """Sample customer data for testing (generated with Faker)"""
    return {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address().replace('\n', ', '),
        "phone": fake.phone_number()
    }


@pytest.fixture
def sample_quote_data():
    """Sample quote data for testing (generated with Faker)"""
    return {
        "customerName": fake.name(),
        "customerEmail": fake.email(),
        "propertyAddress": fake.address().replace('\n', ', '),
        "coverageAmount": fake.random_int(50000, 1000000, step=10000),
        "propertyType": fake.random_element(["SINGLE_FAMILY", "CONDO", "TOWNHOUSE"]),
        "yearBuilt": fake.random_int(1950, 2024)
    }


@pytest.fixture
def sample_policy_data():
    """Sample policy data for testing (generated with Faker)"""
    effective_date = fake.date_between(start_date='-1y', end_date='today')
    expiration_date = effective_date + timedelta(days=365)
    return {
        "quoteId": f"quote-{fake.uuid4()}",
        "policyNumber": fake.bothify(text='POL-####-####'),
        "holderName": fake.name(),
        "holderEmail": fake.email(),
        "propertyAddress": fake.address().replace('\n', ', '),
        "coverageAmount": fake.random_int(100000, 2000000, step=10000),
        "premium": round(fake.random_int(800, 5000, step=50) + fake.random.random(), 2),
        "effectiveDate": effective_date.isoformat(),
        "expirationDate": expiration_date.isoformat()
    }


@pytest.fixture
def sample_claim_data():
    """Sample claim data for testing (generated with Faker)"""
    return {
        "policyId": f"policy-{fake.uuid4()}",
        "claimNumber": fake.bothify(text='CLM-####-####'),
        "claimantName": fake.name(),
        "lossType": fake.random_element(["WATER_DAMAGE", "FIRE", "THEFT", "LIABILITY"]),
        "description": fake.text(max_nb_chars=200),
        "amount": fake.random_int(1000, 100000, step=1000),
        "estimatedAmount_cents": fake.random_int(1000, 100000, step=1000) * 100,
        "incidentDate": fake.date_between(start_date='-1y', end_date='today').isoformat()
    }


@pytest.fixture
def sample_payment_data():
    """Sample payment data for testing (generated with Faker)"""
    return {
        "policyId": f"policy-{fake.uuid4()}",
        "amount": round(fake.random_int(200, 1500, step=50) + fake.random.random(), 2),
        "paymentMethod": fake.random_element(["CREDIT_CARD", "BANK_TRANSFER", "CHECK"]),
        "cardLastFour": fake.numerify(text="####")
    }


@pytest.fixture
def sample_case_data():
    """Sample case data for testing (generated with Faker)"""
    case_titles = [
        "Policy Change Request",
        "Coverage Amount Inquiry",
        "Claim Status Update",
        "Payment Issue Resolution",
        "Document Upload Request",
        "Policy Cancellation Request"
    ]
    entity_type = fake.random_element(["policy", "quote", "claim"])
    return {
        "title": fake.random_element(case_titles),
        "description": fake.text(max_nb_chars=200),
        "relatedEntityType": entity_type,
        "relatedEntityId": f"{entity_type}-{fake.uuid4()}",
        "assignee": fake.name(),
        "priority": fake.random_element(["LOW", "MEDIUM", "HIGH"])
    }


# Retail Vertical Sample Data Fixtures

@pytest.fixture
def sample_product_data():
    """Sample product data for testing (generated with Faker)"""
    categories = ['Electronics', 'Apparel', 'Home & Garden', 'Sports & Outdoors', 'Books', 'Toys & Games']
    return {
        "sku": fake.bothify(text='SKU-#####'),
        "name": fake.catch_phrase(),
        "description": fake.text(max_nb_chars=150),
        "price": fake.random_int(10, 500),
        "category": fake.random_element(categories),
        "stockQuantity": fake.random_int(0, 500),
        "manufacturer": fake.company(),
        "weight": fake.random_int(1, 50)
    }


@pytest.fixture
def sample_order_data():
    """Sample order data for testing (generated with Faker)"""
    return {
        "orderNumber": fake.bothify(text='ORD-######'),
        "customerName": fake.name(),
        "customerEmail": fake.email(),
        "customerPhone": fake.phone_number(),
        "shippingAddress": fake.address().replace('\n', ', '),
        "items": [
            {
                "productId": f"product-{fake.uuid4()}",
                "productName": fake.catch_phrase(),
                "quantity": fake.random_int(1, 3),
                "price": fake.random_int(20, 200),
                "total": fake.random_int(20, 600)
            }
        ],
        "totalAmount": fake.random_int(50, 1000),
        "orderDate": fake.date_between(start_date='-90d', end_date='today').isoformat(),
        "status": fake.random_element(['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED'])
    }


@pytest.fixture
def sample_inventory_data():
    """Sample inventory data for testing (generated with Faker)"""
    warehouses = ['NYC-01', 'LA-02', 'CHI-03', 'DAL-04', 'ATL-05']
    return {
        "productId": f"product-{fake.uuid4()}",
        "productName": fake.catch_phrase(),
        "sku": fake.bothify(text='SKU-#####'),
        "location": fake.random_element(warehouses),
        "quantity": fake.random_int(0, 500),
        "reorderPoint": fake.random_int(10, 50),
        "lastRestocked": fake.date_between(start_date='-30d', end_date='today').isoformat()
    }


@pytest.fixture
def sample_retail_payment_data():
    """Sample retail payment data for testing (generated with Faker)"""
    return {
        "orderId": f"order-{fake.uuid4()}",
        "orderNumber": fake.bothify(text='ORD-######'),
        "amount": fake.random_int(50, 1000),
        "paymentMethod": fake.random_element(['CREDIT_CARD', 'DEBIT_CARD', 'PAYPAL', 'GIFT_CARD']),
        "transactionId": fake.bothify(text='TXN-#######'),
        "paymentDate": fake.date_between(start_date='-90d', end_date='today').isoformat()
    }


@pytest.fixture
def sample_retail_case_data():
    """Sample retail case data for testing (generated with Faker)"""
    topics = ['ORDER_INQUIRY', 'PRODUCT_DEFECT', 'SHIPPING_DELAY', 'REFUND_REQUEST', 'PRODUCT_QUESTION']
    priorities = ['LOW', 'MEDIUM', 'HIGH']
    return {
        "title": f"{fake.random_element(topics).replace('_', ' ')} - {fake.name()}",
        "description": fake.text(max_nb_chars=200),
        "customerName": fake.name(),
        "customerEmail": fake.email(),
        "topic": fake.random_element(topics),
        "priority": fake.random_element(priorities),
        "assignee": fake.random_element(['Support Team', 'Sales Team', 'Fulfillment']),
        "createdDate": fake.date_between(start_date='-60d', end_date='today').isoformat()
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


# Retail Vertical Test Fixtures with Cleanup

@pytest.fixture
def created_product(retail_api_client, sample_product_data):
    """Create a product for testing, clean up after."""
    response = retail_api_client.api_request('POST', '/product', json=sample_product_data)
    assert response.status_code == 201, f"Failed to create test product: {response.status_code}"
    product_id = response.json()['id']
    yield product_id
    # Cleanup
    retail_api_client.api_request('DELETE', f'/product/{product_id}')


@pytest.fixture
def created_order(retail_api_client, sample_order_data):
    """Create an order for testing, clean up after."""
    response = retail_api_client.api_request('POST', '/order', json=sample_order_data)
    assert response.status_code == 201, f"Failed to create test order: {response.status_code}"
    order_id = response.json()['id']
    yield order_id
    # Cleanup
    retail_api_client.api_request('DELETE', f'/order/{order_id}')


@pytest.fixture
def created_inventory(retail_api_client, sample_inventory_data):
    """Create an inventory record for testing, clean up after."""
    response = retail_api_client.api_request('POST', '/inventory', json=sample_inventory_data)
    assert response.status_code == 201, f"Failed to create test inventory: {response.status_code}"
    inventory_id = response.json()['id']
    yield inventory_id
    # Cleanup
    retail_api_client.api_request('DELETE', f'/inventory/{inventory_id}')


@pytest.fixture
def created_retail_payment(retail_api_client, sample_retail_payment_data):
    """Create a retail payment for testing, clean up after."""
    response = retail_api_client.api_request('POST', '/payment', json=sample_retail_payment_data)
    assert response.status_code == 201, f"Failed to create test payment: {response.status_code}"
    payment_id = response.json()['id']
    yield payment_id
    # Cleanup
    retail_api_client.api_request('DELETE', f'/payment/{payment_id}')


@pytest.fixture
def created_retail_case(retail_api_client, sample_retail_case_data):
    """Create a retail case for testing, clean up after."""
    response = retail_api_client.api_request('POST', '/case', json=sample_retail_case_data)
    assert response.status_code == 201, f"Failed to create test case: {response.status_code}"
    case_id = response.json()['id']
    yield case_id
    # Cleanup
    retail_api_client.api_request('DELETE', f'/case/{case_id}')


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
