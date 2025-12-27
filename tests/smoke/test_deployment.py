"""
Deployment Smoke Tests

Minimal checks to verify CloudFormation deployment succeeded.
Does NOT validate specific AWS resources (DynamoDB, S3, Lambda, etc.)
Only checks that deployment completed and URLs are accessible.
"""

import pytest
import requests


@pytest.mark.smoke
@pytest.mark.deployment
def test_stack_deployed_successfully(stack_outputs):
    """Test that CloudFormation stack is in successful state"""
    stack = stack_outputs['stack']

    # Stack should be in a successful state
    assert stack['StackStatus'] in ['CREATE_COMPLETE', 'UPDATE_COMPLETE'], \
        f"Stack should be deployed successfully, got status: {stack['StackStatus']}"


@pytest.mark.smoke
@pytest.mark.deployment
def test_required_outputs_exist(stack_outputs):
    """Test that stack exports required output values"""
    outputs = stack_outputs['outputs']

    # Should have API URL
    assert 'ApiBaseUrl' in outputs, "Stack should export ApiBaseUrl"

    # Should have Web URL (could be WebUrl or CloudFrontUrl)
    assert 'WebUrl' in outputs or 'CloudFrontUrl' in outputs, \
        "Stack should export WebUrl or CloudFrontUrl"


@pytest.mark.smoke
@pytest.mark.deployment
def test_api_url_is_reachable(stack_outputs):
    """Test that API URL responds to requests"""
    outputs = stack_outputs['outputs']
    api_url = outputs.get('ApiBaseUrl')

    assert api_url, "ApiBaseUrl should be present in outputs"

    # API should respond (don't care about specific status code, just that it responds)
    try:
        response = requests.get(api_url, timeout=10)
        # Any response is good (200, 404, etc. - just needs to be reachable)
        assert response.status_code < 500, \
            f"API should be reachable and not return server error, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"API URL not reachable: {e}")


@pytest.mark.smoke
@pytest.mark.deployment
def test_web_url_is_reachable(stack_outputs):
    """Test that Web URL responds to requests"""
    outputs = stack_outputs['outputs']

    # Try WebUrl first, then CloudFrontUrl
    web_url = outputs.get('WebUrl') or outputs.get('CloudFrontUrl')

    assert web_url, "WebUrl or CloudFrontUrl should be present in outputs"

    # Web URL should respond
    try:
        response = requests.get(web_url, timeout=10)
        # Should return 200 (web page loaded)
        assert response.status_code == 200, \
            f"Web URL should return 200, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Web URL not reachable: {e}")


@pytest.mark.smoke
@pytest.mark.deployment
def test_api_returns_json(stack_outputs):
    """Test that API responds with JSON"""
    outputs = stack_outputs['outputs']
    api_url = outputs.get('ApiBaseUrl')

    response = requests.get(api_url, timeout=10)

    # Should return JSON content type
    content_type = response.headers.get('Content-Type', '')
    assert 'application/json' in content_type, \
        f"API should return JSON, got Content-Type: {content_type}"

    # Should be valid JSON
    try:
        data = response.json()
        assert data is not None, "API should return valid JSON data"
    except Exception as e:
        pytest.fail(f"API did not return valid JSON: {e}")
