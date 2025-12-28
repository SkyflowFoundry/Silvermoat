# Lambda Functions

This directory contains the extracted Lambda function code for Silvermoat MVP.

## Structure

```
lambda/
├── mvp_service/
│   └── handler.py       # Main MVP service Lambda (handles all API routes)
└── seeder/
    └── handler.py       # Custom Resource Lambda (seeding + cleanup)
```

## Current State (Phase 1)

The Lambda code has been **extracted from the CloudFormation template** into separate Python files for better maintainability, testing, and development experience.

**However**, the CloudFormation template (`infra/silvermoat-mvp-s3-website.yaml`) still contains **inline Lambda code** to preserve the "one-shot deployable" philosophy.

### Why Keep Inline Code?

- **One-shot deployment**: The stack can be deployed with a single CloudFormation template without pre-requisites
- **No external dependencies**: No need to upload Lambda code to S3 before deployment
- **Backwards compatibility**: Existing deployment workflows continue to work

### Benefits of Extracted Code

Even though the CF template still has inline code, extracting it provides:

1. **Better development experience**:
   - IDE support (autocomplete, type checking, linting)
   - Proper Python modules instead of YAML strings
   - Easy local testing and debugging

2. **Version control**:
   - Clear diffs when Lambda code changes
   - Easier code reviews
   - Can track Lambda changes separately from infrastructure

3. **Testing**:
   - Can add unit tests for Lambda functions
   - Can run linters (pylint, mypy, black) on Lambda code
   - Can import and test functions locally

4. **Transition path**:
   - Foundation for Phase 2: moving to S3-packaged Lambda code
   - Can gradually migrate to AWS SAM or other packaging tools
   - Keeps options open without breaking current workflows

## Keeping Code in Sync

**IMPORTANT**: When modifying Lambda code, you must update BOTH locations:

1. Edit the Python file in `lambda/*/handler.py`
2. Copy the updated code to the inline `ZipFile` section in `infra/silvermoat-mvp-s3-website.yaml`

This is a temporary measure during Phase 1. In Phase 2, we will eliminate this duplication by moving to S3-packaged Lambda code.

### Helper Script

To make syncing easier, you can use:

```bash
# TODO Phase 2: Create sync script
./scripts/sync-lambda-code.sh
```

## Phase 2 Migration (Future)

Phase 2 will migrate to S3-packaged Lambda code:

1. **Add Lambda packaging to deployment**:
   - `./scripts/package-lambda.sh` uploads Lambda ZIPs to S3
   - CloudFormation references S3 location instead of inline code
   - `./scripts/deploy-stack.sh` automatically packages and deploys

2. **Update CloudFormation template**:
   - Add `LambdaCodeBucket` resource
   - Change `MvpServiceFunction.Code` from `ZipFile` to `S3Bucket/S3Key`
   - Change `SeederFunction.Code` from `ZipFile` to `S3Bucket/S3Key`

3. **Benefits of S3 packaging**:
   - No more code duplication (single source of truth)
   - Can add dependencies via `requirements.txt`
   - Faster deployments (only upload code when changed)
   - Better for CI/CD pipelines

## Development Workflow

### Local Development

```bash
# Edit Lambda code
vim lambda/mvp_service/handler.py

# Run linters
cd lambda/mvp_service
pylint handler.py
mypy handler.py

# Run unit tests (TODO: add tests)
pytest tests/

# Sync to CloudFormation template (manual for now)
# Copy the code to infra/silvermoat-mvp-s3-website.yaml
```

### Testing Changes

```bash
# Deploy test stack with updated code
STACK_NAME=silvermoat-test-lambda ./scripts/deploy-stack.sh

# Run smoke tests
STACK_NAME=silvermoat-test-lambda ./scripts/smoke-test.sh

# Delete test stack
STACK_NAME=silvermoat-test-lambda ./scripts/delete-stack.sh --yes
```

## Lambda Functions

### mvp_service/handler.py

**Purpose**: Single Lambda function handling all API Gateway routes

**Handler**: `handler.handler`

**Routes**:
- `GET /` - API root (lists available endpoints)
- `POST /chat` - Chatbot endpoint (Bedrock integration)
- `GET /{domain}` - List all entities (quote/policy/claim/payment/case)
- `POST /{domain}` - Create entity
- `GET /{domain}/{id}` - Get entity by ID
- `DELETE /{domain}/{id}` - Delete entity
- `DELETE /{domain}` - Bulk delete all entities in domain
- `POST /claim/{id}/status` - Update claim status
- `POST /claim/{id}/doc` - Attach document to claim

**Environment Variables**:
- `QUOTES_TABLE`, `POLICIES_TABLE`, `CLAIMS_TABLE`, `PAYMENTS_TABLE`, `CASES_TABLE`
- `DOCS_BUCKET` - S3 bucket for documents
- `SNS_TOPIC_ARN` - SNS topic for notifications
- `BEDROCK_MODEL_ID`, `BEDROCK_REGION` - Bedrock configuration

**Dependencies**: boto3, Decimal (stdlib)

### seeder/handler.py

**Purpose**: CloudFormation Custom Resource for seeding/cleanup

**Handler**: `handler.handler`

**Modes**:
- `seed` - Seeds UI (if `UiSeedingMode=seeded`) and DynamoDB demo data on CREATE/UPDATE
- `cleanup` - Empties S3 buckets and wipes DynamoDB tables on DELETE

**Environment Variables**:
- `UI_BUCKET`, `DOCS_BUCKET` - S3 buckets to manage
- `QUOTES_TABLE`, `POLICIES_TABLE`, `CLAIMS_TABLE`, `PAYMENTS_TABLE`, `CASES_TABLE` - DynamoDB tables
- `API_BASE`, `WEB_BASE` - URLs for seeded UI

**Dependencies**: boto3, urllib (stdlib)

## Adding Dependencies (Phase 2)

Currently, Lambda functions use only boto3 (available in Lambda runtime) and standard library modules.

To add external dependencies in Phase 2:

1. Create `requirements.txt` in each Lambda directory:
   ```txt
   requests==2.31.0
   pydantic==2.5.0
   ```

2. Update `./scripts/package-lambda.sh` to install dependencies:
   ```bash
   pip install -r requirements.txt -t .
   zip -r function.zip .
   ```

3. Consider using AWS Lambda Layers for shared dependencies

## Testing (TODO)

Add unit tests for Lambda functions:

```
tests/
├── unit/
│   ├── test_mvp_service.py
│   └── test_seeder.py
└── integration/
    └── test_api_endpoints.py
```

Run tests before deployment:

```bash
pytest tests/unit/
pytest tests/integration/ --stack-name=silvermoat-test
```

## Monitoring

Lambda functions log to CloudWatch Logs:

```bash
# View logs for MVP service Lambda
aws logs tail /aws/lambda/silvermoat-demo-MvpServiceFunction-* --follow

# View logs for seeder Lambda
aws logs tail /aws/lambda/silvermoat-demo-SeederFunction-* --follow
```
