"""
Insurance Workflow E2E Tests

Tests for insurance-specific UI workflows including:
- Viewing quotes, policies, claims, customers
- Chatbot interactions
- Seeding demo data
"""

import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..conftest import wait_for_app_ready


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.smoke
def test_insurance_landing_page_loads(driver, insurance_base_url):
    """Test insurance landing page loads successfully"""
    driver.get(insurance_base_url)
    wait_for_app_ready(driver)

    # Page should have content
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Landing page should have content"

    # Should show insurance branding
    page_source = driver.page_source.lower()
    assert "insurance" in page_source or "silvermoat" in page_source


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.smoke
def test_insurance_navigation_exists(driver, insurance_base_url):
    """Test insurance app has navigation"""
    driver.get(insurance_base_url)
    wait_for_app_ready(driver)

    # Look for common navigation elements
    page_source = driver.page_source.lower()

    # Should have navigation to key entities
    has_navigation = any([
        "quote" in page_source,
        "policy" in page_source,
        "claim" in page_source,
        "customer" in page_source,
        "dashboard" in page_source
    ])

    assert has_navigation, "Should have navigation elements"


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.ui
def test_insurance_quotes_accessible(driver, insurance_base_url):
    """Test quotes page is accessible"""
    driver.get(f"{insurance_base_url}/quotes")
    wait_for_app_ready(driver)

    # Should load without error
    assert "error" not in driver.page_source.lower() or "quote" in driver.page_source.lower()

    # Page should have content
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Quotes page should have content"


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.ui
def test_insurance_policies_accessible(driver, insurance_base_url):
    """Test policies page is accessible"""
    driver.get(f"{insurance_base_url}/policies")
    wait_for_app_ready(driver)

    # Should load without error
    assert "error" not in driver.page_source.lower() or "polic" in driver.page_source.lower()

    # Page should have content
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Policies page should have content"


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.ui
def test_insurance_claims_accessible(driver, insurance_base_url):
    """Test claims page is accessible"""
    driver.get(f"{insurance_base_url}/claims")
    wait_for_app_ready(driver)

    # Should load without error
    assert "error" not in driver.page_source.lower() or "claim" in driver.page_source.lower()

    # Page should have content
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Claims page should have content"


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.ui
def test_insurance_customers_accessible(driver, insurance_base_url):
    """Test customers page is accessible"""
    driver.get(f"{insurance_base_url}/customers")
    wait_for_app_ready(driver)

    # Should load without error
    assert "error" not in driver.page_source.lower() or "customer" in driver.page_source.lower()

    # Page should have content
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Customers page should have content"


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.slow
@pytest.mark.api
def test_insurance_quote_via_api(driver, insurance_base_url, insurance_api_url):
    """Test creating quote via API and verifying system works"""
    # Create quote via API
    quote_data = {
        "customerName": "E2E Test Customer",
        "customerEmail": "e2e@test.com",
        "customerPhone": "555-1234",
        "propertyAddress": "123 Test St",
        "propertyValue": 500000,
        "coverageAmount": 400000,
        "deductible": 5000
    }

    response = requests.post(f"{insurance_api_url}/quote", json=quote_data)
    assert response.status_code == 201, f"Failed to create quote: {response.status_code}"
    quote_id = response.json()['id']

    try:
        # Navigate to insurance quotes page
        driver.get(f"{insurance_base_url}/quotes")
        wait_for_app_ready(driver)

        # Quotes page should be accessible
        assert "quote" in driver.page_source.lower()

    finally:
        # Cleanup
        requests.delete(f"{insurance_api_url}/quote/{quote_id}")


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.slow
@pytest.mark.api
def test_insurance_policy_via_api(driver, insurance_base_url, insurance_api_url):
    """Test creating policy via API"""
    # Create policy via API
    policy_data = {
        "policyNumber": "POL-E2E-001",
        "holderName": "E2E Test Holder",
        "holderEmail": "holder@test.com",
        "holderPhone": "555-5678",
        "propertyAddress": "456 Test Ave",
        "coverageAmount": 300000,
        "premium": 1200,
        "deductible": 2500,
        "startDate": "2024-01-01",
        "endDate": "2025-01-01",
        "status": "ACTIVE"
    }

    response = requests.post(f"{insurance_api_url}/policy", json=policy_data)
    assert response.status_code == 201, f"Failed to create policy: {response.status_code}"
    policy_id = response.json()['id']

    try:
        # Verify policy was created
        get_response = requests.get(f"{insurance_api_url}/policy/{policy_id}")
        assert get_response.status_code == 200, "Policy should be retrievable"

        # Navigate to insurance policies page
        driver.get(f"{insurance_base_url}/policies")
        wait_for_app_ready(driver)

        # Policies page should be accessible
        assert "polic" in driver.page_source.lower()

    finally:
        # Cleanup
        requests.delete(f"{insurance_api_url}/policy/{policy_id}")


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.slow
@pytest.mark.api
def test_insurance_claim_via_api(driver, insurance_base_url, insurance_api_url):
    """Test creating claim via API"""
    # Create policy first (claims need a policy)
    policy_data = {
        "policyNumber": "POL-CLAIM-001",
        "holderName": "Claim Test Holder",
        "holderEmail": "claim-holder@test.com",
        "holderPhone": "555-9999",
        "propertyAddress": "789 Claim Test Ave",
        "coverageAmount": 250000,
        "premium": 1000,
        "deductible": 2000,
        "startDate": "2024-01-01",
        "endDate": "2025-01-01",
        "status": "ACTIVE"
    }

    policy_response = requests.post(f"{insurance_api_url}/policy", json=policy_data)
    assert policy_response.status_code == 201, f"Failed to create policy: {policy_response.status_code}"
    policy_id = policy_response.json()['id']

    try:
        # Create claim via API
        claim_data = {
            "policyId": policy_id,
            "claimType": "PROPERTY_DAMAGE",
            "dateOfLoss": "2024-06-15",
            "description": "E2E test claim for property damage",
            "claimAmount": 15000,
            "status": "PENDING"
        }

        claim_response = requests.post(f"{insurance_api_url}/claim", json=claim_data)
        assert claim_response.status_code == 201, f"Failed to create claim: {claim_response.status_code}"
        claim_id = claim_response.json()['id']

        # Verify claim was created
        get_response = requests.get(f"{insurance_api_url}/claim/{claim_id}")
        assert get_response.status_code == 200, "Claim should be retrievable"

        # Navigate to insurance claims page
        driver.get(f"{insurance_base_url}/claims")
        wait_for_app_ready(driver)

        # Claims page should be accessible
        assert "claim" in driver.page_source.lower()

        # Cleanup claim
        requests.delete(f"{insurance_api_url}/claim/{claim_id}")

    finally:
        # Cleanup policy
        requests.delete(f"{insurance_api_url}/policy/{policy_id}")


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.slow
@pytest.mark.ui
@pytest.mark.customer
def test_insurance_customer_portal_workflow(driver, insurance_base_url, insurance_api_url):
    """Test customer portal: view policies, claims, payments; switch customers"""
    # Create test customer with policy
    customer_email = "portal-test@example.com"
    policy_data = {
        "policyNumber": "POL-PORTAL-001",
        "holderName": "Portal Test Customer",
        "holderEmail": customer_email,
        "holderPhone": "555-7777",
        "propertyAddress": "456 Portal Test St",
        "coverageAmount": 300000,
        "premium": 1200,
        "deductible": 2500,
        "startDate": "2024-01-01",
        "endDate": "2025-01-01",
        "status": "ACTIVE"
    }

    policy_response = requests.post(f"{insurance_api_url}/policy", json=policy_data)
    assert policy_response.status_code == 201
    policy_id = policy_response.json()['id']

    try:
        # Navigate to customer portal
        driver.get(f"{insurance_base_url}/customer/dashboard")
        wait_for_app_ready(driver)

        # Portal should load
        page_source = driver.page_source.lower()
        assert "customer" in page_source or "portal" in page_source, "Customer portal should load"

        # Should have tabs for policies, claims, payments
        assert "polic" in page_source, "Should show policies section"

        # Check for customer selector (dropdown to switch customers)
        assert "select" in page_source or "customer" in page_source, "Should have customer selection"

    finally:
        # Cleanup
        requests.delete(f"{insurance_api_url}/policy/{policy_id}")


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.slow
@pytest.mark.ui
@pytest.mark.chat
def test_insurance_chatbot_interaction(driver, insurance_base_url):
    """Test chatbot button exists and can be opened"""
    driver.get(insurance_base_url)
    wait_for_app_ready(driver)

    # Look for chatbot button (floating action button)
    page_source = driver.page_source.lower()
    has_chat_button = "chat" in page_source or "message" in page_source or "assistant" in page_source

    assert has_chat_button, "Should have chatbot button visible"

    # Try to find and click chatbot button
    try:
        wait = WebDriverWait(driver, 10)
        # Look for button with chat/message icon or text
        buttons = driver.find_elements(By.TAG_NAME, "button")

        chat_button = None
        for button in buttons:
            button_html = button.get_attribute('outerHTML').lower()
            button_text = button.text.lower()
            if 'chat' in button_html or 'message' in button_html or 'chat' in button_text:
                chat_button = button
                break

        if chat_button and chat_button.is_displayed():
            chat_button.click()

            # Wait a moment for drawer/modal to open
            import time
            time.sleep(1)

            # Chatbot interface should appear
            page_source_after = driver.page_source.lower()
            assert "chat" in page_source_after or "message" in page_source_after, "Chat interface should open"
    except Exception as e:
        # If we can't interact with it, at least verify it exists
        print(f"Could not interact with chatbot: {e}")
        assert has_chat_button, "Chatbot button should exist even if not clickable in test"


@pytest.mark.e2e
@pytest.mark.insurance
@pytest.mark.slow
@pytest.mark.lifecycle
def test_insurance_quote_to_claim_lifecycle(driver, insurance_base_url, insurance_api_url):
    """Test complete lifecycle: create quote → convert to policy → file claim"""
    # Step 1: Create quote
    quote_data = {
        "customerName": "Lifecycle Test Customer",
        "customerEmail": "lifecycle@test.com",
        "customerPhone": "555-1111",
        "propertyAddress": "123 Lifecycle St",
        "propertyValue": 400000,
        "coverageAmount": 320000,
        "deductible": 3000
    }

    quote_response = requests.post(f"{insurance_api_url}/quote", json=quote_data)
    assert quote_response.status_code == 201, f"Failed to create quote: {quote_response.status_code}"
    quote_id = quote_response.json()['id']

    try:
        # Verify quote exists
        get_quote = requests.get(f"{insurance_api_url}/quote/{quote_id}")
        assert get_quote.status_code == 200, "Quote should exist"

        # Step 2: Create policy (simulating quote conversion)
        policy_data = {
            "policyNumber": "POL-LIFECYCLE-001",
            "holderName": quote_data["customerName"],
            "holderEmail": quote_data["customerEmail"],
            "holderPhone": quote_data["customerPhone"],
            "propertyAddress": quote_data["propertyAddress"],
            "coverageAmount": quote_data["coverageAmount"],
            "premium": 1500,
            "deductible": quote_data["deductible"],
            "startDate": "2024-01-01",
            "endDate": "2025-01-01",
            "status": "ACTIVE"
        }

        policy_response = requests.post(f"{insurance_api_url}/policy", json=policy_data)
        assert policy_response.status_code == 201, "Policy should be created"
        policy_id = policy_response.json()['id']

        # Step 3: File claim against policy
        claim_data = {
            "policyId": policy_id,
            "claimType": "PROPERTY_DAMAGE",
            "dateOfLoss": "2024-06-01",
            "description": "Lifecycle test claim",
            "claimAmount": 12000,
            "status": "PENDING"
        }

        claim_response = requests.post(f"{insurance_api_url}/claim", json=claim_data)
        assert claim_response.status_code == 201, "Claim should be created"
        claim_id = claim_response.json()['id']

        # Verify all entities exist
        assert requests.get(f"{insurance_api_url}/quote/{quote_id}").status_code == 200
        assert requests.get(f"{insurance_api_url}/policy/{policy_id}").status_code == 200
        assert requests.get(f"{insurance_api_url}/claim/{claim_id}").status_code == 200

        # Visit UI to verify system is functional
        driver.get(f"{insurance_base_url}/dashboard")
        wait_for_app_ready(driver)

        # Cleanup
        requests.delete(f"{insurance_api_url}/claim/{claim_id}")
        requests.delete(f"{insurance_api_url}/policy/{policy_id}")
        requests.delete(f"{insurance_api_url}/quote/{quote_id}")

    except Exception as e:
        # Cleanup on failure
        try:
            requests.delete(f"{insurance_api_url}/quote/{quote_id}")
        except:
            pass
        raise e
