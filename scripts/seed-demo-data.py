#!/usr/bin/env python3
"""Seed demo data using Faker library v40.1.0 with realistic customer relationships."""
import os
import sys
import requests
from datetime import date
from faker import Faker

API_BASE_URL = os.environ.get('API_BASE_URL', '').rstrip('/')
if not API_BASE_URL:
    print("Error: API_BASE_URL environment variable not set", file=sys.stderr)
    sys.exit(1)

fake = Faker()

# Global storage for created resources to maintain relationships
customers = []
quotes = []
policies = []

def seed_customers(count=50):
    """Seed customer records to database."""
    print(f"Seeding {count} customers...")
    for i in range(count):
        data = {
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address().replace('\n', ', '),
            "phone": fake.phone_number()
        }
        response = requests.post(f"{API_BASE_URL}/customer", json=data, timeout=30)
        response.raise_for_status()

        # Store customer ID and data for quotes/policies
        customer_id = response.json()['id']
        customers.append({
            "id": customer_id,
            "name": data["name"],
            "email": data["email"],
            "address": data["address"]
        })

        if (i + 1) % 25 == 0:
            print(f"  Created {i + 1}/{count} customers")
    print(f"✓ Created {count} customers")

def seed_quotes(count=150):
    """Seed quote records (avg 3 per customer, some customers get 1-5)."""
    print(f"Seeding {count} quotes...")
    for i in range(count):
        # Reuse customer from pool
        customer = fake.random_element(customers)

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

        # Store quote ID and customer for policy generation
        quote_id = response.json()['id']
        quotes.append({
            "id": quote_id,
            "customer": customer,
            "coverage_amount": data["coverageAmount"]
        })

        if (i + 1) % 25 == 0:
            print(f"  Created {i + 1}/{count} quotes")
    print(f"✓ Created {count} quotes")

def seed_policies(count=90):
    """Seed policy records (60% quote conversion rate)."""
    print(f"Seeding {count} policies...")
    for i in range(count):
        # Reference actual quote
        quote = fake.random_element(quotes)

        # Generate dates for policy period
        effective_date = fake.date_between(start_date='-2y', end_date='today')
        expiration_date = fake.date_between(start_date=effective_date, end_date='+1y')

        data = {
            "quoteId": quote["id"],
            "policyNumber": fake.bothify(text='POL-####-####'),
            "holderName": quote["customer"]["name"],
            "holderEmail": quote["customer"]["email"],
            "propertyAddress": quote["customer"]["address"],
            "coverageAmount": quote["coverage_amount"],
            "premium": round(fake.random_int(800, 5000, step=50) + fake.random.random(), 2),
            "effectiveDate": effective_date.isoformat(),
            "expirationDate": expiration_date.isoformat()
        }
        response = requests.post(f"{API_BASE_URL}/policy", json=data, timeout=30)
        response.raise_for_status()

        # Store policy ID for claims/payments
        policy_id = response.json()['id']
        policies.append({
            "id": policy_id,
            "customer": quote["customer"],
            "effective_date": effective_date,
            "expiration_date": expiration_date
        })

        if (i + 1) % 25 == 0:
            print(f"  Created {i + 1}/{count} policies")
    print(f"✓ Created {count} policies")

def seed_claims(count=30):
    """Seed claim records (30% of policies have 1-2 claims)."""
    print(f"Seeding {count} claims...")
    for i in range(count):
        # Reference actual policy
        policy = fake.random_element(policies)

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
        if (i + 1) % 25 == 0:
            print(f"  Created {i + 1}/{count} claims")
    print(f"✓ Created {count} claims")

def seed_payments(count=270):
    """Seed payment records (avg 3 payments per policy - quarterly/monthly premiums)."""
    print(f"Seeding {count} payments...")
    for i in range(count):
        # Reference actual policy
        policy = fake.random_element(policies)

        data = {
            "policyId": policy["id"],
            "amount": round(fake.random_int(200, 1500, step=50) + fake.random.random(), 2),
            "paymentMethod": fake.random_element(["CREDIT_CARD", "BANK_TRANSFER", "CHECK"]),
            "cardLastFour": fake.numerify(text="####")
        }
        response = requests.post(f"{API_BASE_URL}/payment", json=data, timeout=30)
        response.raise_for_status()
        if (i + 1) % 25 == 0:
            print(f"  Created {i + 1}/{count} payments")
    print(f"✓ Created {count} payments")

def seed_cases(count=40):
    """Seed case records (various customer service issues)."""
    print(f"Seeding {count} cases...")

    # Generate pool of customer service reps
    assignees = [fake.name() for _ in range(10)]

    for i in range(count):
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

        # Reference actual resources
        entity_type = fake.random_element(["policy", "quote", "claim"])
        if entity_type == "policy" and policies:
            entity_id = fake.random_element(policies)["id"]
        elif entity_type == "quote" and quotes:
            entity_id = fake.random_element(quotes)["id"]
        else:
            entity_id = f"{entity_type}-{fake.uuid4()}"

        data = {
            "title": fake.random_element(case_titles),
            "description": fake.text(max_nb_chars=200),
            "relatedEntityType": entity_type,
            "relatedEntityId": entity_id,
            "assignee": fake.random_element(assignees),
            "priority": fake.random_element(["LOW", "MEDIUM", "HIGH"])
        }
        response = requests.post(f"{API_BASE_URL}/case", json=data, timeout=30)
        response.raise_for_status()
        if (i + 1) % 25 == 0:
            print(f"  Created {i + 1}/{count} cases")
    print(f"✓ Created {count} cases")

if __name__ == "__main__":
    try:
        print(f"Seeding demo data to {API_BASE_URL}\n")

        # Seed customers first
        seed_customers(50)
        print()

        # Seed resources with realistic relationships
        seed_quotes(150)
        seed_policies(90)
        seed_claims(30)
        seed_payments(270)
        seed_cases(40)

        total = 50 + 150 + 90 + 30 + 270 + 40
        print(f"\n✓ Seeding complete: {total} items created")
        print(f"  - 50 customers")
        print(f"  - 150 quotes (avg 3 per customer)")
        print(f"  - 90 policies (60% quote conversion)")
        print(f"  - 30 claims (30% of policies)")
        print(f"  - 270 payments (avg 3 per policy)")
        print(f"  - 40 cases (customer service issues)")

    except requests.exceptions.RequestException as e:
        print(f"\n✗ Seeding failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
