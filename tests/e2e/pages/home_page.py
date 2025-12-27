"""
Home/Dashboard Page Object
Handles navigation and dashboard interactions
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    """Page object for home/dashboard page"""

    # Navigation locators
    SIDEBAR = (By.CSS_SELECTOR, ".ant-layout-sider")
    HEADER = (By.CSS_SELECTOR, ".ant-layout-header")
    DASHBOARD_LINK = (By.XPATH, "//a[@href='/']")
    QUOTES_LINK = (By.XPATH, "//a[@href='/quotes']")
    POLICIES_LINK = (By.XPATH, "//a[@href='/policies']")
    CLAIMS_LINK = (By.XPATH, "//a[@href='/claims']")
    PAYMENTS_LINK = (By.XPATH, "//a[@href='/payments']")
    CASES_LINK = (By.XPATH, "//a[@href='/cases']")

    # Dashboard content locators
    STATS_CARDS = (By.CSS_SELECTOR, ".ant-statistic")
    CHARTS = (By.CSS_SELECTOR, ".ant-card")
    RECENT_ACTIVITY = (By.XPATH, "//*[contains(text(), 'Recent Activity')]")

    def navigate(self):
        """Navigate to home/dashboard page"""
        self.navigate_to('/')
        self.wait_for_spinner_to_disappear()

    def is_loaded(self):
        """Check if dashboard page is loaded"""
        return self.is_element_visible(*self.HEADER, timeout=5)

    def click_quotes_link(self):
        """Navigate to quotes page"""
        self.click(*self.QUOTES_LINK)
        self.wait_for_url_contains('/quotes')

    def click_policies_link(self):
        """Navigate to policies page"""
        self.click(*self.POLICIES_LINK)
        self.wait_for_url_contains('/policies')

    def click_claims_link(self):
        """Navigate to claims page"""
        self.click(*self.CLAIMS_LINK)
        self.wait_for_url_contains('/claims')

    def click_payments_link(self):
        """Navigate to payments page"""
        self.click(*self.PAYMENTS_LINK)
        self.wait_for_url_contains('/payments')

    def click_cases_link(self):
        """Navigate to cases page"""
        self.click(*self.CASES_LINK)
        self.wait_for_url_contains('/cases')

    def is_navigation_working(self):
        """Test if sidebar navigation is functional"""
        links = [
            (self.QUOTES_LINK, '/quotes'),
            (self.POLICIES_LINK, '/policies'),
            (self.CLAIMS_LINK, '/claims'),
        ]

        for locator, expected_path in links:
            try:
                self.click(*locator)
                self.wait_for_url_contains(expected_path)
                self.navigate()  # Return to dashboard
            except:
                return False
        return True

    def get_stats_count(self):
        """Get number of stat cards on dashboard"""
        try:
            stats = self.find_elements(*self.STATS_CARDS)
            return len(stats)
        except:
            return 0
