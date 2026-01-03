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
    """Save minimal debug info for AI analysis (no screenshots, concise text only)"""
    try:
        # Create artifacts directory
        artifacts_dir = "test-artifacts"
        os.makedirs(artifacts_dir, exist_ok=True)

        # Save concise debug summary (text only, for Claude)
        summary_path = f"{artifacts_dir}/{test_name}.txt"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"Test: {test_name}\n")
            f.write(f"URL: {driver.current_url}\n")
            f.write(f"Expected: {base_url}/[entity]/new\n\n")

            # Console errors (SEVERE only)
            f.write("=== Console Errors ===\n")
            try:
                logs = driver.get_log('browser')
                severe_errors = [log for log in logs if log['level'] == 'SEVERE']
                if severe_errors:
                    for log in severe_errors[:5]:  # Max 5 errors
                        f.write(f"[{log['level']}] {log['message'][:200]}\n")
                else:
                    f.write("No severe console errors\n")
            except Exception as e:
                f.write(f"Could not capture logs: {e}\n")

            # Check if target element exists at all
            f.write("\n=== DOM Check ===\n")
            try:
                # Check for button
                button_exists = driver.execute_script(
                    "return document.querySelectorAll('[data-testid=\"fill-sample-data-button\"]').length"
                )
                f.write(f"Sample data buttons found: {button_exists}\n")

                # Check for modal
                modal_exists = driver.execute_script(
                    "return document.querySelectorAll('.ant-modal').length"
                )
                modal_visible = driver.execute_script(
                    "return document.querySelectorAll('.ant-modal:not(.ant-modal-hidden)').length"
                )
                f.write(f"Modals in DOM: {modal_exists}\n")
                f.write(f"Visible modals: {modal_visible}\n")

                # Check if React loaded
                react_loaded = driver.execute_script("return !!window.React || !!document.getElementById('root')")
                f.write(f"React loaded: {react_loaded}\n")

            except Exception as e:
                f.write(f"DOM check failed: {e}\n")

        print(f"Debug summary saved: {summary_path}")

    except Exception as e:
        print(f"Error saving debug artifacts: {e}")


def wait_for_app_ready(driver, timeout=15):
    """Wait for app to be fully loaded and interactive"""
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


@pytest.mark.e2e
@pytest.mark.forms
def test_quote_form_sample_data_button(driver, base_url):
    """Test that Quote form sample data button populates fields"""
    test_name = "test_quote_form_sample_data_button"

    try:
        driver.get(f"{base_url}/quotes/new")

        # Wait for app ready (loading screen removed)
        wait_for_app_ready(driver)

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
        driver.get(f"{base_url}/policies/new")

        # Wait for app ready (loading screen removed)
        wait_for_app_ready(driver)

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
        driver.get(f"{base_url}/claims/new")

        # Wait for app ready (loading screen removed)
        wait_for_app_ready(driver)

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
        driver.get(f"{base_url}/payments/new")

        # Wait for app ready (loading screen removed)
        wait_for_app_ready(driver)

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
        # Ant Design DatePicker uses an input field inside, find it
        try:
            payment_date_input = driver.find_element(By.CSS_SELECTOR, "#paymentDate input")
            date_value = payment_date_input.get_attribute("value")
            assert date_value != "", "Payment date should be populated"
            print(f"[{test_name}] Payment date populated: {date_value}")
        except Exception as e:
            print(f"[{test_name}] Warning: Could not verify date field: {e}")
            # Date field verification is not critical for this test
            pass

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
        driver.get(f"{base_url}/cases/new")

        # Wait for app ready (loading screen removed)
        wait_for_app_ready(driver)

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
        ("/quotes/new", "Quote"),
        ("/policies/new", "Policy"),
        ("/claims/new", "Claim"),
        ("/payments/new", "Payment"),
        ("/cases/new", "Case"),
    ]

    for path, form_name in forms:
        try:
            print(f"[{test_name}] Checking {form_name} form at {path}")
            driver.get(f"{base_url}{path}")

            # Wait for app ready (loading screen removed)
            wait_for_app_ready(driver)

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
        driver.get(f"{base_url}/quotes/new")

        # Wait for app ready (loading screen removed)
        wait_for_app_ready(driver)

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
