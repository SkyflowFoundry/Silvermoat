"""
Pytest configuration and fixtures for E2E tests.
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="session")
def base_url():
    """Get base URL from environment or use default."""
    return os.getenv("BASE_URL", "http://localhost:5173")


@pytest.fixture(scope="session")
def api_url():
    """Get API URL from environment or CloudFormation outputs."""
    return os.getenv("API_URL", "")


@pytest.fixture
def chrome_options():
    """Configure Chrome options for testing."""
    options = Options()

    # Required for running in CI
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # Additional options for stability
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")

    return options


@pytest.fixture
def driver(chrome_options):
    """Create and configure Chrome WebDriver."""
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)  # Wait up to 10 seconds for elements

    yield driver

    driver.quit()


@pytest.fixture
def wait_time():
    """Default explicit wait time in seconds."""
    return 10
