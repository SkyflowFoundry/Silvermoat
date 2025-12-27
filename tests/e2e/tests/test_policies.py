"""
Policy Management Tests
Tests for viewing, searching, and managing policies
"""

import pytest
from pages.policies_page import PoliciesPage


@pytest.mark.policies
def test_view_policies_list(driver, base_url):
    """Test viewing policies list"""
    policies = PoliciesPage(driver, base_url)
    policies.navigate()

    # Should see policies table
    assert policies.is_element_visible(*policies.POLICY_TABLE)


@pytest.mark.policies
def test_search_policies(driver, base_url):
    """Test searching/filtering policies"""
    policies = PoliciesPage(driver, base_url)
    policies.navigate()

    # Try to search (search may not be implemented yet)
    policies.search_policies("test")

    # Should still see table after search
    assert policies.is_element_visible(*policies.POLICY_TABLE)


@pytest.mark.policies
def test_view_policy_details(driver, base_url):
    """Test viewing policy details"""
    policies = PoliciesPage(driver, base_url)
    policies.navigate()

    # Check if there are any policies to view
    if policies.get_policy_count() > 0:
        policies.click_first_policy()

        # Should navigate to detail page
        assert policies.is_on_detail_page()
    else:
        pytest.skip("No policies available to view")


@pytest.mark.policies
def test_policy_status_display(driver, base_url):
    """Test that policy status is displayed correctly"""
    policies = PoliciesPage(driver, base_url)
    policies.navigate()

    # Check if there are any policies
    if policies.get_policy_count() > 0:
        policies.click_first_policy()

        # Should see status on detail page
        status = policies.get_policy_status()
        assert status is not None, "Policy status not displayed"
    else:
        pytest.skip("No policies available to test")


@pytest.mark.policies
def test_refresh_policies(driver, base_url):
    """Test refreshing policy list"""
    policies = PoliciesPage(driver, base_url)
    policies.navigate()

    initial_count = policies.get_policy_count()

    policies.refresh_policies()

    # Should reload without errors
    assert policies.is_element_visible(*policies.POLICY_TABLE)
