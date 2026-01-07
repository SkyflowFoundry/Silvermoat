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

    # Check for "Learn More" buttons/links (Ant Design Button with href renders as <a>)
    learn_more_elements = driver.find_elements(By.XPATH, "//*[contains(., 'Learn More') and (self::button or self::a)]")
    assert len(learn_more_elements) >= 2, f"Should have at least 2 'Learn More' buttons/links, found {len(learn_more_elements)}"


@pytest.mark.e2e
@pytest.mark.landing
def test_landing_insurance_link(driver, landing_base_url):
    """Test insurance card has working link"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    # Find all "Learn More" links/buttons with href
    learn_more_links = driver.find_elements(By.XPATH, "//a[contains(., 'Learn More')][@href]")

    # Get all hrefs
    all_hrefs = [link.get_attribute('href') for link in learn_more_links]

    # Find insurance link (should contain 'insurance' in URL)
    insurance_links = [href for href in all_hrefs if href and 'insurance' in href.lower()]

    assert len(insurance_links) > 0, f"Should have insurance link. Found links: {all_hrefs}"

    # Verify href is non-empty and valid (deployment-provided URL)
    href = insurance_links[0]
    assert href and len(href) > 0, "Insurance link should have valid href"
    assert href.startswith('http'), f"Insurance link should be absolute URL, got: {href}"


@pytest.mark.e2e
@pytest.mark.landing
def test_landing_retail_link(driver, landing_base_url):
    """Test retail card has working link"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    # Find all "Learn More" links/buttons with href
    learn_more_links = driver.find_elements(By.XPATH, "//a[contains(., 'Learn More')][@href]")

    # Get all hrefs
    all_hrefs = [link.get_attribute('href') for link in learn_more_links]

    # Find retail link (should contain 'retail' in URL)
    retail_links = [href for href in all_hrefs if href and 'retail' in href.lower()]

    assert len(retail_links) > 0, f"Should have retail link. Found links: {all_hrefs}"

    # Verify href is non-empty and valid (deployment-provided URL)
    href = retail_links[0]
    assert href and len(href) > 0, "Retail link should have valid href"
    assert href.startswith('http'), f"Retail link should be absolute URL, got: {href}"


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
