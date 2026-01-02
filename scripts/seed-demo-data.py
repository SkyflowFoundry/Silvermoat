#!/usr/bin/env python3
"""Seed demo data using Faker library v40.1.0."""
import os
import sys
import requests
from faker import Faker

API_BASE_URL = os.environ.get('API_BASE_URL', '').rstrip('/')
if not API_BASE_URL:
    print("Error: API_BASE_URL environment variable not set", file=sys.stderr)
    sys.exit(1)

fake = Faker()

def seed_quotes(count=100):
    """Seed quote records."""
    print(f"Seeding {count} quotes...")
    for i in range(count):
        data = {
            "customer_name": fake.name(),
            "customer_email": fake.email(),
            "property_address": fake.address().replace('\n', ', '),
            "coverage_amount": fake.random_int(50000, 1000000, step=10000),
            "property_type": fake.random_element(["single_family", "condo", "townhouse"]),
            "year_built": fake.random_int(1950, 2024)
        }
        response = requests.post(f"{API_BASE_URL}/quote", json=data, timeout=30)
        response.raise_for_status()
        if (i + 1) % 25 == 0:
            print(f"  Created {i + 1}/{count} quotes")
    print(f"✓ Created {count} quotes")

def seed_policies(count=100):
    """Seed policy records."""
    print(f"Seeding {count} policies...")
    for i in range(count):
        # Generate dates for policy period
        effective_date = fake.date_between(start_date='-2y', end_date='today')
        expiration_date = fake.date_between(start_date=effective_date, end_date='+1y')

        data = {
            "quote_id": f"quote-{fake.uuid4()}",
            "customer_name": fake.name(),
            "customer_email": fake.email(),
            "property_address": fake.address().replace('\n', ', '),
            "coverage_amount": fake.random_int(100000, 2000000, step=10000),
            "premium_annual": round(fake.random_int(800, 5000, step=50) + fake.random.random(), 2),
            "effective_date": effective_date.isoformat(),
            "expiration_date": expiration_date.isoformat()
        }
        response = requests.post(f"{API_BASE_URL}/policy", json=data, timeout=30)
        response.raise_for_status()
        if (i + 1) % 25 == 0:
            print(f"  Created {i + 1}/{count} policies")
    print(f"✓ Created {count} policies")

def seed_claims(count=100):
    """Seed claim records."""
    print(f"Seeding {count} claims...")
    for i in range(count):
        data = {
            "policy_id": f"policy-{fake.uuid4()}",
            "claim_type": fake.random_element(["water_damage", "fire", "theft", "liability"]),
            "description": fake.text(max_nb_chars=200),
            "claim_amount": fake.random_int(1000, 100000, step=1000),
            "date_of_loss": fake.date_between(start_date='-1y', end_date='today').isoformat()
        }
        response = requests.post(f"{API_BASE_URL}/claim", json=data, timeout=30)
        response.raise_for_status()
        if (i + 1) % 25 == 0:
            print(f"  Created {i + 1}/{count} claims")
    print(f"✓ Created {count} claims")

def seed_payments(count=100):
    """Seed payment records."""
    print(f"Seeding {count} payments...")
    for i in range(count):
        data = {
            "policy_id": f"policy-{fake.uuid4()}",
            "amount": round(fake.random_int(500, 5000, step=100) + fake.random.random(), 2),
            "payment_method": fake.random_element(["credit_card", "bank_transfer", "check"]),
            "card_last_four": fake.numerify(text="####")
        }
        response = requests.post(f"{API_BASE_URL}/payment", json=data, timeout=30)
        response.raise_for_status()
        if (i + 1) % 25 == 0:
            print(f"  Created {i + 1}/{count} payments")
    print(f"✓ Created {count} payments")

def seed_cases(count=100):
    """Seed case records."""
    print(f"Seeding {count} cases...")
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

        data = {
            "title": fake.random_element(case_titles),
            "description": fake.text(max_nb_chars=200),
            "relatedEntityType": fake.random_element(["policy", "quote", "claim"]),
            "relatedEntityId": f"{fake.random_element(['policy', 'quote', 'claim'])}-{fake.uuid4()}",
            "assignee": fake.name(),
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
        seed_quotes(100)
        seed_policies(100)
        seed_claims(100)
        seed_payments(100)
        seed_cases(100)
        print("\n✓ Seeding complete: 500 items created")
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Seeding failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
