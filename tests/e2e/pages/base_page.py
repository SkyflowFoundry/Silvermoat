"""Base Page Object class with common methods."""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """Base class for all page objects."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, by, value):
        """Find element with explicit wait."""
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_elements(self, by, value):
        """Find multiple elements."""
        return self.driver.find_elements(by, value)

    def click_element(self, by, value):
        """Click element with explicit wait."""
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()

    def input_text(self, by, value, text):
        """Input text into element."""
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, value):
        """Get text from element."""
        return self.find_element(by, value).text

    def is_element_visible(self, by, value, timeout=10):
        """Check if element is visible."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except:
            return False
