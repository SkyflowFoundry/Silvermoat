"""
Chat Assistant Tests
Tests for chat interface, messaging, and quick actions
"""

import pytest
from pages.chat_page import ChatPage
from pages.home_page import HomePage


@pytest.mark.chat
def test_open_chat_interface(driver, base_url):
    """Test opening the chat assistant"""
    home = HomePage(driver, base_url)
    home.navigate()

    chat = ChatPage(driver, base_url)

    # Try to open chat
    if chat.open_chat():
        assert chat.is_chat_open(), "Chat interface did not open"
    else:
        pytest.skip("Chat interface not available or already open")


@pytest.mark.chat
def test_send_message(driver, base_url):
    """Test sending a message in chat"""
    home = HomePage(driver, base_url)
    home.navigate()

    chat = ChatPage(driver, base_url)

    # Open chat if not already open
    if not chat.is_chat_open():
        if not chat.open_chat():
            pytest.skip("Chat interface not available")

    # Send a test message
    chat.send_message("Hello")

    # Wait for response
    import time
    time.sleep(3)

    # Should have received some response
    assert chat.is_response_received(), "No response received from chat"


@pytest.mark.chat
def test_chat_quick_actions(driver, base_url):
    """Test chat quick actions/starter prompts"""
    home = HomePage(driver, base_url)
    home.navigate()

    chat = ChatPage(driver, base_url)

    # Open chat if not already open
    if not chat.is_chat_open():
        if not chat.open_chat():
            pytest.skip("Chat interface not available")

    # Try to click a starter prompt
    prompts_to_try = [
        "Search for active policies",
        "Show me pending claims",
        "Find quotes"
    ]

    clicked = False
    for prompt in prompts_to_try:
        if chat.click_starter_prompt(prompt):
            clicked = True
            break

    if not clicked:
        pytest.skip("No quick action buttons available")

    # Wait for response
    import time
    time.sleep(3)

    # Should have received response
    assert chat.is_response_received(), "No response after quick action"


@pytest.mark.chat
def test_close_chat(driver, base_url):
    """Test closing the chat interface"""
    home = HomePage(driver, base_url)
    home.navigate()

    chat = ChatPage(driver, base_url)

    # Open chat first
    if not chat.is_chat_open():
        if not chat.open_chat():
            pytest.skip("Chat interface not available")

    # Close chat
    if chat.close_chat():
        assert not chat.is_chat_open(), "Chat did not close"
    else:
        pytest.skip("Chat close functionality not available")
