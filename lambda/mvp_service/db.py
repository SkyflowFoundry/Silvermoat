"""
Database connection module for PostgreSQL Aurora.

Provides connection management, query execution, and schema initialization.
"""

import os
import json
import boto3
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

# Cache secret and connection parameters
_secret_cache = None
_conn_params = None


def get_db_credentials():
    """
    Fetch database credentials from Secrets Manager (cached).

    Returns:
        dict: Database credentials with 'username' and 'password' keys
    """
    global _secret_cache
    if _secret_cache is not None:
        return _secret_cache

    secret_arn = os.environ.get('DB_SECRET_ARN')
    if not secret_arn:
        raise ValueError("DB_SECRET_ARN environment variable not set")

    sm = boto3.client('secretsmanager')
    response = sm.get_secret_value(SecretId=secret_arn)
    secret = json.loads(response['SecretString'])

    _secret_cache = secret
    return secret


def get_connection_params():
    """
    Get PostgreSQL connection parameters (cached).

    Returns:
        dict: Connection parameters for psycopg2.connect()
    """
    global _conn_params
    if _conn_params is not None:
        return _conn_params

    creds = get_db_credentials()
    _conn_params = {
        'host': os.environ.get('DB_CLUSTER_ENDPOINT'),
        'port': 5432,
        'database': os.environ.get('DB_NAME', 'silvermoat'),
        'user': creds['username'],
        'password': creds['password'],
        'connect_timeout': 5,
    }
    return _conn_params


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.

    Automatically commits on success and rolls back on error.

    Usage:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM customers")
    """
    conn = psycopg2.connect(**get_connection_params())
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_query(query, params=None, fetch=True):
    """
    Execute a query and return results.

    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters for parameterized queries
        fetch (bool): If True, fetch and return results. If False, return row count.

    Returns:
        list[dict] | int: List of result rows as dicts (if fetch=True) or row count (if fetch=False)
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            return cursor.rowcount


def initialize_schema():
    """
    Create customers table if not exists (run on Lambda cold start).

    This function is idempotent and safe to call multiple times.
    """
    schema = """
    CREATE TABLE IF NOT EXISTS customers (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(50) DEFAULT 'ACTIVE',
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(50),
        address TEXT,
        city VARCHAR(100),
        state VARCHAR(50),
        zip VARCHAR(20),
        date_of_birth DATE,
        data JSONB DEFAULT '{}'
    );

    CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
    CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(status);
    """

    execute_query(schema, fetch=False)
