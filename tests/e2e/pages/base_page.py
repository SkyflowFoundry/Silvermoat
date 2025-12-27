"""
Base Page Object
Provides common methods used by all page objects
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def navigate_to(self, path=''):
        """Navigate to a specific path"""
        url = f"{self.base_url}{path}"
        self.driver.get(url)

    def find_element(self, by, value, timeout=10):
        """Find a single element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def find_elements(self, by, value, timeout=10):
        """Find multiple elements with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located((by, value)))
        return self.driver.find_elements(by, value)

    def click(self, by, value, timeout=10):
        """Click an element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        return element

    def type_text(self, by, value, text, timeout=10):
        """Type text into an input field"""
        element = self.find_element(by, value, timeout)
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, by, value, timeout=10):
        """Get text from an element"""
        element = self.find_element(by, value, timeout)
        return element.text

    def is_element_visible(self, by, value, timeout=5):
        """Check if element is visible"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, text, timeout=10):
        """Wait for URL to contain specific text"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.url_contains(text))

    def wait_for_element_to_disappear(self, by, value, timeout=10):
        """Wait for an element to disappear from DOM"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located((by, value)))

    def scroll_to_element(self, by, value, timeout=10):
        """Scroll to an element"""
        element = self.find_element(by, value, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url

    def get_page_title(self):
        """Get page title"""
        return self.driver.title

    def wait_for_spinner_to_disappear(self, timeout=10):
        """Wait for loading spinner to disappear"""
        try:
            self.wait_for_element_to_disappear(
                By.CSS_SELECTOR,
                '.ant-spin-spinning',
                timeout
            )
        except TimeoutException:
            pass  # Spinner may not appear for fast operations
