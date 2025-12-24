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

## Project Overview

Silvermoat is a one-shot deployable insurance MVP demo built on AWS CloudFormation. The entire infrastructure and application can be deployed with a single CloudFormation template, featuring:

- **Frontend**: React SPA (Vite) hosted on S3 website
- **Backend**: Single Lambda function handling all API routes via AWS_PROXY integration
- **Infrastructure**: All AWS resources defined in CloudFormation (no Terraform, CDK, or other tools)

## Key Commands

### Infrastructure Deployment
```bash
# Deploy CloudFormation stack
./scripts/deploy-stack.sh

# Deploy with custom parameters
STACK_NAME=my-silvermoat APP_NAME=silvermoat STAGE_NAME=prod ./scripts/deploy-stack.sh

# Get stack outputs (API URL, S3 bucket names, etc.)
./scripts/get-outputs.sh

# Delete entire stack
./scripts/delete-stack.sh
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
```

## Architecture

### Backend: Single Lambda Pattern

The backend uses a **single Lambda function** (`MvpServiceFunction`) that routes all API requests based on path and HTTP method. This is defined inline in the CloudFormation template at `infra/silvermoat-mvp-s3-website.yaml:236-355`.

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
- Vite for build tooling
- Simple component structure: `App.jsx` → `QuoteForm.jsx` + `QuoteList.jsx`
- API client abstraction in `ui/src/services/api.js`

**API Base URL Configuration:**
The frontend gets the API URL via:
1. Build-time: `VITE_API_BASE_URL` environment variable (set by `deploy-ui.sh`)
2. Runtime: `window.API_BASE_URL` (can be injected in `index.html`)
3. Fallback: `import.meta.env.VITE_API_BASE_URL`

### CloudFormation Custom Resources

The stack includes two Custom Resources powered by a single `SeederFunction` Lambda:

1. **SeedCustomResource** (`Mode: seed`): Runs on CREATE/UPDATE to:
   - Upload initial `index.html` if `UiSeedingMode=seeded`
   - Seed DynamoDB tables with demo data
   - Upload sample documents to S3

2. **CleanupCustomResource** (`Mode: cleanup`): Runs on DELETE to:
   - Empty both S3 buckets (handles versioned objects and delete markers)
   - Wipe all DynamoDB table items
   - Ensures buckets are empty before CloudFormation deletion

The cleanup Lambda is critical for successful stack deletion. Check CloudWatch logs at `/aws/lambda/<stack-name>-SeederFunction-*` if deletion fails.

### DynamoDB Schema

All tables use a simple key schema:
- **Partition Key**: `id` (String)
- **Billing Mode**: PAY_PER_REQUEST (no provisioned capacity)

Tables: `QuotesTable`, `PoliciesTable`, `ClaimsTable`, `PaymentsTable`, `CasesTable`

**Important**: DynamoDB does not accept Python `float` types. Use integers for currency (e.g., `premium_cents: 12550`) or `Decimal` type.

### S3 Buckets

1. **UiBucket**: Public website hosting (HTTP only, no HTTPS/CloudFront in MVP)
   - Website configuration: `IndexDocument: index.html`, `ErrorDocument: index.html`
   - Public read access via bucket policy

2. **DocsBucket**: Private bucket for claim documents/attachments
   - Access controlled via IAM (Lambda-only access)

## Development Workflow

### Making Backend Changes

The backend Lambda code is **inline in the CloudFormation template** (YAML ZipFile). To modify:

1. Edit the Python code in `infra/silvermoat-mvp-s3-website.yaml` (lines 236-355 for `MvpServiceFunction`, lines 481-795 for `SeederFunction`)
2. Redeploy the stack: `./scripts/deploy-stack.sh`
3. CloudFormation will update the Lambda function code

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

1. Locate the `handler` function in the CloudFormation template (line 283)
2. Parse `path` and `method` to add your route
3. Add any required environment variables to `MvpServiceFunction.Environment.Variables`
4. Update IAM permissions in `MvpLambdaRole` if accessing new resources
5. Redeploy: `./scripts/deploy-stack.sh`

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

Without this, API Gateway may not reflect your changes even though CloudFormation shows `UPDATE_COMPLETE`.

### S3 Website Hosting (HTTP Only)

The S3 website endpoint is HTTP, not HTTPS. This is intentional for the MVP to avoid CloudFront complexity. The architecture diagram in README.md shows browser → S3 Website (HTTP) → API Gateway (HTTPS).

### Custom Resource Behavior

- The `SeederFunction` handles both seeding and cleanup using the `Mode` property
- On stack deletion, the cleanup Lambda empties S3 buckets before CloudFormation tries to delete them
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
