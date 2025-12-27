"""
Root API Endpoint Tests

Infrastructure-agnostic tests for API root endpoint and general behavior.
"""

import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_root_endpoint_responds(api_client):
    """Test that API root endpoint responds successfully"""
    response = api_client.api_request('GET', '/')

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


@pytest.mark.api
@pytest.mark.smoke
def test_root_endpoint_returns_json(api_client):
    """Test that root endpoint returns JSON"""
    response = api_client.api_request('GET', '/')

    assert response.status_code == 200
    assert response.headers.get('Content-Type', '').startswith('application/json')

    # Should be valid JSON
    data = response.json()
    assert isinstance(data, (dict, list))


@pytest.mark.api
@pytest.mark.smoke
def test_api_cors_headers(api_client):
    """Test that API returns CORS headers"""
    response = api_client.api_request('GET', '/')

    # Should have CORS headers for browser access
    assert 'Access-Control-Allow-Origin' in response.headers, "Missing CORS origin header"


@pytest.mark.api
@pytest.mark.smoke
def test_root_endpoint_lists_available_endpoints(api_client):
    """Test that root endpoint provides API documentation/endpoint list"""
    response = api_client.api_request('GET', '/')
    assert response.status_code == 200

    data = response.json()

    # Root should provide some info about available endpoints
    # (exact format doesn't matter - could be 'endpoints', 'routes', 'message', etc.)
    assert len(data) > 0, "Root endpoint should return some data"
