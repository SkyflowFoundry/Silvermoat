"""
E2E Smoke Tests

Basic smoke tests to verify application loads and responds.
Infrastructure-agnostic tests focusing on user-facing functionality.
"""

import pytest
import requests
from selenium.webdriver.common.by import By
from ..pages.home_page import HomePage
from ..conftest import wait_for_app_ready


@pytest.mark.e2e
@pytest.mark.smoke
def test_application_loads(driver, base_url):
    """Test that application loads successfully"""
    driver.get(base_url)
    wait_for_app_ready(driver)  # Wait for loading screen removal + React hydration

    # Wait for page to load
    assert "Silvermoat" in driver.title or len(driver.title) > 0, "Page title should be set"

    # Page should have some content
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Page should have content"


@pytest.mark.e2e
@pytest.mark.smoke
def test_api_connectivity(api_base_url):
    """Test that API is accessible from test environment"""
    response = requests.get(f"{api_base_url}/")

    assert response.status_code == 200, f"API should be accessible, got {response.status_code}"


@pytest.mark.e2e
@pytest.mark.smoke
def test_navigation_links_work(driver, base_url):
    """Test that navigation menu items are present and clickable"""
    home_page = HomePage(driver, base_url)
    home_page.load()

    # Should have navigation
    assert home_page.is_loaded(), "Home page should load with navigation"

    # Should have multiple navigation menu items (Ant Design uses role='menuitem')
    menu_items = home_page.get_navigation_links()
    assert len(menu_items) >= 5, f"Should have at least 5 navigation items, found {len(menu_items)}"

    # Menu items should be clickable (have role='menuitem')
    for item in menu_items:
        assert item.get_attribute('role') == 'menuitem', "Navigation items should have role='menuitem'"


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.responsive
def test_mobile_viewport(mobile_driver, base_url):
    """Test that application loads on mobile viewport (375x667)"""
    mobile_driver.get(base_url)

    # Should load successfully
    body = mobile_driver.find_element(By.TAG_NAME, "body")
    assert body.is_displayed()

    # Viewport should be mobile size
    width = mobile_driver.execute_script("return window.innerWidth")
    assert width <= 400, f"Mobile viewport should be ~375px wide, got {width}"


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.responsive
def test_tablet_viewport(tablet_driver, base_url):
    """Test that application loads on tablet viewport (768x1024)"""
    tablet_driver.get(base_url)

    # Should load successfully
    body = tablet_driver.find_element(By.TAG_NAME, "body")
    assert body.is_displayed()

    # Viewport should be tablet size
    width = tablet_driver.execute_script("return window.innerWidth")
    assert 700 <= width <= 800, f"Tablet viewport should be ~768px wide, got {width}"


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.responsive
def test_desktop_viewport(driver, base_url):
    """Test that application loads on desktop viewport (1920x1080)"""
    driver.get(base_url)

    # Should load successfully
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.is_displayed()

    # Viewport should be desktop size
    width = driver.execute_script("return window.innerWidth")
    assert width >= 1900, f"Desktop viewport should be ~1920px wide, got {width}"


@pytest.mark.e2e
@pytest.mark.smoke
def test_no_javascript_errors(driver, base_url):
    """Test that page loads without JavaScript console errors"""
    driver.get(base_url)

    # Get console logs
    logs = driver.get_log('browser')

    # Filter for severe errors (ignore warnings and info)
    severe_errors = [log for log in logs if log['level'] == 'SEVERE']

    # Should not have severe JavaScript errors
    assert len(severe_errors) == 0, f"Found {len(severe_errors)} JavaScript errors: {severe_errors}"
