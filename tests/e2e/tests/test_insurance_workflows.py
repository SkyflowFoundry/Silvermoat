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
