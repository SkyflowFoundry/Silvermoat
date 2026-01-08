"""
Shared business logic for fintech domain operations.

This module contains fintech-specific business logic used by Lambda handlers,
particularly customer upsert logic used when creating accounts and transactions.
"""


def upsert_customer_for_account(storage, body):
    """
    Extract customer data from account body and upsert customer.

    Args:
        storage: DynamoDBBackend instance
        body: Account request body containing customerName and customerEmail

    Returns:
        str: Customer ID if customer data provided, None otherwise

    Side effects:
        - Modifies body dict by removing customerName and customerEmail
        - Creates or updates customer record in DynamoDB
    """
    customer_name = body.get("customerName")
    customer_email = body.get("customerEmail")

    if customer_email:
        customer = storage.upsert_customer(customer_email, {
            "name": customer_name,
            "email": customer_email
        })
        # Remove duplicate fields from body
        body.pop("customerName", None)
        body.pop("customerEmail", None)
        return customer["id"]

    return None


def upsert_customer_for_transaction(storage, body):
    """
    Extract customer data from transaction body and upsert customer.

    Args:
        storage: DynamoDBBackend instance
        body: Transaction request body containing either:
              - customerName and customerEmail (flat structure)
              - customer object (nested structure with email field)

    Returns:
        str: Customer ID if customer data provided, None otherwise

    Side effects:
        - Modifies body dict by removing customerName, customerEmail, or customer
        - Creates or updates customer record in DynamoDB
    """
    # Try nested customer object first (test/API pattern)
    customer_obj = body.get("customer")
    if customer_obj:
        customer_email = customer_obj.get("email")
        if customer_email:
            customer = storage.upsert_customer(customer_email, customer_obj)
            # Remove customer object from body
            body.pop("customer", None)
            return customer["id"]

    # Fall back to flat fields (legacy pattern)
    customer_name = body.get("customerName")
    customer_email = body.get("customerEmail") or body.get("customer_email")

    if customer_email:
        customer = storage.upsert_customer(customer_email, {
            "name": customer_name,
            "email": customer_email
        })
        # Remove duplicate fields from body
        body.pop("customerName", None)
        body.pop("customerEmail", None)
        body.pop("customer_email", None)
        return customer["id"]

    return None


def get_customer_id_from_account(storage, account_id):
    """
    Get customerId from an account (used for transaction creation).

    Args:
        storage: DynamoDBBackend instance
        account_id: Account ID to look up

    Returns:
        str: Customer ID if account exists and has customerId, None otherwise
    """
    if not account_id:
        return None

    account = storage.get("account", account_id)
    if account:
        return account.get("customerId") or account.get("data", {}).get("customerId")

    return None
