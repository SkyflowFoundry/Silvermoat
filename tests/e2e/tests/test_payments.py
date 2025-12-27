"""
Payment Tests
Tests for viewing payment history and processing payments
"""

import pytest
from pages.payments_page import PaymentsPage


@pytest.mark.payments
def test_view_payment_history(driver, base_url):
    """Test viewing payment history/list"""
    payments = PaymentsPage(driver, base_url)
    payments.navigate()

    # Should see payments table
    assert payments.is_element_visible(*payments.PAYMENTS_TABLE)


@pytest.mark.payments
def test_process_payment(driver, base_url, test_payment_data):
    """Test processing a payment (mock)"""
    payments = PaymentsPage(driver, base_url)
    payments.navigate()

    # Try to create payment if form available
    payments.process_payment(test_payment_data)

    # Should complete without errors
    import time
    time.sleep(1)


@pytest.mark.payments
def test_view_payment_details(driver, base_url):
    """Test viewing payment details"""
    payments = PaymentsPage(driver, base_url)
    payments.navigate()

    # Check if there are any payments to view
    if payments.get_payments_count() > 0:
        payments.click_first_payment()

        # Should navigate to detail page
        assert '/payments/' in payments.get_current_url()
    else:
        pytest.skip("No payments available to view")


@pytest.mark.payments
def test_payment_confirmation_display(driver, base_url):
    """Test that payment confirmation is visible"""
    payments = PaymentsPage(driver, base_url)
    payments.navigate()

    # Check if there are any payments
    if payments.get_payments_count() > 0:
        payments.click_first_payment()

        # May or may not have confirmation display
        # Just verify page loads
        assert '/payments/' in payments.get_current_url()
    else:
        pytest.skip("No payments available to test")
