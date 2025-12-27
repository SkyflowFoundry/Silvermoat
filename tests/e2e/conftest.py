"""Pytest configuration and fixtures for E2E tests."""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
    """Get the base URL from environment or use default."""
    url = os.getenv("SILVERMOAT_URL")
    if not url:
        pytest.skip("SILVERMOAT_URL environment variable not set")
    return url


@pytest.fixture(scope="session")
def api_url():
    """Get the API URL from environment or use default."""
    url = os.getenv("SILVERMOAT_API_URL")
    if not url:
        pytest.skip("SILVERMOAT_API_URL environment variable not set")
    return url


@pytest.fixture(scope="function")
def driver(base_url):
    """Create a Chrome WebDriver instance for each test."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Install ChromeDriver automatically
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def authenticated_driver(driver, base_url):
    """Create a driver with authentication if needed."""
    # For now, just navigate to base URL
    # Add authentication logic here if needed
    driver.get(base_url)
    return driver
