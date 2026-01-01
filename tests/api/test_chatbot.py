"""
Chatbot API Contract Tests

Infrastructure-agnostic tests validating chatbot API behavior.
Tests verify chat endpoint request/response validation and error handling.
"""

import pytest


@pytest.mark.api
@pytest.mark.chatbot
def test_chat_success(api_client):
    """Test that valid chat request returns 200 with response"""
    chat_data = {
        "message": "What is the status of my claim?",
        "context": {
            "policyNumber": "POL-2024-001",
            "sessionId": "test-session-123"
        }
    }

    response = api_client.api_request('POST', '/chat', json=chat_data)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()

    assert 'response' in data, "Response should contain chat response"
    assert isinstance(data['response'], str), "Chat response should be a string"
    assert len(data['response']) > 0, "Chat response should not be empty"


@pytest.mark.api
@pytest.mark.chatbot
def test_chat_with_minimal_data(api_client):
    """Test chat with only required fields"""
    chat_data = {
        "message": "Hello"
    }

    response = api_client.api_request('POST', '/chat', json=chat_data)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert 'response' in data


@pytest.mark.api
@pytest.mark.chatbot
def test_chat_with_conversation_history(api_client):
    """Test chat with conversation history context"""
    chat_data = {
        "message": "What about my policy?",
        "context": {
            "sessionId": "test-session-456",
            "conversationHistory": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi! How can I help you today?"}
            ]
        }
    }

    response = api_client.api_request('POST', '/chat', json=chat_data)

    assert response.status_code == 200
    data = response.json()
    assert 'response' in data


@pytest.mark.api
@pytest.mark.chatbot
def test_chat_cors_headers(api_client):
    """Test that chat endpoint returns CORS headers"""
    chat_data = {
        "message": "Test message"
    }

    response = api_client.api_request('POST', '/chat', json=chat_data)

    assert 'Access-Control-Allow-Origin' in response.headers, "Missing CORS origin header"


# Negative Tests

@pytest.mark.api
@pytest.mark.chatbot
@pytest.mark.negative
def test_chat_missing_message(api_client):
    """Test that chat request without message returns 400"""
    chat_data = {
        "context": {
            "sessionId": "test-session"
        }
    }

    response = api_client.api_request('POST', '/chat', json=chat_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.chatbot
@pytest.mark.negative
def test_chat_empty_payload(api_client):
    """Test that empty payload returns 400"""
    response = api_client.api_request('POST', '/chat', json={})

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.chatbot
@pytest.mark.negative
def test_chat_invalid_json(api_client):
    """Test that invalid JSON returns 400"""
    response = api_client.api_request(
        'POST',
        '/chat',
        data='{"invalid": json syntax}',  # Invalid JSON
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.chatbot
@pytest.mark.negative
def test_chat_invalid_data_types(api_client):
    """Test that invalid data types return 400"""
    chat_data = {
        "message": 12345,  # Should be string
        "context": "not-an-object"  # Should be object
    }

    response = api_client.api_request('POST', '/chat', json=chat_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.chatbot
@pytest.mark.negative
def test_chat_empty_message(api_client):
    """Test that empty message string returns 400"""
    chat_data = {
        "message": ""
    }

    response = api_client.api_request('POST', '/chat', json=chat_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


@pytest.mark.api
@pytest.mark.chatbot
@pytest.mark.negative
def test_chat_excessively_long_message(api_client):
    """Test that excessively long message is handled appropriately"""
    # Create a very long message (e.g., 10000 characters)
    long_message = "A" * 10000
    chat_data = {
        "message": long_message
    }

    response = api_client.api_request('POST', '/chat', json=chat_data)

    # Should either accept it (200) or reject as too long (400/413)
    assert response.status_code in [200, 400, 413], f"Expected 200, 400, or 413, got {response.status_code}"


@pytest.mark.api
@pytest.mark.chatbot
@pytest.mark.negative
def test_chat_invalid_context_structure(api_client):
    """Test that invalid context structure returns 400"""
    chat_data = {
        "message": "Test message",
        "context": {
            "conversationHistory": "not-a-list"  # Should be array
        }
    }

    response = api_client.api_request('POST', '/chat', json=chat_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
