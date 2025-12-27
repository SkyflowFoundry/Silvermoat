"""
Quotes Page Object
Handles quote list, form, and detail interactions
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class QuotesPage(BasePage):
    """Page object for quotes management"""

    # Locators
    NEW_QUOTE_BUTTON = (By.XPATH, "//button[contains(., 'New Quote')]")
    REFRESH_BUTTON = (By.XPATH, "//button[contains(., 'Refresh')]")
    QUOTE_TABLE = (By.CSS_SELECTOR, ".ant-table")
    QUOTE_TABLE_ROWS = (By.CSS_SELECTOR, ".ant-table-tbody tr")
    MODAL = (By.CSS_SELECTOR, ".ant-modal")
    MODAL_TITLE = (By.CSS_SELECTOR, ".ant-modal-title")

    # Form locators
    NAME_INPUT = (By.ID, "name")
    ZIP_INPUT = (By.ID, "zip")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    FORM_ERROR = (By.CSS_SELECTOR, ".ant-form-item-explain-error")

    # Table locators
    VIEW_BUTTON = (By.XPATH, "//button[contains(., 'View')]")
    CONVERT_TO_POLICY_BUTTON = (By.XPATH, "//button[contains(., 'Convert to Policy')]")

    def navigate(self):
        """Navigate to quotes list page"""
        self.navigate_to('/quotes')
        self.wait_for_spinner_to_disappear()

    def click_new_quote(self):
        """Click New Quote button"""
        self.click(*self.NEW_QUOTE_BUTTON)
        self.wait.until(lambda d: self.is_element_visible(*self.MODAL))

    def fill_quote_form(self, name, zip_code):
        """Fill out the quote form"""
        self.type_text(*self.NAME_INPUT, name)
        self.type_text(*self.ZIP_INPUT, zip_code)

    def submit_quote_form(self):
        """Submit the quote form"""
        self.click(*self.SUBMIT_BUTTON)

    def create_quote(self, name, zip_code):
        """Complete flow to create a quote"""
        self.click_new_quote()
        self.fill_quote_form(name, zip_code)
        self.submit_quote_form()
        self.wait_for_spinner_to_disappear()

    def is_modal_open(self):
        """Check if quote modal is open"""
        return self.is_element_visible(*self.MODAL)

    def is_form_error_visible(self):
        """Check if form validation error is visible"""
        return self.is_element_visible(*self.FORM_ERROR, timeout=3)

    def get_quote_count(self):
        """Get number of quotes in table"""
        try:
            rows = self.find_elements(*self.QUOTE_TABLE_ROWS)
            return len(rows)
        except:
            return 0

    def click_first_quote(self):
        """Click the first quote in the table"""
        self.click(*self.VIEW_BUTTON)
        self.wait_for_url_contains('/quotes/')

    def is_quote_in_table(self, name):
        """Check if a quote with given name exists in table"""
        try:
            self.find_element(By.XPATH, f"//td[contains(text(), '{name}')]")
            return True
        except:
            return False

    def click_convert_to_policy(self):
        """Click Convert to Policy button on detail page"""
        self.click(*self.CONVERT_TO_POLICY_BUTTON)
        self.wait_for_spinner_to_disappear()

    def refresh_quotes(self):
        """Click refresh button"""
        self.click(*self.REFRESH_BUTTON)
        self.wait_for_spinner_to_disappear()
