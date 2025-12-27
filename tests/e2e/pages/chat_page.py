"""
Chat Page Object
Handles chat assistant interactions
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage


class ChatPage(BasePage):
    """Page object for chat assistant"""

    # Chat button/drawer locators
    CHAT_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Open chat']")
    CHAT_DRAWER = (By.CSS_SELECTOR, ".ant-drawer")
    CHAT_HEADER = (By.XPATH, "//*[contains(text(), 'Chat Assistant')]")
    CLOSE_CHAT_BUTTON = (By.XPATH, "//button[@aria-label='Close chat']")

    # Chat interface locators
    MESSAGE_INPUT = (By.CSS_SELECTOR, "textarea[placeholder*='message'], input[placeholder*='message']")
    SEND_BUTTON = (By.XPATH, "//button[contains(., 'Send')]")
    MESSAGE_LIST = (By.CSS_SELECTOR, ".ant-empty, .chat-message, [class*='message']")
    TYPING_INDICATOR = (By.CSS_SELECTOR, ".ant-spin-spinning")

    # Quick action buttons
    STARTER_PROMPT_BUTTONS = (By.XPATH, "//button[contains(@class, 'ant-btn')]")

    def open_chat(self):
        """Open the chat assistant"""
        try:
            # Look for chat button or trigger
            self.click(*self.CHAT_BUTTON, timeout=5)
            self.wait.until(lambda d: self.is_element_visible(*self.CHAT_DRAWER, 2))
            return True
        except:
            # Chat might already be open or integrated in layout
            return self.is_chat_open()

    def close_chat(self):
        """Close the chat assistant"""
        try:
            self.click(*self.CLOSE_CHAT_BUTTON)
            self.wait_for_element_to_disappear(*self.CHAT_DRAWER)
            return True
        except:
            return False

    def is_chat_open(self):
        """Check if chat interface is visible"""
        return self.is_element_visible(*self.CHAT_HEADER, timeout=3)

    def send_message(self, message):
        """Send a message in the chat"""
        message_input = self.find_element(*self.MESSAGE_INPUT)
        message_input.clear()
        message_input.send_keys(message)

        # Try to click send button, or use Enter key
        try:
            self.click(*self.SEND_BUTTON, timeout=2)
        except:
            message_input.send_keys(Keys.RETURN)

        # Wait for typing indicator to appear and disappear
        try:
            self.wait.until(lambda d: self.is_element_visible(*self.TYPING_INDICATOR, 2))
            self.wait_for_element_to_disappear(*self.TYPING_INDICATOR, timeout=30)
        except:
            pass  # Response may be instant

    def is_response_received(self):
        """Check if a response was received"""
        try:
            messages = self.find_elements(*self.MESSAGE_LIST, timeout=5)
            return len(messages) > 0
        except:
            return False

    def click_starter_prompt(self, prompt_text):
        """Click a quick action/starter prompt button"""
        try:
            button = self.find_element(
                By.XPATH,
                f"//button[contains(., '{prompt_text}')]"
            )
            button.click()
            return True
        except:
            return False

    def get_last_message_text(self):
        """Get text of the last message in chat"""
        try:
            messages = self.find_elements(*self.MESSAGE_LIST)
            if messages:
                return messages[-1].text
        except:
            pass
        return None
