# Silvermoat Test Suite

End-to-end testing framework for Silvermoat multi-vertical platform.

## Testing Strategy

**E2E Tests Only** - We validate user-facing functionality through browser automation, not unit tests or API contracts.

## Test Organization

### E2E Browser Tests (`tests/e2e/`)

**Purpose:** Validate complete user workflows across both verticals (insurance + retail)

**What it tests:**
- Application loads and renders correctly
- Navigation and routing works
- User can interact with entities (quotes, policies, products, orders)
- Data persists across pages
- API integration works end-to-end

**Coverage:**
- **Insurance:** Landing page, quotes, policies, claims, customers, chatbot
- **Retail:** Landing page, dashboard, product/order management

**Run tests:**
```bash
cd tests/e2e

# Insurance vertical
INSURANCE_URL=https://insurance.example.com \
INSURANCE_API_URL=https://api-insurance.example.com \
pytest -v -m insurance

# Retail vertical
RETAIL_URL=https://retail.example.com \
RETAIL_API_URL=https://api-retail.example.com \
pytest -v -m retail

# All tests
INSURANCE_URL=... RETAIL_URL=... pytest -v

# Headless mode (for CI)
HEADLESS=1 pytest -v
```

---

## Installation

```bash
# Install test dependencies
pip install -r requirements-test.txt
```

**Dependencies:**
- `pytest` - Test framework
- `selenium` - Browser automation
- `webdriver-manager` - Automatic ChromeDriver management
- `requests` - HTTP client for API interactions in E2E tests
- `boto3` - AWS SDK (for fetching CloudFormation outputs)

---

## Running Tests Locally

### Against Deployed Stack
```bash
# Tests auto-fetch URLs from CloudFormation
export STACK_NAME=silvermoat-test-pr-123

cd tests/e2e
pytest -v -m insurance  # Insurance tests
pytest -v -m retail     # Retail tests
```

### Against Specific URLs
```bash
export INSURANCE_URL=https://insurance.silvermoat.net
export INSURANCE_API_URL=https://api.silvermoat.net/insurance
export RETAIL_URL=https://retail.silvermoat.net
export RETAIL_API_URL=https://api.silvermoat.net/retail

cd tests/e2e
pytest -v
```

### With Visual Debugging
```bash
# Run in non-headless mode to watch browser
unset HEADLESS
cd tests/e2e
pytest -v -m insurance
```

---

## Test Markers

```bash
# By vertical
pytest -m insurance   # Insurance tests only
pytest -m retail      # Retail tests only

# By speed
pytest -m "not slow"  # Fast tests only
pytest -m slow        # Integration-heavy tests

# By feature
pytest -m quotes      # Quote workflows
pytest -m policies    # Policy management
pytest -m claims      # Claims processing
pytest -m chat        # Chatbot interactions
```

---

## CI/CD Integration

**Workflow:** `.github/workflows/deploy-test.yml`

**Pipeline per vertical:**
1. Deploy infrastructure (CDK stack)
2. Deploy UI (build + S3 sync)
3. Run E2E tests (Selenium + Chrome)
4. Seed demo data
5. Post PR summary

**Stack naming:**
- PR-based: `silvermoat-test-pr-{PR_NUMBER}-{vertical}`
- Example: `silvermoat-test-pr-151-insurance`, `silvermoat-test-pr-151-retail`

**Test environment:**
- Headless Chrome in GitHub Actions
- Auto-fetches URLs from CloudFormation outputs
- Parallel execution: Insurance and retail pipelines run independently

---

## Test Structure

```
tests/
├── e2e/
│   ├── conftest.py                    # Pytest fixtures (driver, URLs)
│   ├── pytest.ini                     # Test markers configuration
│   └── tests/
│       ├── test_insurance_workflows.py  # Insurance E2E tests
│       └── test_retail_workflows.py     # Retail E2E tests
└── README.md
```

---

## Design Principles

### E2E Tests Validate Real User Flows

**Good:**
- ✅ User can navigate to quotes page
- ✅ Creating a quote via API makes it appear in UI
- ✅ Landing page loads within 5 seconds
- ✅ Chatbot responds to messages

**Bad:**
- ❌ Testing React component in isolation
- ❌ Mocking API responses
- ❌ Validating DynamoDB table structure
- ❌ Checking Lambda environment variables

### Infrastructure Agnostic

E2E tests don't care about backend implementation:
- Switch from DynamoDB → Postgres? **Tests still pass**
- Move from Lambda → ECS? **Tests still pass**
- Change storage from S3 → R2? **Tests still pass**

Tests validate **what users see and experience**, not **how it's implemented**.

---

## Troubleshooting

### ChromeDriver not found
```bash
# Install Chrome
# ChromeDriver auto-installs via webdriver-manager

# Verify
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

### Tests timeout waiting for page
- Increase timeout in `conftest.py:wait_for_app_ready()`
- Check if loading screen is properly removed (see `ui-*/index.html`)
- Run without headless to debug: `unset HEADLESS`

### Stack outputs not found
```bash
# Verify stack exists
aws cloudformation describe-stacks --stack-name silvermoat-test-pr-123-insurance

# Check outputs
aws cloudformation describe-stacks \
  --stack-name silvermoat-test-pr-123-insurance \
  --query 'Stacks[0].Outputs'
```

### Tests fail with "RETAIL_URL not configured"
Retail tests skip if `RETAIL_URL` not provided (by design).
Set environment variable or deploy retail stack first.

---

## Contributing

### Adding New Tests

1. **Create test file:**
   - Insurance: Add to `test_insurance_workflows.py`
   - Retail: Add to `test_retail_workflows.py`

2. **Mark tests appropriately:**
   ```python
   @pytest.mark.e2e
   @pytest.mark.insurance  # or @pytest.mark.retail
   def test_new_workflow(driver, insurance_base_url):
       ...
   ```

3. **Use fixtures from conftest.py:**
   - `driver` - Selenium WebDriver
   - `insurance_base_url` / `retail_base_url` - UI URLs
   - `insurance_api_url` / `retail_api_url` - API URLs
   - `wait_for_app_ready()` - Helper to wait for React app

4. **Follow patterns:**
   - Navigate to page
   - Wait for app ready
   - Interact with elements
   - Assert expected behavior
   - Cleanup (delete test data)

### Anti-Patterns to Avoid

- ❌ Don't mock API responses (use real APIs)
- ❌ Don't test React components in isolation (test full flows)
- ❌ Don't validate AWS resource config (test user experience)
- ❌ Don't use boto3 to check DynamoDB/S3 (use browser + HTTP)
- ✅ DO test complete user workflows
- ✅ DO use real API calls in E2E tests
- ✅ DO verify data persists across page navigations
- ✅ DO test error handling visible to users

---

## Why E2E Only?

**Benefits:**
- Tests what users actually experience
- Faster to write (no mocking, no setup)
- More reliable (no brittle unit tests)
- Infrastructure agnostic (backend can change)
- Catches integration issues early

**Trade-offs:**
- Slower than unit tests (but we optimize with parallelization)
- Requires deployed environment (handled by CI/CD)
- More complex debugging (but we have visual mode)

**Decision:** E2E tests provide the most value for the least maintenance cost in a multi-vertical cloud application.
