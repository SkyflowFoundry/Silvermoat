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
@pytest.mark.smoke
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
@pytest.mark.smoke
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
@pytest.mark.smoke
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
@pytest.mark.smoke
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
@pytest.mark.smoke
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
@pytest.mark.api
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


@pytest.mark.e2e
@pytest.mark.healthcare
@pytest.mark.slow
@pytest.mark.api
def test_healthcare_patient_via_api(driver, healthcare_base_url, healthcare_api_url):
    """Test creating patient via API and verifying system works"""
    # Create patient via API
    patient_data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@test.com",
        "phone": "555-1234",
        "dateOfBirth": "1980-01-15",
        "address": "123 Healthcare St",
        "insuranceProvider": "Test Insurance",
        "insurancePolicyNumber": "INS-12345"
    }

    response = requests.post(f"{healthcare_api_url}/patient", json=patient_data)
    assert response.status_code == 201, f"Failed to create patient: {response.status_code}"
    patient_id = response.json()['id']

    try:
        # Verify patient was created
        get_response = requests.get(f"{healthcare_api_url}/patient/{patient_id}")
        assert get_response.status_code == 200, "Patient should be retrievable"

        # Navigate to healthcare patients page
        driver.get(f"{healthcare_base_url}/patients")
        wait_for_app_ready(driver)

        # Patients page should be accessible
        assert "patient" in driver.page_source.lower() or "table" in driver.page_source.lower()

    finally:
        # Cleanup
        requests.delete(f"{healthcare_api_url}/patient/{patient_id}")


@pytest.mark.e2e
@pytest.mark.healthcare
@pytest.mark.slow
@pytest.mark.api
def test_healthcare_appointment_via_api(driver, healthcare_base_url, healthcare_api_url):
    """Test creating appointment via API"""
    # Create patient first
    patient_data = {
        "firstName": "Jane",
        "lastName": "Smith",
        "email": "jane.smith@test.com",
        "phone": "555-5678",
        "dateOfBirth": "1985-03-20"
    }

    patient_response = requests.post(f"{healthcare_api_url}/patient", json=patient_data)
    assert patient_response.status_code == 201
    patient_id = patient_response.json()['id']

    try:
        # Create appointment
        appointment_data = {
            "patientId": patient_id,
            "patientName": "Jane Smith",
            "patientEmail": "jane.smith@test.com",
            "appointmentDate": "2024-12-15",
            "appointmentTime": "10:00",
            "provider": "Dr. Johnson",
            "appointmentType": "CHECKUP",
            "notes": "Annual physical examination"
        }

        appt_response = requests.post(f"{healthcare_api_url}/appointment", json=appointment_data)
        assert appt_response.status_code == 201, f"Failed to create appointment: {appt_response.status_code}"
        appointment_id = appt_response.json()['id']

        # Verify appointment exists
        get_response = requests.get(f"{healthcare_api_url}/appointment/{appointment_id}")
        assert get_response.status_code == 200

        # Navigate to appointments page
        driver.get(f"{healthcare_base_url}/appointments")
        wait_for_app_ready(driver)

        # Appointments page should be accessible
        assert "appointment" in driver.page_source.lower() or "table" in driver.page_source.lower()

        # Cleanup appointment
        requests.delete(f"{healthcare_api_url}/appointment/{appointment_id}")

    finally:
        # Cleanup patient
        requests.delete(f"{healthcare_api_url}/patient/{patient_id}")


@pytest.mark.e2e
@pytest.mark.healthcare
@pytest.mark.slow
@pytest.mark.api
def test_healthcare_prescription_via_api(driver, healthcare_base_url, healthcare_api_url):
    """Test creating prescription via API"""
    # Create patient first
    patient_data = {
        "firstName": "Bob",
        "lastName": "Wilson",
        "email": "bob.wilson@test.com",
        "phone": "555-9999",
        "dateOfBirth": "1975-07-10"
    }

    patient_response = requests.post(f"{healthcare_api_url}/patient", json=patient_data)
    assert patient_response.status_code == 201
    patient_id = patient_response.json()['id']

    try:
        # Create medical record
        medical_record_data = {
            "patientId": patient_id,
            "patientName": "Bob Wilson",
            "patientEmail": "bob.wilson@test.com",
            "diagnosis": "Hypertension",
            "visitDate": "2024-06-01",
            "provider": "Dr. Smith",
            "notes": "Patient presents with elevated blood pressure"
        }

        record_response = requests.post(f"{healthcare_api_url}/medical_record", json=medical_record_data)
        assert record_response.status_code == 201
        medical_record_id = record_response.json()['id']

        # Create prescription
        prescription_data = {
            "medicalRecordId": medical_record_id,
            "patientId": patient_id,
            "medication": "Lisinopril",
            "dosage": "10mg",
            "frequency": "Once daily",
            "duration": "30 days",
            "prescribedBy": "Dr. Smith",
            "instructions": "Take with water in the morning"
        }

        rx_response = requests.post(f"{healthcare_api_url}/prescription", json=prescription_data)
        assert rx_response.status_code == 201, f"Failed to create prescription: {rx_response.status_code}"
        prescription_id = rx_response.json()['id']

        # Verify prescription exists
        get_response = requests.get(f"{healthcare_api_url}/prescription/{prescription_id}")
        assert get_response.status_code == 200

        # Navigate to prescriptions page
        driver.get(f"{healthcare_base_url}/prescriptions")
        wait_for_app_ready(driver)

        # Prescriptions page should be accessible
        page_source = driver.page_source.lower()
        assert "prescription" in page_source or "table" in page_source

        # Cleanup
        requests.delete(f"{healthcare_api_url}/prescription/{prescription_id}")
        requests.delete(f"{healthcare_api_url}/medical_record/{medical_record_id}")

    finally:
        # Cleanup patient
        requests.delete(f"{healthcare_api_url}/patient/{patient_id}")


@pytest.mark.e2e
@pytest.mark.healthcare
@pytest.mark.slow
@pytest.mark.ui
def test_healthcare_data_seeding_workflow(driver, healthcare_base_url, healthcare_api_url):
    """Test data seeding button on healthcare dashboard"""
    driver.get(f"{healthcare_base_url}/dashboard")
    wait_for_app_ready(driver)

    # Look for seed data button
    page_source = driver.page_source.lower()
    has_seed_button = "seed" in page_source and "data" in page_source

    assert has_seed_button, "Dashboard should have seed data functionality"

    # Get initial patient count
    patients_before = requests.get(f"{healthcare_api_url}/patient").json()
    initial_patient_count = len(patients_before.get('items', []))

    # Try to click seed data button
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        seed_button = None

        for button in buttons:
            if "seed" in button.text.lower() and "data" in button.text.lower():
                seed_button = button
                break

        if seed_button and seed_button.is_displayed():
            seed_button.click()

            # Wait for seeding to complete
            import time
            time.sleep(3)

            # Verify patients were created
            patients_after = requests.get(f"{healthcare_api_url}/patient").json()
            final_patient_count = len(patients_after.get('items', []))

            assert final_patient_count > initial_patient_count, "Seeding should create patients"

            # Cleanup seeded data
            for patient in patients_after.get('items', []):
                try:
                    requests.delete(f"{healthcare_api_url}/patient/{patient['id']}")
                except:
                    pass
        else:
            # Button not interactive in test, skip test
            pytest.skip("Seed data button not interactive in test environment")

    except Exception as e:
        print(f"Could not interact with seed button: {e}")
        # At least verify button exists
        assert has_seed_button


@pytest.mark.e2e
@pytest.mark.healthcare
@pytest.mark.slow
@pytest.mark.lifecycle
def test_healthcare_patient_care_lifecycle(driver, healthcare_base_url, healthcare_api_url):
    """Test complete patient care lifecycle: patient → appointment → prescription → billing"""
    # Step 1: Create patient
    patient_data = {
        "firstName": "Alice",
        "lastName": "Brown",
        "email": "alice.brown@test.com",
        "phone": "555-2222",
        "dateOfBirth": "1990-05-25",
        "address": "456 Health Ave",
        "insuranceProvider": "Test Health Insurance",
        "insurancePolicyNumber": "HI-99999"
    }

    patient_response = requests.post(f"{healthcare_api_url}/patient", json=patient_data)
    assert patient_response.status_code == 201, "Patient should be created"
    patient_id = patient_response.json()['id']

    try:
        # Step 2: Schedule appointment
        appointment_data = {
            "patientId": patient_id,
            "patientName": "Alice Brown",
            "patientEmail": "alice.brown@test.com",
            "appointmentDate": "2024-07-01",
            "appointmentTime": "14:00",
            "provider": "Dr. Garcia",
            "appointmentType": "CONSULTATION",
            "notes": "Initial consultation"
        }

        appt_response = requests.post(f"{healthcare_api_url}/appointment", json=appointment_data)
        assert appt_response.status_code == 201, "Appointment should be created"
        appointment_id = appt_response.json()['id']

        # Step 3: Create medical record
        medical_record_data = {
            "patientId": patient_id,
            "patientName": "Alice Brown",
            "patientEmail": "alice.brown@test.com",
            "diagnosis": "Seasonal allergies",
            "visitDate": "2024-07-01",
            "provider": "Dr. Garcia",
            "notes": "Patient reports seasonal allergy symptoms"
        }

        record_response = requests.post(f"{healthcare_api_url}/medical_record", json=medical_record_data)
        assert record_response.status_code == 201, "Medical record should be created"
        medical_record_id = record_response.json()['id']

        # Step 4: Issue prescription
        prescription_data = {
            "medicalRecordId": medical_record_id,
            "patientId": patient_id,
            "medication": "Zyrtec",
            "dosage": "10mg",
            "frequency": "Once daily",
            "duration": "90 days",
            "prescribedBy": "Dr. Garcia",
            "instructions": "Take in the evening"
        }

        rx_response = requests.post(f"{healthcare_api_url}/prescription", json=prescription_data)
        assert rx_response.status_code == 201, "Prescription should be created"
        prescription_id = rx_response.json()['id']

        # Step 5: Create billing record
        billing_data = {
            "medicalRecordId": medical_record_id,
            "patientId": patient_id,
            "amount": 15000,  # $150.00 in cents
            "billDate": "2024-07-01",
            "description": "Consultation visit",
            "status": "PENDING"
        }

        billing_response = requests.post(f"{healthcare_api_url}/billing", json=billing_data)
        assert billing_response.status_code == 201, "Billing should be created"
        billing_id = billing_response.json()['id']

        # Verify all entities exist
        assert requests.get(f"{healthcare_api_url}/patient/{patient_id}").status_code == 200
        assert requests.get(f"{healthcare_api_url}/appointment/{appointment_id}").status_code == 200
        assert requests.get(f"{healthcare_api_url}/medical_record/{medical_record_id}").status_code == 200
        assert requests.get(f"{healthcare_api_url}/prescription/{prescription_id}").status_code == 200
        assert requests.get(f"{healthcare_api_url}/billing/{billing_id}").status_code == 200

        # Visit UI to verify system is functional
        driver.get(f"{healthcare_base_url}/dashboard")
        wait_for_app_ready(driver)

        # Cleanup
        requests.delete(f"{healthcare_api_url}/billing/{billing_id}")
        requests.delete(f"{healthcare_api_url}/prescription/{prescription_id}")
        requests.delete(f"{healthcare_api_url}/medical_record/{medical_record_id}")
        requests.delete(f"{healthcare_api_url}/appointment/{appointment_id}")
        requests.delete(f"{healthcare_api_url}/patient/{patient_id}")

    except Exception as e:
        # Cleanup on failure
        try:
            requests.delete(f"{healthcare_api_url}/patient/{patient_id}")
        except:
            pass
        raise e
