"""
Pytest configuration and fixtures for E2E tests.
"""
import os
import pytest
import boto3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from botocore.exceptions import ClientError


@pytest.fixture(scope="session")
def base_url():
    """
    Get base URL for E2E tests.

    Priority:
    1. SILVERMOAT_URL environment variable
    2. Fetch from CloudFormation stack (TEST_STACK_NAME or STACK_NAME)
    3. Default to localhost
    """
    # Check environment variable first
    url = os.environ.get("SILVERMOAT_URL")
    if url:
        return url.rstrip("/")

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get("TEST_STACK_NAME") or os.environ.get("STACK_NAME")
    if stack_name:
        try:
            region = os.environ.get("AWS_REGION", "us-east-1")
            cfn = boto3.client("cloudformation", region_name=region)
            response = cfn.describe_stacks(StackName=stack_name)

            outputs = response["Stacks"][0].get("Outputs", [])
            for output in outputs:
                if output["OutputKey"] == "WebUrl":
                    return output["OutputValue"].rstrip("/")
        except (ClientError, KeyError, IndexError):
            pass

    # Default to localhost
    return "http://localhost:5173"


@pytest.fixture(scope="session")
def api_base_url():
    """
    Get API base URL for E2E tests.

    Priority:
    1. SILVERMOAT_API_URL environment variable
    2. Fetch from CloudFormation stack (TEST_STACK_NAME or STACK_NAME)
    3. None (tests will skip API validation)
    """
    # Check environment variable first
    url = os.environ.get("SILVERMOAT_API_URL")
    if url:
        return url.rstrip("/")

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get("TEST_STACK_NAME") or os.environ.get("STACK_NAME")
    if stack_name:
        try:
            region = os.environ.get("AWS_REGION", "us-east-1")
            cfn = boto3.client("cloudformation", region_name=region)
            response = cfn.describe_stacks(StackName=stack_name)

            outputs = response["Stacks"][0].get("Outputs", [])
            for output in outputs:
                if output["OutputKey"] == "ApiBaseUrl":
                    return output["OutputValue"].rstrip("/")
        except (ClientError, KeyError, IndexError):
            pass

    return None


@pytest.fixture(scope="function")
def driver(base_url):
    """
    Selenium WebDriver fixture.

    Scope: function (new driver for each test)
    """
    chrome_options = Options()

    # Headless mode for CI/CD
    if os.environ.get("CI") or os.environ.get("HEADLESS") == "1":
        chrome_options.add_argument("--headless=new")

    # Additional options for CI/CD environments
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Create driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Set implicit wait
    driver.implicitly_wait(10)

    # Navigate to base URL
    driver.get(base_url)

    yield driver

    # Teardown
    driver.quit()


@pytest.fixture(scope="function")
def mobile_driver(base_url):
    """
    Selenium WebDriver with mobile viewport.

    Viewport: 375x667 (iPhone SE)
    """
    chrome_options = Options()

    if os.environ.get("CI") or os.environ.get("HEADLESS") == "1":
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # Mobile viewport
    mobile_emulation = {"deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0}}
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(base_url)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def tablet_driver(base_url):
    """
    Selenium WebDriver with tablet viewport.

    Viewport: 768x1024 (iPad)
    """
    chrome_options = Options()

    if os.environ.get("CI") or os.environ.get("HEADLESS") == "1":
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # Tablet viewport
    chrome_options.add_argument("--window-size=768,1024")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(base_url)

    yield driver

    driver.quit()
