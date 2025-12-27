"""
Chat Interface Page Object
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class ChatPage(BasePage):
    """Page object for chat interface"""

    # Locators
    CHAT_DRAWER = (By.CSS_SELECTOR, ".ant-drawer")
    CHAT_BUTTON = (By.CSS_SELECTOR, "button[title='Open Chat Assistant']")
    STARTER_PROMPT_BUTTONS = (By.CSS_SELECTOR, "[data-testid^='starter-prompt-']")
    MESSAGE_INPUT = (By.CSS_SELECTOR, "textarea[placeholder*='message' i], input[placeholder*='message' i]")
    SEND_BUTTON = (By.CSS_SELECTOR, "button[aria-label*='send' i]")
    CHAT_MESSAGES = (By.CSS_SELECTOR, "[class*='ChatMessage'], [role='article']")
    CLOSE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Close chat']")

    def open_chat(self):
        """Open the chat drawer"""
        # Look for chat button (usually floating or in header)
        if self.is_element_present(*self.CHAT_BUTTON, timeout=5):
            self.click(*self.CHAT_BUTTON)
            self.wait_for_element(*self.CHAT_DRAWER, timeout=5)
        # If drawer is already open, do nothing
        elif not self.is_element_present(*self.CHAT_DRAWER, timeout=1):
            raise Exception("Could not find chat button or drawer")

    def is_chat_open(self):
        """Check if chat drawer is open"""
        return self.is_element_present(*self.CHAT_DRAWER, timeout=2)

    def close_chat(self):
        """Close the chat drawer"""
        if self.is_chat_open():
            self.click(*self.CLOSE_BUTTON)

    def get_starter_prompts(self):
        """Get all visible starter prompt buttons"""
        if not self.is_chat_open():
            self.open_chat()

        prompts = self.find_elements(*self.STARTER_PROMPT_BUTTONS)
        return [p.text for p in prompts if p.is_displayed()]

    def click_starter_prompt(self, index=0):
        """Click a starter prompt by index"""
        if not self.is_chat_open():
            self.open_chat()

        prompts = self.find_elements(*self.STARTER_PROMPT_BUTTONS)
        visible_prompts = [p for p in prompts if p.is_displayed()]

        if index < len(visible_prompts):
            visible_prompts[index].click()
        else:
            raise Exception(f"Starter prompt index {index} not found (only {len(visible_prompts)} prompts)")

    def send_message(self, text):
        """Type and send a message"""
        if not self.is_chat_open():
            self.open_chat()

        input_field = self.find_element(*self.MESSAGE_INPUT)
        input_field.clear()
        input_field.send_keys(text)
        self.click(*self.SEND_BUTTON)

    def get_messages(self):
        """Get all chat messages"""
        if not self.is_chat_open():
            self.open_chat()

        messages = self.find_elements(*self.CHAT_MESSAGES)
        return [m.text for m in messages if m.is_displayed()]

    def wait_for_messages(self, min_count=1, timeout=10):
        """Wait for at least N messages to appear in chat"""
        from selenium.webdriver.support.ui import WebDriverWait

        def messages_present(driver):
            messages = self.find_elements(*self.CHAT_MESSAGES)
            visible_messages = [m for m in messages if m.is_displayed()]
            return len(visible_messages) >= min_count

        WebDriverWait(self.driver, timeout).until(messages_present)
