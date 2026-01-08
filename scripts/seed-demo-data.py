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

fake = Faker()

# Parallel execution configuration
MAX_WORKERS = 10  # Number of concurrent API requests

# Global storage for created resources to maintain relationships
customers = []
quotes = []
policies = []
products = []
orders = []

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

# ========================================
# Retail Vertical Seeding Functions
# ========================================

def create_product(index):
    """Create a single product."""
    categories = ['Electronics', 'Apparel', 'Home & Garden', 'Sports & Outdoors',
                  'Books', 'Toys & Games', 'Health & Beauty', 'Automotive']
    adjectives = ['Premium', 'Deluxe', 'Classic', 'Modern', 'Eco-Friendly', 'Smart', 'Pro', 'Essential']
    nouns = ['Widget', 'Gadget', 'Tool', 'Device', 'Kit', 'Set', 'System', 'Solution']

    category = fake.random_element(categories)
    product_name = f"{fake.random_element(adjectives)} {fake.random_element(nouns)}"

    data = {
        "sku": f"SKU-{fake.random_int(10000, 99999)}",
        "name": product_name,
        "description": f"High-quality {product_name.lower()} for {category.lower()}",
        "price": fake.random_int(10, 500),
        "category": category,
        "stockQuantity": fake.random_int(0, 500),
        "manufacturer": fake.random_element(['BrandCo', 'TechCorp', 'QualityGoods', 'PremiumMfg']),
        "weight": fake.random_int(1, 50)
    }

    response = requests.post(f"{API_BASE_URL}/product", json=data, timeout=30)
    response.raise_for_status()

    product_id = response.json()['id']
    return {
        "id": product_id,
        "name": data["name"],
        "sku": data["sku"],
        "price": data["price"]
    }

def seed_products(count=50):
    """Seed product records in parallel."""
    print(f"Seeding {count} products...")

    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_product, i) for i in range(count)]

        for future in as_completed(futures):
            product = future.result()
            products.append(product)
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} products")

    print(f"✓ Created {count} products")

def create_order(product_list):
    """Create a single order with items."""
    customer_name = fake.name()
    num_items = fake.random_int(1, 5)
    order_items = []
    total_amount = 0

    for _ in range(num_items):
        product = fake.random_element(product_list)
        quantity = fake.random_int(1, 3)
        item_total = product["price"] * quantity
        total_amount += item_total

        order_items.append({
            "productId": product["id"],
            "productName": product["name"],
            "quantity": quantity,
            "price": product["price"],
            "total": item_total
        })

    data = {
        "orderNumber": f"ORD-{fake.random_int(100000, 999999)}",
        "customerName": customer_name,
        "customerEmail": fake.email(),
        "customerPhone": fake.phone_number(),
        "shippingAddress": fake.address().replace('\n', ', '),
        "items": order_items,
        "totalAmount": total_amount,
        "orderDate": fake.date_between(start_date='-90d', end_date='today').isoformat(),
        "status": fake.random_element(['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED'])
    }

    response = requests.post(f"{API_BASE_URL}/order", json=data, timeout=30)
    response.raise_for_status()

    order_id = response.json()['id']
    return {
        "id": order_id,
        "orderNumber": data["orderNumber"],
        "totalAmount": total_amount,
        "orderDate": data["orderDate"]
    }

def seed_orders(count=30):
    """Seed order records in parallel."""
    print(f"Seeding {count} orders...")

    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_order, products) for _ in range(count)]

        for future in as_completed(futures):
            order = future.result()
            orders.append(order)
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} orders")

    print(f"✓ Created {count} orders")

def create_inventory(product):
    """Create a single inventory record for a product."""
    warehouses = ['NYC-01', 'LA-02', 'CHI-03', 'DAL-04', 'ATL-05']

    data = {
        "productId": product["id"],
        "productName": product["name"],
        "sku": product["sku"],
        "location": fake.random_element(warehouses),
        "quantity": fake.random_int(0, 500),
        "reorderPoint": fake.random_int(10, 50),
        "lastRestocked": fake.date_between(start_date='-30d', end_date='today').isoformat()
    }

    response = requests.post(f"{API_BASE_URL}/inventory", json=data, timeout=30)
    response.raise_for_status()
    return response.json()['id']

def seed_inventory(count=50):
    """Seed inventory records in parallel."""
    print(f"Seeding {count} inventory records...")

    product_list = products[:count]
    completed = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_inventory, product) for product in product_list]

        for future in as_completed(futures):
            future.result()
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} inventory records")

    print(f"✓ Created {count} inventory records")

def create_retail_payment(order):
    """Create a single payment for an order."""
    payment_methods = ['CREDIT_CARD', 'DEBIT_CARD', 'PAYPAL', 'GIFT_CARD']

    data = {
        "orderId": order["id"],
        "orderNumber": order["orderNumber"],
        "amount": order["totalAmount"],
        "paymentMethod": fake.random_element(payment_methods),
        "transactionId": f"TXN-{fake.random_int(1000000, 9999999)}",
        "paymentDate": order["orderDate"]
    }

    response = requests.post(f"{API_BASE_URL}/payment", json=data, timeout=30)
    response.raise_for_status()
    return response.json()['id']

def seed_retail_payments(count):
    """Seed payment records for orders in parallel."""
    print(f"Seeding {count} payments...")

    order_list = orders[:count]
    completed = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_retail_payment, order) for order in order_list]

        for future in as_completed(futures):
            future.result()
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} payments")

    print(f"✓ Created {count} payments")

def create_retail_case(index):
    """Create a single support case."""
    topics = ['ORDER_INQUIRY', 'PRODUCT_DEFECT', 'SHIPPING_DELAY', 'REFUND_REQUEST', 'PRODUCT_QUESTION']
    priorities = ['LOW', 'MEDIUM', 'HIGH']
    assignees = ['Support Team', 'Sales Team', 'Fulfillment']

    customer_name = fake.name()
    topic = fake.random_element(topics)

    data = {
        "title": f"{topic.replace('_', ' ')} - {customer_name}",
        "description": f"Customer {customer_name} has reported an issue regarding {topic.lower().replace('_', ' ')}.",
        "customerName": customer_name,
        "customerEmail": fake.email(),
        "topic": topic,
        "priority": fake.random_element(priorities),
        "assignee": fake.random_element(assignees),
        "createdDate": fake.date_between(start_date='-60d', end_date='today').isoformat()
    }

    response = requests.post(f"{API_BASE_URL}/case", json=data, timeout=30)
    response.raise_for_status()
    return response.json()['id']

def seed_retail_cases(count=15):
    """Seed support case records in parallel."""
    print(f"Seeding {count} support cases...")

    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_retail_case, i) for i in range(count)]

        for future in as_completed(futures):
            future.result()
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} cases")

    print(f"✓ Created {count} cases")

# ============================================
# Healthcare Vertical Seeding Functions
# ============================================

# Storage for healthcare entities
patients = []
appointments = []
prescriptions = []

def create_patient(idx):
    """Create a single patient and return data."""
    patient_email = fake.email()
    data = {
        "name": fake.name(),
        "email": patient_email,
        "address": fake.address().replace('\n', ', '),
        "phone": fake.phone_number(),
        "dateOfBirth": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        "status": fake.random_element(["ACTIVE", "ACTIVE", "ACTIVE", "INACTIVE"]),  # Mostly active
    }
    response = requests.post(f"{API_BASE_URL}/patient", json=data, timeout=30)
    response.raise_for_status()

    patient_id = response.json()['id']
    return {
        "id": patient_id,
        "name": data["name"],
        "email": patient_email,
        "address": data["address"]
    }

def seed_patients(count=50):
    """Seed patient records to database in parallel."""
    print(f"Seeding {count} patients...")

    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_patient, i) for i in range(count)]

        for future in as_completed(futures):
            patient = future.result()
            patients.append(patient)
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} patients")

    print(f"✓ Created {count} patients")

def create_appointment(patient):
    """Create a single appointment for a patient."""
    # Generate appointment date (past or future)
    appointment_date = fake.date_time_between(start_date='-6M', end_date='+3M')

    data = {
        "patientId": patient["id"],
        "patientName": patient["name"],
        "patientEmail": patient["email"],
        "appointmentDate": appointment_date.isoformat(),
        "appointmentType": fake.random_element(["CHECK_UP", "FOLLOW_UP", "CONSULTATION", "EMERGENCY"]),
        "provider": fake.name(),
        "status": fake.random_element(["SCHEDULED", "CONFIRMED", "COMPLETED", "COMPLETED", "CANCELLED"]),
        "notes": fake.sentence(nb_words=10)
    }
    response = requests.post(f"{API_BASE_URL}/appointment", json=data, timeout=30)
    response.raise_for_status()

    appointment_id = response.json()['id']
    return {
        "id": appointment_id,
        "patient": patient,
        "date": appointment_date
    }

def seed_appointments(count=100):
    """Seed appointment records ensuring each patient gets at least one (parallel)."""
    print(f"Seeding {count} appointments...")

    # Build list of patients for appointments
    num_patients = len(patients)
    patient_assignments = []

    # First pass: one appointment per patient
    for i in range(min(count, num_patients)):
        patient_assignments.append(patients[i])

    # Second pass: remaining appointments randomly distributed
    for i in range(num_patients, count):
        patient_assignments.append(fake.random_element(patients))

    # Create appointments in parallel
    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_appointment, patient) for patient in patient_assignments]

        for future in as_completed(futures):
            appointment = future.result()
            appointments.append(appointment)
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} appointments")

    print(f"✓ Created {count} appointments")

def create_prescription(patient):
    """Create a single prescription for a patient."""
    issue_date = fake.date_between(start_date='-1y', end_date='today')

    data = {
        "patientId": patient["id"],
        "patientName": patient["name"],
        "patientEmail": patient["email"],
        "medication": fake.random_element([
            "Lisinopril", "Metformin", "Atorvastatin", "Amlodipine",
            "Omeprazole", "Levothyroxine", "Albuterol", "Gabapentin"
        ]),
        "dosage": fake.random_element(["5mg", "10mg", "20mg", "50mg", "100mg"]),
        "frequency": fake.random_element(["Once daily", "Twice daily", "Three times daily", "As needed"]),
        "prescribedDate": issue_date.isoformat(),
        "provider": fake.name(),
        "status": fake.random_element(["ACTIVE", "ACTIVE", "FILLED", "EXPIRED"]),
        "refillsRemaining": fake.random_int(0, 5)
    }
    response = requests.post(f"{API_BASE_URL}/prescription", json=data, timeout=30)
    response.raise_for_status()

    prescription_id = response.json()['id']
    return {
        "id": prescription_id,
        "patient": patient
    }

def seed_prescriptions(count=75):
    """Seed prescription records in parallel."""
    print(f"Seeding {count} prescriptions...")

    # Distribute prescriptions across patients
    patient_assignments = []
    num_patients = len(patients)

    for i in range(count):
        patient_assignments.append(fake.random_element(patients))

    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_prescription, patient) for patient in patient_assignments]

        for future in as_completed(futures):
            prescription = future.result()
            prescriptions.append(prescription)
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} prescriptions")

    print(f"✓ Created {count} prescriptions")

def create_healthcare_billing(patient):
    """Create a single billing record for a patient."""
    service_date = fake.date_between(start_date='-6M', end_date='today')

    data = {
        "patientId": patient["id"],
        "patientName": patient["name"],
        "patientEmail": patient["email"],
        "serviceDate": service_date.isoformat(),
        "amount": fake.random_int(50, 5000),
        "status": fake.random_element(["PENDING", "PAID", "PAID", "OVERDUE"]),
        "description": fake.random_element([
            "Office Visit", "Lab Work", "X-Ray", "Surgery",
            "Medication", "Physical Therapy", "Consultation"
        ])
    }
    response = requests.post(f"{API_BASE_URL}/billing", json=data, timeout=30)
    response.raise_for_status()
    return response.json()['id']

def seed_healthcare_billing(count=80):
    """Seed billing records in parallel."""
    print(f"Seeding {count} billing records...")

    patient_assignments = []
    for i in range(count):
        patient_assignments.append(fake.random_element(patients))

    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_healthcare_billing, patient) for patient in patient_assignments]

        for future in as_completed(futures):
            future.result()
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} billing records")

    print(f"✓ Created {count} billing records")

def create_healthcare_case(patient):
    """Create a single support case for a patient."""
    data = {
        "customerId": patient["id"],
        "customerEmail": patient["email"],
        "subject": fake.random_element([
            "Appointment Scheduling Issue",
            "Prescription Refill Request",
            "Billing Question",
            "Medical Records Request",
            "Insurance Coverage Question",
            "Test Results Inquiry"
        ]),
        "description": fake.text(max_nb_chars=200),
        "priority": fake.random_element(["LOW", "MEDIUM", "HIGH", "URGENT"]),
        "status": fake.random_element(["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"])
    }

    response = requests.post(f"{API_BASE_URL}/case", json=data, timeout=30)
    response.raise_for_status()
    return response.json()['id']

def seed_healthcare_cases(count=40):
    """Seed support case records in parallel."""
    print(f"Seeding {count} support cases...")

    patient_assignments = []
    for i in range(count):
        patient_assignments.append(fake.random_element(patients))

    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_healthcare_case, patient) for patient in patient_assignments]

        for future in as_completed(futures):
            future.result()
            completed += 1

            if completed % 25 == 0:
                print(f"  Created {completed}/{count} cases")

    print(f"✓ Created {count} cases")

if __name__ == "__main__":
    try:
        print(f"Seeding {VERTICAL} demo data to {API_BASE_URL}\n")

        if VERTICAL == 'retail':
            # Retail seeding
            seed_products(50)
            print()
            seed_orders(30)
            seed_inventory(50)
            seed_retail_payments(30)
            seed_retail_cases(15)

            total = 50 + 30 + 50 + 30 + 15
            print(f"\n✓ Retail seeding complete: {total} items created")
            print(f"  - 50 products")
            print(f"  - 30 orders")
            print(f"  - 50 inventory records")
            print(f"  - 30 payments")
            print(f"  - 15 support cases")

        elif VERTICAL == 'healthcare':
            # Healthcare seeding
            seed_patients(50)
            print()

            # Seed resources with realistic relationships
            # Note: Each patient guaranteed at least 1 appointment
            seed_appointments(100)
            seed_prescriptions(75)
            seed_healthcare_billing(80)
            seed_healthcare_cases(40)

            total = 50 + 100 + 75 + 80 + 40
            print(f"\n✓ Healthcare seeding complete: {total} items created")
            print(f"  - 50 patients")
            print(f"  - 100 appointments (each patient has 1+)")
            print(f"  - 75 prescriptions")
            print(f"  - 80 billing records")
            print(f"  - 40 support cases")

        else:
            # Insurance seeding
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
            print(f"\n✓ Insurance seeding complete: {total} items created")
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
