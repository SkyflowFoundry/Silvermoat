"""
Fintech Workflow E2E Tests

Tests for fintech-specific UI workflows including:
- Viewing customers, accounts, transactions, loans, cards
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
@pytest.mark.fintech
def test_fintech_landing_page_loads(driver, fintech_base_url):
    """Test fintech landing page loads successfully"""
    driver.get(fintech_base_url)
    wait_for_app_ready(driver)

    # Page should have content
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Landing page should have content"

    # Should show fintech branding
    page_source = driver.page_source.lower()
    assert "fintech" in page_source or "silvermoat" in page_source or "financial" in page_source


@pytest.mark.e2e
@pytest.mark.fintech
def test_fintech_navigation_exists(driver, fintech_base_url):
    """Test fintech app has navigation"""
    driver.get(fintech_base_url)
    wait_for_app_ready(driver)

    # Look for common navigation elements
    page_source = driver.page_source.lower()

    # Should have navigation to key entities
    has_navigation = any([
        "customer" in page_source,
        "account" in page_source,
        "transaction" in page_source,
        "loan" in page_source,
        "card" in page_source,
        "dashboard" in page_source,
    ])
    assert has_navigation, "Fintech portal should have navigation to key entities"


@pytest.mark.e2e
@pytest.mark.fintech
def test_fintech_customers_page_loads(driver, fintech_base_url):
    """Test customers page loads (even if empty)"""
    driver.get(f"{fintech_base_url}/customers")
    wait_for_app_ready(driver)

    # Page should render without error
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Customers page should have content"

    # Should show customer-related content
    page_source = driver.page_source.lower()
    has_customer_context = "customer" in page_source or "table" in page_source
    assert has_customer_context, "Customers page should show customer-related content"


@pytest.mark.e2e
@pytest.mark.fintech
def test_fintech_accounts_page_loads(driver, fintech_base_url):
    """Test accounts page loads (even if empty)"""
    driver.get(f"{fintech_base_url}/accounts")
    wait_for_app_ready(driver)

    # Page should render without error
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Accounts page should have content"

    # Should show account-related content
    page_source = driver.page_source.lower()
    has_account_context = "account" in page_source or "table" in page_source
    assert has_account_context, "Accounts page should show account-related content"


@pytest.mark.e2e
@pytest.mark.fintech
def test_fintech_chatbot_visible(driver, fintech_base_url):
    """Test chatbot button is visible"""
    driver.get(fintech_base_url)
    wait_for_app_ready(driver)

    # Look for chatbot trigger button (floating action button pattern)
    page_source = driver.page_source.lower()
    has_chat = "chat" in page_source or "message" in page_source or "assistant" in page_source
    assert has_chat, "Fintech portal should have chatbot interface visible"


@pytest.mark.e2e
@pytest.mark.fintech
def test_fintech_api_health(fintech_api_url):
    """Test fintech API is responding"""
    response = requests.get(fintech_api_url, timeout=10)
    assert response.status_code == 200, "Fintech API should be healthy"
    data = response.json()
    assert "message" in data or "status" in data, "API should return valid JSON"


@pytest.mark.e2e
@pytest.mark.fintech
def test_fintech_customer_via_api(fintech_api_url):
    """Test creating and retrieving a customer via API"""
    # Create a customer
    customer_data = {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "555-1234"
    }

    create_response = requests.post(
        f"{fintech_api_url}/customer",
        json=customer_data,
        timeout=10
    )
    assert create_response.status_code in [200, 201], "Should create customer successfully"

    customer = create_response.json()
    assert "id" in customer, "Response should include customer ID"
    customer_id = customer["id"]

    # Retrieve the customer
    get_response = requests.get(
        f"{fintech_api_url}/customer/{customer_id}",
        timeout=10
    )
    assert get_response.status_code == 200, "Should retrieve customer successfully"

    retrieved_customer = get_response.json()
    assert retrieved_customer["data"]["name"] == "Test Customer"


@pytest.mark.e2e
@pytest.mark.fintech
def test_fintech_transaction_via_api(fintech_api_url):
    """Test creating a transaction via API"""
    # First create a customer
    customer_data = {
        "name": "Transaction Test Customer",
        "email": "transaction@example.com"
    }

    customer_response = requests.post(
        f"{fintech_api_url}/customer",
        json=customer_data,
        timeout=10
    )
    assert customer_response.status_code in [200, 201]

    # Create a transaction
    transaction_data = {
        "customerName": "Transaction Test Customer",
        "customerEmail": "transaction@example.com",
        "amount": 100.50,
        "type": "DEPOSIT",
        "description": "Test deposit"
    }

    transaction_response = requests.post(
        f"{fintech_api_url}/transaction",
        json=transaction_data,
        timeout=10
    )
    assert transaction_response.status_code in [200, 201], "Should create transaction successfully"

    transaction = transaction_response.json()
    assert "id" in transaction, "Response should include transaction ID"
    assert transaction["data"]["amount"] == 100.50
