"""
Home/Dashboard Page Object
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    """Page object for home/dashboard page"""

    # Locators
    LOGO = (By.CSS_SELECTOR, "[class*='logo'], [alt*='logo']")
    NAVIGATION_MENU = (By.CSS_SELECTOR, "nav, [class*='nav'], [role='navigation']")
    QUOTES_LINK = (By.XPATH, "//a[contains(., 'Quote')]")
    POLICIES_LINK = (By.XPATH, "//a[contains(., 'Polic')]")
    CLAIMS_LINK = (By.XPATH, "//a[contains(., 'Claim')]")
    PAYMENTS_LINK = (By.XPATH, "//a[contains(., 'Payment')]")

    def load(self):
        """Load the home page"""
        self.navigate_to("/")
        self.wait_for_page_load()

    def is_loaded(self):
        """Check if home page is loaded"""
        # Page is loaded if we can find either logo or navigation
        return (
            self.is_element_present(*self.LOGO, timeout=5) or
            self.is_element_present(*self.NAVIGATION_MENU, timeout=5)
        )

    def navigate_to_quotes(self):
        """Navigate to quotes page"""
        self.click(*self.QUOTES_LINK)

    def navigate_to_policies(self):
        """Navigate to policies page"""
        self.click(*self.POLICIES_LINK)

    def navigate_to_claims(self):
        """Navigate to claims page"""
        self.click(*self.CLAIMS_LINK)

    def navigate_to_payments(self):
        """Navigate to payments page"""
        self.click(*self.PAYMENTS_LINK)

    def get_navigation_links(self):
        """Get all navigation links"""
        links = self.find_elements(By.TAG_NAME, "a")
        return [link for link in links if link.is_displayed()]
