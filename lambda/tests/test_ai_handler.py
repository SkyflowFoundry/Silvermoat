"""
Unit tests for ai_handler - AI chatbot operations.

Tests all routes:
- POST /chat (internal chatbot)
- POST /customer-chat (customer chatbot)
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from ai_handler.handler import handler


class TestChatEndpoints:
    """Tests for /chat and /customer-chat routing"""

    @patch("ai_handler.handler.handle_chat")
    def test_internal_chat_endpoint(
        self, mock_handle_chat, api_gateway_event, lambda_context, dynamodb_tables
    ):
        """POST /chat should call handle_chat"""
        # Mock chatbot response
        mock_handle_chat.return_value = {
            "statusCode": 200,
            "body": json.dumps({"response": "Test response"}),
            "headers": {"Content-Type": "application/json"},
        }

        event = api_gateway_event(method="POST", path="/chat", body={"message": "Hello"})
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["response"] == "Test response"

        # Verify handle_chat was called with correct arguments
        mock_handle_chat.assert_called_once()
        call_args = mock_handle_chat.call_args
        assert call_args[0][0] == event  # First arg is event
        # Second arg is storage backend
        assert hasattr(call_args[0][1], "create")

    @patch("ai_handler.handler.handle_customer_chat")
    def test_customer_chat_endpoint(
        self, mock_handle_customer_chat, api_gateway_event, lambda_context, dynamodb_tables
    ):
        """POST /customer-chat should call handle_customer_chat"""
        # Mock chatbot response
        mock_handle_customer_chat.return_value = {
            "statusCode": 200,
            "body": json.dumps({"response": "Customer test response"}),
            "headers": {"Content-Type": "application/json"},
        }

        event = api_gateway_event(method="POST", path="/customer-chat", body={"message": "I need help"})
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["response"] == "Customer test response"

        # Verify handle_customer_chat was called
        mock_handle_customer_chat.assert_called_once()
        call_args = mock_handle_customer_chat.call_args
        assert call_args[0][0] == event
        assert hasattr(call_args[0][1], "create")

    def test_cors_preflight(self, api_gateway_event, lambda_context, dynamodb_tables):
        """OPTIONS requests should return 200 for CORS"""
        event = api_gateway_event(method="OPTIONS", path="/chat")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["message"] == "CORS preflight"

    def test_invalid_path_returns_404(self, api_gateway_event, lambda_context, dynamodb_tables):
        """Invalid paths should return 404"""
        event = api_gateway_event(method="POST", path="/invalid-path")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 404
        body = json.loads(response["body"])
        assert body["error"] == "not_found"

    def test_get_method_returns_404(self, api_gateway_event, lambda_context, dynamodb_tables):
        """GET method on chat endpoints should return 404"""
        event = api_gateway_event(method="GET", path="/chat")
        response = handler(event, lambda_context)

        assert response["statusCode"] == 404
        body = json.loads(response["body"])
        assert body["error"] == "not_found"
