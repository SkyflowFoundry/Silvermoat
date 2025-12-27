# Silvermoat Test Suite

Infrastructure-agnostic test framework for Silvermoat Insurance MVP.

## Architecture Overview

The test suite is organized into three layers:

### 1. API Contract Tests (`tests/api/`)
**Purpose:** Validate API behavior regardless of backend implementation

**What it tests:**
- API endpoint availability and responses
- Request/response contracts (schema, status codes)
- Business logic (quote creation, policy management, claims processing)
- CORS headers and error handling

**What it does NOT test:**
- DynamoDB table structure or data format
- S3 bucket configuration
- Lambda function implementation
- AWS resource details

**Run tests:**
```bash
cd tests/api

# Against deployed stack (auto-fetch URLs)
STACK_NAME=silvermoat pytest -v

# Against specific API URL
SILVERMOAT_API_URL=https://api.example.com pytest -v

# Run specific categories
pytest -m quotes  # Quote tests only
pytest -m "api and not slow"  # Fast API tests only
```

---

### 2. E2E Functional Tests (`tests/e2e/`)
**Purpose:** Validate user workflows work end-to-end in a browser

**What it tests:**
- Application loads successfully
- Navigation works
- Responsive design (mobile, tablet, desktop)
- User workflows (quotes, policies, claims, payments)

**What it does NOT test:**
- Specific backend technology (DynamoDB vs Postgres)
- AWS resource configuration
- Infrastructure implementation details

**Run tests:**
```bash
cd tests/e2e

# Against deployed stack
STACK_NAME=silvermoat pytest -v

# Against local dev server
BASE_URL=http://localhost:5173 pytest -v

# Headless mode (for CI/CD)
HEADLESS=1 STACK_NAME=silvermoat pytest -v

# Run specific categories
pytest -m smoke  # Smoke tests only
pytest -m responsive  # Responsive design tests
```

---

### 3. Deployment Smoke Tests (`tests/smoke/`)
**Purpose:** Verify CloudFormation deployment succeeded

**What it tests:**
- Stack status is CREATE_COMPLETE or UPDATE_COMPLETE
- Required outputs exist (ApiBaseUrl, WebUrl)
- URLs are reachable (basic connectivity)

**What it does NOT test:**
- DynamoDB tables, S3 buckets, Lambda functions
- IAM roles and policies
- CloudFormation resource details

**Run tests:**
```bash
cd tests/smoke

# Against deployed stack
STACK_NAME=silvermoat pytest -v
```

---

## GitHub Actions Integration

The test suite includes a GitHub Actions workflow (`e2e-tests.yml`) that:

1. **Deploys ephemeral test stack** (e.g., `silvermoat-test-pr-123`)
2. **Runs all tests** sequentially:
   - Deployment smoke tests
   - API contract tests
   - E2E browser tests
3. **Always cleans up** test stack (even on failure)

**Triggers:**
- Pull requests to `main` (when infra/UI/tests change)
- Manual workflow dispatch

**Required secret:**
- `AWS_ROLE_ARN` - IAM role for CloudFormation access

---

## Installation

```bash
# Install all test dependencies
pip install -r requirements-test.txt
```

**Dependencies:**
- `pytest` - Test framework
- `requests` - HTTP client for API tests
- `selenium` - Browser automation for E2E tests
- `webdriver-manager` - Automatic ChromeDriver management
- `boto3` - AWS SDK (only for fetching CloudFormation outputs)

---

## Running Tests Locally

### Option 1: Against Deployed Stack
```bash
# Export stack name (tests auto-fetch URLs from CloudFormation)
export STACK_NAME=silvermoat

# Run all tests
pytest -v

# Run specific layers
cd tests/api && pytest -v
cd tests/e2e && pytest -v
cd tests/smoke && pytest -v
```

### Option 2: Against Local Dev Server
```bash
# Start UI dev server
cd ui && npm run dev

# Run tests (in separate terminal)
export BASE_URL=http://localhost:5173
export API_BASE_URL=http://localhost:3000

cd tests/e2e && pytest -v
cd tests/api && pytest -v
```

### Option 3: Custom URLs
```bash
export SILVERMOAT_URL=https://silvermoat.net
export SILVERMOAT_API_URL=https://api.silvermoat.net

pytest -v
```

---

## Test Markers

Use pytest markers to run specific test categories:

```bash
# Smoke tests only (fast)
pytest -m smoke

# API contract tests
pytest -m api

# E2E tests
pytest -m e2e

# Specific domains
pytest -m quotes
pytest -m policies
pytest -m claims
pytest -m payments

# Responsive design tests
pytest -m responsive

# Exclude slow tests
pytest -m "not slow"
```

---

## Design Principles

### Infrastructure Agnostic
Tests validate **what the system does**, not **how it does it**:

**Good:**
- ✅ `POST /quote` returns 201 with quote ID
- ✅ Created quote can be retrieved via `GET /quote/{id}`
- ✅ Quote form accepts input and submits successfully

**Bad:**
- ❌ Quote is stored in DynamoDB with partition key `id`
- ❌ S3 bucket contains uploaded document
- ❌ Lambda function has correct environment variables

### Why This Matters

If you switch from DynamoDB to Postgres, or S3 to CloudFlare R2, or Lambda to ECS:
- **Tests should NOT break** - they validate behavior, not implementation
- **No test rewrites** needed - API contracts and user workflows remain the same

---

## Troubleshooting

### Tests fail with "STACK_NAME required"
Export the stack name environment variable:
```bash
export STACK_NAME=silvermoat
```

### ChromeDriver not found
Install Chrome and ChromeDriver:
```bash
# Ubuntu/Debian
sudo apt-get install -y chromium-browser chromium-chromedriver

# Or use webdriver-manager (automatic)
pip install webdriver-manager
```

### API tests fail with connection refused
Ensure the API is running or the stack is deployed:
```bash
# Check stack outputs
./scripts/get-outputs.sh

# Or manually check API
curl https://your-api-url.amazonaws.com/
```

### E2E tests fail with "element not found"
- Ensure UI is deployed and accessible
- Try increasing timeouts in `tests/e2e/pages/base_page.py`
- Run in non-headless mode to debug: `unset HEADLESS`

---

## CI/CD Workflow

**File:** `e2e-tests.yml` (must be moved to `.github/workflows/`)

**Workflow steps:**
1. Deploy test stack (`silvermoat-test-pr-{PR_NUMBER}`)
2. Wait for CloudFormation completion
3. Fetch stack outputs (URLs)
4. Run deployment smoke tests
5. Run API contract tests
6. Run E2E smoke tests
7. **Always cleanup:** Delete test stack
8. Post results to PR comment

**Stack naming:**
- PR-based: `silvermoat-test-pr-123`
- Manual run: `silvermoat-test-{RUN_ID}`

**Cleanup guarantee:**
- Uses `if: always()` to ensure cleanup runs even on test failure
- Deletes ALL resources created by CloudFormation
- No orphaned resources or test data

---

## Contributing

When adding new tests:

1. **Follow the architecture:** Tests should be infrastructure-agnostic
2. **Use appropriate layer:**
   - API contracts → `tests/api/`
   - User workflows → `tests/e2e/`
   - Deployment checks → `tests/smoke/` (rarely needed)
3. **Add markers:** Tag tests with appropriate pytest markers
4. **Update documentation:** Add test descriptions to this README

**Anti-patterns to avoid:**
- ❌ Don't use boto3 to validate DynamoDB/S3/Lambda (in API/E2E tests)
- ❌ Don't check AWS resource configuration
- ❌ Don't couple tests to specific backend technology
- ✅ DO validate API contracts and user-facing behavior
- ✅ DO use HTTP requests to test APIs
- ✅ DO use Selenium to test browser workflows
