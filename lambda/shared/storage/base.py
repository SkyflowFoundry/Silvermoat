"""Abstract base class for storage backends"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any


class StorageBackend(ABC):
    """Abstract interface for data persistence layer"""

    @abstractmethod
    def create(self, domain: str, data: dict, status: str) -> dict:
        """Create a new item in the specified domain

        Args:
            domain: Entity type (quote, policy, claim, payment, case)
            data: Item data to store
            status: Initial status for the item

        Returns:
            Complete item with id, createdAt, data, and status
        """
        pass

    @abstractmethod
    def get(self, domain: str, item_id: str) -> dict:
        """Retrieve an item by ID

        Args:
            domain: Entity type
            item_id: Unique identifier

        Returns:
            Item dict or None if not found
        """
        pass

    @abstractmethod
    def list(self, domain: str) -> List[dict]:
        """List all items in a domain

        Args:
            domain: Entity type

        Returns:
            List of items, sorted by createdAt descending
        """
        pass

    @abstractmethod
    def update_status(self, domain: str, item_id: str, status: str) -> bool:
        """Update the status of an item

        Args:
            domain: Entity type
            item_id: Unique identifier
            status: New status value

        Returns:
            True if successful
        """
        pass

    @abstractmethod
    def delete(self, domain: str, item_id: str) -> bool:
        """Delete a single item

        Args:
            domain: Entity type
            item_id: Unique identifier

        Returns:
            True if successful
        """
        pass

    @abstractmethod
    def delete_all(self, domain: str) -> int:
        """Delete all items in a domain

        Args:
            domain: Entity type

        Returns:
            Number of items deleted
        """
        pass

    @abstractmethod
    def scan(self, domain: str) -> List[dict]:
        """Scan all items (for search operations)

        Args:
            domain: Entity type

        Returns:
            List of all items (unsorted)
        """
        pass
