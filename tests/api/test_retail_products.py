"""
Retail Product API Contract Tests

Infrastructure-agnostic tests validating retail product API behavior.
"""

import pytest


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.products
def test_create_product_success(retail_api_client, sample_product_data):
    """Test that valid product creation returns 201 with product ID"""
    response = retail_api_client.api_request('POST', '/product', json=sample_product_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    data = response.json()

    # Validate response structure
    assert 'id' in data, "Response should contain product ID"
    assert isinstance(data['id'], str), "Product ID should be a string"
    assert len(data['id']) > 0, "Product ID should not be empty"

    # Cleanup
    retail_api_client.api_request('DELETE', f'/product/{data["id"]}')


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.products
def test_get_product_by_id(retail_api_client, created_product):
    """Test that created product can be retrieved by ID"""
    # Retrieve the product
    get_response = retail_api_client.api_request('GET', f'/product/{created_product}')

    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
    product = get_response.json()

    # Validate product structure
    assert product['id'] == created_product
    assert 'sku' in product['data']
    assert 'name' in product['data']
    assert 'price' in product['data']
    assert 'category' in product['data']


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.products
def test_get_product_not_found(retail_api_client):
    """Test that requesting non-existent product returns 404"""
    non_existent_id = 'product-does-not-exist-999999'

    response = retail_api_client.api_request('GET', f'/product/{non_existent_id}')

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.products
def test_product_data_persistence(retail_api_client, created_product, sample_product_data):
    """Test that product data persists correctly"""
    # Retrieve product
    get_response = retail_api_client.api_request('GET', f'/product/{created_product}')
    assert get_response.status_code == 200
    product = get_response.json()

    # Verify data matches what was submitted
    assert product['data']['sku'] == sample_product_data['sku']
    assert product['data']['name'] == sample_product_data['name']
    assert product['data']['price'] == sample_product_data['price']
    assert product['data']['category'] == sample_product_data['category']


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.products
def test_product_cors_headers(retail_api_client, sample_product_data):
    """Test that product endpoints return CORS headers"""
    response = retail_api_client.api_request('POST', '/product', json=sample_product_data)

    # Should have CORS headers in actual responses
    assert 'Access-Control-Allow-Origin' in response.headers, "Missing CORS origin header"

    # Cleanup
    if response.status_code == 201:
        retail_api_client.api_request('DELETE', f'/product/{response.json()["id"]}')


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.products
def test_delete_product_success(retail_api_client, sample_product_data):
    """Test that product can be deleted successfully"""
    # Create a product
    create_response = retail_api_client.api_request('POST', '/product', json=sample_product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()['id']

    # Delete the product
    delete_response = retail_api_client.api_request('DELETE', f'/product/{product_id}')
    assert delete_response.status_code in [200, 204], f"Expected 200 or 204, got {delete_response.status_code}"

    # Verify product no longer exists
    get_response = retail_api_client.api_request('GET', f'/product/{product_id}')
    assert get_response.status_code == 404, "Deleted product should return 404"


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.products
def test_delete_product_not_found(retail_api_client):
    """Test that deleting non-existent product succeeds (idempotent DELETE)"""
    non_existent_id = 'product-does-not-exist-999999'

    response = retail_api_client.api_request('DELETE', f'/product/{non_existent_id}')

    # DELETE is idempotent - both 200 and 404 are acceptable
    assert response.status_code in [200, 204, 404], f"Expected 200, 204, or 404, got {response.status_code}"


@pytest.mark.api
@pytest.mark.retail
@pytest.mark.products
def test_list_products(retail_api_client, created_product):
    """Test that products can be listed"""
    response = retail_api_client.api_request('GET', '/product')

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()

    # Validate response structure
    assert 'items' in data, "Response should contain items list"
    assert isinstance(data['items'], list), "Items should be a list"

    # Created product should be in the list
    product_ids = [item['id'] for item in data['items']]
    assert created_product in product_ids, "Created product should be in list"
