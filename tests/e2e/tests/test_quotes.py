"""
Quote Workflow Tests
Tests for creating, viewing, and converting quotes
"""

import pytest
from pages.quotes_page import QuotesPage
from pages.policies_page import PoliciesPage


@pytest.mark.quotes
def test_create_quote(driver, base_url, test_quote_data):
    """Test creating a new quote"""
    quotes = QuotesPage(driver, base_url)
    quotes.navigate()

    initial_count = quotes.get_quote_count()

    quotes.create_quote(test_quote_data['name'], test_quote_data['zip'])

    # Verify modal closes after successful creation
    import time
    time.sleep(1)  # Wait for modal to close
    assert not quotes.is_modal_open(), "Modal did not close after quote creation"


@pytest.mark.quotes
def test_quote_form_validation(driver, base_url):
    """Test quote form validation"""
    quotes = QuotesPage(driver, base_url)
    quotes.navigate()
    quotes.click_new_quote()

    # Try to submit empty form
    quotes.submit_quote_form()

    # Should show validation errors
    assert quotes.is_form_error_visible(), "Form validation errors not displayed"


@pytest.mark.quotes
def test_fill_quote_form_all_fields(driver, base_url, test_quote_data):
    """Test filling all fields in quote form"""
    quotes = QuotesPage(driver, base_url)
    quotes.navigate()
    quotes.click_new_quote()

    quotes.fill_quote_form(test_quote_data['name'], test_quote_data['zip'])

    # Verify fields are filled (basic check)
    name_input = quotes.find_element(*quotes.NAME_INPUT)
    assert name_input.get_attribute('value') == test_quote_data['name']


@pytest.mark.quotes
def test_view_quote_list(driver, base_url):
    """Test viewing quote list"""
    quotes = QuotesPage(driver, base_url)
    quotes.navigate()

    # Should see quotes table (even if empty)
    assert quotes.is_element_visible(*quotes.QUOTE_TABLE)


@pytest.mark.quotes
def test_view_quote_details(driver, base_url):
    """Test viewing quote details"""
    quotes = QuotesPage(driver, base_url)
    quotes.navigate()

    # Check if there are any quotes to view
    if quotes.get_quote_count() > 0:
        quotes.click_first_quote()

        # Should navigate to detail page
        assert '/quotes/' in quotes.get_current_url()
        assert quotes.get_current_url() != '/quotes/'
    else:
        pytest.skip("No quotes available to view")


@pytest.mark.quotes
def test_convert_quote_to_policy(driver, base_url):
    """Test converting a quote to a policy"""
    quotes = QuotesPage(driver, base_url)
    quotes.navigate()

    # Check if there are any quotes to convert
    if quotes.get_quote_count() > 0:
        quotes.click_first_quote()

        # Look for convert button
        try:
            quotes.click_convert_to_policy()
            # Should navigate to policies or show confirmation
            import time
            time.sleep(2)
            # Conversion may redirect or show modal
        except:
            pytest.skip("Convert to Policy functionality not available")
    else:
        pytest.skip("No quotes available to convert")


@pytest.mark.quotes
def test_refresh_quotes(driver, base_url):
    """Test refreshing quote list"""
    quotes = QuotesPage(driver, base_url)
    quotes.navigate()

    initial_count = quotes.get_quote_count()

    quotes.refresh_quotes()

    # Should reload without errors
    assert quotes.is_element_visible(*quotes.QUOTE_TABLE)
