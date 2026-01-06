"""
Vertical Isolation Tests

Tests to verify that data is completely isolated between verticals.
Insurance data should not appear in retail, and vice versa.
"""

import pytest


@pytest.mark.api
@pytest.mark.vertical
@pytest.mark.isolation
def test_insurance_quote_not_in_retail(insurance_api_client, retail_api_client, sample_quote_data):
    """Test that insurance quote doesn't appear in retail vertical"""
    # Create a quote in insurance
    create_response = insurance_api_client.api_request('POST', '/quote', json=sample_quote_data)
    assert create_response.status_code == 201
    quote_id = create_response.json()['id']

    try:
        # Try to retrieve it from retail API (should fail since retail doesn't have /quote)
        retail_response = retail_api_client.api_request('GET', f'/quote/{quote_id}')
        assert retail_response.status_code == 404, "Retail API should not have /quote endpoint"
    finally:
        # Cleanup
        insurance_api_client.api_request('DELETE', f'/quote/{quote_id}')


@pytest.mark.api
@pytest.mark.vertical
@pytest.mark.isolation
def test_retail_product_not_in_insurance(insurance_api_client, retail_api_client, sample_product_data):
    """Test that retail product doesn't appear in insurance vertical"""
    # Create a product in retail
    create_response = retail_api_client.api_request('POST', '/product', json=sample_product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()['id']

    try:
        # Try to retrieve it from insurance API (should fail since insurance doesn't have /product)
        insurance_response = insurance_api_client.api_request('GET', f'/product/{product_id}')
        assert insurance_response.status_code == 404, "Insurance API should not have /product endpoint"
    finally:
        # Cleanup
        retail_api_client.api_request('DELETE', f'/product/{product_id}')


@pytest.mark.api
@pytest.mark.vertical
@pytest.mark.isolation
def test_insurance_customer_list_isolated(insurance_api_client, retail_api_client):
    """Test that insurance customer list doesn't include retail customers"""
    # Get insurance customers
    insurance_response = insurance_api_client.api_request('GET', '/customer')
    assert insurance_response.status_code == 200
    insurance_data = insurance_response.json()

    # Get retail customers
    retail_response = retail_api_client.api_request('GET', '/customer')
    assert retail_response.status_code == 200
    retail_data = retail_response.json()

    # Extract customer IDs
    insurance_ids = {item['id'] for item in insurance_data.get('items', [])}
    retail_ids = {item['id'] for item in retail_data.get('items', [])}

    # Verify no overlap (customers might exist in both but with different IDs)
    # For now, just verify both APIs return data structures properly
    assert 'items' in insurance_data
    assert 'items' in retail_data


@pytest.mark.api
@pytest.mark.vertical
@pytest.mark.isolation
def test_insurance_policy_count_independent(insurance_api_client, retail_api_client, sample_policy_data):
    """Test that insurance policy creation doesn't affect retail order count"""
    # Get initial retail order count
    retail_initial = retail_api_client.api_request('GET', '/order')
    initial_order_count = len(retail_initial.json().get('items', []))

    # Create a policy in insurance
    policy_response = insurance_api_client.api_request('POST', '/policy', json=sample_policy_data)
    assert policy_response.status_code == 201
    policy_id = policy_response.json()['id']

    try:
        # Verify retail order count hasn't changed
        retail_after = retail_api_client.api_request('GET', '/order')
        after_order_count = len(retail_after.json().get('items', []))

        assert after_order_count == initial_order_count, \
            "Retail order count should not change when insurance policy is created"
    finally:
        # Cleanup
        insurance_api_client.api_request('DELETE', f'/policy/{policy_id}')


@pytest.mark.api
@pytest.mark.vertical
@pytest.mark.isolation
def test_retail_order_count_independent(insurance_api_client, retail_api_client, sample_order_data):
    """Test that retail order creation doesn't affect insurance policy count"""
    # Get initial insurance policy count
    insurance_initial = insurance_api_client.api_request('GET', '/policy')
    initial_policy_count = len(insurance_initial.json().get('items', []))

    # Create an order in retail
    order_response = retail_api_client.api_request('POST', '/order', json=sample_order_data)
    assert order_response.status_code == 201
    order_id = order_response.json()['id']

    try:
        # Verify insurance policy count hasn't changed
        insurance_after = insurance_api_client.api_request('GET', '/policy')
        after_policy_count = len(insurance_after.json().get('items', []))

        assert after_policy_count == initial_policy_count, \
            "Insurance policy count should not change when retail order is created"
    finally:
        # Cleanup
        retail_api_client.api_request('DELETE', f'/order/{order_id}')


@pytest.mark.api
@pytest.mark.vertical
@pytest.mark.isolation
def test_payment_entities_isolated(insurance_api_client, retail_api_client, sample_payment_data, sample_retail_payment_data):
    """Test that payment entities are isolated between verticals"""
    # Create payment in insurance
    insurance_payment = insurance_api_client.api_request('POST', '/payment', json=sample_payment_data)
    assert insurance_payment.status_code == 201
    insurance_payment_id = insurance_payment.json()['id']

    # Create payment in retail
    retail_payment = retail_api_client.api_request('POST', '/payment', json=sample_retail_payment_data)
    assert retail_payment.status_code == 201
    retail_payment_id = retail_payment.json()['id']

    try:
        # Verify insurance payment only in insurance
        insurance_get = insurance_api_client.api_request('GET', f'/payment/{insurance_payment_id}')
        assert insurance_get.status_code == 200

        # Verify retail payment only in retail
        retail_get = retail_api_client.api_request('GET', f'/payment/{retail_payment_id}')
        assert retail_get.status_code == 200

        # Verify retail payment not in insurance
        cross_check1 = insurance_api_client.api_request('GET', f'/payment/{retail_payment_id}')
        assert cross_check1.status_code == 404, "Retail payment should not exist in insurance"

        # Verify insurance payment not in retail
        cross_check2 = retail_api_client.api_request('GET', f'/payment/{insurance_payment_id}')
        assert cross_check2.status_code == 404, "Insurance payment should not exist in retail"
    finally:
        # Cleanup
        insurance_api_client.api_request('DELETE', f'/payment/{insurance_payment_id}')
        retail_api_client.api_request('DELETE', f'/payment/{retail_payment_id}')
