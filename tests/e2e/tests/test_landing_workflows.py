"""
Landing Page E2E Tests

Tests for landing page functionality including:
- Page load and rendering
- Logo display
- Vertical cards visibility and navigation
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..conftest import wait_for_app_ready


@pytest.mark.e2e
@pytest.mark.landing
def test_landing_page_loads(driver, landing_base_url):
    """Test landing page loads successfully"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    # Page should load without error
    assert "Silvermoat" in driver.title.lower() or "silvermoat" in driver.page_source.lower()

    # Body should have content
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Landing page should have content"


@pytest.mark.e2e
@pytest.mark.landing
def test_landing_logo_displays(driver, landing_base_url):
    """Test logo displays correctly"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    # Find logo image
    logo = driver.find_element(By.CSS_SELECTOR, 'img[alt*="Silvermoat"]')
    assert logo.is_displayed(), "Logo should be visible"

    # Verify logo src
    logo_src = logo.get_attribute('src')
    assert 'silvermoat-logo.png' in logo_src, "Logo should point to silvermoat-logo.png"


@pytest.mark.e2e
@pytest.mark.landing
def test_landing_vertical_cards_visible(driver, landing_base_url):
    """Test insurance and retail cards are visible"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    page_source = driver.page_source.lower()

    # Both verticals should be mentioned
    assert "insurance" in page_source, "Insurance vertical should be displayed"
    assert "retail" in page_source, "Retail vertical should be displayed"

    # Check for "Learn More" buttons
    learn_more_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Learn More')]")
    assert len(learn_more_buttons) >= 2, "Should have at least 2 'Learn More' buttons"


@pytest.mark.e2e
@pytest.mark.landing
def test_landing_insurance_link(driver, landing_base_url):
    """Test insurance card has correct link"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    # Find insurance link
    insurance_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'insurance.silvermoat.net')]")
    assert len(insurance_links) > 0, "Should have insurance link"

    # Verify href
    insurance_link = insurance_links[0]
    href = insurance_link.get_attribute('href')
    assert 'insurance.silvermoat.net' in href, "Insurance link should point to insurance.silvermoat.net"


@pytest.mark.e2e
@pytest.mark.landing
def test_landing_retail_link(driver, landing_base_url):
    """Test retail card has correct link"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    # Find retail link
    retail_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'retail.silvermoat.net')]")
    assert len(retail_links) > 0, "Should have retail link"

    # Verify href
    retail_link = retail_links[0]
    href = retail_link.get_attribute('href')
    assert 'retail.silvermoat.net' in href, "Retail link should point to retail.silvermoat.net"


@pytest.mark.e2e
@pytest.mark.landing
def test_landing_page_responsive(driver, landing_base_url):
    """Test landing page is responsive"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    # Test desktop view
    driver.set_window_size(1200, 800)
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.is_displayed()

    # Test mobile view
    driver.set_window_size(375, 667)
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.is_displayed()

    # Cards should still be visible on mobile
    page_source = driver.page_source.lower()
    assert "insurance" in page_source
    assert "retail" in page_source
