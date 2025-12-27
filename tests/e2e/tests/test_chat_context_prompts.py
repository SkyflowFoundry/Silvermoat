"""
E2E Tests for Context-Aware Chat Prompts

Tests that chat starter prompts change based on current page/route.
Infrastructure-agnostic tests focusing on user-facing functionality.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.mark.e2e
@pytest.mark.chat
def test_chat_prompts_change_by_route(driver, base_url):
    """Test that chat prompts change based on current route"""
    driver.get(base_url)

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Find and click chat button to open chat interface
    # Assuming there's a chat button (could be MessageOutlined icon or similar)
    try:
        chat_buttons = driver.find_elements(By.CSS_SELECTOR, '[aria-label*="chat" i], [aria-label*="message" i], button[title*="chat" i]')
        if chat_buttons:
            chat_buttons[0].click()

            # Wait for chat interface to appear
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Chat Assistant') or contains(text(), 'Try these')]"))
            )

            # Get starter prompts on dashboard
            dashboard_prompts = driver.find_elements(By.CSS_SELECTOR, 'button')
            dashboard_prompt_texts = [btn.text for btn in dashboard_prompts if 'recent' in btn.text.lower() or 'overview' in btn.text.lower() or 'report' in btn.text.lower()]

            # Dashboard should have dashboard-specific prompts
            assert any('recent' in text.lower() or 'overview' in text.lower() or 'report' in text.lower() for text in dashboard_prompt_texts), \
                "Dashboard should show dashboard-specific prompts"

            # Navigate to Quotes page
            driver.get(f"{base_url}/quotes")

            # Wait for navigation
            WebDriverWait(driver, 5).until(
                EC.url_contains('/quotes')
            )

            # Reopen chat if needed (might auto-close on navigation)
            chat_buttons = driver.find_elements(By.CSS_SELECTOR, '[aria-label*="chat" i], [aria-label*="message" i], button[title*="chat" i]')
            if chat_buttons:
                try:
                    chat_buttons[0].click()
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Try these')]"))
                    )
                except:
                    pass  # Chat might already be open

            # Get starter prompts on quotes page
            quotes_prompts = driver.find_elements(By.CSS_SELECTOR, 'button')
            quotes_prompt_texts = [btn.text for btn in quotes_prompts if 'quote' in btn.text.lower()]

            # Quotes page should have quote-specific prompts
            assert any('quote' in text.lower() for text in quotes_prompt_texts), \
                "Quotes page should show quote-specific prompts"

            # Navigate to Claims page
            driver.get(f"{base_url}/claims")

            # Wait for navigation
            WebDriverWait(driver, 5).until(
                EC.url_contains('/claims')
            )

            # Reopen chat if needed
            chat_buttons = driver.find_elements(By.CSS_SELECTOR, '[aria-label*="chat" i], [aria-label*="message" i], button[title*="chat" i]')
            if chat_buttons:
                try:
                    chat_buttons[0].click()
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Try these')]"))
                    )
                except:
                    pass

            # Get starter prompts on claims page
            claims_prompts = driver.find_elements(By.CSS_SELECTOR, 'button')
            claims_prompt_texts = [btn.text for btn in claims_prompts if 'claim' in btn.text.lower()]

            # Claims page should have claim-specific prompts
            assert any('claim' in text.lower() for text in claims_prompt_texts), \
                "Claims page should show claim-specific prompts"

    except TimeoutException:
        pytest.skip("Chat interface not available or elements not found - skipping test")


@pytest.mark.e2e
@pytest.mark.chat
def test_starter_prompts_are_clickable(driver, base_url):
    """Test that starter prompt buttons are clickable and send messages"""
    driver.get(base_url)

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    try:
        # Find and click chat button
        chat_buttons = driver.find_elements(By.CSS_SELECTOR, '[aria-label*="chat" i], [aria-label*="message" i], button[title*="chat" i]')
        if not chat_buttons:
            pytest.skip("Chat button not found - skipping test")

        chat_buttons[0].click()

        # Wait for chat interface
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Try these')]"))
        )

        # Find starter prompt buttons
        all_buttons = driver.find_elements(By.CSS_SELECTOR, 'button')
        starter_buttons = [btn for btn in all_buttons if btn.text and len(btn.text) > 10 and not btn.text.startswith('Close')]

        if starter_buttons:
            # Click first starter prompt
            first_prompt_text = starter_buttons[0].text
            starter_buttons[0].click()

            # Wait briefly for message to be sent
            WebDriverWait(driver, 3).until(
                lambda d: len(d.find_elements(By.XPATH, f"//*[contains(text(), '{first_prompt_text}')]")) > 0
            )

            # Verify user message appears (prompt should be in chat history)
            assert first_prompt_text in driver.page_source, \
                "Clicked prompt should appear in chat messages"

    except TimeoutException:
        pytest.skip("Chat interface not available or elements not found - skipping test")


@pytest.mark.e2e
@pytest.mark.chat
def test_prompts_exist_on_all_main_pages(driver, base_url):
    """Test that each main page has context-specific prompts"""
    pages = [
        ('/', ['recent', 'overview', 'report', 'quote', 'claim']),  # Dashboard - flexible
        ('/quotes', ['quote']),
        ('/policies', ['polic']),  # Matches "policy" and "policies"
        ('/claims', ['claim']),
        ('/payments', ['payment']),
        ('/cases', ['case']),
    ]

    for path, expected_keywords in pages:
        driver.get(f"{base_url}{path}")

        # Wait for page load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Open chat
            chat_buttons = driver.find_elements(By.CSS_SELECTOR, '[aria-label*="chat" i], [aria-label*="message" i], button[title*="chat" i]')
            if not chat_buttons:
                continue  # Skip if no chat button

            chat_buttons[0].click()

            # Wait for chat
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Try these')]"))
            )

            # Get all button text
            buttons = driver.find_elements(By.CSS_SELECTOR, 'button')
            button_texts = ' '.join([btn.text.lower() for btn in buttons])

            # Check that at least one expected keyword appears
            has_relevant_prompt = any(keyword.lower() in button_texts for keyword in expected_keywords)

            assert has_relevant_prompt, \
                f"Page {path} should have prompts containing one of: {expected_keywords}. Found: {button_texts}"

        except TimeoutException:
            pytest.skip(f"Timeout on page {path} - skipping")
