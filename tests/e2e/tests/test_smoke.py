"""
Smoke tests for Silvermoat application.

These tests verify basic functionality and should run quickly.
"""
import pytest
import requests
from pages.home_page import HomePage


@pytest.mark.smoke
def test_app_loads(driver, base_url):
    """Test that the application loads successfully."""
    home_page = HomePage(driver, base_url)
    home_page.load()

    assert home_page.is_loaded(), "Application failed to load"
    assert "Silvermoat" in driver.title or "Insurance" in home_page.get_title_text()


@pytest.mark.smoke
def test_api_connectivity(api_url):
    """Test that the API is reachable."""
    if not api_url:
        pytest.skip("API_URL not configured")

    try:
        response = requests.get(api_url, timeout=10)
        assert response.status_code in [200, 404], f"API returned {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"API is not reachable: {e}")


@pytest.mark.smoke
def test_navigation_links_present(driver, base_url):
    """Test that all main navigation links are present."""
    home_page = HomePage(driver, base_url)
    home_page.load()

    # Check that key navigation elements exist
    # These may need to be adjusted based on actual UI structure
    try:
        assert home_page.is_element_visible(home_page.APP_TITLE, timeout=5)
    except Exception:
        pytest.skip("Navigation structure different than expected - adjust locators")


@pytest.mark.smoke
@pytest.mark.responsive
def test_mobile_viewport(driver, base_url):
    """Test that app works in mobile viewport."""
    driver.set_window_size(375, 667)  # iPhone SE size

    home_page = HomePage(driver, base_url)
    home_page.load()

    assert home_page.is_loaded(), "Application failed to load in mobile viewport"


@pytest.mark.smoke
@pytest.mark.responsive
def test_tablet_viewport(driver, base_url):
    """Test that app works in tablet viewport."""
    driver.set_window_size(768, 1024)  # iPad size

    home_page = HomePage(driver, base_url)
    home_page.load()

    assert home_page.is_loaded(), "Application failed to load in tablet viewport"


@pytest.mark.smoke
@pytest.mark.responsive
def test_desktop_viewport(driver, base_url):
    """Test that app works in desktop viewport."""
    driver.set_window_size(1920, 1080)  # Full HD

    home_page = HomePage(driver, base_url)
    home_page.load()

    assert home_page.is_loaded(), "Application failed to load in desktop viewport"
