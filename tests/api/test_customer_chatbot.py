"""
Customer Chatbot API Contract Tests

Infrastructure-agnostic tests validating customer chatbot API behavior.
Tests verify customer chat endpoint with email filtering and data scoping.
"""

import pytest


@pytest.mark.api
@pytest.mark.customer_chatbot
def test_customer_chat_success(api_client):
    """Test that valid customer chat request returns 200 with response"""
    chat_data = {
        "message": "Show me my policies",
        "customerEmail": "customer@example.com",
        "history": []
    }

    response = api_client.api_request('POST', '/customer-chat', json=chat_data)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()

    assert 'response' in data, "Response should contain chat response"
    assert isinstance(data['response'], str), "Chat response should be a string"
    assert len(data['response']) > 0, "Chat response should not be empty"


@pytest.mark.api
@pytest.mark.customer_chatbot
def test_customer_chat_with_history(api_client):
    """Test customer chat with conversation history"""
    chat_data = {
        "message": "What about my claims?",
        "customerEmail": "customer@example.com",
        "history": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi! How can I help you today?"}
        ]
    }

    response = api_client.api_request('POST', '/customer-chat', json=chat_data)

    assert response.status_code == 200
    data = response.json()
    assert 'response' in data
    assert 'conversation' in data


@pytest.mark.api
@pytest.mark.customer_chatbot
def test_customer_chat_cors_headers(api_client):
    """Test that customer chat endpoint returns CORS headers"""
    chat_data = {
        "message": "Test message",
        "customerEmail": "customer@example.com"
    }

    response = api_client.api_request('POST', '/customer-chat', json=chat_data)

    assert 'Access-Control-Allow-Origin' in response.headers, "Missing CORS origin header"


@pytest.mark.api
@pytest.mark.customer_chatbot
def test_customer_chat_returns_status_messages(api_client):
    """Test that customer chat response includes status_messages for operation transparency"""
    chat_data = {
        "message": "Show me my policies",
        "customerEmail": "customer@example.com"
    }

    response = api_client.api_request('POST', '/customer-chat', json=chat_data)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()

    # Verify status_messages field exists
    assert 'status_messages' in data, "Response should contain status_messages array"
    assert isinstance(data['status_messages'], list), "status_messages should be a list"

    # Verify status messages have expected structure
    if len(data['status_messages']) > 0:
        status_msg = data['status_messages'][0]
        assert 'timestamp' in status_msg, "Status message should have timestamp"
        assert 'operation' in status_msg, "Status message should have operation type"
        assert 'message' in status_msg, "Status message should have message text"
        assert status_msg['operation'] in ['dynamodb_query', 'tool_execution', 'ai_processing'], \
            "Operation type should be one of the valid types"


# Negative Tests

@pytest.mark.api
@pytest.mark.customer_chatbot
@pytest.mark.negative
def test_customer_chat_missing_message(api_client):
    """Test that customer chat request without message returns 400"""
    chat_data = {
        "customerEmail": "customer@example.com"
    }

    response = api_client.api_request('POST', '/customer-chat', json=chat_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = response.json()
    assert 'error' in data
    assert data['error'] == 'message_required'


@pytest.mark.api
@pytest.mark.customer_chatbot
@pytest.mark.negative
def test_customer_chat_missing_email(api_client):
    """Test that customer chat request without customerEmail returns 400"""
    chat_data = {
        "message": "Show me my policies"
    }

    response = api_client.api_request('POST', '/customer-chat', json=chat_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = response.json()
    assert 'error' in data
    assert data['error'] == 'customer_email_required'


@pytest.mark.api
@pytest.mark.customer_chatbot
@pytest.mark.negative
def test_customer_chat_empty_payload(api_client):
    """Test that empty payload returns 400"""
    response = api_client.api_request('POST', '/customer-chat', json={})

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.customer_chatbot
@pytest.mark.negative
def test_customer_chat_empty_message(api_client):
    """Test that empty message string returns 400"""
    chat_data = {
        "message": "",
        "customerEmail": "customer@example.com"
    }

    response = api_client.api_request('POST', '/customer-chat', json=chat_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.customer_chatbot
@pytest.mark.negative
def test_customer_chat_empty_email(api_client):
    """Test that empty customerEmail string returns 400"""
    chat_data = {
        "message": "Show me my policies",
        "customerEmail": ""
    }

    response = api_client.api_request('POST', '/customer-chat', json=chat_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.customer_chatbot
@pytest.mark.negative
def test_customer_chat_invalid_json(api_client):
    """Test that invalid JSON returns 400"""
    response = api_client.api_request(
        'POST',
        '/customer-chat',
        data='{"invalid": json syntax}',
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.customer_chatbot
@pytest.mark.negative
def test_customer_chat_invalid_history_type(api_client):
    """Test that invalid history type returns 400"""
    chat_data = {
        "message": "Test message",
        "customerEmail": "customer@example.com",
        "history": "not-a-list"
    }

    response = api_client.api_request('POST', '/customer-chat', json=chat_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
