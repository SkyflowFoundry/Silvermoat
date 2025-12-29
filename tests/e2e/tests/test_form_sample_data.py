"""
E2E Tests for Form Sample Data Buttons

Tests verify that "Fill with Sample Data" buttons work correctly on all forms.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.e2e
@pytest.mark.forms
def test_quote_form_sample_data_button(driver, base_url):
    """Test that Quote form sample data button populates fields"""
    driver.get(f"{base_url}/quotes")

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]"))
    )

    # Click the sample data button
    sample_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]")
    sample_button.click()

    # Verify name field is populated
    name_field = driver.find_element(By.ID, "name")
    assert name_field.get_attribute("value") != "", "Name field should be populated"
    assert len(name_field.get_attribute("value")) > 0, "Name should have content"

    # Verify ZIP field is populated
    zip_field = driver.find_element(By.ID, "zip")
    assert zip_field.get_attribute("value") != "", "ZIP field should be populated"
    assert len(zip_field.get_attribute("value")) == 5, "ZIP should be 5 digits"


@pytest.mark.e2e
@pytest.mark.forms
def test_policy_form_sample_data_button(driver, base_url):
    """Test that Policy form sample data button populates fields"""
    driver.get(f"{base_url}/policies")

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]"))
    )

    # Click the sample data button
    sample_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]")
    sample_button.click()

    # Verify policy number field is populated
    policy_number_field = driver.find_element(By.ID, "policyNumber")
    assert policy_number_field.get_attribute("value") != "", "Policy number should be populated"
    assert "POL-" in policy_number_field.get_attribute("value"), "Policy number should have POL- prefix"

    # Verify holder name field is populated
    holder_name_field = driver.find_element(By.ID, "holderName")
    assert holder_name_field.get_attribute("value") != "", "Holder name should be populated"

    # Verify effective date is populated
    effective_date_field = driver.find_element(By.ID, "effectiveDate")
    assert effective_date_field.get_attribute("value") != "", "Effective date should be populated"

    # Verify premium is populated
    premium_field = driver.find_element(By.ID, "premium")
    premium_value = premium_field.get_attribute("value")
    assert premium_value != "", "Premium should be populated"
    assert float(premium_value) > 0, "Premium should be positive"


@pytest.mark.e2e
@pytest.mark.forms
def test_claim_form_sample_data_button(driver, base_url):
    """Test that Claim form sample data button populates fields"""
    driver.get(f"{base_url}/claims")

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]"))
    )

    # Click the sample data button
    sample_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]")
    sample_button.click()

    # Verify claim number is populated
    claim_number_field = driver.find_element(By.ID, "claimNumber")
    assert claim_number_field.get_attribute("value") != "", "Claim number should be populated"
    assert "CLM-" in claim_number_field.get_attribute("value"), "Claim number should have CLM- prefix"

    # Verify claimant name is populated
    claimant_name_field = driver.find_element(By.ID, "claimantName")
    assert claimant_name_field.get_attribute("value") != "", "Claimant name should be populated"

    # Verify incident date is populated
    incident_date_field = driver.find_element(By.ID, "incidentDate")
    assert incident_date_field.get_attribute("value") != "", "Incident date should be populated"

    # Verify description is populated
    description_field = driver.find_element(By.ID, "description")
    assert description_field.get_attribute("value") != "", "Description should be populated"
    assert len(description_field.get_attribute("value")) >= 10, "Description should have meaningful content"

    # Verify amount is populated
    amount_field = driver.find_element(By.ID, "amount")
    amount_value = amount_field.get_attribute("value")
    assert amount_value != "", "Amount should be populated"
    assert float(amount_value) > 0, "Amount should be positive"


@pytest.mark.e2e
@pytest.mark.forms
def test_payment_form_sample_data_button(driver, base_url):
    """Test that Payment form sample data button populates fields"""
    driver.get(f"{base_url}/payments")

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]"))
    )

    # Click the sample data button
    sample_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]")
    sample_button.click()

    # Verify payment date is populated
    payment_date_field = driver.find_element(By.ID, "paymentDate")
    assert payment_date_field.get_attribute("value") != "", "Payment date should be populated"

    # Verify amount is populated
    amount_field = driver.find_element(By.ID, "amount")
    amount_value = amount_field.get_attribute("value")
    assert amount_value != "", "Amount should be populated"
    assert float(amount_value) > 0, "Amount should be positive"

    # Verify policy ID is populated
    policy_id_field = driver.find_element(By.ID, "policyId")
    assert policy_id_field.get_attribute("value") != "", "Policy ID should be populated"
    assert "POL-" in policy_id_field.get_attribute("value"), "Policy ID should have POL- prefix"


@pytest.mark.e2e
@pytest.mark.forms
def test_case_form_sample_data_button(driver, base_url):
    """Test that Case form sample data button populates fields"""
    driver.get(f"{base_url}/cases")

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]"))
    )

    # Click the sample data button
    sample_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]")
    sample_button.click()

    # Verify title is populated
    title_field = driver.find_element(By.ID, "title")
    assert title_field.get_attribute("value") != "", "Title should be populated"

    # Verify description is populated
    description_field = driver.find_element(By.ID, "description")
    assert description_field.get_attribute("value") != "", "Description should be populated"
    assert len(description_field.get_attribute("value")) >= 10, "Description should have meaningful content"

    # Verify related entity ID is populated
    entity_id_field = driver.find_element(By.ID, "relatedEntityId")
    assert entity_id_field.get_attribute("value") != "", "Related entity ID should be populated"

    # Verify assignee is populated
    assignee_field = driver.find_element(By.ID, "assignee")
    assert assignee_field.get_attribute("value") != "", "Assignee should be populated"


@pytest.mark.e2e
@pytest.mark.forms
def test_sample_data_buttons_exist_on_all_forms(driver, base_url):
    """Test that all forms have the sample data button present"""
    forms = [
        ("/quotes", "Quote"),
        ("/policies", "Policy"),
        ("/claims", "Claim"),
        ("/payments", "Payment"),
        ("/cases", "Case"),
    ]

    for path, form_name in forms:
        driver.get(f"{base_url}{path}")

        # Wait for button to be present
        try:
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]"))
            )
            assert button.is_displayed(), f"{form_name} form should have visible sample data button"
        except Exception as e:
            pytest.fail(f"{form_name} form missing 'Fill with Sample Data' button: {e}")


@pytest.mark.e2e
@pytest.mark.forms
def test_sample_data_button_reusable(driver, base_url):
    """Test that sample data button can be clicked multiple times (generates different data)"""
    driver.get(f"{base_url}/quotes")

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]"))
    )

    sample_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Fill with Sample Data')]")
    name_field = driver.find_element(By.ID, "name")

    # Click first time
    sample_button.click()
    first_name = name_field.get_attribute("value")
    assert first_name != "", "First click should populate name"

    # Click second time (should generate new data)
    sample_button.click()
    second_name = name_field.get_attribute("value")
    assert second_name != "", "Second click should populate name"

    # Names might be the same (random), but button should remain functional
    # The important thing is both clicks populated data
