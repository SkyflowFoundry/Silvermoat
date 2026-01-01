"""
Dashboard Page Object
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class DashboardPage(BasePage):
    """Page object for employee dashboard page"""

    # Locators - Ant Design Menu structure
    LOGO = (By.CSS_SELECTOR, "[class*='logo'], [alt*='logo']")
    NAVIGATION_MENU = (By.CSS_SELECTOR, "[role='menu']")  # Ant Design uses role="menu"
    NAV_MENU_ITEMS = (By.CSS_SELECTOR, "[role='menuitem']")  # Menu items
    QUOTES_LINK = (By.XPATH, "//*[@role='menuitem' and contains(., 'Quote')]")
    POLICIES_LINK = (By.XPATH, "//*[@role='menuitem' and contains(., 'Polic')]")
    CLAIMS_LINK = (By.XPATH, "//*[@role='menuitem' and contains(., 'Claim')]")
    PAYMENTS_LINK = (By.XPATH, "//*[@role='menuitem' and contains(., 'Payment')]")

    def load(self):
        """Load the dashboard page"""
        self.navigate_to("/dashboard")
        self.wait_for_page_load()

    def is_loaded(self):
        """Check if dashboard page is loaded"""
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
        """Get all navigation menu items (Ant Design uses role='menuitem')"""
        menu_items = self.find_elements(*self.NAV_MENU_ITEMS)
        return [item for item in menu_items if item.is_displayed()]
