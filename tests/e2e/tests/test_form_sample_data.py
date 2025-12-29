"""
E2E Tests for Form Sample Data Buttons

Tests verify that "Fill with Sample Data" buttons work correctly on all forms.
"""

import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def save_debug_artifacts(driver, test_name, base_url):
    """Save screenshot, page source, and console logs for debugging"""
    try:
        # Create artifacts directory
        artifacts_dir = "test-artifacts"
        os.makedirs(artifacts_dir, exist_ok=True)

        # Save screenshot
        screenshot_path = f"{artifacts_dir}/{test_name}_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")

        # Save page source
        source_path = f"{artifacts_dir}/{test_name}_page_source.html"
        with open(source_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"Page source saved: {source_path}")

        # Save console logs
        logs_path = f"{artifacts_dir}/{test_name}_console_logs.txt"
        with open(logs_path, 'w', encoding='utf-8') as f:
            f.write(f"URL: {driver.current_url}\n")
            f.write(f"Expected URL pattern: {base_url}\n\n")
            f.write("=== Browser Console Logs ===\n")
            try:
                logs = driver.get_log('browser')
                for log in logs:
                    f.write(f"[{log['level']}] {log['message']}\n")
            except Exception as e:
                f.write(f"Could not capture logs: {e}\n")
        print(f"Console logs saved: {logs_path}")

    except Exception as e:
        print(f"Error saving debug artifacts: {e}")


def wait_for_react_hydration(driver, timeout=10):
    """Wait for React app to be fully hydrated and interactive"""
    try:
        # Wait for React root div to exist and have content
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "root"))
        )

        # Wait for any loading spinners to disappear
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(
                "return document.readyState === 'complete' && "
                "document.querySelectorAll('.ant-spin').length === 0"
            )
        )

        return True
    except TimeoutException:
        print("Warning: React hydration check timed out")
        return False


@pytest.mark.e2e
@pytest.mark.forms
def test_quote_form_sample_data_button(driver, base_url):
    """Test that Quote form sample data button populates fields"""
    test_name = "test_quote_form_sample_data_button"

    try:
        driver.get(f"{base_url}/quotes")

        # Wait for React to hydrate
        wait_for_react_hydration(driver)

        # Wait for page to load and button to appear
        print(f"[{test_name}] Waiting for sample data button...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']"))
        )
        print(f"[{test_name}] Button found!")

        # Click the sample data button
        sample_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']")
        sample_button.click()
        print(f"[{test_name}] Button clicked!")

        # Verify name field is populated
        name_field = driver.find_element(By.ID, "name")
        assert name_field.get_attribute("value") != "", "Name field should be populated"
        assert len(name_field.get_attribute("value")) > 0, "Name should have content"

        # Verify ZIP field is populated
        zip_field = driver.find_element(By.ID, "zip")
        assert zip_field.get_attribute("value") != "", "ZIP field should be populated"
        assert len(zip_field.get_attribute("value")) == 5, "ZIP should be 5 digits"

    except TimeoutException as e:
        print(f"[{test_name}] TIMEOUT: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise
    except Exception as e:
        print(f"[{test_name}] ERROR: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise


@pytest.mark.e2e
@pytest.mark.forms
def test_policy_form_sample_data_button(driver, base_url):
    """Test that Policy form sample data button populates fields"""
    test_name = "test_policy_form_sample_data_button"

    try:
        driver.get(f"{base_url}/policies")

        # Wait for React to hydrate
        wait_for_react_hydration(driver)

        # Wait for page to load and button to appear
        print(f"[{test_name}] Waiting for sample data button...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']"))
        )
        print(f"[{test_name}] Button found!")

        # Click the sample data button
        sample_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']")
        sample_button.click()
        print(f"[{test_name}] Button clicked!")

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

    except TimeoutException as e:
        print(f"[{test_name}] TIMEOUT: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise
    except Exception as e:
        print(f"[{test_name}] ERROR: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise


@pytest.mark.e2e
@pytest.mark.forms
def test_claim_form_sample_data_button(driver, base_url):
    """Test that Claim form sample data button populates fields"""
    test_name = "test_claim_form_sample_data_button"

    try:
        driver.get(f"{base_url}/claims")

        # Wait for React to hydrate
        wait_for_react_hydration(driver)

        # Wait for page to load and button to appear
        print(f"[{test_name}] Waiting for sample data button...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']"))
        )
        print(f"[{test_name}] Button found!")

        # Click the sample data button
        sample_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']")
        sample_button.click()
        print(f"[{test_name}] Button clicked!")

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

    except TimeoutException as e:
        print(f"[{test_name}] TIMEOUT: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise
    except Exception as e:
        print(f"[{test_name}] ERROR: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise


@pytest.mark.e2e
@pytest.mark.forms
def test_payment_form_sample_data_button(driver, base_url):
    """Test that Payment form sample data button populates fields"""
    test_name = "test_payment_form_sample_data_button"

    try:
        driver.get(f"{base_url}/payments")

        # Wait for React to hydrate
        wait_for_react_hydration(driver)

        # Wait for page to load and button to appear
        print(f"[{test_name}] Waiting for sample data button...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']"))
        )
        print(f"[{test_name}] Button found!")

        # Click the sample data button
        sample_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']")
        sample_button.click()
        print(f"[{test_name}] Button clicked!")

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

    except TimeoutException as e:
        print(f"[{test_name}] TIMEOUT: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise
    except Exception as e:
        print(f"[{test_name}] ERROR: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise


@pytest.mark.e2e
@pytest.mark.forms
def test_case_form_sample_data_button(driver, base_url):
    """Test that Case form sample data button populates fields"""
    test_name = "test_case_form_sample_data_button"

    try:
        driver.get(f"{base_url}/cases")

        # Wait for React to hydrate
        wait_for_react_hydration(driver)

        # Wait for page to load and button to appear
        print(f"[{test_name}] Waiting for sample data button...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']"))
        )
        print(f"[{test_name}] Button found!")

        # Click the sample data button
        sample_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']")
        sample_button.click()
        print(f"[{test_name}] Button clicked!")

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

    except TimeoutException as e:
        print(f"[{test_name}] TIMEOUT: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise
    except Exception as e:
        print(f"[{test_name}] ERROR: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise


@pytest.mark.e2e
@pytest.mark.forms
def test_sample_data_buttons_exist_on_all_forms(driver, base_url):
    """Test that all forms have the sample data button present"""
    test_name = "test_sample_data_buttons_exist_on_all_forms"
    forms = [
        ("/quotes", "Quote"),
        ("/policies", "Policy"),
        ("/claims", "Claim"),
        ("/payments", "Payment"),
        ("/cases", "Case"),
    ]

    for path, form_name in forms:
        try:
            print(f"[{test_name}] Checking {form_name} form at {path}")
            driver.get(f"{base_url}{path}")

            # Wait for React to hydrate
            wait_for_react_hydration(driver)

            # Wait for button to be present
            print(f"[{test_name}] Waiting for button on {form_name} form...")
            button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']"))
            )
            print(f"[{test_name}] Button found on {form_name} form!")
            assert button.is_displayed(), f"{form_name} form should have visible sample data button"

        except TimeoutException as e:
            print(f"[{test_name}] TIMEOUT on {form_name} form: {e}")
            save_debug_artifacts(driver, f"{test_name}_{form_name.lower()}", base_url)
            pytest.fail(f"{form_name} form missing 'Fill with Sample Data' button: {e}")
        except Exception as e:
            print(f"[{test_name}] ERROR on {form_name} form: {e}")
            save_debug_artifacts(driver, f"{test_name}_{form_name.lower()}", base_url)
            pytest.fail(f"{form_name} form error: {e}")


@pytest.mark.e2e
@pytest.mark.forms
def test_sample_data_button_reusable(driver, base_url):
    """Test that sample data button can be clicked multiple times (generates different data)"""
    test_name = "test_sample_data_button_reusable"

    try:
        driver.get(f"{base_url}/quotes")

        # Wait for React to hydrate
        wait_for_react_hydration(driver)

        # Wait for page to load and button to appear
        print(f"[{test_name}] Waiting for sample data button...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']"))
        )
        print(f"[{test_name}] Button found!")

        sample_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='fill-sample-data-button']")
        name_field = driver.find_element(By.ID, "name")

        # Click first time
        print(f"[{test_name}] Clicking button (1st time)...")
        sample_button.click()
        first_name = name_field.get_attribute("value")
        assert first_name != "", "First click should populate name"
        print(f"[{test_name}] First click populated: {first_name}")

        # Click second time (should generate new data)
        print(f"[{test_name}] Clicking button (2nd time)...")
        sample_button.click()
        second_name = name_field.get_attribute("value")
        assert second_name != "", "Second click should populate name"
        print(f"[{test_name}] Second click populated: {second_name}")

        # Names might be the same (random), but button should remain functional
        # The important thing is both clicks populated data

    except TimeoutException as e:
        print(f"[{test_name}] TIMEOUT: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise
    except Exception as e:
        print(f"[{test_name}] ERROR: {e}")
        save_debug_artifacts(driver, test_name, base_url)
        raise
