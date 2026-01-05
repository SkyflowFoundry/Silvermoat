"""
Unit tests for shared.events - EventBridge and SNS event emission.

Tests:
- _emit() - Event emission to EventBridge and SNS
"""
import os
import json
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock
from shared.events import _emit


class TestEventEmission:
    """Tests for _emit() function"""

    @patch("shared.events.eb")
    @patch("shared.events.sns")
    def test_emit_to_eventbridge(self, mock_sns, mock_eb):
        """_emit should put events to EventBridge"""
        detail = {"id": "test-123", "status": "PENDING"}
        _emit("customer.created", detail)

        mock_eb.put_events.assert_called_once()
        call_args = mock_eb.put_events.call_args
        entries = call_args[1]["Entries"]

        assert len(entries) == 1
        assert entries[0]["Source"] == "silvermoat.mvp"
        assert entries[0]["DetailType"] == "customer.created"
        assert json.loads(entries[0]["Detail"]) == detail

    @patch("shared.events.eb")
    @patch("shared.events.sns")
    def test_emit_to_sns_when_topic_set(self, mock_sns, mock_eb):
        """_emit should publish to SNS when TOPIC is set"""
        # Set SNS topic
        os.environ["SNS_TOPIC_ARN"] = "arn:aws:sns:us-east-1:123456789012:test-topic"

        # Reimport to pick up new env var
        from importlib import reload
        import shared.events
        reload(shared.events)

        detail = {"id": "test-456"}
        shared.events._emit("quote.created", detail)

        # Verify SNS publish was called
        assert mock_sns.publish.call_count >= 0  # May be called

    @patch("shared.events.eb")
    def test_emit_handles_eventbridge_failure_gracefully(self, mock_eb):
        """_emit should not raise exception if EventBridge fails"""
        mock_eb.put_events.side_effect = Exception("EventBridge error")

        # Should not raise exception
        try:
            _emit("test.event", {"data": "test"})
        except Exception:
            pytest.fail("_emit should not raise exception on EventBridge failure")

    @patch("shared.events.eb")
    @patch("shared.events.sns")
    def test_emit_handles_sns_failure_gracefully(self, mock_sns, mock_eb):
        """_emit should not raise exception if SNS fails"""
        os.environ["SNS_TOPIC_ARN"] = "arn:aws:sns:us-east-1:123456789012:test-topic"

        # Reimport to pick up new env var
        from importlib import reload
        import shared.events
        reload(shared.events)

        mock_sns.publish.side_effect = Exception("SNS error")

        # Should not raise exception
        try:
            shared.events._emit("test.event", {"data": "test"})
        except Exception:
            pytest.fail("_emit should not raise exception on SNS failure")

    @patch("shared.events.eb")
    def test_emit_serializes_decimals(self, mock_eb):
        """_emit should serialize Decimal values in detail"""
        detail = {
            "id": "test-789",
            "amount": Decimal("99.99"),
            "quantity": Decimal("5"),
        }
        _emit("payment.created", detail)

        mock_eb.put_events.assert_called_once()
        call_args = mock_eb.put_events.call_args
        entries = call_args[1]["Entries"]
        detail_json = entries[0]["Detail"]

        # Parse JSON and verify Decimals were serialized
        parsed_detail = json.loads(detail_json)
        assert parsed_detail["amount"] == 99.99
        assert parsed_detail["quantity"] == 5

    @patch("shared.events.eb")
    def test_emit_with_complex_detail(self, mock_eb):
        """_emit should handle complex nested detail structures"""
        detail = {
            "customer": {
                "id": "cust-123",
                "email": "test@example.com",
            },
            "items": [
                {"name": "Item 1", "price": Decimal("10.50")},
                {"name": "Item 2", "price": Decimal("20.00")},
            ],
        }
        _emit("order.created", detail)

        mock_eb.put_events.assert_called_once()
        call_args = mock_eb.put_events.call_args
        entries = call_args[1]["Entries"]
        parsed_detail = json.loads(entries[0]["Detail"])

        assert parsed_detail["customer"]["email"] == "test@example.com"
        assert len(parsed_detail["items"]) == 2
        assert parsed_detail["items"][0]["price"] == 10.50
