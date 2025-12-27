# Silvermoat E2E Test Suite

End-to-end tests using Selenium WebDriver to validate UI functionality and workflows.

## Prerequisites

- Python 3.9+
- Chrome browser
- ChromeDriver (automatically managed by Selenium 4.6+)

## Installation

```bash
# Install test dependencies
pip install -r requirements-test.txt
```

## Running Tests

### Local Development

Run against local dev server:

```bash
# Start the UI dev server
cd ui
npm run dev

# In another terminal, run tests
cd tests/e2e
BASE_URL=http://localhost:5173 pytest
```

### Against Deployed Stack

Run against a deployed CloudFormation stack:

```bash
# Set stack name (defaults to 'silvermoat')
export STACK_NAME=silvermoat

# Tests will automatically fetch URLs from stack outputs
cd tests/e2e
pytest
```

Alternatively, provide URLs directly:

```bash
cd tests/e2e
BASE_URL=https://xyz123.cloudfront.net API_URL=https://api.example.com pytest
```

## Test Organization

```
tests/e2e/
├── conftest.py          # Pytest fixtures (driver, URLs)
├── pytest.ini           # Pytest configuration
├── pages/               # Page Object Model classes
│   ├── base_page.py     # Base page with common methods
│   └── home_page.py     # Home page object
├── tests/               # Test cases
│   └── test_smoke.py    # Smoke tests
└── utils/               # Helper functions
    └── aws_helpers.py   # CloudFormation stack helpers
```

## Test Markers

Use pytest markers to run specific test categories:

```bash
# Run only smoke tests
pytest -m smoke

# Run responsive design tests
pytest -m responsive

# Run quote workflow tests
pytest -m quote

# Run all except slow tests
pytest -m "not slow"
```

Available markers:
- `smoke` - Quick validation tests
- `quote` - Quote workflow tests
- `policy` - Policy management tests
- `claims` - Claims processing tests
- `payments` - Payment tests
- `chat` - Chat assistant tests
- `responsive` - Responsive design tests
- `slow` - Long-running tests

## Running in Headless Mode

Tests run in headless mode by default (configured in `conftest.py`). To run with visible browser:

```bash
# Edit conftest.py and comment out:
# options.add_argument("--headless")
```

## Parallel Execution

Run tests in parallel for faster execution:

```bash
# Run with 4 workers
pytest -n 4
```

## Test Reports

Tests generate an HTML report by default:

```bash
pytest
# Opens test-report.html
```

## Writing New Tests

### 1. Create a Page Object

```python
# tests/e2e/pages/quotes_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class QuotesPage(BasePage):
    # Locators
    NEW_QUOTE_BUTTON = (By.ID, "new-quote")

    def click_new_quote(self):
        self.click_element(self.NEW_QUOTE_BUTTON)
```

### 2. Write Test Cases

```python
# tests/e2e/tests/test_quotes.py
import pytest
from pages.quotes_page import QuotesPage

@pytest.mark.quote
def test_create_quote(driver, base_url):
    quotes_page = QuotesPage(driver, base_url)
    quotes_page.load()
    quotes_page.click_new_quote()

    assert quotes_page.is_form_visible()
```

## Troubleshooting

### ChromeDriver Issues

If you see ChromeDriver errors:

```bash
# Selenium 4.6+ automatically manages ChromeDriver
# If issues persist, ensure Chrome browser is installed:
google-chrome --version
```

### Element Not Found

If tests fail with element not found:
1. Increase wait times in `conftest.py`
2. Update locators in page objects
3. Check if UI structure changed

### AWS Credentials

If using stack outputs, ensure AWS credentials are configured:

```bash
aws configure
# or set environment variables:
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
```

## CI/CD Integration

Tests are configured to run in GitHub Actions on pull requests. See `.github/workflows/e2e-tests.yml`.

The workflow:
- Triggers on PRs to main
- Fetches stack outputs from CloudFormation
- Installs Chrome and ChromeDriver
- Runs pytest with HTML reports
- Posts results as PR comment
- Uploads test artifacts

## Next Steps

### Planned Test Coverage

- [ ] Quote workflow (create, view, convert to policy)
- [ ] Policy management (list, search, view details)
- [ ] Claims processing (file claim, upload docs, status updates)
- [ ] Payments (view history, process payment)
- [ ] Chat assistant (open chat, send message, verify response)
- [ ] Navigation and routing
- [ ] Form validation
- [ ] Error handling

### Enhancements

- [ ] Add Allure reporting for better test reports
- [ ] Implement data-driven tests with parameterization
- [ ] Add performance testing (page load times)
- [ ] Screenshot capture on test failure
- [ ] Video recording for failed tests
- [ ] Integration with test management tools
