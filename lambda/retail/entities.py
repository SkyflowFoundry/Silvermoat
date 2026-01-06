"""
Retail business logic for domain operations.

Handles customer upsert logic for products, orders, and inventory management.
"""


def upsert_customer_for_order(storage, body):
    """
    Extract customer data from order body and upsert customer.

    Args:
        storage: DynamoDBBackend instance
        body: Order request body containing customerEmail and optional customer data

    Returns:
        str: Customer ID if customer data provided, None otherwise

    Side effects:
        - Modifies body dict by removing customer-related fields
        - Creates or updates customer record in DynamoDB
    """
    customer_email = body.get("customerEmail")

    if customer_email:
        # Check if there's additional customer data
        customer_name = body.get("customerName")
        customer_phone = body.get("customerPhone")
        customer_address = body.get("customerAddress")

        customer_data = {"email": customer_email}
        if customer_name:
            customer_data["name"] = customer_name
        if customer_phone:
            customer_data["phone"] = customer_phone
        if customer_address:
            customer_data["address"] = customer_address

        customer = storage.upsert_customer(customer_email, customer_data)

        # Remove duplicate fields from body
        body.pop("customerEmail", None)
        body.pop("customerName", None)
        body.pop("customerPhone", None)
        body.pop("customerAddress", None)

        return customer["id"]

    return None


def calculate_order_total(items):
    """
    Calculate total amount for order items.

    Args:
        items: List of order items with quantity and price

    Returns:
        float: Total order amount
    """
    total = 0.0
    for item in items:
        quantity = item.get("quantity", 1)
        price = item.get("price", 0.0)
        total += quantity * price
    return total
