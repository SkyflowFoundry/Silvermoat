"""
E2E tests for README viewer functionality on the landing page.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestReadmeViewer:
    """Test suite for README viewer modal on landing page."""

    def test_floating_icon_visible(self, driver, base_url):
        """Test that floating info icon is visible on landing page."""
        driver.get(base_url)

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        # Find the floating icon (InfoCircleOutlined within the floating div)
        floating_icon = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[style*='position: fixed'][style*='bottom: 24px']")
            )
        )

        assert floating_icon.is_displayed(), "Floating info icon should be visible"

    def test_click_icon_opens_modal(self, driver, base_url):
        """Test that clicking the floating icon opens the README modal."""
        driver.get(base_url)

        # Wait for page to load and find floating icon
        floating_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div[style*='position: fixed'][style*='bottom: 24px']")
            )
        )

        # Click the icon
        floating_icon.click()

        # Wait for modal to appear
        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-modal"))
        )

        assert modal.is_displayed(), "Modal should be displayed after clicking icon"

        # Check for modal title
        modal_title = driver.find_element(By.CSS_SELECTOR, ".ant-modal-title")
        assert modal_title.text == "Project Documentation", "Modal should have correct title"

    def test_modal_displays_readme_content(self, driver, base_url):
        """Test that the modal displays README content."""
        driver.get(base_url)

        # Click floating icon
        floating_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div[style*='position: fixed'][style*='bottom: 24px']")
            )
        )
        floating_icon.click()

        # Wait for modal content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".readme-content"))
        )

        # Check for README content markers (h1 should contain "Silvermoat")
        readme_content = driver.find_element(By.CSS_SELECTOR, ".readme-content")
        assert "Silvermoat" in readme_content.text, "README content should contain 'Silvermoat'"

    def test_close_modal(self, driver, base_url):
        """Test that the modal can be closed."""
        driver.get(base_url)

        # Open modal
        floating_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div[style*='position: fixed'][style*='bottom: 24px']")
            )
        )
        floating_icon.click()

        # Wait for modal to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-modal"))
        )

        # Find and click close button
        close_button = driver.find_element(By.CSS_SELECTOR, ".ant-modal-close")
        close_button.click()

        # Wait for modal to disappear
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ant-modal"))
        )

        # Verify modal is no longer visible
        modals = driver.find_elements(By.CSS_SELECTOR, ".ant-modal")
        assert len(modals) == 0 or not modals[0].is_displayed(), "Modal should be closed"

    def test_modal_renders_mermaid_diagrams(self, driver, base_url):
        """Test that mermaid diagrams are rendered in the modal."""
        driver.get(base_url)

        # Open modal
        floating_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div[style*='position: fixed'][style*='bottom: 24px']")
            )
        )
        floating_icon.click()

        # Wait for modal and README content
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".readme-content"))
        )

        # Wait a bit for mermaid rendering (may take a moment)
        import time
        time.sleep(2)

        # Check for mermaid elements (rendered as SVG)
        mermaid_elements = driver.find_elements(By.CSS_SELECTOR, ".mermaid")

        # Should have mermaid elements since README contains diagrams
        assert len(mermaid_elements) > 0, "README should contain mermaid diagrams"

    def test_icon_not_on_other_pages(self, driver, base_url):
        """Test that the floating icon only appears on landing page."""
        # Navigate to dashboard page
        driver.get(f"{base_url}/dashboard")

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Check that floating icon is not present
        floating_icons = driver.find_elements(
            By.CSS_SELECTOR,
            "div[style*='position: fixed'][style*='bottom: 24px']"
        )

        # Should not find the icon on non-landing pages
        assert len(floating_icons) == 0, "Floating icon should only appear on landing page"
