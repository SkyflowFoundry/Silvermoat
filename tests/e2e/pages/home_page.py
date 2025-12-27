"""Home Page Object."""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    """Page object for the home page."""

    # Locators
    HEADER = (By.TAG_NAME, "h1")
    NAV_QUOTES = (By.LINK_TEXT, "Quotes")
    NAV_POLICIES = (By.LINK_TEXT, "Policies")
    NAV_CLAIMS = (By.LINK_TEXT, "Claims")
    NAV_PAYMENTS = (By.LINK_TEXT, "Payments")

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url

    def navigate(self):
        """Navigate to home page."""
        self.driver.get(self.base_url)
        return self

    def is_loaded(self):
        """Check if page is loaded."""
        return self.is_element_visible(*self.HEADER)

    def navigate_to_quotes(self):
        """Navigate to quotes page."""
        self.click_element(*self.NAV_QUOTES)

    def navigate_to_policies(self):
        """Navigate to policies page."""
        self.click_element(*self.NAV_POLICIES)

    def navigate_to_claims(self):
        """Navigate to claims page."""
        self.click_element(*self.NAV_CLAIMS)

    def navigate_to_payments(self):
        """Navigate to payments page."""
        self.click_element(*self.NAV_PAYMENTS)
