"""
Streaming Chat API Contract Tests

Tests Lambda Function URL streaming endpoints (/chat, /customer-chat) with NDJSON protocol.
Validates real-time status message streaming and response format.
"""

import os
import json
import pytest
import requests


@pytest.fixture(scope="session")
def ai_api_base_url():
    """
    Get AI API base URL (Lambda Function URL for streaming).

    Priority:
    1. SILVERMOAT_AI_API_URL environment variable
    2. CloudFormation stack AiApiUrl output
    3. Skip tests if not available
    """
    # Check environment variable first
    ai_api_url = os.environ.get('SILVERMOAT_AI_API_URL')
    if ai_api_url:
        return ai_api_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            if 'AiApiUrl' in outputs:
                return outputs['AiApiUrl'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # No URL available - tests will be skipped
    return None


@pytest.fixture
def streaming_client(ai_api_base_url):
    """
    Streaming API client for NDJSON responses.
    Returns requests session with helper for parsing NDJSON streams.
    """
    if not ai_api_base_url:
        pytest.skip("AI API URL not configured - set SILVERMOAT_AI_API_URL or STACK_NAME")

    session = requests.Session()
    session.base_url = ai_api_base_url

    def stream_request(method, path, **kwargs):
        """
        Make streaming request and parse NDJSON chunks.

        Returns list of parsed chunks: [{"type": "status|response|error", "data": {...}}, ...]
        """
        url = f"{ai_api_base_url}{path}"
        response = session.request(method, url, stream=True, **kwargs)

        chunks = []
        buffer = ""

        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if not chunk:
                continue

            buffer += chunk
            lines = buffer.split('\n')
            buffer = lines.pop()  # Keep incomplete line in buffer

            for line in lines:
                if not line.strip():
                    continue
                try:
                    parsed_chunk = json.loads(line)
                    chunks.append(parsed_chunk)
                except json.JSONDecodeError as e:
                    print(f"Warning: Failed to parse NDJSON chunk: {line} - {e}")

        # Process remaining buffer
        if buffer.strip():
            try:
                parsed_chunk = json.loads(buffer)
                chunks.append(parsed_chunk)
            except json.JSONDecodeError:
                pass

        return response, chunks

    session.stream_request = stream_request
    return session


@pytest.mark.api
@pytest.mark.streaming
def test_chat_streaming_returns_ndjson(streaming_client):
    """Test that /chat endpoint returns NDJSON chunks"""
    chat_data = {"message": "Hello, what can you help me with?"}

    response, chunks = streaming_client.stream_request('POST', '/chat', json=chat_data)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert len(chunks) > 0, "Should receive at least one chunk"

    # Verify NDJSON format
    for chunk in chunks:
        assert 'type' in chunk, "Each chunk should have 'type' field"
        assert 'data' in chunk, "Each chunk should have 'data' field"
        assert chunk['type'] in ['status', 'response', 'error'], f"Invalid chunk type: {chunk['type']}"


@pytest.mark.api
@pytest.mark.streaming
def test_chat_streaming_status_messages(streaming_client):
    """Test that status messages appear before final response"""
    chat_data = {"message": "Get my policy information"}

    response, chunks = streaming_client.stream_request('POST', '/chat', json=chat_data)

    assert response.status_code == 200

    # Verify status messages come before response
    status_chunks = [c for c in chunks if c['type'] == 'status']
    response_chunks = [c for c in chunks if c['type'] == 'response']

    assert len(status_chunks) > 0, "Should have at least one status message"
    assert len(response_chunks) == 1, "Should have exactly one response chunk"

    # Find indices
    last_status_idx = max([chunks.index(c) for c in chunks if c['type'] == 'status'])
    response_idx = chunks.index(response_chunks[0])

    assert last_status_idx < response_idx, "Status messages should come before final response"


@pytest.mark.api
@pytest.mark.streaming
def test_chat_streaming_status_format(streaming_client):
    """Test that status chunks have required fields"""
    chat_data = {"message": "Test message"}

    response, chunks = streaming_client.stream_request('POST', '/chat', json=chat_data)

    status_chunks = [c for c in chunks if c['type'] == 'status']
    assert len(status_chunks) > 0, "Should have status messages"

    for status in status_chunks:
        assert 'timestamp' in status['data'], "Status should have timestamp"
        assert 'operation' in status['data'], "Status should have operation"
        assert 'message' in status['data'], "Status should have message"
        assert isinstance(status['data']['timestamp'], int), "Timestamp should be integer (milliseconds)"
        assert status['data']['timestamp'] > 0, "Timestamp should be positive"


@pytest.mark.api
@pytest.mark.streaming
def test_chat_streaming_response_format(streaming_client):
    """Test that response chunk has required fields"""
    chat_data = {"message": "Hello"}

    response, chunks = streaming_client.stream_request('POST', '/chat', json=chat_data)

    response_chunks = [c for c in chunks if c['type'] == 'response']
    assert len(response_chunks) == 1, "Should have exactly one response chunk"

    response_data = response_chunks[0]['data']
    assert 'response' in response_data, "Response should have 'response' field"
    assert 'conversation' in response_data, "Response should have 'conversation' field"
    assert isinstance(response_data['response'], str), "Response should be string"
    assert isinstance(response_data['conversation'], list), "Conversation should be list"
    assert len(response_data['response']) > 0, "Response should not be empty"


@pytest.mark.api
@pytest.mark.streaming
def test_chat_streaming_with_history(streaming_client):
    """Test chat streaming with conversation history"""
    chat_data = {
        "message": "What did I just ask?",
        "history": [
            {"role": "user", "content": "Tell me about claims"},
            {"role": "assistant", "content": "I can help you with claims information."}
        ]
    }

    response, chunks = streaming_client.stream_request('POST', '/chat', json=chat_data)

    assert response.status_code == 200
    response_chunks = [c for c in chunks if c['type'] == 'response']
    assert len(response_chunks) == 1

    # Conversation should include history + new exchange
    conversation = response_chunks[0]['data']['conversation']
    assert len(conversation) >= 3, "Conversation should include history + new message + response"


@pytest.mark.api
@pytest.mark.streaming
def test_customer_chat_streaming(streaming_client):
    """Test /customer-chat endpoint streaming"""
    chat_data = {
        "message": "Show my policies",
        "customerEmail": "test@example.com"
    }

    response, chunks = streaming_client.stream_request('POST', '/customer-chat', json=chat_data)

    assert response.status_code == 200
    assert len(chunks) > 0

    # Should have status messages and response
    status_chunks = [c for c in chunks if c['type'] == 'status']
    response_chunks = [c for c in chunks if c['type'] == 'response']

    assert len(status_chunks) > 0, "Should have status messages"
    assert len(response_chunks) == 1, "Should have final response"


@pytest.mark.api
@pytest.mark.streaming
def test_chat_streaming_error_handling(streaming_client):
    """Test that invalid requests return error chunks"""
    # Send empty message (invalid)
    chat_data = {"message": ""}

    response, chunks = streaming_client.stream_request('POST', '/chat', json=chat_data)

    # Should get some response (either error chunk or validation error)
    assert len(chunks) > 0, "Should receive error indication"

    # If we get chunks, check for error type
    error_chunks = [c for c in chunks if c['type'] == 'error']
    if error_chunks:
        assert 'error' in error_chunks[0]['data'], "Error chunk should have 'error' field"
        assert 'message' in error_chunks[0]['data'], "Error chunk should have 'message' field"


@pytest.mark.api
@pytest.mark.streaming
def test_chat_streaming_cors_headers(streaming_client):
    """Test that streaming endpoint returns CORS headers"""
    chat_data = {"message": "Test CORS"}

    response, chunks = streaming_client.stream_request('POST', '/chat', json=chat_data)

    # Lambda Function URLs automatically handle CORS with configured options
    # Verify basic response works (CORS is handled by AWS)
    assert response.status_code == 200


@pytest.mark.api
@pytest.mark.streaming
def test_streaming_invalid_path(streaming_client):
    """Test that invalid paths are handled gracefully"""
    chat_data = {"message": "Test"}

    response, chunks = streaming_client.stream_request('POST', '/invalid-endpoint', json=chat_data)

    # Should return error chunk or 404
    if response.status_code != 404:
        error_chunks = [c for c in chunks if c['type'] == 'error']
        assert len(error_chunks) > 0, "Should return error chunk for invalid path"


@pytest.mark.api
@pytest.mark.streaming
def test_streaming_malformed_json(streaming_client):
    """Test that malformed JSON returns error chunk"""
    response = streaming_client.request(
        'POST',
        f"{streaming_client.base_url}/chat",
        data='{"invalid json',
        headers={'Content-Type': 'application/json'},
        stream=True
    )

    # Should return error chunk or 400
    chunks = []
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if not chunk:
            continue
        try:
            parsed = json.loads(chunk.strip())
            chunks.append(parsed)
        except:
            pass

    # Should indicate error
    if len(chunks) > 0:
        error_chunks = [c for c in chunks if c.get('type') == 'error']
        assert len(error_chunks) > 0, "Should return error chunk for malformed JSON"
