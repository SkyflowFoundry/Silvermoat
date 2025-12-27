# Silvermoat Test Suite

Comprehensive testing infrastructure for Silvermoat MVP.

## Test Categories

### 1. Infrastructure Tests (`tests/infra/`)
Validates AWS infrastructure and CloudFormation deployment.

**What's tested:**
- CloudFormation stack deployment and configuration
- AWS resources (DynamoDB, S3, Lambda, API Gateway, CloudFront)
- API endpoints and integration
- Resource configuration and permissions

**Run tests:**
```bash
cd tests/infra
pytest tests/ -v
```

**[Full documentation →](infra/README.md)**

---

### 2. E2E Tests (`tests/e2e/`)
End-to-end UI testing using Selenium WebDriver.

**What's tested:**
- Application loads and navigation
- Quote workflow (create, submit, view, convert)
- Policy management (view, search, filter)
- Claims processing (file, upload docs, status updates)
- Payment processing
- Chat assistant
- Responsive design (mobile, tablet, desktop)

**Run tests:**
```bash
cd tests/e2e
pytest tests/ -v
```

**[Full documentation →](e2e/README.md)**

---

### 3. Smoke Tests (`scripts/smoke-test.sh`)
Quick shell-based validation of deployed stack.

**What's tested:**
- API root endpoint responds
- Create quote via API
- Retrieve quote via API
- Basic error handling

**Run tests:**
```bash
STACK_NAME=silvermoat ./scripts/smoke-test.sh
```

---

## Quick Start

### Install Dependencies

```bash
pip install -r requirements-test.txt
```

### Run All Tests

```bash
# Infrastructure tests
cd tests/infra && pytest tests/ -v

# E2E tests (requires UI running)
cd tests/e2e && pytest tests/ -v

# Smoke tests
./scripts/smoke-test.sh
```

### Run Tests Against Specific Stack

```bash
# Infrastructure + API tests
TEST_STACK_NAME=silvermoat pytest tests/infra/ -v

# E2E tests
STACK_NAME=silvermoat pytest tests/e2e/ -v
```

---

## CI/CD Integration

### GitHub Actions Workflow

The project includes automated testing via GitHub Actions (`.github/workflows/infra-tests.yml`).

**Workflow:**
1. Deploy ephemeral test stack (`silvermoat-test-pr-123`)
2. Run infrastructure validation tests
3. Run API integration tests
4. Run smoke tests
5. Run E2E tests (Selenium)
6. Generate HTML reports
7. Post results to PR
8. **Always cleanup test stack** (even on failure)

**Triggers:**
- Pull requests to `main` (when infra/UI/tests change)
- Manual workflow dispatch

**Required Secrets:**
- `AWS_ROLE_ARN` - IAM role for OIDC authentication

---

## Test Stack Lifecycle

### Deploy Test Stack

```bash
# Generate unique stack name
STACK_NAME="silvermoat-test-$(date +%s)"

# Deploy with test parameters
STACK_NAME=$STACK_NAME \
APP_NAME=silvermoat \
STAGE_NAME=test \
UI_SEEDING_MODE=seeded \
./scripts/deploy-stack.sh
```

### Run Tests

```bash
# Infrastructure tests
TEST_STACK_NAME=$STACK_NAME pytest tests/infra/ -v

# E2E tests
TEST_STACK_NAME=$STACK_NAME pytest tests/e2e/ -v
```

### Cleanup Test Stack

```bash
STACK_NAME=$STACK_NAME ./scripts/delete-stack.sh
```

---

## Test Data

### Seeded Data (CloudFormation)
CloudFormation Custom Resource seeds initial demo data:
- 1 quote (Alice Johnson, auto insurance)
- 1 policy (Bob Smith, home insurance)
- 1 claim (CLM-12345678, auto)
- Sample documents in S3

### Test-Specific Data
Use test data utilities (`tests/infra/utils/test_data.py`) to generate additional test data:

```python
from tests.infra.utils.test_data import create_test_quote, create_test_policy

# Generate test quote
quote = create_test_quote(customer_name="Test User", coverage_type="auto")

# Generate test policy
policy = create_test_policy(customer_name="Test User", status="active")
```

**Cleanup:** Test data utilities maintain parity with seed data format.

---

## Test Markers

### Infrastructure Tests
- `@pytest.mark.infra` - Infrastructure validation
- `@pytest.mark.api` - API integration tests
- `@pytest.mark.slow` - Slow-running tests (e.g., drift detection)

### E2E Tests
- `@pytest.mark.smoke` - Quick smoke tests
- `@pytest.mark.quote` - Quote workflow tests
- `@pytest.mark.policy` - Policy management tests
- `@pytest.mark.claim` - Claims processing tests
- `@pytest.mark.payment` - Payment tests
- `@pytest.mark.chat` - Chat assistant tests
- `@pytest.mark.responsive` - Responsive design tests

**Usage:**
```bash
# Run only smoke tests
pytest -m smoke -v

# Exclude slow tests
pytest -m "not slow" -v

# Multiple markers
pytest -m "smoke or api" -v
```

---

## Configuration

### Environment Variables

**Infrastructure Tests:**
- `TEST_STACK_NAME` or `STACK_NAME` - CloudFormation stack name
- `AWS_REGION` - AWS region (default: us-east-1)

**E2E Tests:**
- `SILVERMOAT_URL` - Application URL (or auto-detect from stack)
- `SILVERMOAT_API_URL` - API URL (or auto-detect from stack)
- `TEST_STACK_NAME` or `STACK_NAME` - CloudFormation stack name
- `HEADLESS` - Run Chrome in headless mode (1=true)
- `CI` - CI environment (automatically enables headless)

### Auto-Detection

Tests automatically fetch URLs from CloudFormation stack outputs:
1. Check environment variables (`SILVERMOAT_URL`, `SILVERMOAT_API_URL`)
2. Query CloudFormation stack (`TEST_STACK_NAME` or `STACK_NAME`)
3. Fallback to defaults (localhost for E2E)

---

## Reporting

### HTML Reports

```bash
# Infrastructure tests
cd tests/infra
pytest tests/ -v --html=report-infra.html --self-contained-html

# E2E tests
cd tests/e2e
pytest tests/ -v --html=report-e2e.html --self-contained-html
```

### CI/CD Reports

GitHub Actions workflow:
- Generates HTML reports for all test suites
- Uploads reports as artifacts (7-day retention)
- Posts test results as PR comments

---

## Troubleshooting

### Stack Not Found
```bash
# Verify stack exists
aws cloudformation describe-stacks --stack-name silvermoat

# Get stack outputs
./scripts/get-outputs.sh
```

### ChromeDriver Issues
```bash
# Update ChromeDriver
pip install --upgrade webdriver-manager

# Check Chrome version
google-chrome --version
```

### Test Failures
```bash
# Verbose output
pytest tests/ -vv --tb=long

# Run specific test
pytest tests/infra/tests/test_cloudformation.py::test_stack_exists -vv
```

### Cleanup Issues
```bash
# Force delete test stack
aws cloudformation delete-stack --stack-name silvermoat-test-pr-123

# Check CloudWatch logs
aws logs tail /aws/lambda/silvermoat-test-pr-123-SeederFunction-* --follow
```

---

## Architecture

```
tests/
├── infra/                    # Infrastructure tests
│   ├── tests/
│   │   ├── test_cloudformation.py
│   │   ├── test_resources.py
│   │   └── test_api_integration.py
│   ├── utils/
│   │   ├── test_data.py      # Test data generation
│   │   └── cleanup.py        # Cleanup utilities
│   ├── conftest.py           # Pytest fixtures
│   └── README.md
│
├── e2e/                      # E2E tests (Selenium)
│   ├── tests/
│   │   ├── test_smoke.py
│   │   ├── test_quotes.py
│   │   └── test_policies.py
│   ├── pages/                # Page Object Model
│   │   ├── base_page.py
│   │   └── home_page.py
│   ├── conftest.py           # Pytest fixtures
│   └── README.md
│
└── README.md                 # This file
```

---

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Cleanup**: Always cleanup test resources
3. **Explicit Waits**: Use `WebDriverWait` for dynamic content
4. **Test Data**: Use test data utilities for consistency
5. **Markers**: Tag tests appropriately for selective execution
6. **Reports**: Generate HTML reports for debugging
7. **CI/CD**: Run tests on every PR

---

## Future Enhancements

- [ ] Performance tests (load testing API endpoints)
- [ ] Security tests (IAM policy validation, OWASP)
- [ ] Visual regression testing (Percy, Applitools)
- [ ] Accessibility testing (axe-core)
- [ ] Cross-browser testing (Firefox, Safari)
- [ ] Parallel execution (pytest-xdist)
- [ ] Code coverage tracking
- [ ] Mutation testing
