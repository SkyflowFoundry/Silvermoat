"""
Vertical Routing Tests

Tests to verify that the multi-vertical architecture correctly routes requests
to the appropriate vertical based on subdomain detection.
"""

import pytest
import os


@pytest.mark.api
@pytest.mark.vertical
def test_insurance_vertical_detection():
    """Test that insurance subdomain is detected correctly"""
    # This test verifies the CDK stack has created separate API endpoints
    insurance_url = os.environ.get('INSURANCE_API_URL')
    retail_url = os.environ.get('RETAIL_API_URL')

    # Skip if vertical-specific URLs not configured
    if not insurance_url or not retail_url:
        pytest.skip("Vertical-specific API URLs not configured (INSURANCE_API_URL, RETAIL_API_URL)")

    assert insurance_url != retail_url, "Insurance and retail should have separate API endpoints"


@pytest.mark.api
@pytest.mark.vertical
def test_retail_vertical_detection():
    """Test that retail subdomain is detected correctly"""
    retail_url = os.environ.get('RETAIL_API_URL')

    if not retail_url:
        pytest.skip("RETAIL_API_URL not configured")

    assert 'retail' in retail_url or 'RETAIL' in retail_url, "Retail URL should indicate retail vertical"


@pytest.mark.api
@pytest.mark.vertical
def test_insurance_entities_accessible(insurance_api_client, sample_quote_data):
    """Test that insurance entities are accessible via insurance API"""
    # Create a quote via insurance API
    response = insurance_api_client.api_request('POST', '/quote', json=sample_quote_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    quote_id = response.json()['id']

    # Cleanup
    insurance_api_client.api_request('DELETE', f'/quote/{quote_id}')


@pytest.mark.api
@pytest.mark.vertical
def test_retail_entities_accessible(retail_api_client, sample_product_data):
    """Test that retail entities are accessible via retail API"""
    # Create a product via retail API
    response = retail_api_client.api_request('POST', '/product', json=sample_product_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    product_id = response.json()['id']

    # Cleanup
    retail_api_client.api_request('DELETE', f'/product/{product_id}')


@pytest.mark.api
@pytest.mark.vertical
def test_insurance_doesnt_accept_retail_entities(insurance_api_client, sample_product_data):
    """Test that insurance API doesn't accept retail-specific entities"""
    # Try to create a product via insurance API (should fail)
    response = insurance_api_client.api_request('POST', '/product', json=sample_product_data)

    # Insurance API should not have /product endpoint
    assert response.status_code in [404, 400], f"Insurance API should reject /product endpoint"


@pytest.mark.api
@pytest.mark.vertical
def test_retail_doesnt_accept_insurance_entities(retail_api_client, sample_quote_data):
    """Test that retail API doesn't accept insurance-specific entities"""
    # Try to create a quote via retail API (should fail)
    response = retail_api_client.api_request('POST', '/quote', json=sample_quote_data)

    # Retail API should not have /quote endpoint
    assert response.status_code in [404, 400], f"Retail API should reject /quote endpoint"
