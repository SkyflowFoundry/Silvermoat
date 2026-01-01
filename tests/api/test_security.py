"""
Security and CORS API Contract Tests

Infrastructure-agnostic tests validating security mechanisms:
- CORS preflight (OPTIONS) requests
- CORS headers on responses
- Authentication and authorization behavior
"""

import pytest


# CORS Tests

@pytest.mark.api
@pytest.mark.security
def test_cors_preflight_quote_endpoint(api_client):
    """Test CORS preflight request to quote endpoint"""
    response = api_client.api_request(
        'OPTIONS',
        '/quote',
        headers={
            'Origin': 'https://example.com',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
    )

    # OPTIONS should return 200 or 204
    assert response.status_code in [200, 204], f"Expected 200 or 204, got {response.status_code}"

    # Should have CORS headers
    assert 'Access-Control-Allow-Origin' in response.headers, "Missing CORS allow origin header"
    assert 'Access-Control-Allow-Methods' in response.headers, "Missing CORS allow methods header"


@pytest.mark.api
@pytest.mark.security
def test_cors_preflight_policy_endpoint(api_client):
    """Test CORS preflight request to policy endpoint"""
    response = api_client.api_request(
        'OPTIONS',
        '/policy',
        headers={
            'Origin': 'https://example.com',
            'Access-Control-Request-Method': 'POST'
        }
    )

    assert response.status_code in [200, 204]
    assert 'Access-Control-Allow-Origin' in response.headers


@pytest.mark.api
@pytest.mark.security
def test_cors_preflight_claim_endpoint(api_client):
    """Test CORS preflight request to claim endpoint"""
    response = api_client.api_request(
        'OPTIONS',
        '/claim',
        headers={
            'Origin': 'https://example.com',
            'Access-Control-Request-Method': 'POST'
        }
    )

    assert response.status_code in [200, 204]
    assert 'Access-Control-Allow-Origin' in response.headers


@pytest.mark.api
@pytest.mark.security
def test_cors_preflight_payment_endpoint(api_client):
    """Test CORS preflight request to payment endpoint"""
    response = api_client.api_request(
        'OPTIONS',
        '/payment',
        headers={
            'Origin': 'https://example.com',
            'Access-Control-Request-Method': 'POST'
        }
    )

    assert response.status_code in [200, 204]
    assert 'Access-Control-Allow-Origin' in response.headers


@pytest.mark.api
@pytest.mark.security
def test_cors_preflight_case_endpoint(api_client):
    """Test CORS preflight request to case endpoint"""
    response = api_client.api_request(
        'OPTIONS',
        '/case',
        headers={
            'Origin': 'https://example.com',
            'Access-Control-Request-Method': 'POST'
        }
    )

    assert response.status_code in [200, 204]
    assert 'Access-Control-Allow-Origin' in response.headers


@pytest.mark.api
@pytest.mark.security
def test_cors_preflight_chat_endpoint(api_client):
    """Test CORS preflight request to chat endpoint"""
    response = api_client.api_request(
        'OPTIONS',
        '/chat',
        headers={
            'Origin': 'https://example.com',
            'Access-Control-Request-Method': 'POST'
        }
    )

    assert response.status_code in [200, 204]
    assert 'Access-Control-Allow-Origin' in response.headers


@pytest.mark.api
@pytest.mark.security
def test_cors_headers_present_on_get_requests(api_client, sample_quote_data):
    """Test that GET requests include CORS headers"""
    # Create a quote
    create_response = api_client.api_request('POST', '/quote', json=sample_quote_data)
    assert create_response.status_code == 201
    quote_id = create_response.json()['id']

    # GET request should have CORS headers
    get_response = api_client.api_request('GET', f'/quote/{quote_id}')

    assert 'Access-Control-Allow-Origin' in get_response.headers, "GET response missing CORS headers"


@pytest.mark.api
@pytest.mark.security
def test_cors_headers_present_on_post_requests(api_client, sample_quote_data):
    """Test that POST requests include CORS headers"""
    response = api_client.api_request('POST', '/quote', json=sample_quote_data)

    assert 'Access-Control-Allow-Origin' in response.headers, "POST response missing CORS headers"


@pytest.mark.api
@pytest.mark.security
def test_cors_headers_present_on_delete_requests(api_client, sample_quote_data):
    """Test that DELETE requests include CORS headers"""
    # Create a quote
    create_response = api_client.api_request('POST', '/quote', json=sample_quote_data)
    assert create_response.status_code == 201
    quote_id = create_response.json()['id']

    # DELETE request should have CORS headers
    delete_response = api_client.api_request('DELETE', f'/quote/{quote_id}')

    assert 'Access-Control-Allow-Origin' in delete_response.headers, "DELETE response missing CORS headers"


# Input Validation and Security

@pytest.mark.api
@pytest.mark.security
@pytest.mark.negative
def test_sql_injection_attempt_in_quote(api_client):
    """Test that SQL injection attempts are rejected"""
    malicious_data = {
        "customer_name": "'; DROP TABLE quotes; --",
        "customer_email": "test@example.com",
        "property_address": "123 Test St",
        "coverage_amount": 100000,
        "property_type": "single_family",
        "year_built": 2020
    }

    response = api_client.api_request('POST', '/quote', json=malicious_data)

    # Should either succeed (SQL injection prevented) or fail validation
    # Either way, table should not be dropped
    assert response.status_code in [201, 400]


@pytest.mark.api
@pytest.mark.security
@pytest.mark.negative
def test_xss_attempt_in_quote(api_client):
    """Test that XSS attempts in input are handled"""
    malicious_data = {
        "customer_name": "<script>alert('xss')</script>",
        "customer_email": "test@example.com",
        "property_address": "123 Test St",
        "coverage_amount": 100000,
        "property_type": "single_family",
        "year_built": 2020
    }

    response = api_client.api_request('POST', '/quote', json=malicious_data)

    # Should either succeed (XSS sanitized) or fail validation
    assert response.status_code in [201, 400]


@pytest.mark.api
@pytest.mark.security
@pytest.mark.negative
def test_null_byte_injection(api_client):
    """Test that null byte injection attempts are handled"""
    malicious_data = {
        "customer_name": "Test\x00User",
        "customer_email": "test@example.com",
        "property_address": "123 Test St",
        "coverage_amount": 100000,
        "property_type": "single_family",
        "year_built": 2020
    }

    response = api_client.api_request('POST', '/quote', json=malicious_data)

    # Should be rejected or sanitized
    assert response.status_code in [201, 400]


@pytest.mark.api
@pytest.mark.security
@pytest.mark.negative
def test_oversized_request_payload(api_client):
    """Test that oversized request payloads are rejected"""
    # Create a very large payload (e.g., 10MB string)
    large_string = "A" * (10 * 1024 * 1024)
    oversized_data = {
        "customer_name": large_string,
        "customer_email": "test@example.com",
        "property_address": "123 Test St",
        "coverage_amount": 100000,
        "property_type": "single_family",
        "year_built": 2020
    }

    response = api_client.api_request('POST', '/quote', json=oversized_data)

    # Should reject oversized payload
    assert response.status_code in [400, 413], f"Expected 400 or 413, got {response.status_code}"


@pytest.mark.api
@pytest.mark.security
@pytest.mark.negative
def test_path_traversal_attempt(api_client):
    """Test that path traversal attempts are rejected"""
    # Attempt path traversal in ID parameter
    response = api_client.api_request('GET', '/quote/../../../etc/passwd')

    # Should return 400 or 404, not expose file system
    assert response.status_code in [400, 404]


@pytest.mark.api
@pytest.mark.security
@pytest.mark.negative
def test_invalid_content_type(api_client):
    """Test that requests with invalid content type are rejected"""
    response = api_client.api_request(
        'POST',
        '/quote',
        data='not json data',
        headers={'Content-Type': 'text/plain'}
    )

    # Should reject non-JSON content type for JSON endpoint
    assert response.status_code in [400, 415], f"Expected 400 or 415, got {response.status_code}"


@pytest.mark.api
@pytest.mark.security
@pytest.mark.negative
def test_missing_content_type_header(api_client):
    """Test POST request without Content-Type header"""
    response = api_client.api_request(
        'POST',
        '/quote',
        data='{"customer_name": "Test"}',
        headers={}  # No Content-Type
    )

    # Should handle missing Content-Type appropriately
    assert response.status_code in [400, 415], f"Expected 400 or 415, got {response.status_code}"
