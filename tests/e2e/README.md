# Silvermoat E2E Test Suite

End-to-end tests using Selenium WebDriver with pytest.

## Setup

### Prerequisites
- Python 3.11+
- Chrome browser (for local testing)
- Deployed Silvermoat stack (or local dev server)

### Installation

```bash
# Install test dependencies
pip install -r requirements-test.txt
```

## Running Tests

### Against Deployed Stack

```bash
# Set environment variables
export SILVERMOAT_URL="https://your-silvermoat-url.com"
export SILVERMOAT_API_URL="https://your-api-url.com"
export STACK_NAME="silvermoat"  # optional

# Run all tests
cd tests/e2e
pytest tests/ -v

# Run specific test categories
pytest tests/ -m smoke -v
pytest tests/ -m quotes -v
```

### Automatic URL Discovery

If you have AWS credentials configured, tests can auto-discover URLs:

```bash
export STACK_NAME="silvermoat"
cd tests/e2e
pytest tests/ -v
```

The test suite will fetch stack outputs automatically.

### Local Development

```bash
# Start UI dev server
cd ui
npm run dev

# In another terminal, run tests
export SILVERMOAT_URL="http://localhost:5173"
export SILVERMOAT_API_URL="https://your-deployed-api-url.com"
cd tests/e2e
pytest tests/ -v
```

## Test Structure

```
tests/e2e/
├── conftest.py          # Pytest configuration and fixtures
├── pytest.ini           # Pytest settings
├── pages/               # Page Object Model classes
│   ├── base_page.py
│   ├── home_page.py
│   └── ...
├── tests/               # Test cases
│   ├── test_smoke.py
│   ├── test_quotes.py
│   └── ...
└── utils/               # Helper functions
    └── aws_helpers.py
```

## Page Object Model

Tests use the Page Object Model pattern to separate page structure from test logic:

```python
from pages.home_page import HomePage

def test_navigation(driver, base_url):
    home = HomePage(driver, base_url)
    home.navigate()
    home.navigate_to_quotes()
    # assertions...
```

## Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.smoke` - Basic functionality
- `@pytest.mark.quotes` - Quote workflows
- `@pytest.mark.policies` - Policy management
- `@pytest.mark.claims` - Claims processing
- `@pytest.mark.payments` - Payment tests
- `@pytest.mark.chat` - Chat assistant
- `@pytest.mark.responsive` - Responsive design

Run specific markers:
```bash
pytest -m smoke
pytest -m "quotes or policies"
```

## CI/CD Integration

Tests run automatically on pull requests via GitHub Actions (`.github/workflows/e2e-tests.yml`).

### Required Secrets
- `AWS_ROLE_ARN` - IAM role for accessing stack outputs

### Workflow Triggers
- Pull requests to `main` affecting UI, infra, or tests
- Manual trigger via workflow dispatch

## Test Reports

HTML reports are generated automatically:

```bash
pytest tests/ --html=test-report.html --self-contained-html
```

Reports are uploaded as artifacts in CI/CD runs.

## Writing New Tests

1. Create page object in `pages/` if needed:
```python
from .base_page import BasePage

class MyPage(BasePage):
    ELEMENT = (By.ID, "my-id")

    def do_action(self):
        self.click_element(*self.ELEMENT)
```

2. Create test in `tests/`:
```python
from pages.my_page import MyPage

def test_my_feature(driver, base_url):
    page = MyPage(driver, base_url)
    page.navigate()
    page.do_action()
    assert page.is_loaded()
```

3. Add appropriate marker:
```python
@pytest.mark.smoke
def test_my_feature(driver, base_url):
    # test code
```

## Troubleshooting

### ChromeDriver issues
Tests auto-install ChromeDriver via `webdriver-manager`. If issues occur:
```bash
pip install --upgrade webdriver-manager
```

### Timeout errors
Adjust implicit wait in `conftest.py`:
```python
driver.implicitly_wait(20)  # seconds
```

### Element not found
Check if page is using dynamic rendering. Use explicit waits:
```python
from selenium.webdriver.support import expected_conditions as EC
wait.until(EC.presence_of_element_located((By.ID, "my-id")))
```

### AWS credentials
For local testing with stack outputs:
```bash
aws configure
# or
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
```
