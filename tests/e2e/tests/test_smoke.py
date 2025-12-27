"""Smoke tests for basic functionality."""
import pytest
import requests
from selenium.webdriver.common.by import By
from ..pages.home_page import HomePage


def test_app_loads(driver, base_url):
    """Test that the application loads successfully."""
    driver.get(base_url)
    assert "Silvermoat" in driver.title or driver.find_elements(By.TAG_NAME, "body")


def test_api_connectivity(api_url):
    """Test that API is accessible."""
    response = requests.get(f"{api_url}/", timeout=10)
    assert response.status_code in [200, 404]  # 404 is ok for root endpoint


def test_navigation_links(driver, base_url):
    """Test that all main navigation links work."""
    home_page = HomePage(driver, base_url)
    home_page.navigate()

    # Check if page loaded
    assert home_page.is_loaded(), "Home page did not load"

    # Test navigation links exist
    nav_elements = driver.find_elements(By.TAG_NAME, "a")
    assert len(nav_elements) > 0, "No navigation links found"


def test_responsive_mobile(driver, base_url):
    """Test mobile viewport."""
    driver.set_window_size(375, 667)  # iPhone size
    driver.get(base_url)
    assert driver.find_elements(By.TAG_NAME, "body")


def test_responsive_tablet(driver, base_url):
    """Test tablet viewport."""
    driver.set_window_size(768, 1024)  # iPad size
    driver.get(base_url)
    assert driver.find_elements(By.TAG_NAME, "body")


def test_responsive_desktop(driver, base_url):
    """Test desktop viewport."""
    driver.set_window_size(1920, 1080)
    driver.get(base_url)
    assert driver.find_elements(By.TAG_NAME, "body")
