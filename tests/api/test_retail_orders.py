"""
Retail Order API Contract Tests

Infrastructure-agnostic tests validating retail order API behavior.
"""

import pytest


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.orders
def test_create_order_success(retail_api_client, sample_order_data):
    """Test that valid order creation returns 201 with order ID"""
    response = retail_api_client.api_request('POST', '/order', json=sample_order_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    data = response.json()

    # Validate response structure
    assert 'id' in data, "Response should contain order ID"
    assert isinstance(data['id'], str), "Order ID should be a string"
    assert len(data['id']) > 0, "Order ID should not be empty"

    # Cleanup
    retail_api_client.api_request('DELETE', f'/order/{data["id"]}')


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.orders
def test_get_order_by_id(retail_api_client, created_order):
    """Test that created order can be retrieved by ID"""
    # Retrieve the order
    get_response = retail_api_client.api_request('GET', f'/order/{created_order}')

    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
    order = get_response.json()

    # Validate order structure
    assert order['id'] == created_order
    assert 'orderNumber' in order['data']
    assert 'customerName' in order['data']
    assert 'items' in order['data']
    assert 'totalAmount' in order['data']
    assert 'status' in order['data']


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.orders
def test_get_order_not_found(retail_api_client):
    """Test that requesting non-existent order returns 404"""
    non_existent_id = 'order-does-not-exist-999999'

    response = retail_api_client.api_request('GET', f'/order/{non_existent_id}')

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.orders
def test_order_data_persistence(retail_api_client, created_order, sample_order_data):
    """Test that order data persists correctly"""
    # Retrieve order
    get_response = retail_api_client.api_request('GET', f'/order/{created_order}')
    assert get_response.status_code == 200
    order = get_response.json()

    # Verify data matches what was submitted
    assert order['data']['orderNumber'] == sample_order_data['orderNumber']
    assert order['data']['customerName'] == sample_order_data['customerName']
    assert order['data']['totalAmount'] == sample_order_data['totalAmount']
    assert order['data']['status'] == sample_order_data['status']


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.orders
def test_order_items_persistence(retail_api_client, created_order, sample_order_data):
    """Test that order items persist correctly"""
    # Retrieve order
    get_response = retail_api_client.api_request('GET', f'/order/{created_order}')
    assert get_response.status_code == 200
    order = get_response.json()

    # Verify items are present
    assert 'items' in order['data']
    assert isinstance(order['data']['items'], list)
    assert len(order['data']['items']) > 0


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.orders
def test_delete_order_success(retail_api_client, sample_order_data):
    """Test that order can be deleted successfully"""
    # Create an order
    create_response = retail_api_client.api_request('POST', '/order', json=sample_order_data)
    assert create_response.status_code == 201
    order_id = create_response.json()['id']

    # Delete the order
    delete_response = retail_api_client.api_request('DELETE', f'/order/{order_id}')
    assert delete_response.status_code in [200, 204], f"Expected 200 or 204, got {delete_response.status_code}"

    # Verify order no longer exists
    get_response = retail_api_client.api_request('GET', f'/order/{order_id}')
    assert get_response.status_code == 404, "Deleted order should return 404"


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.orders
def test_delete_order_not_found(retail_api_client):
    """Test that deleting non-existent order succeeds (idempotent DELETE)"""
    non_existent_id = 'order-does-not-exist-999999'

    response = retail_api_client.api_request('DELETE', f'/order/{non_existent_id}')

    # DELETE is idempotent - both 200 and 404 are acceptable
    assert response.status_code in [200, 204, 404], f"Expected 200, 204, or 404, got {response.status_code}"


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.orders
def test_list_orders(retail_api_client, created_order):
    """Test that orders can be listed"""
    response = retail_api_client.api_request('GET', '/order')

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()

    # Validate response structure
    assert 'items' in data, "Response should contain items list"
    assert isinstance(data['items'], list), "Items should be a list"

    # Created order should be in the list
    order_ids = [item['id'] for item in data['items']]
    assert created_order in order_ids, "Created order should be in list"
