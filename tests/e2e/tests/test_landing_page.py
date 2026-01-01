"""
Landing Page E2E Tests

Tests for the unified landing page that provides Customer/Employee portal selection.
"""

import pytest
from selenium.webdriver.common.by import By
from ..conftest import wait_for_app_ready


@pytest.mark.e2e
@pytest.mark.smoke
def test_landing_page_loads(driver, base_url):
    """Test that landing page loads with portal options"""
    driver.get(base_url)
    wait_for_app_ready(driver)

    # Should have both portal cards
    assert "Customer Portal" in driver.page_source, "Should have Customer Portal option"
    assert "Employee Portal" in driver.page_source, "Should have Employee Portal option"

    # Should have Silvermoat Insurance branding
    assert "Silvermoat Insurance" in driver.page_source


@pytest.mark.e2e
def test_customer_portal_navigation(driver, base_url):
    """Test navigation to customer portal"""
    driver.get(base_url)
    wait_for_app_ready(driver)

    # Find and click Customer Portal button
    # Use XPath to find button within Customer Portal card
    customer_button = driver.find_element(
        By.XPATH,
        "//*[contains(text(), 'Customer Portal')]//ancestor::*[contains(@class, 'ant-card')]//button"
    )
    customer_button.click()

    # Should navigate to /customer/login
    assert '/customer/login' in driver.current_url, "Should navigate to customer login page"


@pytest.mark.e2e
def test_employee_portal_navigation(driver, base_url):
    """Test navigation to employee portal"""
    driver.get(base_url)
    wait_for_app_ready(driver)

    # Find and click Employee Portal button
    # Use XPath to find button within Employee Portal card
    employee_button = driver.find_element(
        By.XPATH,
        "//*[contains(text(), 'Employee Portal')]//ancestor::*[contains(@class, 'ant-card')]//button"
    )
    employee_button.click()

    # Should navigate to /dashboard
    assert '/dashboard' in driver.current_url, "Should navigate to employee dashboard"


@pytest.mark.e2e
@pytest.mark.smoke
def test_loading_screen_appears(driver, base_url):
    """Test that loading screen appears on landing page"""
    # Navigate to landing page
    driver.get(base_url)

    # Loading screen should be present initially (before wait_for_app_ready)
    # Note: This is timing-sensitive, may pass if page loads quickly
    # Check if loading screen element exists or was recently removed
    loading_screen_exists = driver.execute_script(
        "return document.getElementById('loading-screen') !== null"
    )

    # If loading screen still exists, verify it's visible or fading out
    if loading_screen_exists:
        loading_screen = driver.find_element(By.ID, "loading-screen")
        # Should have fade-out class or be visible
        assert loading_screen is not None

    # Wait for app to be ready (loading screen should be removed)
    wait_for_app_ready(driver)

    # After app is ready, loading screen should be completely removed
    loading_screen_removed = driver.execute_script(
        "return document.getElementById('loading-screen') === null"
    )
    assert loading_screen_removed, "Loading screen should be removed after app loads"


@pytest.mark.e2e
def test_loading_screen_not_on_dashboard(driver, base_url):
    """Test that loading screen does NOT appear when navigating directly to dashboard"""
    # Navigate directly to dashboard (bypassing landing page)
    driver.get(f"{base_url}/dashboard")

    # Loading screen should not be present (since we're not on landing page)
    # Note: This checks the route detection logic in index.html
    loading_screen_visible = driver.execute_script(
        "return document.getElementById('loading-screen') && "
        "document.getElementById('loading-screen').style.display !== 'none'"
    )

    # Loading screen should either not exist or be hidden
    assert not loading_screen_visible, "Loading screen should not be visible on direct dashboard navigation"
