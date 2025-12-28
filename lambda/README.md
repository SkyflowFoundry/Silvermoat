# Lambda Functions

This directory contains the Lambda function code for Silvermoat MVP.

## Structure

```
lambda/
├── mvp_service/
│   └── handler.py       # Main MVP service Lambda (handles all API routes)
└── seeder/
    └── handler.py       # Custom Resource Lambda (seeding + cleanup)
```

## Current State (S3-Packaged Lambda Code)

The Lambda code is **stored in separate Python files** and **packaged to S3** during deployment.

The CloudFormation template (`infra/silvermoat-mvp-s3-website.yaml`) references the Lambda code from S3 using the `S3Bucket` and `S3Key` properties.

### Benefits

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

4. **No code duplication**:
   - Single source of truth for Lambda code
   - No need to sync code between files

5. **Scalability**:
   - Can add dependencies via `requirements.txt`
   - Faster deployments (only upload code when changed)
   - Better for CI/CD pipelines

## Deployment Workflow

The `./scripts/deploy-stack.sh` script automatically:
1. Packages Lambda functions to ZIP files
2. Uploads ZIP files to S3 (same bucket as CloudFormation templates)
3. Deploys CloudFormation stack with references to S3 code

You don't need to manually package or upload Lambda code.

## Migration from Inline Code (Complete)

The migration from inline Lambda code to S3-packaged code is **complete**:

1. ✅ **Lambda packaging integrated into deployment**:
   - `./scripts/deploy-stack.sh` automatically packages and uploads Lambda ZIPs to S3
   - CloudFormation template references S3 location instead of inline code
   - Uses same S3 bucket as CloudFormation templates

2. ✅ **CloudFormation template updated**:
   - Added `LambdaCodeS3Bucket`, `MvpServiceCodeS3Key`, `SeederCodeS3Key` parameters
   - Changed `MvpServiceFunction.Code` from `ZipFile` to `S3Bucket/S3Key`
   - Changed `SeederFunction.Code` from `ZipFile` to `S3Bucket/S3Key`
   - Removed all inline Lambda code (no more duplication)

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
