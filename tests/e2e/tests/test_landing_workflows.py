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
    """Test insurance, retail, and healthcare cards are visible"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    page_source = driver.page_source.lower()

    # All verticals should be mentioned
    assert "insurance" in page_source, "Insurance vertical should be displayed"
    assert "retail" in page_source, "Retail vertical should be displayed"
    assert "healthcare" in page_source, "Healthcare vertical should be displayed"

    # Check for "Enter Portal" buttons/links (Ant Design Button with href renders as <a>)
    enter_portal_elements = driver.find_elements(By.XPATH, "//*[contains(., 'Enter Portal') and (self::button or self::a)]")
    assert len(enter_portal_elements) >= 3, f"Should have at least 3 'Enter Portal' buttons/links, found {len(enter_portal_elements)}"


@pytest.mark.e2e
@pytest.mark.landing
def test_landing_insurance_link(driver, landing_base_url):
    """Test insurance card has working link"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    # Find all "Enter Portal" links/buttons with href
    enter_portal_links = driver.find_elements(By.XPATH, "//a[contains(., 'Enter Portal')][@href]")

    # Get all hrefs
    all_hrefs = [link.get_attribute('href') for link in enter_portal_links]

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

    # Find all "Enter Portal" links/buttons with href
    enter_portal_links = driver.find_elements(By.XPATH, "//a[contains(., 'Enter Portal')][@href]")

    # Get all hrefs
    all_hrefs = [link.get_attribute('href') for link in enter_portal_links]

    # Find retail link (should contain 'retail' in URL)
    retail_links = [href for href in all_hrefs if href and 'retail' in href.lower()]

    assert len(retail_links) > 0, f"Should have retail link. Found links: {all_hrefs}"

    # Verify href is non-empty and valid (deployment-provided URL)
    href = retail_links[0]
    assert href and len(href) > 0, "Retail link should have valid href"
    assert href.startswith('http'), f"Retail link should be absolute URL, got: {href}"


@pytest.mark.e2e
@pytest.mark.landing
def test_landing_healthcare_link(driver, landing_base_url):
    """Test healthcare card has working link"""
    driver.get(landing_base_url)
    wait_for_app_ready(driver)

    # Find all "Enter Portal" links/buttons with href
    enter_portal_links = driver.find_elements(By.XPATH, "//a[contains(., 'Enter Portal')][@href]")

    # Get all hrefs
    all_hrefs = [link.get_attribute('href') for link in enter_portal_links]

    # Find healthcare link (should contain 'healthcare' in URL)
    healthcare_links = [href for href in all_hrefs if href and 'healthcare' in href.lower()]

    assert len(healthcare_links) > 0, f"Should have healthcare link. Found links: {all_hrefs}"

    # Verify href is non-empty and valid (deployment-provided URL)
    href = healthcare_links[0]
    assert href and len(href) > 0, "Healthcare link should have valid href"
    assert href.startswith('http'), f"Healthcare link should be absolute URL, got: {href}"


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
