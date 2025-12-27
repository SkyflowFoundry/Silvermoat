"""
Home Page Object for Silvermoat application.
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    """Page object for the home page."""

    # Locators
    APP_TITLE = (By.CSS_SELECTOR, "h1")
    NAV_QUOTES = (By.LINK_TEXT, "Quotes")
    NAV_POLICIES = (By.LINK_TEXT, "Policies")
    NAV_CLAIMS = (By.LINK_TEXT, "Claims")
    NAV_PAYMENTS = (By.LINK_TEXT, "Payments")
    QUOTE_FORM = (By.CSS_SELECTOR, "form")
    QUOTE_LIST = (By.CSS_SELECTOR, ".quote-list, [class*='quote']")

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url

    def load(self):
        """Load the home page."""
        self.navigate_to(self.base_url)

    def is_loaded(self):
        """Check if the page has loaded."""
        return self.is_element_visible(self.APP_TITLE, timeout=5)

    def get_title_text(self):
        """Get the application title text."""
        return self.get_text(self.APP_TITLE)

    def click_quotes_nav(self):
        """Click Quotes navigation link."""
        self.click_element(self.NAV_QUOTES)

    def click_policies_nav(self):
        """Click Policies navigation link."""
        self.click_element(self.NAV_POLICIES)

    def click_claims_nav(self):
        """Click Claims navigation link."""
        self.click_element(self.NAV_CLAIMS)

    def click_payments_nav(self):
        """Click Payments navigation link."""
        self.click_element(self.NAV_PAYMENTS)

    def is_quote_form_visible(self):
        """Check if quote form is visible."""
        return self.is_element_visible(self.QUOTE_FORM, timeout=5)
