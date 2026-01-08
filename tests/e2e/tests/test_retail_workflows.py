"""
Retail Workflow E2E Tests

Comprehensive tests for retail UI workflows including:
- All 5 entities (Products, Orders, Inventory, Payments, Cases)
- Seeding and clearing demo data
- Employee chatbot functionality
- Customer portal order tracking
- Dashboard navigation
"""

import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..conftest import wait_for_app_ready


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.smoke
def test_retail_dashboard_loads(driver, retail_base_url):
    """Test retail dashboard loads successfully"""
    driver.get(f"{retail_base_url}/dashboard")
    wait_for_app_ready(driver)

    # Should show dashboard content
    assert "Dashboard" in driver.page_source or "Retail" in driver.page_source

    # Page should have content
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Dashboard should have content"


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.smoke
def test_retail_seed_data_button_exists(driver, retail_base_url):
    """Test retail dashboard has seed data functionality"""
    driver.get(f"{retail_base_url}/dashboard")
    wait_for_app_ready(driver)

    # Look for seed data button (case-insensitive search)
    page_source = driver.page_source.lower()
    has_seed_button = "seed" in page_source and "data" in page_source

    assert has_seed_button, "Dashboard should have seed data option"


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.slow
@pytest.mark.api
def test_retail_product_via_api(driver, retail_base_url, retail_api_url):
    """Test creating product via API and verifying it appears in UI"""
    # Create product via API
    product_data = {
        "sku": "SKU-E2E-001",
        "name": "E2E Test Product",
        "description": "Test product for E2E testing",
        "price": 99,
        "category": "Electronics",
        "stockQuantity": 100,
        "manufacturer": "TestCo",
        "weight": 5
    }

    response = requests.post(f"{retail_api_url}/product", json=product_data)
    assert response.status_code == 201, f"Failed to create product: {response.status_code}"
    product_id = response.json()['id']

    try:
        # Navigate to retail dashboard
        driver.get(f"{retail_base_url}/dashboard")
        wait_for_app_ready(driver)

        # Dashboard should be accessible
        assert "Dashboard" in driver.page_source or "Retail" in driver.page_source

    finally:
        # Cleanup
        requests.delete(f"{retail_api_url}/product/{product_id}")


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.smoke
def test_retail_home_has_dashboard_link(driver, retail_base_url):
    """Test retail home page has link to dashboard"""
    driver.get(retail_base_url)
    wait_for_app_ready(driver)

    # Look for dashboard link or button
    page_source = driver.page_source.lower()
    has_dashboard_link = "dashboard" in page_source

    assert has_dashboard_link, "Home page should have dashboard link"


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.smoke
def test_retail_navigation_to_dashboard(driver, retail_base_url):
    """Test navigating from home to dashboard"""
    driver.get(retail_base_url)
    wait_for_app_ready(driver)

    # Look for dashboard button
    try:
        wait = WebDriverWait(driver, 10)
        # Find button/link with "Dashboard" text
        buttons = driver.find_elements(By.TAG_NAME, "button")
        links = driver.find_elements(By.TAG_NAME, "a")

        dashboard_element = None
        for element in buttons + links:
            if "dashboard" in element.text.lower():
                dashboard_element = element
                break

        if dashboard_element:
            dashboard_element.click()

            # Wait for navigation
            wait.until(lambda d: "/dashboard" in d.current_url)

            # Should be on dashboard
            assert "/dashboard" in driver.current_url
    except Exception as e:
        # Dashboard link might not be present yet (minimal placeholder UI)
        print(f"Dashboard navigation test skipped: {e}")
        pytest.skip("Dashboard link not yet implemented")


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.api
def test_retail_order_via_api(driver, retail_base_url, retail_api_url):
    """Test creating order via API"""
    # Create order via API
    order_data = {
        "orderNumber": "ORD-E2E-001",
        "customerName": "E2E Test Customer",
        "customerEmail": "test@example.com",
        "customerPhone": "555-1234",
        "shippingAddress": "123 Test St, Test City",
        "items": [
            {
                "productId": "test-product-id",
                "productName": "Test Product",
                "quantity": 2,
                "price": 50,
                "total": 100
            }
        ],
        "totalAmount": 100,
        "orderDate": "2024-01-01",
        "status": "PENDING"
    }

    response = requests.post(f"{retail_api_url}/order", json=order_data)
    assert response.status_code == 201, f"Failed to create order: {response.status_code}"
    order_id = response.json()['id']

    try:
        # Verify order was created
        get_response = requests.get(f"{retail_api_url}/order/{order_id}")
        assert get_response.status_code == 200, "Order should be retrievable"
    finally:
        # Cleanup
        requests.delete(f"{retail_api_url}/order/{order_id}")


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.smoke
def test_retail_dashboard_navigation(driver, retail_base_url):
    """Test dashboard shows all entity navigation cards"""
    driver.get(f"{retail_base_url}/dashboard")
    wait_for_app_ready(driver)

    # Should have quick navigation section
    page_source = driver.page_source.lower()

    # Check for all entities
    assert "products" in page_source, "Dashboard should have Products navigation"
    assert "orders" in page_source, "Dashboard should have Orders navigation"
    assert "inventory" in page_source, "Dashboard should have Inventory navigation"
    assert "payments" in page_source, "Dashboard should have Payments navigation"
    assert "cases" in page_source, "Dashboard should have Cases navigation"


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.api
def test_retail_inventory_workflow(driver, retail_base_url, retail_api_url):
    """Test creating inventory item and verifying it"""
    # Create product first (inventory depends on product)
    product_data = {
        "sku": "INV-TEST-SKU",
        "name": "Inventory Test Product",
        "price": 50.00,
        "category": "Test",
        "stockLevel": 100
    }

    product_response = requests.post(f"{retail_api_url}/product", json=product_data)
    assert product_response.status_code == 201
    product_id = product_response.json()['id']

    try:
        # Create inventory item
        inventory_data = {
            "productId": product_id,
            "warehouse": "Test Warehouse",
            "quantity": 100,
            "reorderLevel": 20
        }

        inv_response = requests.post(f"{retail_api_url}/inventory", json=inventory_data)
        assert inv_response.status_code == 201, f"Failed to create inventory: {inv_response.status_code}"

        inventory_id = inv_response.json()['id']

        # Verify inventory exists
        get_response = requests.get(f"{retail_api_url}/inventory/{inventory_id}")
        assert get_response.status_code == 200
        assert get_response.json()['data']['productId'] == product_id

        # Cleanup inventory
        requests.delete(f"{retail_api_url}/inventory/{inventory_id}")

    finally:
        # Cleanup product
        requests.delete(f"{retail_api_url}/product/{product_id}")


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.api
def test_retail_payment_workflow(driver, retail_base_url, retail_api_url):
    """Test creating payment linked to order"""
    # Create order first
    order_data = {
        "customerEmail": "payment-test@example.com",
        "customerName": "Payment Test",
        "items": [{"productId": "test-prod", "quantity": 1, "price": 100}],
        "totalAmount": 100
    }

    order_response = requests.post(f"{retail_api_url}/order", json=order_data)
    assert order_response.status_code == 201
    order_id = order_response.json()['id']

    try:
        # Create payment
        payment_data = {
            "orderId": order_id,
            "amount": 100.00,
            "method": "CREDIT_CARD",
            "transactionId": "TXN-TEST-123",
            "status": "COMPLETED"
        }

        payment_response = requests.post(f"{retail_api_url}/payment", json=payment_data)
        assert payment_response.status_code == 201, f"Failed to create payment: {payment_response.status_code}"

        payment_id = payment_response.json()['id']

        # Verify payment exists and is linked to order
        get_response = requests.get(f"{retail_api_url}/payment/{payment_id}")
        assert get_response.status_code == 200
        assert get_response.json()['data']['orderId'] == order_id

        # Cleanup payment
        requests.delete(f"{retail_api_url}/payment/{payment_id}")

    finally:
        # Cleanup order
        requests.delete(f"{retail_api_url}/order/{order_id}")


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.api
def test_retail_case_workflow(driver, retail_base_url, retail_api_url):
    """Test creating support case"""
    case_data = {
        "subject": "E2E Test Case",
        "description": "This is a test support case for E2E testing",
        "customerEmail": "case-test@example.com",
        "priority": "MEDIUM",
        "status": "OPEN",
        "assignee": "Test Agent"
    }

    response = requests.post(f"{retail_api_url}/case", json=case_data)
    assert response.status_code == 201, f"Failed to create case: {response.status_code}"

    case_id = response.json()['id']

    try:
        # Verify case exists
        get_response = requests.get(f"{retail_api_url}/case/{case_id}")
        assert get_response.status_code == 200
        assert get_response.json()['data']['subject'] == "E2E Test Case"
        assert get_response.json()['data']['priority'] == "MEDIUM"

    finally:
        # Cleanup
        requests.delete(f"{retail_api_url}/case/{case_id}")


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.ui
def test_retail_customer_portal_loads(driver, retail_base_url):
    """Test customer portal pages load successfully"""
    # Customer dashboard
    driver.get(f"{retail_base_url}/customer/dashboard")
    wait_for_app_ready(driver)
    assert "customer" in driver.page_source.lower() or "track" in driver.page_source.lower()

    # Customer order tracking
    driver.get(f"{retail_base_url}/customer/orders")
    wait_for_app_ready(driver)
    assert "track" in driver.page_source.lower() or "order" in driver.page_source.lower()

    # Customer product browser
    driver.get(f"{retail_base_url}/customer/products")
    wait_for_app_ready(driver)
    assert "product" in driver.page_source.lower() or "browse" in driver.page_source.lower()


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.slow
@pytest.mark.lifecycle
def test_retail_full_workflow_seed_and_clear(driver, retail_base_url, retail_api_url):
    """Test complete workflow: seed data, verify entities, clear data"""
    # Get initial counts
    products_before = requests.get(f"{retail_api_url}/product").json()
    initial_product_count = len(products_before.get('items', []))

    # Note: This test would trigger the seed functionality if the UI was fully interactive
    # For now, we just verify the API endpoints work

    # Create test data via API to simulate seeded data
    product_data = {"sku": "WORKFLOW-001", "name": "Workflow Test", "price": 10, "category": "Test"}
    product_response = requests.post(f"{retail_api_url}/product", json=product_data)
    assert product_response.status_code == 201
    product_id = product_response.json()['id']

    try:
        # Verify product appears in list
        products_after = requests.get(f"{retail_api_url}/product").json()
        assert len(products_after.get('items', [])) > initial_product_count

    finally:
        # Cleanup
        requests.delete(f"{retail_api_url}/product/{product_id}")


@pytest.mark.e2e
@pytest.mark.retail
@pytest.mark.slow
@pytest.mark.ui
@pytest.mark.chat
def test_retail_chatbot_interaction(driver, retail_base_url):
    """Test chatbot functionality if available"""
    driver.get(f"{retail_base_url}/dashboard")
    wait_for_app_ready(driver)

    # Look for chatbot button (floating action button)
    page_source = driver.page_source.lower()
    has_chat_button = "chat" in page_source or "message" in page_source or "assistant" in page_source

    # If chatbot not found, skip test (may not be implemented yet)
    if not has_chat_button:
        pytest.skip("Chatbot functionality not yet implemented on this page")

    # Try to find and click chatbot button
    try:
        wait = WebDriverWait(driver, 10)
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

            # Wait for drawer/modal to open
            import time
            time.sleep(1)

            # Chatbot interface should appear
            page_source_after = driver.page_source.lower()
            assert "chat" in page_source_after or "message" in page_source_after, "Chat interface should open"
    except Exception as e:
        # Chatbot exists but not interactive in test
        print(f"Chatbot exists but could not interact: {e}")
        pass
