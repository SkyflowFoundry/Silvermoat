"""
Healthcare Workflow E2E Tests

Tests for healthcare-specific UI workflows including:
- Viewing patients, appointments, prescriptions, billing
- Chatbot interactions
- Seeding demo data
"""

import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..conftest import wait_for_app_ready


@pytest.mark.e2e
@pytest.mark.healthcare
def test_healthcare_landing_page_loads(driver, healthcare_base_url):
    """Test healthcare landing page loads successfully"""
    driver.get(healthcare_base_url)
    wait_for_app_ready(driver)

    # Page should have content
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Landing page should have content"

    # Should show healthcare branding
    page_source = driver.page_source.lower()
    assert "healthcare" in page_source or "silvermoat" in page_source


@pytest.mark.e2e
@pytest.mark.healthcare
def test_healthcare_navigation_exists(driver, healthcare_base_url):
    """Test healthcare app has navigation"""
    driver.get(healthcare_base_url)
    wait_for_app_ready(driver)

    # Look for common navigation elements
    page_source = driver.page_source.lower()

    # Should have navigation to key entities
    has_navigation = any([
        "patient" in page_source,
        "appointment" in page_source,
        "prescription" in page_source,
        "billing" in page_source,
        "dashboard" in page_source,
    ])
    assert has_navigation, "Healthcare portal should have navigation to key entities"


@pytest.mark.e2e
@pytest.mark.healthcare
def test_healthcare_patients_page_loads(driver, healthcare_base_url):
    """Test patients page loads (even if empty)"""
    driver.get(f"{healthcare_base_url}/patients")
    wait_for_app_ready(driver)

    # Page should render without error
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Patients page should have content"

    # Should show patient-related content
    page_source = driver.page_source.lower()
    # Accept either "patient" text or table/list components
    has_patient_context = "patient" in page_source or "table" in page_source
    assert has_patient_context, "Patients page should show patient-related content"


@pytest.mark.e2e
@pytest.mark.healthcare
def test_healthcare_appointments_page_loads(driver, healthcare_base_url):
    """Test appointments page loads (even if empty)"""
    driver.get(f"{healthcare_base_url}/appointments")
    wait_for_app_ready(driver)

    # Page should render without error
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.text.strip() != "", "Appointments page should have content"

    # Should show appointment-related content
    page_source = driver.page_source.lower()
    has_appointment_context = "appointment" in page_source or "table" in page_source
    assert has_appointment_context, "Appointments page should show appointment-related content"


@pytest.mark.e2e
@pytest.mark.healthcare
def test_healthcare_chatbot_visible(driver, healthcare_base_url):
    """Test chatbot button is visible"""
    driver.get(healthcare_base_url)
    wait_for_app_ready(driver)

    # Look for chatbot trigger button (floating action button pattern)
    page_source = driver.page_source.lower()
    has_chat = "chat" in page_source or "message" in page_source or "assistant" in page_source

    # Basic check - chatbot UI elements should be present
    assert has_chat, "Healthcare portal should have chatbot functionality"


@pytest.mark.e2e
@pytest.mark.healthcare
def test_healthcare_api_accessible(driver, healthcare_base_url, healthcare_api_url):
    """Test healthcare API is accessible"""
    # Test API health/connectivity
    try:
        # Try accessing patients endpoint
        response = requests.get(f"{healthcare_api_url}patient", timeout=10)
        # API should respond (200 OK or 4xx is fine - just needs to be reachable)
        assert response.status_code < 500, f"Healthcare API should be accessible, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Healthcare API not accessible: {e}")
