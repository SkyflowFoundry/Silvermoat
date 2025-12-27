"""
Base Page Object

Common methods for all page objects.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def navigate_to(self, path="/"):
        """Navigate to a specific path"""
        url = f"{self.base_url}{path}"
        self.driver.get(url)

    def wait_for_element(self, by, value, timeout=10):
        """Wait for element to be present"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def wait_for_element_clickable(self, by, value, timeout=10):
        """Wait for element to be clickable"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))

    def find_element(self, by, value):
        """Find a single element"""
        return self.driver.find_element(by, value)

    def find_elements(self, by, value):
        """Find multiple elements"""
        return self.driver.find_elements(by, value)

    def click(self, by, value):
        """Click an element"""
        element = self.wait_for_element_clickable(by, value)
        element.click()

    def type_text(self, by, value, text):
        """Type text into an input field"""
        element = self.wait_for_element(by, value)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, value):
        """Get text from an element"""
        element = self.wait_for_element(by, value)
        return element.text

    def is_element_present(self, by, value, timeout=5):
        """Check if element is present (returns bool)"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((by, value)))
            return True
        except:
            return False

    def wait_for_page_load(self):
        """Wait for page to finish loading"""
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
