#!/usr/bin/env python3
"""
Clear all demo data from API.

Deletes all records from all resource types to ensure clean slate for seeding.
"""

import os
import sys
import requests

API_BASE_URL = os.environ.get('API_BASE_URL', '').rstrip('/')

if not API_BASE_URL:
    print("Error: API_BASE_URL environment variable not set", file=sys.stderr)
    sys.exit(1)

RESOURCE_TYPES = ['customer', 'quote', 'policy', 'claim', 'payment', 'case']

def clear_resource(resource_type):
    """Delete all records of a given resource type."""
    try:
        response = requests.delete(f"{API_BASE_URL}/{resource_type}", timeout=30)
        response.raise_for_status()

        result = response.json()
        deleted_count = result.get('deletedCount', 0)
        print(f"✓ Cleared {deleted_count} {resource_type}(s)")
        return deleted_count
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to clear {resource_type}s: {e}", file=sys.stderr)
        return 0

def main():
    """Clear all demo data from API."""
    print("Clearing all demo data...")
    print(f"API Base URL: {API_BASE_URL}\n")

    total_deleted = 0

    for resource_type in RESOURCE_TYPES:
        deleted = clear_resource(resource_type)
        total_deleted += deleted

    print(f"\n✓ Data clearing complete: {total_deleted} records deleted")

    if total_deleted == 0:
        print("ℹ️  No records found (database was already empty)")

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n✗ Data clearing failed: {e}", file=sys.stderr)
        sys.exit(1)
