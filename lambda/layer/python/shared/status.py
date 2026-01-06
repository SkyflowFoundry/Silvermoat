"""Status message tracking for chatbot operations"""
import time
from typing import List, Dict, Any, Optional
from contextlib import contextmanager


class StatusTracker:
    """Tracks status messages during chatbot operations"""

    def __init__(self):
        self.messages: List[Dict[str, Any]] = []
        self._callback = None  # Optional streaming callback

    def set_callback(self, callback):
        """
        Set callback for real-time status streaming.

        Args:
            callback: Function to call with (operation, message, metadata) when status added
        """
        self._callback = callback

    def add(self, operation: str, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a status message"""
        status_msg = {
            "timestamp": int(time.time() * 1000),  # milliseconds
            "operation": operation,
            "message": message
        }
        if metadata:
            status_msg["metadata"] = metadata
        self.messages.append(status_msg)

        # Call streaming callback if set
        if self._callback:
            try:
                self._callback(operation, message, metadata)
            except Exception as e:
                # Don't let callback errors break status tracking
                print(f"Warning: Status callback failed: {e}")

    @contextmanager
    def track_operation(self, operation: str, start_message: str, metadata: Optional[Dict[str, Any]] = None):
        """Context manager to track operation with timing"""
        start_time = time.time()
        self.add(operation, start_message, metadata)

        try:
            yield self
        finally:
            elapsed_ms = int((time.time() - start_time) * 1000)
            # Update metadata with latency
            if metadata is None:
                metadata = {}
            metadata["latency_ms"] = elapsed_ms

    def get_messages(self) -> List[Dict[str, Any]]:
        """Get all status messages"""
        return self.messages.copy()

    def clear(self):
        """Clear all messages"""
        self.messages.clear()
