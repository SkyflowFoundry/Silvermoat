# E2E Tests (Selenium)

End-to-end UI tests using Selenium WebDriver.

## Overview

Selenium-based tests for:
- Smoke tests (app loads, navigation, API connectivity)
- Quote workflow (create, submit, view, convert)
- Policy management (view, search, filter)
- Claims processing (file, upload docs, status updates)
- Payments (view history, process payments)
- Chat assistant interaction
- Responsive design (mobile, tablet, desktop)

## Running Tests

### Prerequisites

```bash
# Install dependencies
pip install -r requirements-test.txt
```

### Against Local Dev Server

```bash
cd ui
npm install
npm run dev

# In another terminal
cd tests/e2e
SILVERMOAT_URL=http://localhost:5173 pytest tests/ -v
```

### Against Deployed Stack

```bash
cd tests/e2e

# Using environment variables
export SILVERMOAT_URL="https://your-cloudfront-url.com"
export SILVERMOAT_API_URL="https://api-gateway-url.com/demo"
pytest tests/ -v

# Or inline
SILVERMOAT_URL=https://your-url.com pytest tests/ -v

# Or using CloudFormation stack name
STACK_NAME=silvermoat pytest tests/ -v
TEST_STACK_NAME=silvermoat-test-pr-123 pytest tests/ -v
```

### Test Markers

```bash
# Smoke tests only (fast)
pytest tests/ -v -m smoke

# Quote workflow tests
pytest tests/ -v -m quote

# Responsive design tests
pytest tests/ -v -m responsive

# Exclude slow tests
pytest tests/ -v -m "not slow"
```

### Headless Mode

```bash
# Headless Chrome (no GUI)
HEADLESS=1 pytest tests/ -v

# CI mode (automatically headless)
CI=1 pytest tests/ -v
```

### HTML Reports

```bash
pytest tests/ -v --html=report.html --self-contained-html
```

## Test Fixtures

### `driver` (function scope)
Standard desktop WebDriver (1920x1080)

```python
def test_example(driver):
    driver.get("https://example.com")
    assert driver.title == "Example"
```

### `mobile_driver` (function scope)
Mobile viewport (375x667, iPhone SE)

```python
@pytest.mark.responsive
def test_mobile(mobile_driver):
    mobile_driver.get("https://example.com")
    # Test mobile layout
```

### `tablet_driver` (function scope)
Tablet viewport (768x1024, iPad)

```python
@pytest.mark.responsive
def test_tablet(tablet_driver):
    tablet_driver.get("https://example.com")
    # Test tablet layout
```

### `base_url` (session scope)
Application base URL (auto-detected or configurable)

### `api_base_url` (session scope)
API base URL (auto-detected or configurable)

## Configuration Priority

### Base URL Resolution
1. `SILVERMOAT_URL` environment variable
2. CloudFormation stack output (`TEST_STACK_NAME` or `STACK_NAME`)
3. Default: `http://localhost:5173`

### API URL Resolution
1. `SILVERMOAT_API_URL` environment variable
2. CloudFormation stack output (`TEST_STACK_NAME` or `STACK_NAME`)
3. None (tests skip API validation)

## Page Object Model (POM)

Tests use the Page Object Model pattern for maintainability:

```
tests/e2e/
├── pages/
│   ├── base_page.py       # Base class with common methods
│   ├── home_page.py       # Home page
│   ├── quote_page.py      # Quote form/list
│   ├── policy_page.py     # Policy management
│   ├── claim_page.py      # Claims processing
│   └── payment_page.py    # Payment history
└── tests/
    ├── test_smoke.py      # Smoke tests
    ├── test_quotes.py     # Quote workflow
    ├── test_policies.py   # Policy management
    └── test_claims.py     # Claims processing
```

## CI/CD Integration

E2E tests run automatically in GitHub Actions (`.github/workflows/infra-tests.yml`):

1. Test stack deployed with seeded data
2. Chrome + ChromeDriver installed
3. Selenium dependencies installed
4. Tests run in headless mode
5. HTML reports uploaded as artifacts
6. Test results posted to PR

## Troubleshooting

### ChromeDriver Issues
```bash
# Update ChromeDriver
pip install --upgrade webdriver-manager

# Check Chrome version
google-chrome --version
```

### Element Not Found
```python
# Increase implicit wait
driver.implicitly_wait(20)

# Or use explicit wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "element-id"))
)
```

### Headless Mode Issues
```bash
# Run in GUI mode for debugging
HEADLESS=0 pytest tests/test_smoke.py::test_app_loads -v
```

### Screenshots on Failure
```python
def test_example(driver):
    try:
        driver.get("https://example.com")
        # Test logic
    except Exception as e:
        driver.save_screenshot("failure.png")
        raise
```

## Best Practices

1. **Use Page Objects**: Keep test logic in tests, page interactions in page objects
2. **Explicit Waits**: Use `WebDriverWait` for dynamic content
3. **Unique Selectors**: Prefer IDs and data attributes over XPath
4. **Independent Tests**: Each test should be runnable in isolation
5. **Cleanup**: Remove test data after tests (use fixtures)
6. **Screenshots**: Capture screenshots on failures for debugging

## Future Enhancements

- [ ] Visual regression testing (Percy, Applitools)
- [ ] Accessibility testing (axe-core)
- [ ] Performance testing (Lighthouse)
- [ ] Cross-browser testing (Firefox, Safari)
- [ ] Parallel execution (pytest-xdist)
