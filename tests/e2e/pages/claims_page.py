"""
Claims Page Object
Handles claim list, form, document upload, and status updates
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class ClaimsPage(BasePage):
    """Page object for claims processing"""

    # List page locators
    NEW_CLAIM_BUTTON = (By.XPATH, "//button[contains(., 'New Claim')]")
    CLAIMS_TABLE = (By.CSS_SELECTOR, ".ant-table")
    CLAIMS_TABLE_ROWS = (By.CSS_SELECTOR, ".ant-table-tbody tr")
    VIEW_BUTTON = (By.XPATH, "//button[contains(., 'View')]")
    MODAL = (By.CSS_SELECTOR, ".ant-modal")

    # Form locators
    CLAIM_NUMBER_INPUT = (By.ID, "claimNumber")
    CLAIMANT_NAME_INPUT = (By.ID, "claimantName")
    INCIDENT_DATE_INPUT = (By.ID, "incidentDate")
    DESCRIPTION_INPUT = (By.ID, "description")
    AMOUNT_INPUT = (By.ID, "amount")
    STATUS_SELECT = (By.ID, "status")
    POLICY_ID_INPUT = (By.ID, "policyId")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Detail page locators
    CLAIM_STATUS = (By.CSS_SELECTOR, ".ant-tag")
    UPDATE_STATUS_BUTTON = (By.XPATH, "//button[contains(., 'Update Status')]")
    UPLOAD_DOCUMENT_BUTTON = (By.XPATH, "//button[contains(., 'Upload')]")
    CLAIM_HISTORY = (By.CSS_SELECTOR, ".ant-timeline")
    FILE_INPUT = (By.CSS_SELECTOR, "input[type='file']")

    def navigate(self):
        """Navigate to claims list page"""
        self.navigate_to('/claims')
        self.wait_for_spinner_to_disappear()

    def click_new_claim(self):
        """Click New Claim button"""
        self.click(*self.NEW_CLAIM_BUTTON)
        self.wait.until(lambda d: self.is_element_visible(*self.MODAL))

    def fill_claim_form(self, claim_data):
        """Fill out the claim form"""
        self.type_text(*self.CLAIM_NUMBER_INPUT, claim_data['claimNumber'])
        self.type_text(*self.CLAIMANT_NAME_INPUT, claim_data['claimantName'])

        # Handle date picker
        date_input = self.find_element(*self.INCIDENT_DATE_INPUT)
        date_input.click()
        date_input.send_keys(claim_data['incidentDate'])

        self.type_text(*self.DESCRIPTION_INPUT, claim_data['description'])
        self.type_text(*self.AMOUNT_INPUT, claim_data['amount'])

    def submit_claim_form(self):
        """Submit the claim form"""
        self.click(*self.SUBMIT_BUTTON)

    def create_claim(self, claim_data):
        """Complete flow to create a claim"""
        self.click_new_claim()
        self.fill_claim_form(claim_data)
        self.submit_claim_form()
        self.wait_for_spinner_to_disappear()

    def get_claims_count(self):
        """Get number of claims in table"""
        try:
            rows = self.find_elements(*self.CLAIMS_TABLE_ROWS)
            return len(rows)
        except:
            return 0

    def click_first_claim(self):
        """Click the first claim in the table"""
        self.click(*self.VIEW_BUTTON)
        self.wait_for_url_contains('/claims/')

    def is_claim_in_table(self, claim_number):
        """Check if a claim with given number exists in table"""
        try:
            self.find_element(By.XPATH, f"//td[contains(text(), '{claim_number}')]")
            return True
        except:
            return False

    def click_update_status(self):
        """Click Update Status button on detail page"""
        try:
            self.click(*self.UPDATE_STATUS_BUTTON)
            return True
        except:
            return False

    def upload_document(self, file_path):
        """Upload a document to the claim"""
        try:
            file_input = self.find_element(*self.FILE_INPUT)
            file_input.send_keys(file_path)
            self.wait_for_spinner_to_disappear()
            return True
        except:
            return False

    def get_claim_status(self):
        """Get claim status from detail page"""
        try:
            status_element = self.find_element(*self.CLAIM_STATUS)
            return status_element.text
        except:
            return None

    def is_history_visible(self):
        """Check if claim history timeline is visible"""
        return self.is_element_visible(*self.CLAIM_HISTORY, timeout=5)
