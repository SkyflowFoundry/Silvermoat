"""
Test data generation utilities.
Maintains parity with seed data from CloudFormation Custom Resource.
"""
import uuid
from datetime import datetime, timedelta
from decimal import Decimal


def generate_quote_id():
    """Generate a unique quote ID."""
    return f"quote-{uuid.uuid4().hex[:12]}"


def generate_policy_id():
    """Generate a unique policy ID."""
    return f"pol-{uuid.uuid4().hex[:12]}"


def generate_claim_id():
    """Generate a unique claim ID."""
    return f"claim-{uuid.uuid4().hex[:12]}"


def generate_payment_id():
    """Generate a unique payment ID."""
    return f"pay-{uuid.uuid4().hex[:12]}"


def generate_case_id():
    """Generate a unique case ID."""
    return f"case-{uuid.uuid4().hex[:12]}"


def generate_policy_number():
    """Generate a policy number similar to seed data."""
    return f"POL-{uuid.uuid4().hex[:8].upper()}"


def generate_claim_number():
    """Generate a claim number similar to seed data."""
    return f"CLM-{uuid.uuid4().hex[:8].upper()}"


def create_test_quote(customer_name="Test Customer", coverage_type="auto"):
    """
    Create a test quote matching seed data format.

    Args:
        customer_name: Customer name
        coverage_type: Coverage type (auto, home, life, health)

    Returns:
        dict: Quote data ready for DynamoDB
    """
    coverage_amounts = {
        "auto": 100000,
        "home": 250000,
        "life": 500000,
        "health": 50000,
    }

    premium_cents = {
        "auto": 50000,  # $500/year
        "home": 125000,  # $1250/year
        "life": 75000,   # $750/year
        "health": 40000,  # $400/year
    }

    quote_id = generate_quote_id()
    timestamp = datetime.utcnow().isoformat()

    return {
        "id": quote_id,
        "customer_name": customer_name,
        "customer_email": f"{customer_name.lower().replace(' ', '.')}@example.com",
        "coverage_type": coverage_type,
        "coverage_amount": coverage_amounts.get(coverage_type, 100000),
        "annual_premium_cents": premium_cents.get(coverage_type, 50000),
        "created_at": timestamp,
        "status": "pending",
    }


def create_test_policy(customer_name="Test Customer", coverage_type="auto", status="active"):
    """
    Create a test policy matching seed data format.

    Args:
        customer_name: Customer name
        coverage_type: Coverage type
        status: Policy status (active, expired, cancelled)

    Returns:
        dict: Policy data ready for DynamoDB
    """
    policy_id = generate_policy_id()
    policy_number = generate_policy_number()
    timestamp = datetime.utcnow().isoformat()

    coverage_amounts = {
        "auto": 100000,
        "home": 250000,
        "life": 500000,
        "health": 50000,
    }

    premium_cents = {
        "auto": 50000,
        "home": 125000,
        "life": 75000,
        "health": 40000,
    }

    return {
        "id": policy_id,
        "policy_number": policy_number,
        "customer_name": customer_name,
        "customer_email": f"{customer_name.lower().replace(' ', '.')}@example.com",
        "coverage_type": coverage_type,
        "coverage_amount": coverage_amounts.get(coverage_type, 100000),
        "annual_premium_cents": premium_cents.get(coverage_type, 50000),
        "status": status,
        "effective_date": (datetime.utcnow() - timedelta(days=30)).isoformat(),
        "expiration_date": (datetime.utcnow() + timedelta(days=335)).isoformat(),
        "created_at": timestamp,
    }


def create_test_claim(policy_id=None, claim_type="auto", status="submitted"):
    """
    Create a test claim matching seed data format.

    Args:
        policy_id: Associated policy ID (generated if None)
        claim_type: Claim type
        status: Claim status (submitted, under_review, approved, denied)

    Returns:
        dict: Claim data ready for DynamoDB
    """
    if policy_id is None:
        policy_id = generate_policy_id()

    claim_id = generate_claim_id()
    claim_number = generate_claim_number()
    timestamp = datetime.utcnow().isoformat()

    claim_amounts = {
        "auto": 15000,  # $150
        "home": 35000,  # $350
        "life": 500000,  # $5000
        "health": 25000,  # $250
    }

    return {
        "id": claim_id,
        "claim_number": claim_number,
        "policy_id": policy_id,
        "claim_type": claim_type,
        "amount_cents": claim_amounts.get(claim_type, 15000),
        "status": status,
        "description": f"Test {claim_type} claim",
        "claim_date": (datetime.utcnow() - timedelta(days=7)).isoformat(),
        "created_at": timestamp,
        "documents": [],
    }


def create_test_payment(policy_id=None, amount_cents=50000, status="completed"):
    """
    Create a test payment matching seed data format.

    Args:
        policy_id: Associated policy ID (generated if None)
        amount_cents: Payment amount in cents
        status: Payment status (pending, completed, failed)

    Returns:
        dict: Payment data ready for DynamoDB
    """
    if policy_id is None:
        policy_id = generate_policy_id()

    payment_id = generate_payment_id()
    timestamp = datetime.utcnow().isoformat()

    return {
        "id": payment_id,
        "policy_id": policy_id,
        "amount_cents": amount_cents,
        "payment_method": "credit_card",
        "status": status,
        "payment_date": timestamp,
        "created_at": timestamp,
    }


def create_test_case(claim_id=None, case_type="claim_review", status="open"):
    """
    Create a test case matching seed data format.

    Args:
        claim_id: Associated claim ID (generated if None)
        case_type: Case type (claim_review, policy_inquiry, billing_issue)
        status: Case status (open, in_progress, resolved, closed)

    Returns:
        dict: Case data ready for DynamoDB
    """
    if claim_id is None:
        claim_id = generate_claim_id()

    case_id = generate_case_id()
    timestamp = datetime.utcnow().isoformat()

    return {
        "id": case_id,
        "related_id": claim_id,
        "case_type": case_type,
        "status": status,
        "priority": "medium",
        "description": f"Test {case_type} case",
        "assigned_to": "test-adjuster",
        "created_at": timestamp,
        "updated_at": timestamp,
    }


def dynamodb_format(data):
    """
    Convert Python dict to DynamoDB format (handles Decimal conversion).

    Args:
        data: Python dict with native types

    Returns:
        dict: Same data with int values converted to Decimal
    """
    formatted = {}
    for key, value in data.items():
        if isinstance(value, int) and key.endswith("_cents"):
            formatted[key] = Decimal(str(value))
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            formatted[key] = Decimal(str(value))
        else:
            formatted[key] = value
    return formatted
