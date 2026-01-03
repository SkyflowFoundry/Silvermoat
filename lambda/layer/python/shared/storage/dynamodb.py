"""DynamoDB implementation of storage backend"""
import os
import time
import uuid
import boto3
from .base import StorageBackend
from ..validators import convert_floats_to_decimal


class DynamoDBBackend(StorageBackend):
    """Storage backend using DynamoDB"""

    def __init__(self):
        self.ddb = boto3.resource("dynamodb")
        self.tables = {
            "customer": self.ddb.Table(os.environ["CUSTOMERS_TABLE"]),
            "quote": self.ddb.Table(os.environ["QUOTES_TABLE"]),
            "policy": self.ddb.Table(os.environ["POLICIES_TABLE"]),
            "claim": self.ddb.Table(os.environ["CLAIMS_TABLE"]),
            "payment": self.ddb.Table(os.environ["PAYMENTS_TABLE"]),
            "case": self.ddb.Table(os.environ["CASES_TABLE"]),
        }

    def _get_table(self, domain: str):
        """Get table for domain, raise error if invalid"""
        if domain not in self.tables:
            raise ValueError(f"Unknown domain: {domain}")
        return self.tables[domain]

    def create(self, domain: str, data: dict, status: str, top_level_fields: dict = None) -> dict:
        """Create a new item with optional top-level fields for GSI indexing"""
        table = self._get_table(domain)
        item_id = str(uuid.uuid4())

        # Convert floats to Decimal for DynamoDB compatibility
        clean_data = convert_floats_to_decimal(data)

        item = {
            "id": item_id,
            "createdAt": int(time.time()),
            "data": clean_data,
            "status": status
        }

        # Add top-level fields for GSI indexing (e.g., customerId)
        if top_level_fields:
            item.update(top_level_fields)

        print(f"Creating {domain} with id={item_id}, status={status}")
        table.put_item(Item=item)
        return item

    def get(self, domain: str, item_id: str) -> dict:
        """Retrieve an item by ID"""
        table = self._get_table(domain)
        response = table.get_item(Key={"id": item_id})
        return response.get("Item")

    def list(self, domain: str) -> list:
        """List all items, sorted by createdAt descending"""
        table = self._get_table(domain)
        response = table.scan()
        items = response.get("Items", [])
        # Sort by createdAt descending (most recent first)
        items.sort(key=lambda x: x.get("createdAt", 0), reverse=True)
        return items

    def update_status(self, domain: str, item_id: str, status: str) -> bool:
        """Update item status"""
        table = self._get_table(domain)
        table.update_item(
            Key={"id": item_id},
            UpdateExpression="SET #s = :s, updatedAt = :u",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":s": status, ":u": int(time.time())},
        )
        return True

    def delete(self, domain: str, item_id: str) -> bool:
        """Delete a single item"""
        table = self._get_table(domain)
        table.delete_item(Key={"id": item_id})
        return True

    def delete_all(self, domain: str) -> int:
        """Delete all items in domain"""
        table = self._get_table(domain)
        response = table.scan()
        items = response.get("Items", [])
        deleted_count = 0
        for item in items:
            table.delete_item(Key={"id": item["id"]})
            deleted_count += 1
        return deleted_count

    def scan(self, domain: str) -> list:
        """Scan all items (for search operations)"""
        table = self._get_table(domain)
        response = table.scan()
        return response.get("Items", [])

    def query_by_email(self, domain: str, email: str) -> list:
        """Query customer by email using GSI"""
        table = self._get_table(domain)
        response = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression="email = :email",
            ExpressionAttributeValues={":email": email}
        )
        return response.get("Items", [])

    def query_by_customer_id(self, domain: str, customer_id: str) -> list:
        """Query policies/claims by customerId using GSI"""
        table = self._get_table(domain)
        response = table.query(
            IndexName="CustomerIdIndex",
            KeyConditionExpression="customerId = :customerId",
            ExpressionAttributeValues={":customerId": customer_id}
        )
        return response.get("Items", [])

    def upsert_customer(self, email: str, data: dict) -> dict:
        """Create customer if not exists by email, else return existing"""
        # Check if customer exists
        existing = self.query_by_email("customer", email)
        if existing:
            return existing[0]

        # Create new customer with email at top level for GSI
        customer_data = dict(data)
        email_value = customer_data.pop("email", email)

        table = self._get_table("customer")
        item_id = str(uuid.uuid4())

        clean_data = convert_floats_to_decimal(customer_data)

        item = {
            "id": item_id,
            "email": email_value,
            "createdAt": int(time.time()),
            "data": clean_data,
            "status": "ACTIVE"
        }

        print(f"Creating customer with id={item_id}, email={email_value}")
        table.put_item(Item=item)
        return item
