"""
E2E Tests for Context-Aware Chat Starter Prompts

Tests that chat starter prompts change based on the current page/route.
Infrastructure-agnostic tests focusing on user-facing functionality.
"""

import pytest
from ..pages.chat_page import ChatPage
from ..pages.home_page import HomePage


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.chat
def test_chat_opens_on_homepage(driver, base_url):
    """Test that chat interface can be opened"""
    chat_page = ChatPage(driver, base_url)
    chat_page.navigate_to("/")
    chat_page.wait_for_page_load()

    # Open chat
    chat_page.open_chat()

    # Chat should be open
    assert chat_page.is_chat_open(), "Chat drawer should be open"


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.chat
def test_dashboard_starter_prompts(driver, base_url):
    """Test that dashboard shows dashboard-specific starter prompts"""
    chat_page = ChatPage(driver, base_url)
    chat_page.navigate_to("/")
    chat_page.wait_for_page_load()

    # Open chat on dashboard
    chat_page.open_chat()

    # Get starter prompts
    prompts = chat_page.get_starter_prompts()

    # Should have at least 3 prompts
    assert len(prompts) >= 3, f"Should have at least 3 starter prompts, found {len(prompts)}"

    # Dashboard prompts should be relevant to dashboard
    prompt_text = " ".join(prompts).lower()
    assert any(keyword in prompt_text for keyword in ['recent', 'overview', 'report', 'quote', 'claim']), \
        f"Dashboard prompts should be relevant to dashboard: {prompts}"


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.chat
def test_quotes_page_starter_prompts(driver, base_url):
    """Test that quotes page shows quote-specific starter prompts"""
    chat_page = ChatPage(driver, base_url)
    home_page = HomePage(driver, base_url)

    # Navigate to quotes page
    home_page.load()
    home_page.navigate_to_quotes()
    chat_page.wait_for_page_load()

    # Open chat on quotes page
    chat_page.open_chat()

    # Get starter prompts
    prompts = chat_page.get_starter_prompts()

    # Should have at least 3 prompts
    assert len(prompts) >= 3, f"Should have at least 3 starter prompts, found {len(prompts)}"

    # Quotes prompts should mention quotes
    prompt_text = " ".join(prompts).lower()
    assert 'quote' in prompt_text, f"Quotes page prompts should mention 'quote': {prompts}"


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.chat
def test_policies_page_starter_prompts(driver, base_url):
    """Test that policies page shows policy-specific starter prompts"""
    chat_page = ChatPage(driver, base_url)
    home_page = HomePage(driver, base_url)

    # Navigate to policies page
    home_page.load()
    home_page.navigate_to_policies()
    chat_page.wait_for_page_load()

    # Open chat on policies page
    chat_page.open_chat()

    # Get starter prompts
    prompts = chat_page.get_starter_prompts()

    # Should have at least 3 prompts
    assert len(prompts) >= 3, f"Should have at least 3 starter prompts, found {len(prompts)}"

    # Policies prompts should mention policies
    prompt_text = " ".join(prompts).lower()
    assert 'policy' in prompt_text or 'policies' in prompt_text, \
        f"Policies page prompts should mention 'policy' or 'policies': {prompts}"


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.chat
def test_claims_page_starter_prompts(driver, base_url):
    """Test that claims page shows claim-specific starter prompts"""
    chat_page = ChatPage(driver, base_url)
    home_page = HomePage(driver, base_url)

    # Navigate to claims page
    home_page.load()
    home_page.navigate_to_claims()
    chat_page.wait_for_page_load()

    # Open chat on claims page
    chat_page.open_chat()

    # Get starter prompts
    prompts = chat_page.get_starter_prompts()

    # Should have at least 3 prompts
    assert len(prompts) >= 3, f"Should have at least 3 starter prompts, found {len(prompts)}"

    # Claims prompts should mention claims
    prompt_text = " ".join(prompts).lower()
    assert 'claim' in prompt_text, f"Claims page prompts should mention 'claim': {prompts}"


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.chat
def test_payments_page_starter_prompts(driver, base_url):
    """Test that payments page shows payment-specific starter prompts"""
    chat_page = ChatPage(driver, base_url)
    home_page = HomePage(driver, base_url)

    # Navigate to payments page
    home_page.load()
    home_page.navigate_to_payments()
    chat_page.wait_for_page_load()

    # Open chat on payments page
    chat_page.open_chat()

    # Get starter prompts
    prompts = chat_page.get_starter_prompts()

    # Should have at least 3 prompts
    assert len(prompts) >= 3, f"Should have at least 3 starter prompts, found {len(prompts)}"

    # Payments prompts should mention payments or invoices
    prompt_text = " ".join(prompts).lower()
    assert any(keyword in prompt_text for keyword in ['payment', 'invoice']), \
        f"Payments page prompts should mention 'payment' or 'invoice': {prompts}"


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.chat
def test_prompts_differ_by_page(driver, base_url):
    """Test that starter prompts actually change between pages"""
    chat_page = ChatPage(driver, base_url)
    home_page = HomePage(driver, base_url)

    # Get dashboard prompts
    home_page.load()
    chat_page.open_chat()
    dashboard_prompts = chat_page.get_starter_prompts()
    chat_page.close_chat()

    # Get quotes page prompts
    home_page.navigate_to_quotes()
    chat_page.wait_for_page_load()
    chat_page.open_chat()
    quotes_prompts = chat_page.get_starter_prompts()
    chat_page.close_chat()

    # Prompts should be different
    assert dashboard_prompts != quotes_prompts, \
        f"Starter prompts should differ between pages.\nDashboard: {dashboard_prompts}\nQuotes: {quotes_prompts}"


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.chat
def test_starter_prompt_clickable(driver, base_url):
    """Test that starter prompts are clickable and send messages"""
    chat_page = ChatPage(driver, base_url)
    chat_page.navigate_to("/")
    chat_page.wait_for_page_load()

    # Open chat
    chat_page.open_chat()

    # Get first starter prompt text
    prompts = chat_page.get_starter_prompts()
    first_prompt = prompts[0] if prompts else None

    assert first_prompt, "Should have at least one starter prompt"

    # Click first starter prompt
    chat_page.click_starter_prompt(0)

    # Wait for message to appear
    chat_page.wait_for_messages(min_count=1, timeout=10)

    # Should have at least one message (user's message from clicking prompt)
    messages = chat_page.get_messages()
    assert len(messages) > 0, "Clicking starter prompt should send a message"

    # First message should match the prompt text
    first_message = messages[0].strip().lower()
    assert first_message == first_prompt.lower(), \
        f"First message should exactly match prompt. Expected: '{first_prompt}', Got: '{messages[0]}'"
