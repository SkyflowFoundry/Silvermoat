# Infrastructure Tests

Comprehensive infrastructure validation and API integration tests for Silvermoat.

## Overview

This test suite validates:
- **CloudFormation stack** deployment and configuration
- **AWS resources** (DynamoDB, S3, Lambda, API Gateway, CloudFront)
- **API endpoints** and integration
- **Test data** generation and cleanup

## Test Categories

### Infrastructure Tests (`@pytest.mark.infra`)
- CloudFormation stack existence and status
- Stack outputs and resources
- DynamoDB tables (schema, billing, seeded data)
- S3 buckets (website config, policies, content)
- Lambda functions (configuration, environment variables)
- CloudFront distributions (origins, configuration)

### API Tests (`@pytest.mark.api`)
- API root endpoint
- CORS headers
- Create/retrieve quotes, policies, claims, payments
- Error handling
- Response format validation

## Running Tests

### Prerequisites

```bash
# Install dependencies
pip install -r requirements-test.txt
```

### Against Existing Stack

```bash
cd tests/infra

# Use environment variable
export TEST_STACK_NAME=silvermoat
pytest tests/ -v

# Or inline
TEST_STACK_NAME=my-stack pytest tests/ -v
```

### Test Markers

```bash
# Infrastructure tests only
pytest tests/ -v -m infra

# API tests only
pytest tests/ -v -m api

# Exclude slow tests
pytest tests/ -v -m "not slow"
```

### With HTML Reports

```bash
pytest tests/ -v --html=report.html --self-contained-html
```

## Test Data Utilities

### Generating Test Data

```python
from utils.test_data import create_test_quote, create_test_policy

# Create test quote
quote = create_test_quote(customer_name="John Doe", coverage_type="auto")

# Create test policy
policy = create_test_policy(customer_name="Jane Smith", status="active")
```

### Cleanup Test Data

```python
from utils.cleanup import delete_test_items

# Delete specific test items
delete_test_items(
    table_name="silvermoat-quotes",
    test_ids=["quote-abc123", "quote-def456"]
)
```

## CI/CD Integration

The GitHub Actions workflow (`.github/workflows/infra-tests.yml`) automates:

1. **Deploy test stack** with unique name (`silvermoat-test-pr-123`)
2. **Run infrastructure tests** (validate resources)
3. **Run API integration tests** (validate endpoints)
4. **Run smoke tests** (shell script validation)
5. **Run E2E tests** (Selenium, if available)
6. **Generate reports** (HTML artifacts)
7. **Cleanup test stack** (always runs, even on failure)

### Workflow Triggers

- **Pull requests** to `main` (when infra/UI/tests change)
- **Manual dispatch** (workflow_dispatch with custom stack name)

### Required Secrets

- `AWS_ROLE_ARN` - IAM role for OIDC authentication

### Workflow Behavior

- Test stack name: `silvermoat-test-pr-{PR_NUMBER}` or `silvermoat-test-run-{RUN_ID}`
- Stack parameters: `UiSeedingMode=seeded` (basic HTML for quick tests)
- Cleanup: **Always** deletes test stack (uses `if: always()`)
- Reports: Posted as PR comment + uploaded as artifacts

## Stack Parameters for Testing

When deploying test stacks:

```bash
STACK_NAME=silvermoat-test-pr-123 \
APP_NAME=silvermoat \
STAGE_NAME=test \
API_DEPLOYMENT_TOKEN=test-v1 \
UI_SEEDING_MODE=seeded \
./scripts/deploy-stack.sh
```

**Note:** Use `UiSeedingMode=seeded` for fast basic HTML deployment. Skip CloudFront custom domain (tests use S3 website URL).

## Test Data Format

Test data utilities maintain parity with CloudFormation seed data:

### Quote Format
```python
{
    "id": "quote-abc123",
    "customer_name": "John Doe",
    "customer_email": "john.doe@example.com",
    "coverage_type": "auto",
    "coverage_amount": 100000,
    "annual_premium_cents": 50000,
    "created_at": "2025-01-01T00:00:00",
    "status": "pending"
}
```

### Policy Format
```python
{
    "id": "pol-abc123",
    "policy_number": "POL-12345678",
    "customer_name": "Jane Smith",
    "coverage_type": "home",
    "status": "active",
    "annual_premium_cents": 125000,
    "effective_date": "2024-12-01T00:00:00",
    "expiration_date": "2025-12-01T00:00:00"
}
```

### Claim Format
```python
{
    "id": "claim-abc123",
    "claim_number": "CLM-12345678",
    "policy_id": "pol-abc123",
    "claim_type": "auto",
    "amount_cents": 15000,
    "status": "submitted",
    "description": "Accident claim",
    "documents": []
}
```

## Troubleshooting

### Stack Not Found
```bash
# Verify stack exists
aws cloudformation describe-stacks --stack-name silvermoat

# Check stack outputs
./scripts/get-outputs.sh
```

### Test Failures
```bash
# Run with verbose output
pytest tests/ -vv --tb=long

# Run specific test
pytest tests/test_cloudformation.py::test_stack_exists -vv
```

### Cleanup Issues
```bash
# Manually delete test stack
STACK_NAME=silvermoat-test-pr-123 ./scripts/delete-stack.sh

# Or force delete via AWS CLI
aws cloudformation delete-stack --stack-name silvermoat-test-pr-123
```

### CloudWatch Logs
Check Lambda logs for Custom Resource errors:
```bash
aws logs tail /aws/lambda/silvermoat-test-pr-123-SeederFunction-* --follow
```

## Architecture

```
GitHub Actions Workflow
├── Deploy Test Stack
│   └── CloudFormation (UiSeedingMode=seeded)
├── Infrastructure Tests (pytest)
│   ├── CloudFormation validation
│   ├── Resource validation (DynamoDB, S3, Lambda)
│   └── API integration tests
├── Smoke Tests (bash)
│   └── scripts/smoke-test.sh
├── E2E Tests (Selenium, optional)
│   └── tests/e2e/
└── Cleanup (always)
    └── CloudFormation delete-stack
```

## Future Enhancements

- [ ] Performance tests (load testing API endpoints)
- [ ] Security tests (IAM policy validation)
- [ ] Cost estimation (resource usage tracking)
- [ ] Multi-region testing
- [ ] Chaos engineering (fault injection)
