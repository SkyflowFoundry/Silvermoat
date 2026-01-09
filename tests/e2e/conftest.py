"""
E2E Test Configuration

Pytest fixtures for end-to-end browser testing with Selenium.
Tests are infrastructure-agnostic and focus on user-facing functionality.
"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
    """
    Get application base URL from environment or CloudFormation stack.
    Defaults to insurance vertical for backwards compatibility.

    Priority:
    1. SILVERMOAT_URL or INSURANCE_URL environment variable
    2. CloudFormation stack outputs (via STACK_NAME)
    3. Default localhost
    """
    # Check environment variable first
    app_url = os.environ.get('SILVERMOAT_URL') or os.environ.get('INSURANCE_URL')
    if app_url:
        return app_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            # Try insurance-specific URL first, then generic
            if 'InsuranceUiBucketWebsiteURL' in outputs:
                return outputs['InsuranceUiBucketWebsiteURL'].rstrip('/')
            if 'WebUrl' in outputs:
                return outputs['WebUrl'].rstrip('/')
            if 'CloudFrontUrl' in outputs:
                url = outputs['CloudFrontUrl'].rstrip('/')
                # For CloudFront with wildcard domain, append insurance subdomain
                if 'InsuranceDomainUrl' in outputs:
                    return outputs['InsuranceDomainUrl'].rstrip('/')
                return url
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # Fallback to localhost
    return os.environ.get('BASE_URL', 'http://localhost:5173').rstrip('/')


@pytest.fixture(scope="session")
def insurance_base_url():
    """Get insurance vertical base URL"""
    # Check environment variable first
    app_url = os.environ.get('INSURANCE_URL')
    if app_url:
        return app_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            if 'InsuranceDomainUrl' in outputs:
                return outputs['InsuranceDomainUrl'].rstrip('/')
            if 'InsuranceUiBucketWebsiteURL' in outputs:
                return outputs['InsuranceUiBucketWebsiteURL'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # Fallback to base_url
    return os.environ.get('BASE_URL', 'http://localhost:5173').rstrip('/')


@pytest.fixture(scope="session")
def retail_base_url():
    """Get retail vertical base URL"""
    # Check environment variable first
    app_url = os.environ.get('RETAIL_URL')
    if app_url:
        return app_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            if 'RetailDomainUrl' in outputs:
                return outputs['RetailDomainUrl'].rstrip('/')
            if 'RetailUiBucketWebsiteURL' in outputs:
                return outputs['RetailUiBucketWebsiteURL'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # No fallback - skip retail tests if not configured
    pytest.skip("RETAIL_URL not configured")


@pytest.fixture(scope="session")
def healthcare_base_url():
    """Get healthcare vertical base URL"""
    # Check environment variable first
    app_url = os.environ.get('HEALTHCARE_URL')
    if app_url:
        return app_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            if 'HealthcareDomainUrl' in outputs:
                return outputs['HealthcareDomainUrl'].rstrip('/')
            if 'HealthcareUiBucketWebsiteURL' in outputs:
                return outputs['HealthcareUiBucketWebsiteURL'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # No fallback - skip healthcare tests if not configured
    pytest.skip("HEALTHCARE_URL not configured")


@pytest.fixture(scope="session")
def fintech_base_url():
    """Get fintech vertical base URL"""
    # Check environment variable first
    app_url = os.environ.get('FINTECH_URL')
    if app_url:
        return app_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            if 'FintechDomainUrl' in outputs:
                return outputs['FintechDomainUrl'].rstrip('/')
            if 'FintechUiBucketWebsiteURL' in outputs:
                return outputs['FintechUiBucketWebsiteURL'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # No fallback - skip fintech tests if not configured
    pytest.skip("FINTECH_URL not configured")


@pytest.fixture(scope="session")
def landing_base_url():
    """Get landing page base URL"""
    # Check environment variable first
    app_url = os.environ.get('LANDING_URL')
    if app_url:
        return app_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            if 'LandingDomainUrl' in outputs:
                return outputs['LandingDomainUrl'].rstrip('/')
            if 'LandingUiBucketWebsiteURL' in outputs:
                return outputs['LandingUiBucketWebsiteURL'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch stack outputs: {e}")

    # No fallback - skip landing tests if not configured
    pytest.skip("LANDING_URL not configured")


@pytest.fixture(scope="session")
def api_base_url():
    """Get API base URL for E2E tests (defaults to insurance vertical)"""
    # Check environment variable first
    api_url = os.environ.get('SILVERMOAT_API_URL') or os.environ.get('INSURANCE_API_URL')
    if api_url:
        return api_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            # Try insurance-specific API first, then generic
            if 'InsuranceApiUrl' in outputs:
                return outputs['InsuranceApiUrl'].rstrip('/')
            if 'ApiBaseUrl' in outputs:
                return outputs['ApiBaseUrl'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch API URL: {e}")

    return os.environ.get('API_BASE_URL', 'http://localhost:3000').rstrip('/')


@pytest.fixture(scope="session")
def insurance_api_url():
    """Get insurance vertical API URL"""
    # Check environment variable first
    api_url = os.environ.get('INSURANCE_API_URL')
    if api_url:
        return api_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            if 'InsuranceApiUrl' in outputs:
                return outputs['InsuranceApiUrl'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch API URL: {e}")

    # Fallback to api_base_url
    return os.environ.get('API_BASE_URL', 'http://localhost:3000').rstrip('/')


@pytest.fixture(scope="session")
def retail_api_url():
    """Get retail vertical API URL"""
    # Check environment variable first
    api_url = os.environ.get('RETAIL_API_URL')
    if api_url:
        return api_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            if 'RetailApiUrl' in outputs:
                return outputs['RetailApiUrl'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch API URL: {e}")

    # No fallback - skip retail tests if not configured
    pytest.skip("RETAIL_API_URL not configured")


@pytest.fixture(scope="session")
def healthcare_api_url():
    """Get healthcare vertical API URL"""
    # Check environment variable first
    api_url = os.environ.get('HEALTHCARE_API_URL')
    if api_url:
        return api_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            if 'HealthcareApiUrl' in outputs:
                return outputs['HealthcareApiUrl'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch API URL: {e}")

    # No fallback - skip healthcare tests if not configured
    pytest.skip("HEALTHCARE_API_URL not configured")


@pytest.fixture(scope="session")
def fintech_api_url():
    """Get fintech vertical API URL"""
    # Check environment variable first
    api_url = os.environ.get('FINTECH_API_URL')
    if api_url:
        return api_url.rstrip('/')

    # Try to fetch from CloudFormation stack
    stack_name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if stack_name:
        try:
            import boto3
            cfn = boto3.client('cloudformation')
            response = cfn.describe_stacks(StackName=stack_name)
            outputs = {o['OutputKey']: o['OutputValue'] for o in response['Stacks'][0].get('Outputs', [])}
            if 'FintechApiUrl' in outputs:
                return outputs['FintechApiUrl'].rstrip('/')
        except Exception as e:
            print(f"Warning: Could not fetch API URL: {e}")

    # No fallback - skip fintech tests if not configured
    pytest.skip("FINTECH_API_URL not configured")


@pytest.fixture
def driver():
    """
    Create Selenium WebDriver instance with Chrome.
    Supports headless mode via HEADLESS environment variable.
    """
    chrome_options = Options()

    # Headless mode for CI/CD
    if os.environ.get('HEADLESS', '').lower() in ['1', 'true', 'yes']:
        chrome_options.add_argument('--headless')

    # Standard options for stability
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    # Create driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver

    # Cleanup
    driver.quit()


@pytest.fixture
def mobile_driver():
    """Chrome WebDriver with mobile viewport (375x667)"""
    chrome_options = Options()

    if os.environ.get('HEADLESS', '').lower() in ['1', 'true', 'yes']:
        chrome_options.add_argument('--headless')

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    # Don't set --window-size when using mobileEmulation - deviceMetrics handles viewport

    mobile_emulation = {
        "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver

    driver.quit()


@pytest.fixture
def tablet_driver():
    """Chrome WebDriver with tablet viewport (768x1024)"""
    chrome_options = Options()

    if os.environ.get('HEADLESS', '').lower() in ['1', 'true', 'yes']:
        chrome_options.add_argument('--headless')

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=768,1024')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver

    driver.quit()


def wait_for_app_ready(driver, timeout=15):
    """Wait for app to be fully loaded and interactive (includes 3s+ loading screen)"""
    try:
        # Wait for React root div to exist
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "root"))
        )

        # CRITICAL: Wait for loading screen to be REMOVED from DOM (not just fade-out)
        # Loading screen has 3s minimum + 800ms fade = 3.8s total minimum
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(
                "return !document.getElementById('loading-screen')"
            )
        )
        print("Loading screen removed")

        # Wait for any Ant Design loading spinners to disappear
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(
                "return document.readyState === 'complete' && "
                "document.querySelectorAll('.ant-spin').length === 0"
            )
        )

        return True
    except TimeoutException:
        print("Warning: App ready check timed out")
        return False
