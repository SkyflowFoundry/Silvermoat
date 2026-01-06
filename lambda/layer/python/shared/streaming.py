"""
Streaming utility functions for Lambda response streaming.

Provides NDJSON (newline-delimited JSON) chunk writers for streaming
status messages and responses in real-time.
"""

import json
from typing import Any, Dict, IO


def write_chunk(stream: IO, chunk_type: str, data: Dict[str, Any]) -> None:
    """
    Write a JSON chunk to the response stream in NDJSON format.

    Args:
        stream: Output stream to write to (typically Lambda response stream)
        chunk_type: Type of chunk ("status", "response", "error")
        data: Chunk data to serialize

    Format:
        {"type": "status|response|error", "data": {...}}\n
    """
    try:
        chunk = {"type": chunk_type, "data": data}
        json.dump(chunk, stream)
        stream.write("\n")
        stream.flush()
    except Exception as e:
        # If writing fails, try to write error chunk
        try:
            error_chunk = {
                "type": "error",
                "data": {"error": "stream_write_failed", "message": str(e)},
            }
            json.dump(error_chunk, stream)
            stream.write("\n")
            stream.flush()
        except:
            # If even error writing fails, give up silently
            pass


def write_status_chunk(
    stream: IO, operation: str, message: str, metadata: Dict[str, Any] = None
) -> None:
    """
    Write a status message chunk to the stream.

    Args:
        stream: Output stream
        operation: Operation category (e.g., "ai_processing", "dynamodb_query")
        message: Human-readable status message
        metadata: Optional additional context
    """
    import time

    data = {
        "timestamp": int(time.time() * 1000),
        "operation": operation,
        "message": message,
    }
    if metadata:
        data["metadata"] = metadata

    write_chunk(stream, "status", data)


def write_response_chunk(
    stream: IO, response: str, conversation: list, usage: Dict[str, Any] = None
) -> None:
    """
    Write the final response chunk to the stream.

    Args:
        stream: Output stream
        response: AI assistant response text
        conversation: Full conversation history
        usage: Optional token usage stats
    """
    data = {"response": response, "conversation": conversation}
    if usage:
        data["usage"] = usage

    write_chunk(stream, "response", data)


def write_error_chunk(stream: IO, error: str, message: str) -> None:
    """
    Write an error chunk to the stream.

    Args:
        stream: Output stream
        error: Error code (e.g., "invalid_request", "internal_error")
        message: Human-readable error message
    """
    data = {"error": error, "message": message}
    write_chunk(stream, "error", data)
