"""
Unit tests for shared.storage.dynamodb - DynamoDB storage backend.

Tests:
- DynamoDBBackend class methods
- CRUD operations
- Query methods
- Customer upsert logic
"""
import pytest
from decimal import Decimal
from shared.storage import DynamoDBBackend


class TestDynamoDBBackendCreation:
    """Tests for DynamoDBBackend initialization and configuration"""

    def test_backend_initialization(self, dynamodb_tables):
        """DynamoDBBackend should initialize with all required tables"""
        backend = DynamoDBBackend()

        assert backend.tables is not None
        assert "customer" in backend.tables
        assert "quote" in backend.tables
        assert "policy" in backend.tables
        assert "claim" in backend.tables
        assert "payment" in backend.tables
        assert "case" in backend.tables

    def test_get_table_valid_domain(self, storage_backend):
        """_get_table should return table for valid domain"""
        table = storage_backend._get_table("customer")
        assert table is not None

    def test_get_table_invalid_domain_raises_error(self, storage_backend):
        """_get_table should raise ValueError for invalid domain"""
        with pytest.raises(ValueError, match="Unknown domain"):
            storage_backend._get_table("invalid_domain")


class TestCreateOperations:
    """Tests for create() method"""

    def test_create_item_basic(self, storage_backend):
        """Should create item with generated ID and timestamp"""
        data = {"name": "Test Customer", "email": "test@example.com"}
        item = storage_backend.create("customer", data, "ACTIVE")

        assert "id" in item
        assert item["id"] is not None
        assert "createdAt" in item
        assert item["status"] == "ACTIVE"
        assert item["data"] == data

    def test_create_item_converts_floats_to_decimal(self, storage_backend):
        """Should convert floats to Decimal for DynamoDB compatibility"""
        data = {"amount": 99.99, "quantity": 5}
        item = storage_backend.create("payment", data, "PENDING")

        # Data should have Decimals
        assert isinstance(item["data"]["amount"], Decimal)
        assert item["data"]["amount"] == Decimal("99.99")

    def test_create_item_with_top_level_fields(self, storage_backend):
        """Should add top-level fields for GSI indexing"""
        data = {"policyNumber": "POL-123"}
        top_level = {"customerId": "cust-456"}
        item = storage_backend.create("policy", data, "ACTIVE", top_level)

        # Top-level field should be present
        assert item.get("customerId") == "cust-456"


class TestReadOperations:
    """Tests for get() and list() methods"""

    def test_get_item_by_id(self, storage_backend):
        """Should retrieve item by ID"""
        # Create item
        created = storage_backend.create("customer", {"name": "John"}, "ACTIVE")
        item_id = created["id"]

        # Get item
        retrieved = storage_backend.get("customer", item_id)

        assert retrieved is not None
        assert retrieved["id"] == item_id
        assert retrieved["data"]["name"] == "John"

    def test_get_nonexistent_item_returns_none(self, storage_backend):
        """Should return None for non-existent ID"""
        item = storage_backend.get("customer", "nonexistent-id")
        assert item is None

    def test_list_items(self, storage_backend):
        """Should list all items in domain"""
        # Create multiple items
        storage_backend.create("customer", {"name": "Customer 1"}, "ACTIVE")
        storage_backend.create("customer", {"name": "Customer 2"}, "ACTIVE")

        items = storage_backend.list("customer")

        assert len(items) >= 2

    def test_list_items_sorted_by_created_at_descending(self, storage_backend):
        """Should return items sorted by createdAt descending (most recent first)"""
        import time

        # Create items with longer delay to ensure different timestamps
        item1 = storage_backend.create("customer", {"name": "First"}, "ACTIVE")
        time.sleep(1)
        item2 = storage_backend.create("customer", {"name": "Second"}, "ACTIVE")

        items = storage_backend.list("customer")

        # Most recent should be first
        assert items[0]["id"] == item2["id"]
        assert items[1]["id"] == item1["id"]

    def test_list_empty_domain(self, storage_backend):
        """Should return empty list for domain with no items"""
        items = storage_backend.list("case")
        assert items == []


class TestUpdateOperations:
    """Tests for update_status() method"""

    def test_update_status(self, storage_backend):
        """Should update item status"""
        # Create item
        item = storage_backend.create("claim", {"claimNumber": "CLM-123"}, "PENDING")
        item_id = item["id"]

        # Update status
        result = storage_backend.update_status("claim", item_id, "APPROVED")

        assert result is True

        # Verify status was updated
        updated_item = storage_backend.get("claim", item_id)
        assert updated_item["status"] == "APPROVED"
        assert "updatedAt" in updated_item


class TestDeleteOperations:
    """Tests for delete() and delete_all() methods"""

    def test_delete_item(self, storage_backend):
        """Should delete single item"""
        # Create item
        item = storage_backend.create("customer", {"name": "To Delete"}, "ACTIVE")
        item_id = item["id"]

        # Delete item
        result = storage_backend.delete("customer", item_id)

        assert result is True

        # Verify item is deleted
        deleted_item = storage_backend.get("customer", item_id)
        assert deleted_item is None

    def test_delete_all_items(self, storage_backend):
        """Should delete all items in domain"""
        # Create multiple items
        storage_backend.create("payment", {"amount": 100}, "PENDING")
        storage_backend.create("payment", {"amount": 200}, "PENDING")
        storage_backend.create("payment", {"amount": 300}, "PENDING")

        # Delete all
        deleted_count = storage_backend.delete_all("payment")

        assert deleted_count == 3

        # Verify all items deleted
        items = storage_backend.list("payment")
        assert len(items) == 0


class TestScanOperations:
    """Tests for scan() method"""

    def test_scan_items(self, storage_backend):
        """Should scan and return all items"""
        # Create items
        storage_backend.create("case", {"subject": "Case 1"}, "OPEN")
        storage_backend.create("case", {"subject": "Case 2"}, "OPEN")

        items = storage_backend.scan("case")

        assert len(items) >= 2


class TestQueryOperations:
    """Tests for query_by_email() and query_by_customer_id()"""

    def test_query_by_email(self, storage_backend):
        """Should query customers by email using GSI"""
        # Create customer
        customer = storage_backend.upsert_customer("john@example.com", {"name": "John"})

        # Query by email
        results = storage_backend.query_by_email("customer", "john@example.com")

        assert len(results) == 1
        assert results[0]["id"] == customer["id"]
        assert results[0]["email"] == "john@example.com"

    def test_query_by_email_nonexistent(self, storage_backend):
        """Should return empty list for non-existent email"""
        results = storage_backend.query_by_email("customer", "nonexistent@example.com")

        assert results == []

    def test_query_by_customer_id(self, storage_backend):
        """Should query items by customerId using GSI"""
        # Create customer
        customer = storage_backend.upsert_customer("jane@example.com", {"name": "Jane"})
        customer_id = customer["id"]

        # Create policy for customer
        policy = storage_backend.create(
            "policy", {"policyNumber": "POL-123"}, "ACTIVE", {"customerId": customer_id}
        )

        # Query policies by customerId
        results = storage_backend.query_by_customer_id("policy", customer_id)

        assert len(results) >= 1
        assert any(p["id"] == policy["id"] for p in results)

    def test_query_by_customer_id_nonexistent(self, storage_backend):
        """Should return empty list for non-existent customerId"""
        results = storage_backend.query_by_customer_id("quote", "nonexistent-customer-id")

        assert results == []


class TestCustomerUpsert:
    """Tests for upsert_customer() method"""

    def test_upsert_customer_creates_new(self, storage_backend):
        """Should create new customer if email doesn't exist"""
        customer = storage_backend.upsert_customer("new@example.com", {"name": "New Customer"})

        assert "id" in customer
        assert customer["email"] == "new@example.com"
        assert customer["status"] == "ACTIVE"
        assert customer["data"]["name"] == "New Customer"

    def test_upsert_customer_returns_existing(self, storage_backend):
        """Should return existing customer if email exists"""
        # Create customer
        first_customer = storage_backend.upsert_customer("existing@example.com", {"name": "First"})
        first_id = first_customer["id"]

        # Try to upsert again
        second_customer = storage_backend.upsert_customer("existing@example.com", {"name": "Second"})

        # Should return same customer ID
        assert second_customer["id"] == first_id

    def test_upsert_customer_removes_email_from_data(self, storage_backend):
        """Should remove email from data dict (email is top-level)"""
        data = {"email": "test@example.com", "name": "Test"}
        customer = storage_backend.upsert_customer("test@example.com", data)

        # Email should be top-level, not in data
        assert customer["email"] == "test@example.com"
        # Name should be in data
        assert customer["data"]["name"] == "Test"
        # Email should NOT be duplicated in data
        assert "email" not in customer["data"]

    def test_upsert_customer_converts_floats(self, storage_backend):
        """Should convert floats in customer data to Decimal"""
        data = {"name": "Test", "balance": 1234.56}
        customer = storage_backend.upsert_customer("test@example.com", data)

        assert isinstance(customer["data"]["balance"], Decimal)
