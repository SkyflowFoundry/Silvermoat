# E2E Test Suite for Silvermoat

Comprehensive end-to-end testing using Selenium WebDriver to validate UI functionality and workflows.

## Overview

This test suite covers:
- **Smoke Tests**: Application loading, API connectivity, navigation (6 tests)
- **Quote Workflow**: Create, view, validate, convert quotes (7 tests)
- **Policy Management**: View, search, status display (5 tests)
- **Claims Processing**: File, view, status updates, history (6 tests)
- **Payments**: View history, process, confirmations (4 tests)
- **Chat Assistant**: Open, send messages, quick actions (4 tests)
- **Responsive Design**: Mobile, tablet, desktop viewports (3 tests)

**Total: 35+ test cases**

## Architecture

### Page Object Model (POM)
Tests use the Page Object Model pattern for maintainability:

```
tests/e2e/
├── pages/              # Page objects (UI abstractions)
│   ├── base_page.py    # Common methods for all pages
│   ├── home_page.py    # Dashboard and navigation
│   ├── quotes_page.py  # Quote management
│   ├── policies_page.py
│   ├── claims_page.py
│   ├── payments_page.py
│   └── chat_page.py
├── tests/              # Test cases
│   ├── test_smoke.py
│   ├── test_quotes.py
│   ├── test_policies.py
│   ├── test_claims.py
│   ├── test_payments.py
│   └── test_chat.py
├── utils/              # Helper functions
│   └── aws_helpers.py  # CloudFormation integration
├── conftest.py         # Pytest fixtures
└── pytest.ini          # Pytest configuration
```

## Setup

### Prerequisites
- Python 3.11+
- Chrome browser
- AWS credentials (optional, for CloudFormation integration)

### Installation

```bash
# Install dependencies
pip install -r requirements-test.txt

# Chrome/ChromeDriver will be auto-managed by webdriver-manager
```

## Running Tests

### Local Development

Test against local dev server:

```bash
# Start UI dev server
cd ui
npm run dev

# Run tests
cd tests/e2e
BASE_URL=http://localhost:5173 pytest tests/ -v
```

### Against Deployed Stack

Test against a deployed CloudFormation stack:

```bash
cd tests/e2e

# Option 1: Use stack name (auto-fetches URLs)
STACK_NAME=silvermoat pytest tests/ -v

# Option 2: Specify URLs directly
SILVERMOAT_URL=https://your-bucket.s3-website.amazonaws.com \
SILVERMOAT_API_URL=https://your-api.execute-api.us-east-1.amazonaws.com/demo \
pytest tests/ -v
```

### Test Filtering

Run specific test categories using markers:

```bash
# Smoke tests only
pytest -m smoke

# Quote workflow tests
pytest -m quotes

# All except slow tests
pytest -m "not slow"

# Multiple markers
pytest -m "smoke or quotes"
```

Available markers:
- `smoke`: Basic functionality tests
- `quotes`: Quote workflow tests
- `policies`: Policy management tests
- `claims`: Claims processing tests
- `payments`: Payment tests
- `chat`: Chat assistant tests
- `responsive`: Responsive design tests
- `slow`: Tests that take longer to run

### Headless Mode

Run tests headless (for CI/CD):

```bash
HEADLESS=1 pytest tests/ -v
```

### Specific Test Files

```bash
# Run single test file
pytest tests/test_quotes.py -v

# Run single test function
pytest tests/test_quotes.py::test_create_quote -v
```

## Configuration

### Environment Variables

- `BASE_URL` / `SILVERMOAT_URL`: Application URL (default: `http://localhost:5173`)
- `API_BASE_URL` / `SILVERMOAT_API_URL`: API endpoint URL
- `STACK_NAME` / `TEST_STACK_NAME`: CloudFormation stack name (auto-fetches URLs)
- `HEADLESS`: Set to `1` to run headless
- `CI`: Auto-detected in CI/CD environments

### Pytest Configuration

See `pytest.ini` for:
- Test discovery patterns
- Marker definitions
- Output options
- Logging configuration

## Test Reports

HTML reports are generated automatically:

```bash
# Run tests with HTML report
pytest tests/ --html=reports/e2e-report.html --self-contained-html

# Open report
open reports/e2e-report.html
```

## Writing New Tests

### Example: Add a new test

```python
# tests/test_example.py
import pytest
from pages.quotes_page import QuotesPage

@pytest.mark.quotes
def test_example(driver, base_url):
    """Test description"""
    quotes = QuotesPage(driver, base_url)
    quotes.navigate()

    # Your test logic
    assert quotes.is_element_visible(*quotes.QUOTE_TABLE)
```

### Page Object Example

```python
# pages/example_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class ExamplePage(BasePage):
    # Locators
    BUTTON = (By.ID, "my-button")

    def click_button(self):
        self.click(*self.BUTTON)
```

## CI/CD Integration

Tests can be integrated with GitHub Actions. See `.github/workflows/e2e-tests.yml` for workflow configuration.

Workflow features:
- Runs on PR to main
- Fetches stack outputs automatically
- Installs Chrome/ChromeDriver
- Generates HTML reports
- Posts results as PR comment

## Troubleshooting

### ChromeDriver Issues

```bash
# Update ChromeDriver manually
pip install --upgrade webdriver-manager
```

### Element Not Found

- Increase implicit wait in `conftest.py`
- Use explicit waits in page objects
- Check element locators match actual UI

### Tests Pass Locally but Fail in CI

- Add `HEADLESS=1` locally to debug
- Check timing issues (add waits)
- Verify CloudFormation stack is deployed

### AWS Credentials

```bash
# Configure AWS CLI
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
```

## Best Practices

1. **Use Page Objects**: Never interact with Selenium directly in tests
2. **Explicit Waits**: Use `wait_for_*` methods instead of `time.sleep()`
3. **Markers**: Tag tests appropriately for filtering
4. **Test Data**: Use fixtures for test data
5. **Skip Wisely**: Use `pytest.skip()` when preconditions aren't met
6. **Cleanup**: Tests should not leave side effects

## Test Data

Test data is provided via pytest fixtures in `conftest.py`:
- `test_quote_data`: Sample quote data
- `test_claim_data`: Sample claim data
- `test_payment_data`: Sample payment data

Tests use seeded demo data from CloudFormation deployment plus additional test-specific data with parity to seed data format.

## Coverage Summary

| Category | Tests | Status |
|----------|-------|--------|
| Smoke | 6 | ✅ Complete |
| Quote Workflow | 7 | ✅ Complete |
| Policy Management | 5 | ✅ Complete |
| Claims Processing | 6 | ✅ Complete |
| Payments | 4 | ✅ Complete |
| Chat Assistant | 4 | ✅ Complete |
| Responsive Design | 3 | ✅ Complete |
| **Total** | **35+** | **✅ Complete** |

## Next Steps

- Expand test data utilities for complex scenarios
- Add visual regression testing
- Integrate with Allure reporting
- Add performance testing metrics
- Implement parallel test execution with Selenium Grid
