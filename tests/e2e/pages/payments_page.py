"""
Payments Page Object
Handles payment list, processing, and history
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class PaymentsPage(BasePage):
    """Page object for payment management"""

    # List page locators
    NEW_PAYMENT_BUTTON = (By.XPATH, "//button[contains(., 'New Payment')]")
    PAYMENTS_TABLE = (By.CSS_SELECTOR, ".ant-table")
    PAYMENTS_TABLE_ROWS = (By.CSS_SELECTOR, ".ant-table-tbody tr")
    VIEW_BUTTON = (By.XPATH, "//button[contains(., 'View')]")
    REFRESH_BUTTON = (By.XPATH, "//button[contains(., 'Refresh')]")

    # Form locators (in modal)
    MODAL = (By.CSS_SELECTOR, ".ant-modal")
    PAYMENT_NUMBER_INPUT = (By.ID, "paymentNumber")
    AMOUNT_INPUT = (By.ID, "amount")
    METHOD_SELECT = (By.ID, "method")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Detail page locators
    PAYMENT_STATUS = (By.CSS_SELECTOR, ".ant-tag")
    PAYMENT_CONFIRMATION = (By.XPATH, "//*[contains(text(), 'Confirmation')]")

    def navigate(self):
        """Navigate to payments list page"""
        self.navigate_to('/payments')
        self.wait_for_spinner_to_disappear()

    def click_new_payment(self):
        """Click New Payment button"""
        try:
            self.click(*self.NEW_PAYMENT_BUTTON)
            self.wait.until(lambda d: self.is_element_visible(*self.MODAL))
            return True
        except:
            return False

    def fill_payment_form(self, payment_data):
        """Fill out the payment form"""
        if 'paymentNumber' in payment_data:
            self.type_text(*self.PAYMENT_NUMBER_INPUT, payment_data['paymentNumber'])
        self.type_text(*self.AMOUNT_INPUT, payment_data['amount'])

    def submit_payment_form(self):
        """Submit the payment form"""
        self.click(*self.SUBMIT_BUTTON)

    def process_payment(self, payment_data):
        """Complete flow to process a payment"""
        if self.click_new_payment():
            self.fill_payment_form(payment_data)
            self.submit_payment_form()
            self.wait_for_spinner_to_disappear()

    def get_payments_count(self):
        """Get number of payments in table"""
        try:
            rows = self.find_elements(*self.PAYMENTS_TABLE_ROWS)
            return len(rows)
        except:
            return 0

    def click_first_payment(self):
        """Click the first payment in the table"""
        self.click(*self.VIEW_BUTTON)
        self.wait_for_url_contains('/payments/')

    def is_payment_in_table(self, payment_number):
        """Check if a payment with given number exists in table"""
        try:
            self.find_element(By.XPATH, f"//td[contains(text(), '{payment_number}')]")
            return True
        except:
            return False

    def get_payment_status(self):
        """Get payment status from detail page"""
        try:
            status_element = self.find_element(*self.PAYMENT_STATUS)
            return status_element.text
        except:
            return None

    def is_confirmation_visible(self):
        """Check if payment confirmation is visible"""
        return self.is_element_visible(*self.PAYMENT_CONFIRMATION, timeout=5)

    def refresh_payments(self):
        """Click refresh button"""
        self.click(*self.REFRESH_BUTTON)
        self.wait_for_spinner_to_disappear()
