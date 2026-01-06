#!/usr/bin/env python3
"""Seed demo data using Faker library v40.1.0 with realistic customer relationships."""
import os
import sys
import requests
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed
from faker import Faker

API_BASE_URL = os.environ.get('API_BASE_URL', '').rstrip('/')
VERTICAL = os.environ.get('VERTICAL', 'insurance')

if not API_BASE_URL:
    print("Error: API_BASE_URL environment variable not set", file=sys.stderr)
    sys.exit(1)

# Retail vertical uses UI-based seeding (JavaScript in ui-retail/src/utils/seedData.js)
if VERTICAL == 'retail':
    print(f"✓ Retail seeding skipped - use Dashboard UI for retail demo data")
    print(f"  (UI-based seeding provides retail-specific entities: products, orders, inventory)")
    sys.exit(0)

fake = Faker()

# Parallel execution configuration
MAX_WORKERS = 10  # Number of concurrent API requests

# Global storage for created resources to maintain relationships
customers = []
quotes = []
policies = []

def create_customer(index):
    """Create a single customer and return data."""
    customer_email = fake.email()
    data = {
        "name": fake.name(),
        "email": customer_email,
        "address": fake.address().replace('\n', ', '),
        "phone": fake.phone_number()
    }
    response = requests.post(f"{API_BASE_URL}/customer", json=data, timeout=30)
    response.raise_for_status()

    customer_id = response.json()['id']
    return {
        "id": customer_id,
        "name": data["name"],
        "email": customer_email,
        "address": data["address"]
    }

def seed_customers(count=50):
    """Seed customer records to database in parallel."""
    print(f"Seeding {count} customers...")

    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_customer, i) for i in range(count)]

        for future in as_completed(futures):
            customer = future.result()
            customers.append(customer)
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} customers")

    print(f"✓ Created {count} customers")

def create_quote(customer):
    """Create a single quote for a customer."""
    data = {
        "customerName": customer["name"],
        "customerEmail": customer["email"],
        "propertyAddress": customer["address"],
        "coverageAmount": fake.random_int(50000, 1000000, step=10000),
        "propertyType": fake.random_element(["SINGLE_FAMILY", "CONDO", "TOWNHOUSE"]),
        "yearBuilt": fake.random_int(1950, 2024)
    }
    response = requests.post(f"{API_BASE_URL}/quote", json=data, timeout=30)
    response.raise_for_status()

    quote_id = response.json()['id']
    return {
        "id": quote_id,
        "customer": customer,
        "coverage_amount": data["coverageAmount"]
    }

def seed_quotes(count=150):
    """Seed quote records ensuring each customer gets at least one (parallel)."""
    print(f"Seeding {count} quotes...")

    # Build list of customers for quotes
    num_customers = len(customers)
    customer_assignments = []

    # First pass: one quote per customer
    for i in range(min(count, num_customers)):
        customer_assignments.append(customers[i])

    # Second pass: remaining quotes randomly distributed
    for i in range(num_customers, count):
        customer_assignments.append(fake.random_element(customers))

    # Create quotes in parallel
    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_quote, customer) for customer in customer_assignments]

        for future in as_completed(futures):
            quote = future.result()
            quotes.append(quote)
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} quotes")

    print(f"✓ Created {count} quotes")

def create_policy(quote):
    """Create a single policy for a quote."""
    # Generate dates for policy period
    effective_date = fake.date_between(start_date='-2y', end_date='today')
    expiration_date = fake.date_between(start_date=effective_date, end_date='+1y')

    data = {
        "quoteId": quote["id"],
        "policyNumber": fake.bothify(text='POL-####-####'),
        "holderName": quote["customer"]["name"],
        "holderEmail": quote["customer"]["email"],
        "customer_email": quote["customer"]["email"],  # Frontend expects this field
        "propertyAddress": quote["customer"]["address"],
        "coverageAmount": quote["coverage_amount"],
        "premium": round(fake.random_int(800, 5000, step=50) + fake.random.random(), 2),
        "effectiveDate": effective_date.isoformat(),
        "expirationDate": expiration_date.isoformat()
    }
    response = requests.post(f"{API_BASE_URL}/policy", json=data, timeout=30)
    response.raise_for_status()

    policy_id = response.json()['id']
    return {
        "id": policy_id,
        "customer": quote["customer"],
        "effective_date": effective_date,
        "expiration_date": expiration_date
    }

def seed_policies(count=90):
    """Seed policy records ensuring each customer gets at least one (parallel)."""
    print(f"Seeding {count} policies...")

    num_customers = len(customers)
    quote_assignments = []

    # Build list of quotes for policies
    for i in range(count):
        # First N policies: ensure each customer gets one policy
        if i < num_customers:
            customer = customers[i]
            customer_quotes = [q for q in quotes if q["customer"]["id"] == customer["id"]]
            quote = fake.random_element(customer_quotes) if customer_quotes else fake.random_element(quotes)
        else:
            # Remaining policies: random distribution
            quote = fake.random_element(quotes)
        quote_assignments.append(quote)

    # Create policies in parallel
    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_policy, quote) for quote in quote_assignments]

        for future in as_completed(futures):
            policy = future.result()
            policies.append(policy)
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} policies")

    print(f"✓ Created {count} policies")

def create_claim(policy):
    """Create a single claim for a policy."""
    # Loss date should be during policy period (but not in the future)
    today = date.today()
    end_date = min(policy["expiration_date"], today)

    # If policy is brand new (effective_date >= today), use effective_date as loss date
    if policy["effective_date"] >= end_date:
        loss_date = policy["effective_date"]
    else:
        loss_date = fake.date_between(
            start_date=policy["effective_date"],
            end_date=end_date
        )

    data = {
        "policyId": policy["id"],
        "claimNumber": fake.bothify(text='CLM-####-####'),
        "claimantName": policy["customer"]["name"],
        "lossType": fake.random_element(["WATER_DAMAGE", "FIRE", "THEFT", "LIABILITY"]),
        "description": fake.text(max_nb_chars=200),
        "amount": fake.random_int(1000, 100000, step=1000),
        "estimatedAmount_cents": fake.random_int(1000, 100000, step=1000) * 100,
        "incidentDate": loss_date.isoformat()
    }
    response = requests.post(f"{API_BASE_URL}/claim", json=data, timeout=30)
    response.raise_for_status()
    return response.json()['id']

def seed_claims(count=50):
    """Seed claim records ensuring each customer gets at least one (parallel)."""
    print(f"Seeding {count} claims...")

    num_customers = len(customers)
    policy_assignments = []

    # Build list of policies for claims
    for i in range(count):
        # First N claims: ensure each customer gets one claim
        if i < num_customers:
            customer = customers[i]
            customer_policies = [p for p in policies if p["customer"]["id"] == customer["id"]]
            policy = fake.random_element(customer_policies) if customer_policies else fake.random_element(policies)
        else:
            # Remaining claims: random distribution
            policy = fake.random_element(policies)
        policy_assignments.append(policy)

    # Create claims in parallel
    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_claim, policy) for policy in policy_assignments]

        for future in as_completed(futures):
            future.result()  # Just need to complete, don't store claim IDs
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} claims")

    print(f"✓ Created {count} claims")

def create_payment(policy):
    """Create a single payment for a policy."""
    data = {
        "policyId": policy["id"],
        "amount": round(fake.random_int(200, 1500, step=50) + fake.random.random(), 2),
        "paymentMethod": fake.random_element(["CREDIT_CARD", "BANK_TRANSFER", "CHECK"]),
        "cardLastFour": fake.numerify(text="####")
    }
    response = requests.post(f"{API_BASE_URL}/payment", json=data, timeout=30)
    response.raise_for_status()
    return response.json()['id']

def seed_payments(count=270):
    """Seed payment records ensuring each customer gets at least one (parallel)."""
    print(f"Seeding {count} payments...")

    num_customers = len(customers)
    policy_assignments = []

    # Build list of policies for payments
    for i in range(count):
        # First N payments: ensure each customer gets one payment
        if i < num_customers:
            customer = customers[i]
            customer_policies = [p for p in policies if p["customer"]["id"] == customer["id"]]
            policy = fake.random_element(customer_policies) if customer_policies else fake.random_element(policies)
        else:
            # Remaining payments: random distribution
            policy = fake.random_element(policies)
        policy_assignments.append(policy)

    # Create payments in parallel
    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_payment, policy) for policy in policy_assignments]

        for future in as_completed(futures):
            future.result()  # Just need to complete
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} payments")

    print(f"✓ Created {count} payments")

def create_case(case_data):
    """Create a single case."""
    response = requests.post(f"{API_BASE_URL}/case", json=case_data, timeout=30)
    response.raise_for_status()
    return response.json()['id']

def seed_cases(count=50):
    """Seed case records ensuring each customer gets at least one (parallel)."""
    print(f"Seeding {count} cases...")

    # Generate pool of customer service reps
    assignees = [fake.name() for _ in range(10)]

    # Generate case titles based on common scenarios
    case_titles = [
        "Policy Change Request",
        "Coverage Amount Inquiry",
        "Claim Status Update",
        "Payment Issue Resolution",
        "Document Upload Request",
        "Policy Cancellation Request",
        "Premium Adjustment Inquiry",
        "Coverage Extension Request"
    ]

    num_customers = len(customers)
    case_assignments = []

    # Build list of cases to create
    for i in range(count):
        # First N cases: ensure each customer gets one case (linked to their policy)
        if i < num_customers:
            customer = customers[i]
            customer_policies = [p for p in policies if p["customer"]["id"] == customer["id"]]
            if customer_policies:
                entity_type = "policy"
                entity_id = fake.random_element(customer_policies)["id"]
            else:
                # Fallback to random entity if customer has no policy
                entity_type = fake.random_element(["policy", "quote", "claim"])
                if entity_type == "policy" and policies:
                    entity_id = fake.random_element(policies)["id"]
                elif entity_type == "quote" and quotes:
                    entity_id = fake.random_element(quotes)["id"]
                else:
                    entity_id = f"{entity_type}-{fake.uuid4()}"
        else:
            # Remaining cases: random distribution
            entity_type = fake.random_element(["policy", "quote", "claim"])
            if entity_type == "policy" and policies:
                entity_id = fake.random_element(policies)["id"]
            elif entity_type == "quote" and quotes:
                entity_id = fake.random_element(quotes)["id"]
            else:
                entity_id = f"{entity_type}-{fake.uuid4()}"

        case_data = {
            "title": fake.random_element(case_titles),
            "description": fake.text(max_nb_chars=200),
            "relatedEntityType": entity_type,
            "relatedEntityId": entity_id,
            "assignee": fake.random_element(assignees),
            "priority": fake.random_element(["LOW", "MEDIUM", "HIGH"])
        }
        case_assignments.append(case_data)

    # Create cases in parallel
    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_case, case_data) for case_data in case_assignments]

        for future in as_completed(futures):
            future.result()  # Just need to complete
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} cases")

    print(f"✓ Created {count} cases")

if __name__ == "__main__":
    try:
        print(f"Seeding demo data to {API_BASE_URL}\n")

        # Seed customers first
        seed_customers(50)
        print()

        # Seed resources with realistic relationships
        # Note: Each customer guaranteed at least 1 of each resource type
        seed_quotes(150)
        seed_policies(90)
        seed_claims(50)
        seed_payments(270)
        seed_cases(50)

        total = 50 + 150 + 90 + 50 + 270 + 50
        print(f"\n✓ Seeding complete: {total} items created")
        print(f"  - 50 customers")
        print(f"  - 150 quotes (each customer has 1-5)")
        print(f"  - 90 policies (each customer has 1-3)")
        print(f"  - 50 claims (each customer has 1+)")
        print(f"  - 270 payments (each customer has 1+)")
        print(f"  - 50 cases (each customer has 1+)")

    except requests.exceptions.RequestException as e:
        print(f"\n✗ Seeding failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
