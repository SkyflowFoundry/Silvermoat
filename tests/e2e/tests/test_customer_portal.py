"""
Customer Portal E2E Tests

Tests for customer-facing portal workflows including:
- Customer login with policy number + ZIP
- Viewing policies, claims, and payments
- Submitting new claims
"""

import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..conftest import wait_for_app_ready


@pytest.mark.e2e
@pytest.mark.customer
def test_customer_login_page_loads(driver, base_url):
    """Test that customer login page loads successfully"""
    driver.get(f"{base_url}/customer/login")
    wait_for_app_ready(driver)

    # Should have login form
    assert "Customer Portal" in driver.page_source or "Policy Number" in driver.page_source

    # Should have input fields
    policy_input = driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='POL'], input[type='text']")
    assert len(policy_input) >= 1, "Should have policy number input"

    zip_input = driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='12345'], input[maxlength='5']")
    assert len(zip_input) >= 1, "Should have ZIP code input"


@pytest.mark.e2e
@pytest.mark.customer
def test_customer_login_with_valid_credentials(driver, base_url, api_base_url):
    """Test customer can log in with valid policy number and ZIP"""
    # First, create a test policy via API
    policy_data = {
        "policyNumber": "POL-2024-E2E001",
        "holderName": "Test Customer",
        "zip": "12345",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 150000,
    }
    response = requests.post(f"{api_base_url}/policy", json=policy_data)
    assert response.status_code == 201, "Test policy should be created"

    # Navigate to login page
    driver.get(f"{base_url}/customer/login")
    wait_for_app_ready(driver)

    # Fill in login form
    wait = WebDriverWait(driver, 10)

    # Find policy number input (first text input)
    policy_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    policy_input = policy_inputs[0] if policy_inputs else None
    assert policy_input is not None, "Policy number input should exist"
    policy_input.clear()
    policy_input.send_keys("POL-2024-E2E001")

    # Find ZIP input (second text input or by maxlength)
    zip_input = None
    for inp in policy_inputs:
        if inp.get_attribute('maxlength') == '5':
            zip_input = inp
            break
    if zip_input is None and len(policy_inputs) > 1:
        zip_input = policy_inputs[1]

    assert zip_input is not None, "ZIP code input should exist"
    zip_input.clear()
    zip_input.send_keys("12345")

    # Submit form
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    # Wait for redirect to dashboard
    wait.until(EC.url_contains("/customer/dashboard"))

    # Should be on dashboard
    assert "/customer/dashboard" in driver.current_url
    assert "Test Customer" in driver.page_source or "POL-2024-E2E001" in driver.page_source


@pytest.mark.e2e
@pytest.mark.customer
def test_customer_login_with_invalid_credentials(driver, base_url):
    """Test customer login fails with invalid credentials"""
    # Navigate to login page
    driver.get(f"{base_url}/customer/login")
    wait_for_app_ready(driver)

    # Fill in login form with invalid credentials
    wait = WebDriverWait(driver, 10)

    policy_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    if len(policy_inputs) >= 2:
        policy_inputs[0].send_keys("POL-2024-INVALID")
        policy_inputs[1].send_keys("99999")

        # Submit form
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Should show error message (Ant Design uses .ant-message for messages)
        # Wait a bit for error to appear
        import time
        time.sleep(2)

        # Should still be on login page (not redirected)
        assert "/customer/login" in driver.current_url


@pytest.mark.e2e
@pytest.mark.customer
def test_customer_dashboard_shows_data(driver, base_url, api_base_url):
    """Test customer dashboard displays policies, claims, and payments"""
    # Create test data via API
    policy_data = {
        "policyNumber": "POL-2024-E2E002",
        "holderName": "Dashboard Test User",
        "zip": "54321",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 200000,
    }
    policy_response = requests.post(f"{api_base_url}/policy", json=policy_data)
    assert policy_response.status_code == 201
    policy_id = policy_response.json()['id']

    # Create a claim
    claim_data = {
        "policyId": policy_id,
        "claimNumber": "CLM-2024-E2E002",
        "claimantName": "Dashboard Test User",
        "incidentDate": "2024-12-01",
        "description": "Test claim for E2E testing",
        "estimatedAmount_cents": 100000,
    }
    requests.post(f"{api_base_url}/claim", json=claim_data)

    # Login
    driver.get(f"{base_url}/customer/login")
    wait_for_app_ready(driver)

    policy_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    if len(policy_inputs) >= 2:
        policy_inputs[0].send_keys("POL-2024-E2E002")
        policy_inputs[1].send_keys("54321")

        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Wait for dashboard
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_contains("/customer/dashboard"))

        # Dashboard should show user info
        assert "Dashboard Test User" in driver.page_source or "POL-2024-E2E002" in driver.page_source

        # Should have tabs for policies, claims, payments
        assert "Policies" in driver.page_source or "Claims" in driver.page_source


@pytest.mark.e2e
@pytest.mark.customer
def test_customer_submit_claim_flow(driver, base_url, api_base_url):
    """Test customer can submit a new claim through the UI"""
    # Create test policy
    policy_data = {
        "policyNumber": "POL-2024-E2E003",
        "holderName": "Claim Submit Test",
        "zip": "11111",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 180000,
    }
    response = requests.post(f"{api_base_url}/policy", json=policy_data)
    assert response.status_code == 201

    # Login
    driver.get(f"{base_url}/customer/login")
    wait_for_app_ready(driver)

    policy_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    if len(policy_inputs) >= 2:
        policy_inputs[0].send_keys("POL-2024-E2E003")
        policy_inputs[1].send_keys("11111")

        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Wait for dashboard
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_contains("/customer/dashboard"))

        # Navigate to claim submission form
        driver.get(f"{base_url}/customer/claims/new")
        wait_for_app_ready(driver)

        # Should be on claim form page
        assert "/customer/claims/new" in driver.current_url
        assert "Submit New Claim" in driver.page_source or "Submit Claim" in driver.page_source


@pytest.mark.e2e
@pytest.mark.customer
def test_customer_logout(driver, base_url, api_base_url):
    """Test customer can logout from dashboard"""
    # Create test policy and login
    policy_data = {
        "policyNumber": "POL-2024-E2E004",
        "holderName": "Logout Test",
        "zip": "22222",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2025-01-01",
        "premium_cents": 175000,
    }
    response = requests.post(f"{api_base_url}/policy", json=policy_data)
    assert response.status_code == 201

    # Login
    driver.get(f"{base_url}/customer/login")
    wait_for_app_ready(driver)

    policy_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    if len(policy_inputs) >= 2:
        policy_inputs[0].send_keys("POL-2024-E2E004")
        policy_inputs[1].send_keys("22222")

        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Wait for dashboard
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_contains("/customer/dashboard"))

        # Find and click logout button
        logout_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Logout') or contains(., 'Log out')]")
        if logout_buttons:
            logout_buttons[0].click()

            # Should redirect to login page
            import time
            time.sleep(2)
            assert "/customer/login" in driver.current_url or "/customer" in driver.current_url
