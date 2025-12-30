"""
Customer CRUD operations for PostgreSQL.

Provides create, read, update, delete operations for customer records.
"""

import json
import uuid
from datetime import datetime
from .db import execute_query


def create_customer(data):
    """
    Create a new customer.

    Args:
        data (dict): Customer data with fields:
            - name (str, required): Customer name
            - email (str, required): Customer email (must be unique)
            - phone (str, optional): Customer phone number
            - address (str, optional): Street address
            - city (str, optional): City
            - state (str, optional): State
            - zip (str, optional): ZIP code
            - dateOfBirth (str, optional): Date of birth (YYYY-MM-DD format)
            - data (dict, optional): Additional JSON data

    Returns:
        dict: Created customer record with all fields, or None if creation failed

    Raises:
        psycopg2.IntegrityError: If email already exists
    """
    query = """
    INSERT INTO customers (id, name, email, phone, address, city, state, zip, date_of_birth, data)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id, created_at, updated_at, status, name, email, phone, address, city, state, zip, date_of_birth, data
    """

    customer_id = str(uuid.uuid4())
    params = (
        customer_id,
        data.get('name'),
        data.get('email'),
        data.get('phone'),
        data.get('address'),
        data.get('city'),
        data.get('state'),
        data.get('zip'),
        data.get('dateOfBirth'),  # Frontend sends as dateOfBirth
        json.dumps(data.get('data', {})) if isinstance(data.get('data'), dict) else '{}'
    )

    result = execute_query(query, params)
    return dict(result[0]) if result else None


def get_customer(customer_id):
    """
    Get customer by ID.

    Args:
        customer_id (str): UUID of the customer

    Returns:
        dict: Customer record, or None if not found
    """
    query = """
    SELECT id, created_at, updated_at, status, name, email, phone,
           address, city, state, zip, date_of_birth, data
    FROM customers
    WHERE id = %s
    """
    result = execute_query(query, (customer_id,))
    return dict(result[0]) if result else None


def list_customers(limit=100, offset=0):
    """
    List all customers with pagination.

    Args:
        limit (int): Maximum number of customers to return (default: 100)
        offset (int): Number of customers to skip (default: 0)

    Returns:
        list[dict]: List of customer records
    """
    query = """
    SELECT id, created_at, updated_at, status, name, email, phone,
           address, city, state, zip, date_of_birth, data
    FROM customers
    ORDER BY created_at DESC
    LIMIT %s OFFSET %s
    """
    result = execute_query(query, (limit, offset))
    return [dict(row) for row in result]


def update_customer(customer_id, data):
    """
    Update customer.

    Args:
        customer_id (str): UUID of the customer to update
        data (dict): Customer data to update (same fields as create_customer)

    Returns:
        dict: Updated customer record, or None if not found
    """
    query = """
    UPDATE customers
    SET name = %s, email = %s, phone = %s, address = %s, city = %s,
        state = %s, zip = %s, date_of_birth = %s, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s
    RETURNING id, created_at, updated_at, status, name, email, phone,
              address, city, state, zip, date_of_birth, data
    """
    params = (
        data.get('name'),
        data.get('email'),
        data.get('phone'),
        data.get('address'),
        data.get('city'),
        data.get('state'),
        data.get('zip'),
        data.get('dateOfBirth'),
        customer_id
    )
    result = execute_query(query, params)
    return dict(result[0]) if result else None


def delete_customer(customer_id):
    """
    Delete customer.

    Args:
        customer_id (str): UUID of the customer to delete

    Returns:
        bool: True if customer was deleted, False if not found
    """
    query = "DELETE FROM customers WHERE id = %s"
    rowcount = execute_query(query, (customer_id,), fetch=False)
    return rowcount > 0
