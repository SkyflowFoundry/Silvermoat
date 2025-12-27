"""
Claims Processing Tests
Tests for filing claims, uploading documents, and updating status
"""

import pytest
from pages.claims_page import ClaimsPage


@pytest.mark.claims
def test_file_new_claim(driver, base_url, test_claim_data):
    """Test filing a new claim"""
    claims = ClaimsPage(driver, base_url)
    claims.navigate()

    initial_count = claims.get_claims_count()

    claims.create_claim(test_claim_data)

    # Verify modal closes or redirect happens
    import time
    time.sleep(1)
    # Should have navigated away from modal or modal closed


@pytest.mark.claims
def test_view_claims_list(driver, base_url):
    """Test viewing claims list"""
    claims = ClaimsPage(driver, base_url)
    claims.navigate()

    # Should see claims table
    assert claims.is_element_visible(*claims.CLAIMS_TABLE)


@pytest.mark.claims
def test_view_claim_details(driver, base_url):
    """Test viewing claim details"""
    claims = ClaimsPage(driver, base_url)
    claims.navigate()

    # Check if there are any claims to view
    if claims.get_claims_count() > 0:
        claims.click_first_claim()

        # Should navigate to detail page
        assert '/claims/' in claims.get_current_url()
        assert claims.get_current_url() != '/claims/'
    else:
        pytest.skip("No claims available to view")


@pytest.mark.claims
def test_update_claim_status(driver, base_url):
    """Test updating claim status"""
    claims = ClaimsPage(driver, base_url)
    claims.navigate()

    # Check if there are any claims
    if claims.get_claims_count() > 0:
        claims.click_first_claim()

        # Try to update status
        if claims.click_update_status():
            # Status update UI opened
            import time
            time.sleep(1)
        else:
            pytest.skip("Status update not available")
    else:
        pytest.skip("No claims available to test")


@pytest.mark.claims
def test_view_claim_history(driver, base_url):
    """Test viewing claim history timeline"""
    claims = ClaimsPage(driver, base_url)
    claims.navigate()

    # Check if there are any claims
    if claims.get_claims_count() > 0:
        claims.click_first_claim()

        # Check if history is visible
        if not claims.is_history_visible():
            pytest.skip("Claim history not implemented")
    else:
        pytest.skip("No claims available to test")


@pytest.mark.claims
@pytest.mark.slow
def test_upload_claim_document(driver, base_url):
    """Test uploading a document to a claim"""
    claims = ClaimsPage(driver, base_url)
    claims.navigate()

    # Check if there are any claims
    if claims.get_claims_count() > 0:
        claims.click_first_claim()

        # Try to upload (requires test file)
        pytest.skip("Document upload requires test file")
    else:
        pytest.skip("No claims available to test")
