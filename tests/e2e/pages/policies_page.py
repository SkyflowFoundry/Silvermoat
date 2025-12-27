"""
Policies Page Object
Handles policy list, search, and detail interactions
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage


class PoliciesPage(BasePage):
    """Page object for policy management"""

    # Locators
    POLICY_TABLE = (By.CSS_SELECTOR, ".ant-table")
    POLICY_TABLE_ROWS = (By.CSS_SELECTOR, ".ant-table-tbody tr")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Search']")
    VIEW_BUTTON = (By.XPATH, "//button[contains(., 'View')]")
    REFRESH_BUTTON = (By.XPATH, "//button[contains(., 'Refresh')]")

    # Detail page locators
    POLICY_DETAIL_CARD = (By.CSS_SELECTOR, ".ant-card")
    POLICY_STATUS = (By.CSS_SELECTOR, ".ant-tag")
    POLICY_NUMBER = (By.XPATH, "//*[contains(text(), 'Policy Number')]")

    def navigate(self):
        """Navigate to policies list page"""
        self.navigate_to('/policies')
        self.wait_for_spinner_to_disappear()

    def get_policy_count(self):
        """Get number of policies in table"""
        try:
            rows = self.find_elements(*self.POLICY_TABLE_ROWS)
            return len(rows)
        except:
            return 0

    def search_policies(self, search_term):
        """Search for policies using search input"""
        try:
            search_box = self.find_element(*self.SEARCH_INPUT, timeout=5)
            search_box.clear()
            search_box.send_keys(search_term)
            search_box.send_keys(Keys.RETURN)
            self.wait_for_spinner_to_disappear()
        except:
            pass  # Search input may not be available

    def click_first_policy(self):
        """Click the first policy in the table"""
        self.click(*self.VIEW_BUTTON)
        self.wait_for_url_contains('/policies/')

    def is_policy_in_table(self, policy_number):
        """Check if a policy with given number exists in table"""
        try:
            self.find_element(By.XPATH, f"//td[contains(text(), '{policy_number}')]")
            return True
        except:
            return False

    def get_policy_status(self):
        """Get policy status from detail page"""
        try:
            status_element = self.find_element(*self.POLICY_STATUS)
            return status_element.text
        except:
            return None

    def is_on_detail_page(self):
        """Check if on policy detail page"""
        return '/policies/' in self.get_current_url() and self.get_current_url() != '/policies/'

    def refresh_policies(self):
        """Click refresh button"""
        self.click(*self.REFRESH_BUTTON)
        self.wait_for_spinner_to_disappear()
