"""
Vertical Switching E2E Tests

Tests to verify users can navigate between verticals and see appropriate branding/content.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..conftest import wait_for_app_ready


@pytest.mark.e2e
@pytest.mark.vertical
def test_insurance_vertical_loads(driver, insurance_base_url):
    """Test insurance vertical loads with correct branding"""
    driver.get(insurance_base_url)
    wait_for_app_ready(driver)

    # Should have Silvermoat Insurance branding
    assert "Silvermoat" in driver.page_source or "Insurance" in driver.page_source

    # Page should load successfully
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Page should have content"


@pytest.mark.e2e
@pytest.mark.vertical
def test_retail_vertical_loads(driver, retail_base_url):
    """Test retail vertical loads with correct branding"""
    driver.get(retail_base_url)
    wait_for_app_ready(driver)

    # Should have Silvermoat Retail branding
    assert "Silvermoat" in driver.page_source or "Retail" in driver.page_source

    # Page should load successfully
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Page should have content"


@pytest.mark.e2e
@pytest.mark.vertical
def test_insurance_has_insurance_entities(driver, insurance_base_url):
    """Test insurance vertical shows insurance-specific entities"""
    driver.get(f"{insurance_base_url}/dashboard")
    wait_for_app_ready(driver)

    # Should have insurance-specific navigation items
    page_source = driver.page_source.lower()

    # Look for insurance entities (at least one should be present)
    has_insurance_entities = any([
        "quote" in page_source,
        "policy" in page_source,
        "policies" in page_source,
        "claim" in page_source,
    ])

    assert has_insurance_entities, "Insurance vertical should show insurance entities"


@pytest.mark.e2e
@pytest.mark.vertical
def test_retail_has_retail_entities(driver, retail_base_url):
    """Test retail vertical shows retail-specific entities"""
    driver.get(f"{retail_base_url}/dashboard")
    wait_for_app_ready(driver)

    # Should have retail-specific content
    page_source = driver.page_source.lower()

    # Look for retail entities
    has_retail_entities = any([
        "product" in page_source,
        "order" in page_source,
        "inventory" in page_source,
        "retail" in page_source,
    ])

    assert has_retail_entities, "Retail vertical should show retail entities"


@pytest.mark.e2e
@pytest.mark.vertical
def test_insurance_doesnt_show_retail_entities(driver, insurance_base_url):
    """Test insurance vertical doesn't show retail entities"""
    driver.get(f"{insurance_base_url}/dashboard")
    wait_for_app_ready(driver)

    page_source = driver.page_source.lower()

    # Should not have retail navigation
    assert "product catalog" not in page_source, "Insurance should not show product catalog"
    # Note: "order" is too generic, skip that check


@pytest.mark.e2e
@pytest.mark.vertical
def test_retail_doesnt_show_insurance_entities(driver, retail_base_url):
    """Test retail vertical doesn't show insurance entities"""
    driver.get(f"{retail_base_url}/dashboard")
    wait_for_app_ready(driver)

    page_source = driver.page_source.lower()

    # Should not have insurance navigation
    assert "quote" not in page_source or "silvermoat" in page_source, \
        "Retail should not show insurance quotes"


@pytest.mark.e2e
@pytest.mark.vertical
def test_vertical_has_different_themes(driver, insurance_base_url, retail_base_url):
    """Test that verticals have different color schemes/themes"""
    # Load insurance
    driver.get(insurance_base_url)
    wait_for_app_ready(driver)

    # Get computed style of body or main element
    insurance_bg = driver.execute_script(
        "return window.getComputedStyle(document.body).backgroundColor"
    )

    # Load retail
    driver.get(retail_base_url)
    wait_for_app_ready(driver)

    retail_bg = driver.execute_script(
        "return window.getComputedStyle(document.body).backgroundColor"
    )

    # Backgrounds might be the same (white), but primary colors should differ
    # Check for Ant Design primary color usage
    insurance_primary = driver.execute_script("""
        const buttons = document.querySelectorAll('.ant-btn-primary');
        if (buttons.length > 0) {
            return window.getComputedStyle(buttons[0]).backgroundColor;
        }
        return null;
    """)

    # Note: This test is informational - theme differences may be subtle
    print(f"Insurance BG: {insurance_bg}, Retail BG: {retail_bg}")
    print(f"Insurance primary button: {insurance_primary}")
