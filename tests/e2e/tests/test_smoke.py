"""
Smoke Tests
Basic functionality tests to ensure application loads and core features work
"""

import pytest
import requests
from pages.home_page import HomePage


@pytest.mark.smoke
def test_application_loads(driver, base_url):
    """Test that the application loads successfully"""
    home = HomePage(driver, base_url)
    home.navigate()
    assert home.is_loaded(), "Application failed to load"


@pytest.mark.smoke
def test_api_connectivity(api_url):
    """Test API is accessible"""
    if not api_url:
        pytest.skip("API URL not configured")

    response = requests.get(f"{api_url}/", timeout=10)
    assert response.status_code in [200, 404], f"API not accessible: {response.status_code}"


@pytest.mark.smoke
def test_navigation_links(driver, base_url):
    """Test that main navigation links work"""
    home = HomePage(driver, base_url)
    home.navigate()

    # Test quotes navigation
    home.click_quotes_link()
    assert '/quotes' in home.get_current_url()

    # Test policies navigation
    home.navigate()
    home.click_policies_link()
    assert '/policies' in home.get_current_url()

    # Test claims navigation
    home.navigate()
    home.click_claims_link()
    assert '/claims' in home.get_current_url()


@pytest.mark.smoke
@pytest.mark.responsive
def test_mobile_viewport(mobile_driver, base_url):
    """Test application works on mobile viewport"""
    home = HomePage(mobile_driver, base_url)
    home.navigate()
    assert home.is_loaded(), "Application failed to load on mobile"


@pytest.mark.smoke
@pytest.mark.responsive
def test_tablet_viewport(tablet_driver, base_url):
    """Test application works on tablet viewport"""
    home = HomePage(tablet_driver, base_url)
    home.navigate()
    assert home.is_loaded(), "Application failed to load on tablet"


@pytest.mark.smoke
@pytest.mark.responsive
def test_desktop_viewport(driver, base_url):
    """Test application works on desktop viewport"""
    home = HomePage(driver, base_url)
    home.navigate()
    assert home.is_loaded(), "Application failed to load on desktop"
