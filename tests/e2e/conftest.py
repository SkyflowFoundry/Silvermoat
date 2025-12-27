"""
Pytest fixtures and configuration for E2E tests
Provides WebDriver setup, test data, and helper fixtures
"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_base_url():
    """Get base URL for the application"""
    # Priority: env var > CloudFormation stack outputs > default
    if os.getenv('SILVERMOAT_URL'):
        return os.getenv('SILVERMOAT_URL')

    # Try to fetch from CloudFormation if stack name provided
    stack_name = os.getenv('TEST_STACK_NAME') or os.getenv('STACK_NAME')
    if stack_name:
        try:
            from utils.aws_helpers import get_stack_output
            url = get_stack_output(stack_name, 'WebUrl')
            if url:
                return url
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # Default to localhost for development
    return os.getenv('BASE_URL', 'http://localhost:5173')


def get_api_url():
    """Get API base URL"""
    if os.getenv('SILVERMOAT_API_URL'):
        return os.getenv('SILVERMOAT_API_URL')

    stack_name = os.getenv('TEST_STACK_NAME') or os.getenv('STACK_NAME')
    if stack_name:
        try:
            from utils.aws_helpers import get_stack_output
            url = get_stack_output(stack_name, 'ApiBaseUrl')
            if url:
                return url
        except Exception:
            pass

    return os.getenv('API_BASE_URL', '')


@pytest.fixture(scope='session')
def base_url():
    """Application base URL"""
    return get_base_url()


@pytest.fixture(scope='session')
def api_url():
    """API base URL"""
    return get_api_url()


@pytest.fixture
def chrome_options():
    """Chrome options for WebDriver"""
    options = Options()

    # Run headless in CI/CD
    if os.getenv('CI') or os.getenv('HEADLESS'):
        options.add_argument('--headless=new')

    # Standard options for stability
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    return options


@pytest.fixture
def driver(chrome_options):
    """WebDriver instance for desktop testing"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)  # 10 second implicit wait
    yield driver
    driver.quit()


@pytest.fixture
def mobile_driver(chrome_options):
    """WebDriver instance for mobile viewport testing"""
    chrome_options.add_argument('--window-size=375,667')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(375, 667)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def tablet_driver(chrome_options):
    """WebDriver instance for tablet viewport testing"""
    chrome_options.add_argument('--window-size=768,1024')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(768, 1024)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def test_quote_data():
    """Test data for quote creation"""
    return {
        'name': 'John Test User',
        'zip': '12345'
    }


@pytest.fixture
def test_claim_data():
    """Test data for claim creation"""
    return {
        'claimNumber': 'CLM-TEST-001',
        'claimantName': 'Jane Test Claimant',
        'incidentDate': '12/15/2024',
        'description': 'Test incident description for E2E testing purposes',
        'amount': '5000.00',
        'status': 'PENDING'
    }


@pytest.fixture
def test_payment_data():
    """Test data for payment creation"""
    return {
        'paymentNumber': 'PAY-TEST-001',
        'amount': '1500.00',
        'method': 'Credit Card',
        'status': 'COMPLETED'
    }
