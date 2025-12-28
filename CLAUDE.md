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
  - "Execute phase X"
  - or "Proceed with implementation"
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

## Project Overview

Silvermoat is a one-shot deployable insurance MVP demo built on AWS CDK (TypeScript). Infrastructure and application can be deployed with a single CDK command, featuring:

- **Frontend**: React SPA (Vite) hosted on S3 website with CloudFront CDN (HTTPS)
- **Backend**: Single Lambda function handling all API routes via AWS_PROXY integration
- **Infrastructure**: All AWS resources defined in CDK (TypeScript)

## Key Commands

### Infrastructure Deployment
```bash
# Deploy CDK stack
cd cdk
npm install
npm run deploy

# Deploy with custom parameters
export APP_NAME=silvermoat STAGE_NAME=prod
npm run deploy

# Get stack outputs (API URL, S3 bucket names, etc.)
../scripts/get-outputs.sh

# Delete entire stack
npm run destroy
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
../scripts/deploy-ui.sh
```

### Testing
```bash
# Run smoke tests against deployed stack
./scripts/smoke-test.sh
```

## Architecture

### Backend: Single Lambda Pattern

The backend uses a **single Lambda function** (`MvpServiceFunction`) that routes all API requests based on path and HTTP method. Code is in `cdk/lib/lambda/mvp-service/index.py`.

**Key routing patterns:**
- `POST /{domain}` → Create entity (quote, policy, claim, payment, case)
- `GET /{domain}/{id}` → Read entity by ID
- `POST /claim/{id}/status` → Update claim status
- `POST /claim/{id}/doc` → Attach document to claim
- `POST /chat` → Bedrock AI assistant

The Lambda uses AWS_PROXY integration, meaning it must return responses in API Gateway proxy format with `statusCode`, `headers`, and `body` fields.

**Environment variables injected:**
- `QUOTES_TABLE`, `POLICIES_TABLE`, `CLAIMS_TABLE`, `PAYMENTS_TABLE`, `CASES_TABLE`
- `DOCS_BUCKET` (S3 bucket for documents)
- `SNS_TOPIC_ARN` (for notifications)
- `BEDROCK_MODEL_ID`, `BEDROCK_REGION` (for AI assistant)

**CORS**: The Lambda includes CORS headers (`Access-Control-Allow-Origin: *`) in all responses to allow browser requests from the S3 website.

### Frontend: React SPA with Vite

The UI is located in `ui/` and uses:
- React 18 with functional components and hooks
- React Router v6 with lazy loading
- React Query (TanStack Query v5) for server state
- Ant Design v5 for UI components
- Vite for build tooling

**API Base URL Configuration:**
The frontend gets the API URL via:
1. Build-time: `VITE_API_BASE_URL` environment variable (set by `deploy-ui.sh`)
2. Runtime: `window.API_BASE_URL` (can be injected in `index.html`)
3. Fallback: `import.meta.env.VITE_API_BASE_URL`

### CDK Infrastructure

The stack is defined in `cdk/lib/` using TypeScript:

**Main Stack** (`silvermoat-stack.ts`):
- Orchestrates all constructs
- Creates SNS topic
- Configures Custom Resources for seeding/cleanup

**Storage Construct** (`constructs/storage.ts`):
- Creates 5 DynamoDB tables (Quotes, Policies, Claims, Payments, Cases)
- Creates 2 S3 buckets (UI public, Docs private)

**Compute Construct** (`constructs/compute.ts`):
- Creates MvpServiceFunction Lambda (API handler)
- Creates SeederFunction Lambda (custom resource)
- Creates IAM roles with least-privilege permissions

**API Construct** (`constructs/api.ts`):
- Creates API Gateway REST API
- Configures Lambda proxy integration
- Sets up ANY method on root and {proxy+}

**CDN Construct** (`constructs/cdn.ts`):
- Creates CloudFront distribution (conditional)
- Creates ACM certificate for custom domain (conditional)
- Configures SPA routing (404/403 → index.html)

### Custom Resources

The stack includes Custom Resources powered by `SeederFunction`:

1. **SeedCustomResource** (`Mode: seed`): Runs on CREATE/UPDATE to:
   - Upload initial `index.html` if `UiSeedingMode=seeded`
   - Seed DynamoDB tables with demo data (80 quotes, 60 policies, 40 claims, 180 payments, 50 cases)
   - Upload sample documents to S3

2. **CleanupCustomResource** (`Mode: cleanup`): Runs on DELETE to:
   - Empty both S3 buckets (handles versioned objects and delete markers)
   - Wipe all DynamoDB table items
   - Ensures buckets are empty before CDK deletion

The cleanup Lambda is critical for successful stack deletion. Check CloudWatch logs at `/aws/lambda/SilvermoatStack-Compute-SeederFunction-*` if deletion fails.

### DynamoDB Schema

All tables use a simple key schema:
- **Partition Key**: `id` (String)
- **Billing Mode**: PAY_PER_REQUEST (no provisioned capacity)
- **Removal Policy**: DESTROY (for demo purposes)

Tables: `QuotesTable`, `PoliciesTable`, `ClaimsTable`, `PaymentsTable`, `CasesTable`

**Important**: DynamoDB does not accept Python `float` types. Use integers for currency (e.g., `premium_cents: 12550`) or `Decimal` type.

### S3 Buckets

1. **UiBucket**: Public website hosting
   - Website configuration: `IndexDocument: index.html`, `ErrorDocument: index.html`
   - Public read access via bucket policy
   - Serves as origin for CloudFront distribution
   - `autoDeleteObjects: true` for clean deletion

2. **DocsBucket**: Private bucket for claim documents/attachments
   - Access controlled via IAM (Lambda-only access)
   - `autoDeleteObjects: true` for clean deletion

### CloudFront & Custom Domains

The stack includes CloudFront distribution with optional custom domain support.

**Configuration via parameters:**
- `DomainName`: Custom domain (default: `silvermoat.net`), empty = CloudFront default only
- `CreateCloudFront`: Create distribution (default: `true`), `false` = S3 website URL only

**Resources:**

1. **UiCertificate** (conditional, if `DomainName` provided):
   - Type: ACM Certificate
   - Validation: DNS (requires CNAME in Cloudflare)
   - Used by CloudFront for HTTPS on custom domain

2. **UiDistribution** (conditional, if `CreateCloudFront` true):
   - Origin: S3 website endpoint (HttpOrigin, HTTP only)
   - Aliases: Custom domain (if `DomainName` parameter set)
   - Certificate: ACM cert (if custom domain), else CloudFront default
   - Caching: CachingOptimized policy
   - SPA routing: 404/403 → index.html with 200 status
   - Price class: 100 (US/CA/EU)

**Custom domain setup (default: silvermoat.net):**
1. Deploy stack: `cd cdk && npm run deploy`
2. Stack creates ACM cert, waits for DNS validation
3. Add ACM validation CNAME to Cloudflare (DNS only, gray cloud)
4. Wait for cert validation (~5-15min)
5. Stack completes, CloudFront gets custom domain alias
6. Add CloudFront alias CNAME to Cloudflare (DNS only, gray cloud)
7. Access via `https://silvermoat.net`

**Critical**: Cloudflare proxy must be **disabled** (DNS only, gray cloud) for both records.

## Development Workflow

### Making Backend Changes

The backend Lambda code is in `cdk/lib/lambda/mvp-service/index.py`. To modify:

1. Edit the Python code in `cdk/lib/lambda/mvp-service/index.py`
2. Redeploy: `cd cdk && npm run deploy`
3. CDK automatically packages and uploads Lambda code

**Note**: For API Gateway method changes, increment `API_DEPLOYMENT_TOKEN` environment variable to force a new deployment.

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

### Making Infrastructure Changes

To modify CDK infrastructure:

1. Edit CDK code in `cdk/lib/` (TypeScript)
2. Compile: `cd cdk && npm run build`
3. Preview changes: `npm run diff`
4. Deploy: `npm run deploy`

**Common changes:**
- Add DynamoDB table: Edit `constructs/storage.ts`
- Add Lambda permissions: Edit `constructs/compute.ts`
- Add API endpoint: Edit Lambda code in `lib/lambda/mvp-service/index.py`
- Change CloudFront behavior: Edit `constructs/cdn.ts`

### Adding New API Endpoints

To add a new endpoint to the Lambda function:

1. Edit `cdk/lib/lambda/mvp-service/index.py`
2. Add route handling in the `handler` function
3. If accessing new AWS resources, update IAM role in `constructs/compute.ts`
4. Redeploy: `cd cdk && npm run deploy`

Example route pattern:
```python
# POST /policy/{id}/status
if domain == "policy" and method == "POST" and len(parts) == 3 and parts[2] == "status":
    _id = parts[1]
    # Your logic here
    return _resp(200, {"id": _id, "status": "updated"})
```

## Important Constraints

### CDK Bootstrap

Before first deployment, AWS account must be bootstrapped for CDK:

```bash
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```

### API Gateway Deployment Token

When you modify API Gateway resources, change the `API_DEPLOYMENT_TOKEN` environment variable to force a new deployment:

```bash
export API_DEPLOYMENT_TOKEN=v2
cd cdk && npm run deploy
```

Without this, API Gateway may not reflect changes.

### Lambda Packaging

CDK handles Lambda packaging automatically:
- Reads Python code from `cdk/lib/lambda/*/index.py`
- Creates ZIP file
- Uploads to S3 bucket (created by CDK bootstrap)
- Updates Lambda function code

No manual ZIP files or S3 uploads required.

### Custom Resource Behavior

- The `SeederFunction` handles both seeding and cleanup using the `Mode` property
- On stack deletion, the cleanup Lambda empties S3 buckets before CDK tries to delete them
- If stack deletion fails with "bucket not empty", check `/aws/lambda/SilvermoatStack-Compute-SeederFunction-*` logs
- The Lambda has a 120-second timeout to handle large bucket cleanups

### UI Seeding Mode

The `UI_SEEDING_MODE` environment variable controls initial UI deployment:
- `seeded`: Lambda uploads a basic `index.html` for quick demo
- `external` (default): Skip Lambda upload, deploy React SPA separately with `deploy-ui.sh`

For development, always use `UI_SEEDING_MODE=external` and deploy the React app with the script.

## Stack Parameters

Set via environment variables:

- `APP_NAME` (default: `silvermoat`): Short name used in resource naming
- `STAGE_NAME` (default: `demo`): API Gateway stage name
- `API_DEPLOYMENT_TOKEN` (default: `v1`): Change to force API redeployment
- `UI_SEEDING_MODE` (default: `external`): `seeded` or `external`
- `DOMAIN_NAME` (default: `silvermoat.net`): Custom domain, empty = CloudFront default only
- `CREATE_CLOUDFRONT` (default: `true`): Create CloudFront, `false` = S3 website only

Example:
```bash
export APP_NAME=silvermoat
export STAGE_NAME=prod
export DOMAIN_NAME=app.silvermoat.net
cd cdk && npm run deploy
```

## Troubleshooting

### Stack Deletion Fails

If `DELETE_FAILED` with bucket errors:
1. Check CloudWatch logs: `/aws/lambda/SilvermoatStack-Compute-SeederFunction-*`
2. Verify cleanup Lambda executed successfully
3. Manual fallback: `aws s3 rm s3://<bucket-name> --recursive`

### API Returns 403/404

- Verify API Gateway deployment token was updated
- Check Lambda logs: `/aws/lambda/SilvermoatStack-Compute-MvpServiceFunction-*`
- Confirm Lambda has permission to invoke from API Gateway

### UI Shows "API base URL not configured"

The React app couldn't find the API URL. Options:
1. Ensure `deploy-ui.sh` ran (it sets `VITE_API_BASE_URL` during build)
2. Manually set `window.API_BASE_URL` in `ui/index.html`
3. Check `App.jsx` for URL resolution logic

### CORS Errors

The Lambda returns CORS headers in all responses. If CORS errors persist:
1. Verify API Gateway integration is `AWS_PROXY` (not `AWS`)
2. Check Lambda is returning proper response format with `headers` field
3. Confirm browser is making requests to the correct API URL

### CDK Synth Fails

- Verify Node.js and TypeScript installed
- Run `cd cdk && npm install`
- Run `npm run build` to compile TypeScript
- Check for TypeScript errors in `cdk/lib/`

### CDK Deploy Fails

- Verify AWS credentials: `aws sts get-caller-identity`
- Ensure CDK bootstrap: `cdk bootstrap`
- Check CloudFormation stack events in AWS Console
- Review error messages in terminal

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
