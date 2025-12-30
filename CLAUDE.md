# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Global Rules (Always Apply)

- Be extremely concise.
- Sacrifice grammar for concision.
- Prefer bullets over prose.
- No filler. No restating the obvious.

## Planning First

- Never write code until a plan is approved.
- Default to plan mode for non-trivial work.
- Explore the codebase before proposing a plan.
- Identify ambiguities early.

## Plans

Every plan MUST include:
1. Goal (1 line)
2. Assumptions (if any)
3. Phases (numbered)
4. File-level changes per phase
5. Unresolved questions (required)

### Unresolved Questions
- Always include an **Unresolved Questions** section.
- Questions must be concise.
- Ask only what blocks execution.
- Stop after listing questions.

## Multi-Phase Work

- If work may exceed one context window:
  - Explicitly break into phases.
  - Each phase should be independently executable.
  - Later phases may depend on artifacts from earlier phases.

## Execution

- Do not execute until explicitly told:
  - “Execute phase X”
  - or “Proceed with implementation”
- When executing:
  - Make minimal, correct changes.
  - Leave TODO markers for future phases.
  - Do not refactor unless required.

## Git & GitHub

- Primary interface: GitHub CLI (`gh`)
- Use GitHub Issues to persist plans across context resets.
- When requested:
  - Create or update a GitHub issue with the full plan.
  - Check off completed phases.
- Commit messages:
  - Extremely concise.
  - One-line summary only.

## Context Discipline

- Avoid unnecessary verbosity.
- Do not repeat earlier content unless asked.
- If context may be stale:
  - Ask to re-read files.
  - Do nothing else.

## If Unsure

- Ask.
- Do not guess.

## Testing

### General Principles

- **Always add tests for new functionality** that fits existing test categories.
- Do not create new non-trivial test infrastructure unnecessarily.
- Match existing test patterns and structure exactly.
- Simple tests (unit tests, straightforward integration tests) should be added for new functionality.
- Complex test infrastructure (new test frameworks, new test environments, elaborate mocking) requires justification.

### Test Categories (Add to These)

When adding new functionality, check these test categories and add tests where applicable:

**1. JavaScript Unit Tests** (`ui/src/**/*.test.js`)
- Pure utility functions
- Data generators
- Helper functions
- Pattern: Use Vitest, test all exported functions

**2. E2E Tests** (`tests/e2e/tests/*.py`)
- User-facing UI interactions
- Form submissions
- Navigation flows
- Pattern: Use Selenium, test all user workflows

**3. API Contract Tests** (`tests/api/test_*.py`)
- API endpoints (create, read, update, delete)
- Request/response validation
- Error handling
- Pattern: One test file per resource (quote, policy, claim, payment, case)
- **IMPORTANT**: When adding a new resource/entity, create corresponding API contract tests

### Examples

**Appropriate (DO add tests):**
- New utility function → unit test in same directory
- New form component → E2E test in `test_form_*.py`
- New API endpoint → test in `tests/api/test_<resource>.py`
- New UI button/feature → E2E test for interaction
- New data generator → unit test for output validation

**Requires justification (DON'T add without asking):**
- New test framework (Jest, Mocha, etc.)
- New test environment (Docker, separate test infra)
- Complex mocking infrastructure

### Checklist Before Completing Feature

1. Does feature have UI components? → Add E2E tests
2. Does feature use utility functions? → Add unit tests
3. Does feature touch API endpoints? → Add/update API contract tests
4. Do all similar resources have equivalent test coverage? (e.g., if 4/5 forms have tests, add tests for the 5th)

## Project Overview

Silvermoat is a one-shot deployable insurance MVP demo built on AWS CDK (Python). The entire infrastructure and application can be deployed with a single CDK command, featuring:

- **Frontend**: React SPA (Vite) hosted on S3 website
- **Backend**: Single Lambda function handling all API routes via AWS_PROXY integration
- **Infrastructure**: All AWS resources defined in CDK (Python), synthesizes to CloudFormation

## Key Commands

### Infrastructure Deployment
```bash
# Deploy CDK stack
./scripts/deploy-stack.sh

# Or use CDK CLI directly
cd cdk && cdk deploy silvermoat

# Deploy with custom parameters
STACK_NAME=my-silvermoat APP_NAME=silvermoat STAGE_NAME=prod ./scripts/deploy-stack.sh

# Get stack outputs (API URL, S3 bucket names, etc.)
./scripts/get-outputs.sh

# Delete entire stack
./scripts/delete-stack.sh

# CDK-specific commands
cd cdk
cdk synth silvermoat          # View synthesized CloudFormation
cdk diff silvermoat           # Compare with deployed stack
```

### UI Development
```bash
# Local development server (http://localhost:5173)
cd ui
npm install
npm run dev

# Build production bundle
npm run build

# Deploy UI to S3 (after infrastructure is deployed)
./scripts/deploy-ui.sh
```

### Testing
```bash
# Run smoke tests against deployed stack
./scripts/smoke-test.sh

# Run full E2E test suite
cd tests/e2e
pytest -v -m smoke
```

## CI/CD & A-B Deployment

Silvermoat uses GitHub Actions for automated testing and deployment.

### Composite Actions

Reusable actions to reduce duplication:

**1. Setup Environment** (`.github/actions/setup-env/action.yml`)
- Sets up Python 3.11 + Node.js 24
- Configures npm caching
- Used by: e2e-tests, deploy-production

**2. Install Dependencies** (`.github/actions/install-deps/action.yml`)
- Installs Python test dependencies
- Optionally installs UI dependencies (npm ci)
- Input: `install-ui` (default: 'true')

### Workflows

**1. E2E Tests** (`.github/workflows/e2e-tests.yml`)
- Trigger: PR to main, workflow_dispatch
- Creates ephemeral test stack: `silvermoat-test-pr-{NUMBER}`
- No CloudFront (HTTP S3 only, fast deployment)
- **Matrix strategy**: 6 jobs with parallel test execution
  - `validate-cdk`: Validate CDK stacks via synthesis (5min)
  - `setup-stack`: Deploy infrastructure + UI (20min, waits for validation)
  - `test-suite`: Run smoke/API/E2E in parallel (15min max)
  - `analyze-results`: Aggregate outputs + Claude AI analysis (5min)
  - `post-to-pr`: Post analysis + auto-create issues for failures (5min)
  - `check-results`: Final pass/fail determination
- Tests run in parallel, reducing total runtime ~50% (45min → 25min)
- Stack persists until PR closed
- **Auto-issue creation**: Claude extracts discrete issues from test failures and creates GitHub issues automatically (default: enabled for PRs, controlled by `create_issues` input on workflow_dispatch)
- Test artifacts (screenshots, page source, console logs) uploaded on failure for debugging

**2. PR Stack Cleanup** (`.github/workflows/pr-stack-cleanup.yml`)
- Trigger: PR closed/merged
- Deletes test stack created by E2E workflow
- Ensures no orphaned stacks

**3. Deploy Production** (`.github/workflows/deploy-production.yml`)
- Trigger: Push to main
- Deploys production stack: `silvermoat`
- CloudFront + custom domain enabled
- Smart DNS update via Cloudflare (skips if CloudFront domain unchanged)
- Invalidates CloudFront cache
- Runs smoke tests
- Fails if tests fail
- Uses composite actions for setup

### GitHub Secrets

Required secrets configured:
- `AWS_ROLE_ARN` - IAM role for AWS operations (all workflows)
- `CLOUDFLARE_API_TOKEN` - Cloudflare DNS updates (production only)
- `CLOUDFLARE_ZONE_ID` - Zone ID for silvermoat.net (production only)
- `ANTHROPIC_API_KEY_GITHUB_ACTIONS` - E2E test analysis

### Smart DNS Updates

Script: `scripts/update-cloudflare-dns.sh`

- Fetches current DNS from Cloudflare API
- Fetches target CloudFront domain from stack outputs
- Only updates if different (optimization)
- CloudFront domains rarely change (~10% of deploys)

See `docs/ab-deployment-design.md` for complete architecture.

## Architecture

### CDK Project Structure

Infrastructure defined in `cdk/`:
```
cdk/
├── app.py                          # CDK entry point
├── cdk.json                        # CDK configuration
├── requirements.txt                # CDK dependencies
├── config/
│   ├── base.py                     # Config dataclass
│   └── environments.py             # Per-environment config
├── stacks/
│   ├── silvermoat_stack.py        # Parent orchestrator
│   ├── data_stack.py              # DynamoDB + SNS
│   ├── storage_stack.py           # S3 buckets
│   ├── compute_stack.py           # Lambda + IAM
│   ├── api_stack.py               # API Gateway
│   └── frontend_stack.py          # CloudFront + ACM
└── constructs/
    └── seeder_custom_resource.py  # Custom resources
```

### Backend: Single Lambda Pattern

The backend uses a **single Lambda function** (`MvpServiceFunction`) that routes all API requests based on path and HTTP method. The Lambda code is in `lambda/mvp_service/handler.py` and is packaged to S3 during deployment.

**Key routing patterns:**
- `POST /{domain}` → Create entity (quote, policy, claim, payment, case)
- `GET /{domain}/{id}` → Read entity by ID
- `POST /claim/{id}/status` → Update claim status
- `POST /claim/{id}/doc` → Attach document to claim

The Lambda uses AWS_PROXY integration, meaning it must return responses in API Gateway proxy format with `statusCode`, `headers`, and `body` fields.

**Environment variables injected:**
- `QUOTES_TABLE`, `POLICIES_TABLE`, `CLAIMS_TABLE`, `PAYMENTS_TABLE`, `CASES_TABLE`
- `DOCS_BUCKET` (S3 bucket for documents)
- `SNS_TOPIC_ARN` (for notifications)

**CORS**: The Lambda includes CORS headers (`Access-Control-Allow-Origin: *`) in all responses to allow browser requests from the S3 website.

### Frontend: React SPA with Vite

The UI is located in `ui/` and uses:
- React 18 with functional components and hooks
- Ant Design component library
- Vite for build tooling
- API client abstraction in `ui/src/services/api.js`

**API Base URL Configuration:**
The frontend gets the API URL via:
1. Build-time: `VITE_API_BASE_URL` environment variable (set by `deploy-ui.sh`)
2. Runtime: `window.API_BASE_URL` (can be injected in `index.html`)
3. Fallback: `import.meta.env.VITE_API_BASE_URL`

**Form Sample Data:**
All forms include "Fill with Sample Data" button:
- Utility: `ui/src/utils/formSampleData.js`
- Functions: `generateQuoteSampleData()`, `generatePolicySampleData()`, etc.
- Reuses helpers from `seedData.js` for consistency
- Forms: Quote, Policy, Claim, Payment, Case
- Button uses `ThunderboltOutlined` icon, default styling

### CDK Custom Resources

The stack includes custom resources powered by a single `SeederFunction` Lambda, defined in `cdk/constructs/seeder_custom_resource.py`:

1. **SeedCustomResource** (`Mode: seed`): Runs on CREATE/UPDATE to:
   - Upload initial `index.html` if `UiSeedingMode=seeded`
   - Seed DynamoDB tables with demo data
   - Upload sample documents to S3

2. **CleanupCustomResource** (`Mode: cleanup`): Runs on DELETE to:
   - Empty both S3 buckets (handles versioned objects and delete markers)
   - Wipe all DynamoDB table items

**Note**: CDK's `auto_delete_objects` handles S3 cleanup automatically. Cleanup Lambda primarily needed for DynamoDB. Check CloudWatch logs at `/aws/lambda/<stack-name>-SeederFunction-*` if deletion fails.

### DynamoDB Schema

All tables use a simple key schema:
- **Partition Key**: `id` (String)
- **Billing Mode**: PAY_PER_REQUEST (no provisioned capacity)

Tables: `QuotesTable`, `PoliciesTable`, `ClaimsTable`, `PaymentsTable`, `CasesTable`

**Important**: DynamoDB does not accept Python `float` types. Use integers for currency (e.g., `premium_cents: 12550`) or `Decimal` type.

### S3 Buckets

1. **UiBucket**: Public website hosting
   - Website configuration: `IndexDocument: index.html`, `ErrorDocument: index.html`
   - Public read access via bucket policy
   - Serves as origin for CloudFront distribution

2. **DocsBucket**: Private bucket for claim documents/attachments
   - Access controlled via IAM (Lambda-only access)

### CloudFront & Custom Domains

The stack includes CloudFront distribution with optional custom domain support (added for production HTTPS).

**Resources:**

1. **UiCertificate** (conditional, if `DomainName` provided):
   - Type: AWS::CertificateManager::Certificate
   - Region: us-east-1 (required for CloudFront)
   - Validation: DNS (requires CNAME in Cloudflare)
   - Used by CloudFront for HTTPS on custom domain

2. **UiDistribution** (always created):
   - Type: AWS::CloudFront::Distribution
   - Origin: S3 website endpoint (CustomOriginConfig, HTTP)
   - Aliases: Custom domain (if `DomainName` parameter set)
   - Certificate: ACM cert (if custom domain), else CloudFront default
   - Caching: AWS managed policy (CachingOptimized)
   - SPA routing: 404/403 → index.html with 200 status
   - Price class: 100 (US/CA/EU, cheapest)

**Key behaviors:**
- S3 website endpoint remains accessible (HTTP)
- CloudFront adds HTTPS layer and caching
- Both CloudFront default domain AND custom domain work (if configured)
- HTTP requests redirect to HTTPS
- SPA client-side routing handled (404 errors serve index.html)
- Compression enabled (gzip/brotli)

**Custom domain setup (default: silvermoat.net):**
1. Deploy stack (DomainName defaults to `silvermoat.net`)
2. Stack creates ACM cert, waits for DNS validation
3. Add ACM validation CNAME to Cloudflare (DNS only, gray cloud)
4. Wait for cert validation (~5-15min)
5. Stack completes, CloudFront gets custom domain alias
6. Add CloudFront alias CNAME to Cloudflare (DNS only, gray cloud)
7. Access via `https://silvermoat.net`

**To disable custom domain:** Set `DomainName=""` parameter (CloudFront default domain only)
**To use different domain:** Set `DomainName=app.silvermoat.net` parameter

**Outputs:**
- `CloudFrontUrl`: https://xyz123.cloudfront.net (always available)
- `CustomDomainUrl`: https://silvermoat.net (if `DomainName` configured)
- `CloudFrontDomain`: CloudFront domain for DNS CNAME
- `CertificateArn`: ACM cert ARN (if custom domain)

**Cloudflare DNS setup:**
User must add 2 CNAME records:
1. `_validation-subdomain.silvermoat.net` → `_validation-target.acm-validations.aws.` (cert validation)
2. `silvermoat.net` → `xyz123.cloudfront.net` (site access)

**Critical**: Cloudflare proxy must be **disabled** (DNS only, gray cloud) for both records. Orange cloud (proxied) conflicts with CloudFront's SSL/caching.

**Architecture flow:**
```
Browser → CloudFront (HTTPS) → S3 Website Endpoint (HTTP)
          https://silvermoat.net
          OR
          https://xyz123.cloudfront.net
          ↓
          CloudFront caches, compresses, serves
          ↓
          Origin: bucket-name.s3-website-us-east-1.amazonaws.com
```

S3 website endpoint (HTTP) still works for direct access/testing.

## Development Workflow

### Lambda Code Management

Lambda functions are stored as Python files in the `lambda/` directory and bundled automatically by CDK:

**Structure**:
- `lambda/mvp_service/handler.py` - Main API handler (routes all endpoints)
- `lambda/seeder/handler.py` - Custom Resource handler (seeding/cleanup)
- `lambda/shared/` - Shared utilities (automatically bundled with both functions)
- `lambda/README.md` - Detailed Lambda documentation

**CDK Deployment flow**:
1. CDK `PythonFunction` construct automatically bundles Lambda code
2. Includes shared/ directory with both functions
3. CDK calculates code hash and only redeploys if changed
4. No manual packaging needed (removed `scripts/package-lambda.sh`)

**Benefits**:
- IDE support (autocomplete, linting, type checking)
- Automatic bundling via CDK (no manual ZIP creation)
- CDK handles code hashing and change detection
- Clear git diffs when code changes
- Can add unit tests for Lambda functions

Lambda definitions in `cdk/stacks/compute_stack.py`. See `lambda/README.md` for detailed documentation.

### Making Backend Changes

The backend Lambda code is in separate Python files and bundled automatically by CDK. To modify:

1. Edit the Lambda code:
   - MVP service: `lambda/mvp_service/handler.py`
   - Seeder: `lambda/seeder/handler.py`
2. Redeploy the stack: `./scripts/deploy-stack.sh`
   - CDK automatically detects code changes via content hashing
   - Bundles Lambda code with shared dependencies
   - Only redeploys changed functions
3. No manual packaging needed

**Note**: For API Gateway method changes, increment `API_DEPLOYMENT_TOKEN` parameter to force a new deployment.

### Making Frontend Changes

1. Edit React components in `ui/src/`
2. Test locally: `cd ui && npm run dev`
3. Deploy to S3: `./scripts/deploy-ui.sh`

The `deploy-ui.sh` script:
- Builds the React app with `npm run build`
- Fetches the API base URL from stack outputs
- Sets `VITE_API_BASE_URL` environment variable during build
- Syncs build output to S3 with proper cache headers
- HTML files: `no-cache`, static assets: `max-age=31536000`

### Adding New API Endpoints

To add a new endpoint to the Lambda function:

1. Edit `lambda/mvp_service/handler.py`
2. Locate the `handler` function and add your route logic
3. Parse `path` and `method` to add your route
4. If needed, update environment variables in CloudFormation template:
   - `infra/silvermoat-mvp-s3-website.yaml` → `MvpServiceFunction.Environment.Variables`
5. If needed, update IAM permissions in `MvpLambdaRole` (same file)
6. Redeploy: `./scripts/deploy-stack.sh`

Example route pattern:
```python
# POST /policy/{id}/status
if domain == "policy" and method == "POST" and len(parts) == 3 and parts[2] == "status":
    _id = parts[1]
    # Your logic here
    return _resp(200, {"id": _id, "status": "updated"})
```

## Important Constraints

### API Gateway Deployment Token

When you modify API Gateway resources (methods, integrations), you must change the `ApiDeploymentToken` parameter to force a new deployment:

```bash
API_DEPLOYMENT_TOKEN=v2 ./scripts/deploy-stack.sh
```

Without this, API Gateway may not reflect your changes even though CDK shows no updates needed.

### S3 Website Hosting (HTTP Only)

The S3 website endpoint is HTTP, not HTTPS. This is intentional for the MVP to avoid CloudFront complexity. The architecture diagram in README.md shows browser → S3 Website (HTTP) → API Gateway (HTTPS).

### Custom Resource Behavior

- The `SeederFunction` handles both seeding and cleanup using the `Mode` property
- CDK's `auto_delete_objects` handles S3 cleanup automatically. Cleanup Lambda primarily for DynamoDB.
- If stack deletion fails with "bucket not empty", check `/aws/lambda/<stack-name>-SeederFunction-*` logs
- The Lambda has a 120-second timeout to handle large bucket cleanups

### UI Seeding Mode

The `UiSeedingMode` parameter controls initial UI deployment:
- `seeded` (default): Lambda uploads a basic `index.html` for quick demo
- `external`: Skip Lambda upload, deploy React SPA separately with `deploy-ui.sh`

For development, always use `UiSeedingMode=external` and deploy the React app with the script.

## Stack Parameters

Defined in `infra/silvermoat-mvp-s3-website.yaml:7-35`:

- `AppName` (default: `silvermoat`): Short name used in resource naming
- `StageName` (default: `demo`): API Gateway stage name
- `ApiDeploymentToken` (default: `v1`): Change to force API redeployment
- `UiSeedingMode` (default: `seeded`): `seeded` or `external`

Set via environment variables in `deploy-stack.sh`:
```bash
STACK_NAME=silvermoat APP_NAME=silvermoat STAGE_NAME=demo ./scripts/deploy-stack.sh
```

## Troubleshooting

### Stack Deletion Fails

If `DELETE_FAILED` with bucket errors:
1. Check CloudWatch logs: `/aws/lambda/<stack-name>-SeederFunction-*`
2. Verify cleanup Lambda executed successfully
3. Manual fallback: `aws s3 rm s3://<bucket-name> --recursive`

### API Returns 403/404

- Verify API Gateway deployment token was updated
- Check Lambda logs: `/aws/lambda/<stack-name>-MvpServiceFunction-*`
- Confirm Lambda has permission to invoke from API Gateway (`ApiInvokePermission`)

### UI Shows "API base URL not configured"

The React app couldn't find the API URL. Options:
1. Ensure `deploy-ui.sh` ran (it sets `VITE_API_BASE_URL` during build)
2. Manually set `window.API_BASE_URL` in `ui/index.html`
3. Check `App.jsx:11-20` for URL resolution logic

### CORS Errors

The Lambda returns CORS headers in all responses. If CORS errors persist:
1. Verify API Gateway integration is `AWS_PROXY` (not `AWS`)
2. Check Lambda is returning proper response format with `headers` field
3. Confirm browser is making requests to the correct API URL

## Testing

The `smoke-test.sh` script validates:
- API Gateway root endpoint responds with endpoint list
- Creating a quote via `POST /quote`
- Retrieving the quote via `GET /quote/{id}`
- Basic error handling

Run after deployment to verify the stack is functional:
```bash
./scripts/smoke-test.sh
```
