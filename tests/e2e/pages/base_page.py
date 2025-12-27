"""
Base Page Object with common methods for all pages.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base class for all page objects."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to(self, url):
        """Navigate to a URL."""
        self.driver.get(url)

    def find_element(self, locator, timeout=10):
        """Find element with explicit wait."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator, timeout=10):
        """Find multiple elements with explicit wait."""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click_element(self, locator, timeout=10):
        """Click an element with explicit wait for clickability."""
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def input_text(self, locator, text, timeout=10):
        """Input text into an element."""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=10):
        """Get text from an element."""
        element = self.find_element(locator, timeout)
        return element.text

    def is_element_visible(self, locator, timeout=10):
        """Check if element is visible."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, url_fragment, timeout=10):
        """Wait for URL to contain a specific fragment."""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.url_contains(url_fragment))

    def get_current_url(self):
        """Get current page URL."""
        return self.driver.current_url

    def get_page_title(self):
        """Get page title."""
        return self.driver.title
