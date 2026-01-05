"""
Shared business logic for domain operations across Lambda handlers.

This module contains cross-cutting business logic used by multiple handlers,
particularly customer upsert logic used when creating quotes, policies, and claims.
"""


def upsert_customer_for_quote(storage, body):
    """
    Extract customer data from quote body and upsert customer.

    Args:
        storage: DynamoDBBackend instance
        body: Quote request body containing customerName and customerEmail

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


def upsert_customer_for_policy(storage, body):
    """
    Extract customer data from policy body and upsert customer.

    Args:
        storage: DynamoDBBackend instance
        body: Policy request body containing either:
              - holderName and holderEmail/customer_email (flat structure)
              - customer object (nested structure with email field)

    Returns:
        str: Customer ID if customer data provided, None otherwise

    Side effects:
        - Modifies body dict by removing holderName, holderEmail, customer_email, or customer
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
    holder_name = body.get("holderName")
    holder_email = body.get("holderEmail") or body.get("customer_email")

    if holder_email:
        customer = storage.upsert_customer(holder_email, {
            "name": holder_name,
            "email": holder_email
        })
        # Remove duplicate fields from body
        body.pop("holderName", None)
        body.pop("holderEmail", None)
        body.pop("customer_email", None)
        return customer["id"]

    return None


def get_customer_id_from_policy(storage, policy_id):
    """
    Get customerId from a policy (used for claim creation).

    Args:
        storage: DynamoDBBackend instance
        policy_id: Policy ID to look up

    Returns:
        str: Customer ID if policy exists and has customerId, None otherwise
    """
    if not policy_id:
        return None

    policy = storage.get("policy", policy_id)
    if policy:
        return policy.get("customerId")

    return None
