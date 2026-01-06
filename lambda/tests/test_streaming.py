"""
Unit tests for streaming utilities and StatusTracker callback functionality.

Tests:
- StatusTracker callback invocation
- NDJSON chunk writing (write_chunk, write_status_chunk, etc.)
- Error handling in streaming functions
"""
import json
import time
import pytest
from io import StringIO
from unittest.mock import MagicMock, patch
from shared.status import StatusTracker
from shared.streaming import (
    write_chunk,
    write_status_chunk,
    write_response_chunk,
    write_error_chunk,
)


class TestStatusTrackerCallback:
    """Tests for StatusTracker streaming callback functionality"""

    def test_callback_is_invoked_on_add(self):
        """Callback should be called immediately when status is added"""
        tracker = StatusTracker()
        callback = MagicMock()
        tracker.set_callback(callback)

        tracker.add("test_operation", "Test message", {"key": "value"})

        callback.assert_called_once_with("test_operation", "Test message", {"key": "value"})

    def test_callback_with_no_metadata(self):
        """Callback should work with None metadata"""
        tracker = StatusTracker()
        callback = MagicMock()
        tracker.set_callback(callback)

        tracker.add("test_operation", "Test message")

        callback.assert_called_once_with("test_operation", "Test message", None)

    def test_multiple_callbacks(self):
        """Callback should be invoked for each add() call"""
        tracker = StatusTracker()
        callback = MagicMock()
        tracker.set_callback(callback)

        tracker.add("op1", "Message 1")
        tracker.add("op2", "Message 2")
        tracker.add("op3", "Message 3")

        assert callback.call_count == 3
        assert callback.call_args_list[0][0] == ("op1", "Message 1", None)
        assert callback.call_args_list[1][0] == ("op2", "Message 2", None)
        assert callback.call_args_list[2][0] == ("op3", "Message 3", None)

    def test_callback_error_does_not_break_tracking(self):
        """Callback errors should not prevent status from being tracked"""
        tracker = StatusTracker()
        callback = MagicMock(side_effect=Exception("Callback failed"))
        tracker.set_callback(callback)

        # Should not raise exception
        tracker.add("test_operation", "Test message")

        # Status should still be tracked
        assert len(tracker.messages) == 1
        assert tracker.messages[0]["operation"] == "test_operation"
        assert tracker.messages[0]["message"] == "Test message"

    def test_no_callback_set(self):
        """Should work normally when no callback is set"""
        tracker = StatusTracker()

        # Should not raise exception
        tracker.add("test_operation", "Test message")

        assert len(tracker.messages) == 1
        assert tracker.messages[0]["operation"] == "test_operation"


class TestNDJSONChunkWriting:
    """Tests for NDJSON chunk writing functions"""

    def test_write_chunk_basic_format(self):
        """write_chunk should produce valid NDJSON format"""
        stream = StringIO()
        data = {"key": "value", "number": 123}

        write_chunk(stream, "status", data)

        output = stream.getvalue()
        assert output.endswith("\n")

        # Parse and verify structure
        chunk = json.loads(output.strip())
        assert chunk["type"] == "status"
        assert chunk["data"] == data

    def test_write_status_chunk(self):
        """write_status_chunk should include timestamp, operation, message, metadata"""
        stream = StringIO()
        metadata = {"user": "test@example.com"}

        with patch("time.time", return_value=1234567890.123):
            write_status_chunk(stream, "ai_processing", "Processing request", metadata)

        output = stream.getvalue()
        chunk = json.loads(output.strip())

        assert chunk["type"] == "status"
        assert chunk["data"]["timestamp"] == 1234567890123  # milliseconds
        assert chunk["data"]["operation"] == "ai_processing"
        assert chunk["data"]["message"] == "Processing request"
        assert chunk["data"]["metadata"] == metadata

    def test_write_status_chunk_no_metadata(self):
        """write_status_chunk should work without metadata"""
        stream = StringIO()

        write_status_chunk(stream, "database_query", "Querying database")

        output = stream.getvalue()
        chunk = json.loads(output.strip())

        assert chunk["type"] == "status"
        assert chunk["data"]["operation"] == "database_query"
        assert chunk["data"]["message"] == "Querying database"
        assert "metadata" not in chunk["data"]

    def test_write_response_chunk(self):
        """write_response_chunk should include response, conversation, and usage"""
        stream = StringIO()
        conversation = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
        usage = {"input_tokens": 10, "output_tokens": 5}

        write_response_chunk(stream, "Hi there!", conversation, usage)

        output = stream.getvalue()
        chunk = json.loads(output.strip())

        assert chunk["type"] == "response"
        assert chunk["data"]["response"] == "Hi there!"
        assert chunk["data"]["conversation"] == conversation
        assert chunk["data"]["usage"] == usage

    def test_write_response_chunk_no_usage(self):
        """write_response_chunk should work without usage stats"""
        stream = StringIO()
        conversation = [{"role": "user", "content": "Test"}]

        write_response_chunk(stream, "Response text", conversation)

        output = stream.getvalue()
        chunk = json.loads(output.strip())

        assert chunk["type"] == "response"
        assert chunk["data"]["response"] == "Response text"
        assert chunk["data"]["conversation"] == conversation
        assert "usage" not in chunk["data"]

    def test_write_error_chunk(self):
        """write_error_chunk should include error code and message"""
        stream = StringIO()

        write_error_chunk(stream, "invalid_request", "Missing required field: email")

        output = stream.getvalue()
        chunk = json.loads(output.strip())

        assert chunk["type"] == "error"
        assert chunk["data"]["error"] == "invalid_request"
        assert chunk["data"]["message"] == "Missing required field: email"

    def test_write_chunk_error_handling(self):
        """write_chunk should write error chunk if original write fails"""
        # Create a mock stream that fails on first write
        stream = StringIO()
        original_write = stream.write
        write_count = [0]

        def failing_write(data):
            write_count[0] += 1
            if write_count[0] == 1:
                raise Exception("Write failed")
            return original_write(data)

        stream.write = failing_write

        # Should not raise exception
        write_chunk(stream, "status", {"test": "data"})

        # Should have written error chunk instead
        output = stream.getvalue()
        chunk = json.loads(output.strip())
        assert chunk["type"] == "error"
        assert chunk["data"]["error"] == "stream_write_failed"

    def test_multiple_chunks_ndjson_format(self):
        """Multiple chunks should produce multiple NDJSON lines"""
        stream = StringIO()

        write_status_chunk(stream, "op1", "Message 1")
        write_status_chunk(stream, "op2", "Message 2")
        write_response_chunk(stream, "Final response", [])

        output = stream.getvalue()
        lines = output.strip().split("\n")

        assert len(lines) == 3

        # Each line should be valid JSON
        chunk1 = json.loads(lines[0])
        chunk2 = json.loads(lines[1])
        chunk3 = json.loads(lines[2])

        assert chunk1["type"] == "status"
        assert chunk2["type"] == "status"
        assert chunk3["type"] == "response"


class TestIntegration:
    """Integration tests for StatusTracker + streaming"""

    def test_status_tracker_with_streaming_callback(self):
        """StatusTracker callback should write to stream in real-time"""
        tracker = StatusTracker()
        stream = StringIO()

        # Set up callback to write to stream
        def stream_callback(operation, message, metadata):
            write_status_chunk(stream, operation, message, metadata)

        tracker.set_callback(stream_callback)

        # Add status messages
        tracker.add("step1", "Starting process")
        tracker.add("step2", "Processing data", {"count": 10})
        tracker.add("step3", "Completing")

        # Verify stream contains all status chunks
        output = stream.getvalue()
        lines = output.strip().split("\n")
        assert len(lines) == 3

        chunks = [json.loads(line) for line in lines]
        assert all(chunk["type"] == "status" for chunk in chunks)
        assert chunks[0]["data"]["operation"] == "step1"
        assert chunks[1]["data"]["operation"] == "step2"
        assert chunks[1]["data"]["metadata"] == {"count": 10}
        assert chunks[2]["data"]["operation"] == "step3"

    def test_full_streaming_workflow(self):
        """Test complete streaming workflow: status + response"""
        stream = StringIO()

        # Simulate chatbot processing with status messages
        write_status_chunk(stream, "ai_start", "Starting AI processing")
        write_status_chunk(stream, "database_query", "Fetching customer data")
        write_status_chunk(stream, "bedrock_invoke", "Invoking Bedrock API")

        # Final response
        conversation = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi! How can I help?"},
        ]
        write_response_chunk(stream, "Hi! How can I help?", conversation)

        # Verify complete NDJSON output
        output = stream.getvalue()
        lines = output.strip().split("\n")
        assert len(lines) == 4

        # Verify types
        chunks = [json.loads(line) for line in lines]
        assert chunks[0]["type"] == "status"
        assert chunks[1]["type"] == "status"
        assert chunks[2]["type"] == "status"
        assert chunks[3]["type"] == "response"

        # Verify final response
        assert chunks[3]["data"]["response"] == "Hi! How can I help?"
        assert len(chunks[3]["data"]["conversation"]) == 2
