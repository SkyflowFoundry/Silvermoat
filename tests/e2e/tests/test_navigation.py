"""
Navigation E2E Tests

Tests for navigation flows including:
- Loading page tagline display
- Customer portal home button navigation
- Employee portal logo navigation
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..conftest import wait_for_app_ready


@pytest.mark.e2e
@pytest.mark.navigation
def test_loading_page_shows_tagline(driver, base_url):
    """Test loading page displays tagline 'Securing your future'"""
    # Navigate to landing page
    driver.get(base_url)

    # Check for loading screen elements (they may disappear quickly)
    # We're checking the HTML source to ensure the tagline exists
    page_source = driver.page_source
    assert "Securing your future" in page_source, "Tagline should be in page source"


@pytest.mark.e2e
@pytest.mark.navigation
def test_customer_portal_home_button(driver, base_url):
    """Test customer portal has home button that navigates to landing page"""
    # Navigate to customer dashboard
    driver.get(f"{base_url}/customer/dashboard")
    wait_for_app_ready(driver)

    # Wait for page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Look for home button
    try:
        # Find home button by icon or text
        home_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Home')]"))
        )

        # Click home button
        home_button.click()

        # Should navigate to landing page
        wait.until(EC.url_to_be(base_url + "/"))
        assert driver.current_url == base_url + "/"
    except Exception as e:
        pytest.fail(f"Home button not found or navigation failed: {e}")


@pytest.mark.e2e
@pytest.mark.navigation
def test_employee_portal_logo_navigates_home(driver, base_url):
    """Test employee portal logo navigates to landing page"""
    # Navigate to employee dashboard
    driver.get(f"{base_url}/dashboard")
    wait_for_app_ready(driver)

    # Wait for page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Look for logo/header
    try:
        # Find the logo image or text
        logo_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='Silvermoat Insurance']"))
        )

        # Click on logo or its parent container
        parent = logo_element.find_element(By.XPATH, "./..")
        parent.click()

        # Should navigate to landing page
        wait.until(EC.url_to_be(base_url + "/"))
        assert driver.current_url == base_url + "/"
    except Exception as e:
        pytest.fail(f"Logo not found or navigation failed: {e}")
