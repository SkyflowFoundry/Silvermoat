# A-B Stack Deployment Design

## Goal

Design full A-B stack deployment leveraging GitHub Actions to manage Cloudflare DNS for production traffic routing.

## Overview

**A Stack (Production):**
- Stack name: `silvermoat` (fixed)
- CloudFront enabled (`CreateCloudFront=true`)
- Custom domain via ACM certificate
- Cloudflare DNS points to CloudFront distribution
- Deployed on merge to `main`

**B Stack (Test/Preview):**
- Stack name: `silvermoat-pr-{PR_NUMBER}`
- No CloudFront (`CreateCloudFront=false`)
- S3 website endpoint only (HTTP)
- No DNS configuration (direct S3 URL)
- Deployed on PR open/update
- Cleaned up after PR merge/close

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         GitHub Workflow                          │
└─────────────────────────────────────────────────────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
         PR Event (open/update)          Merge to main
                │                                 │
                ▼                                 ▼
┌───────────────────────────────┐   ┌───────────────────────────────┐
│         B Stack Deploy         │   │         A Stack Deploy         │
│  silvermoat-pr-{PR_NUMBER}    │   │         silvermoat            │
│                                │   │                                │
│  - CloudFront: false           │   │  - CloudFront: true           │
│  - Domain: none                │   │  - Domain: silvermoat.net     │
│  - HTTP S3 website only        │   │  - ACM cert + HTTPS           │
│  - Run E2E tests               │   │  - Update CloudFront          │
│  - Keep until PR closed        │   │  - Update Cloudflare DNS      │
└───────────────────────────────┘   └───────────────────────────────┘
                                                 │
                                                 ▼
                                  ┌──────────────────────────┐
                                  │  Cloudflare DNS Update   │
                                  │  (GitHub Action)         │
                                  │                          │
                                  │  CNAME: silvermoat.net   │
                                  │  → d123.cloudfront.net   │
                                  └──────────────────────────┘
```

## Deployment Workflows

### 1. B Stack Deployment (PR Testing)

**Trigger:** PR opened/updated against `main`

**Workflow:** `.github/workflows/pr-stack-deploy.yml`

**Steps:**
1. Checkout code at PR HEAD
2. Set stack name: `silvermoat-pr-{PR_NUMBER}`
3. Package Lambda functions to S3
4. Deploy CloudFormation with parameters:
   - `CreateCloudFront=false`
   - `DomainName=""`
   - `UiSeedingMode=external`
   - `StageName=pr-{PR_NUMBER}`
5. Build and deploy React UI to S3
6. Run smoke tests (deployment validation)
7. Run API contract tests
8. Run E2E tests (Selenium/Playwright)
9. Post test results to PR comment
10. **Keep stack running** (no cleanup)

**On PR close/merge:**
- Trigger cleanup workflow
- Delete B stack (runs cleanup Lambda)

**Outputs:**
- S3 website URL (HTTP): `http://silvermoat-pr-123-uibucket-xyz.s3-website-us-east-1.amazonaws.com`
- API Gateway URL: `https://abc123.execute-api.us-east-1.amazonaws.com/pr-123`

### 2. A Stack Deployment (Production)

**Trigger:** Push to `main` (PR merged)

**Workflow:** `.github/workflows/deploy-production.yml`

**Steps:**
1. Checkout code at `main` HEAD
2. Set stack name: `silvermoat` (fixed)
3. Package Lambda functions to S3
4. Deploy CloudFormation with parameters:
   - `CreateCloudFront=true`
   - `DomainName=silvermoat.net`
   - `UiSeedingMode=external`
   - `StageName=prod`
5. Wait for CloudFormation completion
   - If ACM cert validation pending, wait (up to 30min)
   - Stack waits for DNS validation CNAME in Cloudflare
6. Build and deploy React UI to S3
7. Get CloudFront distribution domain from stack outputs
8. **Update Cloudflare DNS** (see below)
9. Invalidate CloudFront cache for UI changes
10. Run production smoke tests
11. Post deployment summary to commit status

**Outputs:**
- CloudFront URL: `https://d123abc.cloudfront.net`
- Custom domain URL: `https://silvermoat.net`
- API Gateway URL: `https://xyz789.execute-api.us-east-1.amazonaws.com/prod`

## Cloudflare DNS Management

### Approach: GitHub Actions + Cloudflare API

**Required Secrets:**
- `CLOUDFLARE_API_TOKEN` - Scoped token with `Zone:DNS:Edit` permission
- `CLOUDFLARE_ZONE_ID` - Zone ID for `silvermoat.net`

**DNS Records to Manage:**

1. **ACM Certificate Validation** (one-time, manual)
   - Type: CNAME
   - Name: `_validation-subdomain.silvermoat.net`
   - Value: `_validation-target.acm-validations.aws.`
   - TTL: 300 (5 min)
   - Proxy: **Disabled** (gray cloud)
   - **Action:** Manual setup before first deployment
   - **Reason:** Validation records are stable and don't change

2. **CloudFront Alias** (automated)
   - Type: CNAME
   - Name: `silvermoat.net` (or `@` for apex)
   - Value: `d123abc.cloudfront.net` (from stack outputs)
   - TTL: 300 (5 min)
   - Proxy: **Disabled** (gray cloud)
   - **Action:** Update via GitHub Action on A stack deploy

### Cloudflare DNS Update Action

**Step in `deploy-production.yml`:**

```yaml
- name: Update Cloudflare DNS
  env:
    CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    CLOUDFLARE_ZONE_ID: ${{ secrets.CLOUDFLARE_ZONE_ID }}
  run: |
    # Get CloudFront domain from stack outputs
    CF_DOMAIN=$(aws cloudformation describe-stacks \
      --stack-name silvermoat \
      --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontDomain`].OutputValue' \
      --output text)

    echo "CloudFront domain: $CF_DOMAIN"

    # Update CNAME record via Cloudflare API
    ./scripts/update-cloudflare-dns.sh \
      --zone-id "$CLOUDFLARE_ZONE_ID" \
      --record-name "silvermoat.net" \
      --target "$CF_DOMAIN"
```

**Script: `scripts/update-cloudflare-dns.sh`**

```bash
#!/bin/bash
# Update Cloudflare DNS CNAME record

set -e

ZONE_ID=""
RECORD_NAME=""
TARGET=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --zone-id) ZONE_ID="$2"; shift 2 ;;
    --record-name) RECORD_NAME="$2"; shift 2 ;;
    --target) TARGET="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$CLOUDFLARE_API_TOKEN" ] || [ -z "$ZONE_ID" ] || [ -z "$RECORD_NAME" ] || [ -z "$TARGET" ]; then
  echo "Error: Missing required arguments or CLOUDFLARE_API_TOKEN"
  exit 1
fi

echo "Updating DNS record: $RECORD_NAME -> $TARGET"

# List existing DNS records for the name
RECORD_ID=$(curl -s -X GET \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?name=$RECORD_NAME&type=CNAME" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" | jq -r '.result[0].id // empty')

if [ -z "$RECORD_ID" ]; then
  echo "Record not found, creating new CNAME..."

  # Create new CNAME record
  curl -s -X POST \
    "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data "{
      \"type\": \"CNAME\",
      \"name\": \"$RECORD_NAME\",
      \"content\": \"$TARGET\",
      \"ttl\": 300,
      \"proxied\": false
    }" | jq '.'
else
  echo "Record found (ID: $RECORD_ID), updating..."

  # Update existing CNAME record
  curl -s -X PUT \
    "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data "{
      \"type\": \"CNAME\",
      \"name\": \"$RECORD_NAME\",
      \"content\": \"$TARGET\",
      \"ttl\": 300,
      \"proxied\": false
    }" | jq '.'
fi

echo "DNS update complete"
```

### DNS Validation Wait Strategy

**Problem:** ACM certificate validation requires DNS CNAME before stack completes.

**Solution:** Two-phase deployment for initial setup

**Phase 1: Initial A Stack Deployment (Manual DNS)**
1. Deploy A stack (will pause waiting for cert validation)
2. CloudFormation creates ACM certificate resource
3. Get validation CNAME from ACM console or CLI:
   ```bash
   aws acm describe-certificate \
     --certificate-arn <arn> \
     --query 'Certificate.DomainValidationOptions[0].ResourceRecord'
   ```
4. Manually add validation CNAME to Cloudflare (one-time)
5. Wait for cert validation (~5-15 min)
6. Stack completes, outputs CloudFront domain
7. Manually add CloudFront CNAME to Cloudflare (or run DNS update script)

**Phase 2: Subsequent A Stack Deployments (Automated)**
1. ACM cert already validated, CloudFormation reuses it
2. Stack updates CloudFront distribution (if needed)
3. GitHub Action reads CloudFront domain from outputs
4. GitHub Action updates Cloudflare CNAME automatically
5. No manual intervention needed

## Stack Parameter Matrix

| Parameter          | B Stack (PR)              | A Stack (Prod)       |
|--------------------|---------------------------|----------------------|
| `AppName`          | `silvermoat-pr`           | `silvermoat`         |
| `StageName`        | `pr-{PR_NUMBER}`          | `prod`               |
| `CreateCloudFront` | `false`                   | `true`               |
| `DomainName`       | `""`                      | `silvermoat.net`     |
| `UiSeedingMode`    | `external`                | `external`           |
| Stack Name         | `silvermoat-pr-{PR_NUM}`  | `silvermoat`         |

## Workflow Files

### `.github/workflows/pr-stack-deploy.yml`

```yaml
name: PR Stack Deploy and Test

on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

permissions:
  id-token: write
  contents: read
  pull-requests: write

jobs:
  deploy-and-test:
    runs-on: ubuntu-latest
    timeout-minutes: 45

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: ui/package-lock.json

      - name: Install test dependencies
        run: pip install -r requirements-test.txt

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Set stack name
        id: stack-name
        run: |
          STACK_NAME="silvermoat-pr-${{ github.event.pull_request.number }}"
          echo "stack_name=${STACK_NAME}" >> $GITHUB_OUTPUT
          echo "PR stack name: ${STACK_NAME}"

      - name: Deploy B stack
        env:
          STACK_NAME: ${{ steps.stack-name.outputs.stack_name }}
          APP_NAME: silvermoat-pr
          STAGE_NAME: pr-${{ github.event.pull_request.number }}
          UI_SEEDING_MODE: external
          CREATE_CLOUDFRONT: false
          DOMAIN_NAME: ""
        run: ./scripts/deploy-stack.sh

      - name: Wait for stack deployment
        run: |
          aws cloudformation wait stack-create-complete \
            --stack-name ${{ steps.stack-name.outputs.stack_name }} || \
          aws cloudformation wait stack-update-complete \
            --stack-name ${{ steps.stack-name.outputs.stack_name }}

      - name: Build and deploy UI
        env:
          STACK_NAME: ${{ steps.stack-name.outputs.stack_name }}
        run: ./scripts/deploy-ui.sh

      - name: Get stack outputs
        id: outputs
        run: |
          STACK_NAME="${{ steps.stack-name.outputs.stack_name }}"
          OUTPUTS=$(aws cloudformation describe-stacks \
            --stack-name "${STACK_NAME}" \
            --query 'Stacks[0].Outputs' --output json)

          API_URL=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="ApiBaseUrl") | .OutputValue')
          WEB_URL=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="WebUrl") | .OutputValue')

          echo "api_url=${API_URL}" >> $GITHUB_OUTPUT
          echo "web_url=${WEB_URL}" >> $GITHUB_OUTPUT

      - name: Install Chrome
        uses: browser-actions/setup-chrome@v1

      - name: Run smoke tests
        env:
          STACK_NAME: ${{ steps.stack-name.outputs.stack_name }}
        run: |
          cd tests/smoke
          pytest -v -m smoke --tb=short

      - name: Run API tests
        env:
          SILVERMOAT_API_URL: ${{ steps.outputs.outputs.api_url }}
        run: |
          cd tests/api
          pytest -v -m api --tb=short

      - name: Run E2E tests
        env:
          SILVERMOAT_URL: ${{ steps.outputs.outputs.web_url }}
          SILVERMOAT_API_URL: ${{ steps.outputs.outputs.api_url }}
          HEADLESS: '1'
        run: |
          cd tests/e2e
          pytest -v -m smoke --tb=short

      - name: Post results to PR
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const prNumber = context.payload.pull_request.number;
            const stackName = '${{ steps.stack-name.outputs.stack_name }}';
            const webUrl = '${{ steps.outputs.outputs.web_url }}';
            const apiUrl = '${{ steps.outputs.outputs.api_url }}';
            const runUrl = `${context.serverUrl}/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}`;

            const body = `## 🚀 PR Stack Deployed

            **Stack:** \`${stackName}\`
            **Web URL:** ${webUrl}
            **API URL:** ${apiUrl}

            Tests completed. [View logs](${runUrl})

            Stack will remain active until PR is closed/merged.
            `;

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: prNumber,
              body: body
            });
```

### `.github/workflows/pr-stack-cleanup.yml`

```yaml
name: PR Stack Cleanup

on:
  pull_request:
    types: [closed]

permissions:
  id-token: write
  contents: read

jobs:
  cleanup:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Delete PR stack
        run: |
          STACK_NAME="silvermoat-pr-${{ github.event.pull_request.number }}"
          echo "Deleting stack: ${STACK_NAME}"

          chmod +x scripts/delete-stack.sh
          STACK_NAME="${STACK_NAME}" ./scripts/delete-stack.sh --yes || echo "Stack may not exist"

      - name: Wait for deletion
        run: |
          STACK_NAME="silvermoat-pr-${{ github.event.pull_request.number }}"
          aws cloudformation wait stack-delete-complete \
            --stack-name "${STACK_NAME}" || echo "Stack deletion may still be in progress"
```

### `.github/workflows/deploy-production.yml`

```yaml
name: Deploy Production (A Stack)

on:
  push:
    branches: [main]

permissions:
  id-token: write
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 60

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: ui/package-lock.json

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Deploy A stack
        env:
          STACK_NAME: silvermoat
          APP_NAME: silvermoat
          STAGE_NAME: prod
          UI_SEEDING_MODE: external
          CREATE_CLOUDFRONT: true
          DOMAIN_NAME: silvermoat.net
        run: |
          echo "Deploying production stack..."
          chmod +x scripts/deploy-stack.sh
          ./scripts/deploy-stack.sh

      - name: Wait for stack deployment
        run: |
          echo "Waiting for stack deployment (may take up to 30min for ACM cert validation)..."
          aws cloudformation wait stack-create-complete \
            --stack-name silvermoat || \
          aws cloudformation wait stack-update-complete \
            --stack-name silvermoat

      - name: Build and deploy UI
        env:
          STACK_NAME: silvermoat
        run: |
          chmod +x scripts/deploy-ui.sh
          ./scripts/deploy-ui.sh

      - name: Get stack outputs
        id: outputs
        run: |
          OUTPUTS=$(aws cloudformation describe-stacks \
            --stack-name silvermoat \
            --query 'Stacks[0].Outputs' --output json)

          CF_DOMAIN=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="CloudFrontDomain") | .OutputValue')
          CF_URL=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="CloudFrontUrl") | .OutputValue')
          CUSTOM_URL=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="CustomDomainUrl") | .OutputValue')
          API_URL=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="ApiBaseUrl") | .OutputValue')

          echo "cloudfront_domain=${CF_DOMAIN}" >> $GITHUB_OUTPUT
          echo "cloudfront_url=${CF_URL}" >> $GITHUB_OUTPUT
          echo "custom_url=${CUSTOM_URL}" >> $GITHUB_OUTPUT
          echo "api_url=${API_URL}" >> $GITHUB_OUTPUT

      - name: Update Cloudflare DNS
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          CLOUDFLARE_ZONE_ID: ${{ secrets.CLOUDFLARE_ZONE_ID }}
        run: |
          echo "Updating Cloudflare DNS..."
          chmod +x scripts/update-cloudflare-dns.sh
          ./scripts/update-cloudflare-dns.sh \
            --zone-id "$CLOUDFLARE_ZONE_ID" \
            --record-name "silvermoat.net" \
            --target "${{ steps.outputs.outputs.cloudfront_domain }}"

      - name: Invalidate CloudFront cache
        run: |
          DISTRIBUTION_ID=$(aws cloudformation describe-stacks \
            --stack-name silvermoat \
            --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontDomain`].OutputValue' \
            --output text | cut -d'.' -f1)

          if [ -n "$DISTRIBUTION_ID" ]; then
            echo "Creating CloudFront invalidation..."
            aws cloudfront create-invalidation \
              --distribution-id "$DISTRIBUTION_ID" \
              --paths "/*"
          fi

      - name: Run production smoke tests
        env:
          SILVERMOAT_API_URL: ${{ steps.outputs.outputs.api_url }}
        run: |
          echo "Running production smoke tests..."
          pip install -r requirements-test.txt
          cd tests/smoke
          pytest -v -m smoke --tb=short

      - name: Post deployment summary
        run: |
          echo "✅ Production deployment complete!"
          echo "CloudFront URL: ${{ steps.outputs.outputs.cloudfront_url }}"
          echo "Custom Domain: ${{ steps.outputs.outputs.custom_url }}"
          echo "API URL: ${{ steps.outputs.outputs.api_url }}"
```

## Implementation Phases

### Phase 1: B Stack Enhancement (Current E2E workflow)
- [x] Already implemented in `.github/workflows/e2e-tests.yml`
- [x] Deploys ephemeral stacks for PRs
- [x] Runs full test suite
- [ ] **Update:** Keep stack running until PR closed (remove cleanup step)
- [ ] **Add:** PR cleanup workflow (`.github/workflows/pr-stack-cleanup.yml`)

### Phase 2: A Stack Automation
- [ ] Create `.github/workflows/deploy-production.yml`
- [ ] Set up AWS OIDC role for GitHub Actions (if not exists)
- [ ] Configure GitHub secrets:
  - `AWS_ROLE_ARN`
  - `CLOUDFLARE_API_TOKEN`
  - `CLOUDFLARE_ZONE_ID`
- [ ] Test A stack deployment to staging first

### Phase 3: Cloudflare DNS Integration
- [ ] Create `scripts/update-cloudflare-dns.sh`
- [ ] Manually configure ACM validation CNAME (one-time)
- [ ] Integrate DNS update into production workflow
- [ ] Test DNS update script in isolation
- [ ] Verify CloudFront alias points to correct distribution

### Phase 4: Testing and Validation
- [ ] Test PR workflow: open PR, verify B stack deploys
- [ ] Verify B stack stays running (no auto-cleanup)
- [ ] Close PR, verify cleanup workflow triggers
- [ ] Test production workflow: merge PR to main
- [ ] Verify A stack updates correctly
- [ ] Verify Cloudflare DNS updates
- [ ] Verify `silvermoat.net` resolves to CloudFront

## Secrets Configuration

**GitHub Repository Secrets:**

1. `AWS_ROLE_ARN`
   - IAM role ARN for OIDC authentication
   - Must have permissions: CloudFormation, S3, Lambda, DynamoDB, API Gateway, CloudFront, ACM
   - Example: `arn:aws:iam::123456789012:role/GitHubActionsRole`

2. `CLOUDFLARE_API_TOKEN`
   - Cloudflare API token with `Zone:DNS:Edit` permission
   - Create at: https://dash.cloudflare.com/profile/api-tokens
   - Template: "Edit zone DNS"
   - Zone resources: Include → Specific zone → `silvermoat.net`

3. `CLOUDFLARE_ZONE_ID`
   - Zone ID for `silvermoat.net`
   - Find at: Cloudflare dashboard → Overview → Zone ID
   - Example: `abc123def456ghi789jkl012mno345pq`

## Rollback Strategy

**B Stack (PR):**
- No rollback needed
- Close PR → delete stack
- Or push fixes to PR branch → stack updates

**A Stack (Production):**

**Option 1: Git revert + redeploy**
```bash
git revert <bad-commit>
git push origin main
# GitHub Action deploys previous version
```

**Option 2: Manual CloudFormation rollback**
```bash
aws cloudformation rollback-stack --stack-name silvermoat
```

**Option 3: Emergency DNS switch (last resort)**
- Manually update Cloudflare CNAME to point to known-good CloudFront distribution
- Or point to S3 website URL temporarily (HTTP only)

## Monitoring and Alerts

**Recommended additions (future):**

1. **Stack deployment alerts**
   - CloudWatch alarms on CloudFormation stack failures
   - SNS topic → email/Slack on deployment failures

2. **DNS propagation checks**
   - Post-deployment: verify `dig silvermoat.net` resolves correctly
   - Check from multiple regions (US, EU, APAC)

3. **CloudFront health checks**
   - Synthetic monitoring on `https://silvermoat.net`
   - Alert if site becomes unreachable after deployment

4. **Cost monitoring**
   - CloudWatch billing alarms
   - Alert if B stacks accumulate (forgotten PR cleanup)

## Open Questions

1. **Multi-region ACM cert?**
   - Current design: us-east-1 only (required for CloudFront)
   - Future: Multi-region failover?

2. **B stack retention policy?**
   - Current: Keep until PR closed
   - Alternative: Auto-delete after 7 days of inactivity?

3. **DNS TTL strategy?**
   - Current: 300s (5 min)
   - Production: Lower to 60s for faster rollback?

4. **CloudFront cache invalidation cost?**
   - Current: Invalidate entire distribution (`/*`)
   - Optimization: Invalidate only changed assets?

5. **Blue-green deployments?**
   - Current: In-place A stack updates
   - Future: Deploy A2 stack, switch DNS, delete A1?

## Summary

This design provides:
- ✅ Full A-B deployment with isolated test stacks
- ✅ Automated Cloudflare DNS management via GitHub Actions
- ✅ CloudFront for production (A stack)
- ✅ HTTP-only S3 for testing (B stack)
- ✅ No manual DNS updates after initial ACM setup
- ✅ Clean separation of concerns (infra in code, DNS via API)
- ✅ Existing E2E workflow easily adapted for B stack persistence

**Critical path:** Phase 3 (DNS integration) requires manual ACM validation setup before first production deployment.
