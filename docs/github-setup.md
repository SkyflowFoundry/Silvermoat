# GitHub Setup Guide for A-B Deployment

This guide provides step-by-step instructions for configuring GitHub Actions workflows and secrets to enable A-B stack deployment with automated Cloudflare DNS management.

## Prerequisites

Before proceeding, ensure you have:

1. **AWS Account** with CloudFormation, S3, Lambda, API Gateway, CloudFront, and ACM permissions
2. **Cloudflare Account** with a registered domain (e.g., silvermoat.net)
3. **GitHub Repository** with admin access to configure secrets and workflows

## Part 1: GitHub Secrets Configuration

GitHub Actions workflows require sensitive credentials stored as repository secrets. These secrets are encrypted and only exposed to workflow runs.

### Required Secrets

Navigate to: **Repository Settings → Secrets and variables → Actions → New repository secret**

#### 1. AWS Credentials

**Secret Name**: `AWS_ACCESS_KEY_ID`
**Secret Value**: Your AWS access key ID
**Purpose**: Authenticate GitHub Actions to AWS

**Secret Name**: `AWS_SECRET_ACCESS_KEY`
**Secret Value**: Your AWS secret access key
**Purpose**: Authenticate GitHub Actions to AWS

**How to Create AWS Credentials**:

1. Log into AWS Console
2. Navigate to: **IAM → Users → Add users**
3. User name: `github-actions-silvermoat`
4. Access type: **Programmatic access** (not console)
5. Permissions: Attach existing policies or create custom policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "s3:*",
        "lambda:*",
        "dynamodb:*",
        "apigateway:*",
        "iam:*",
        "cloudfront:*",
        "acm:*",
        "logs:*"
      ],
      "Resource": "*"
    }
  ]
}
```

6. **Important**: Save the access key ID and secret access key (shown only once)
7. Add both values as GitHub secrets

**Security Best Practice**: Use least-privilege IAM permissions. The above policy is broad for simplicity; consider scoping to specific resources in production.

#### 2. Cloudflare Credentials

**Secret Name**: `CLOUDFLARE_API_TOKEN`
**Secret Value**: Your Cloudflare API token (see creation steps below)
**Purpose**: Update DNS records via Cloudflare API

**Secret Name**: `CLOUDFLARE_ZONE_ID`
**Secret Value**: Your Cloudflare zone ID (see retrieval steps below)
**Purpose**: Identify which DNS zone to update

**How to Create Cloudflare API Token**:

1. Log into Cloudflare dashboard
2. Navigate to: **My Profile → API Tokens → Create Token**
3. Template: **Edit zone DNS** (or custom token)
4. Permissions:
   - Zone → DNS → Edit
5. Zone Resources:
   - Include → Specific zone → `silvermoat.net` (your domain)
6. (Optional) IP filtering: Restrict to GitHub Actions IP ranges
7. Click **Continue to summary** → **Create Token**
8. **Important**: Copy the token (shown only once)
9. Add token as GitHub secret: `CLOUDFLARE_API_TOKEN`

**How to Get Cloudflare Zone ID**:

1. Log into Cloudflare dashboard
2. Select your domain (e.g., silvermoat.net)
3. Scroll down in the Overview page
4. Find **Zone ID** in the right sidebar (under API section)
5. Copy the zone ID (format: `abc123def456...`)
6. Add zone ID as GitHub secret: `CLOUDFLARE_ZONE_ID`

**Security Note**: The zone ID is not highly sensitive (it's used in API calls), but storing it as a secret keeps configuration centralized.

### Summary of Required Secrets

After completing the above steps, you should have **4 secrets** configured:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
CLOUDFLARE_API_TOKEN
CLOUDFLARE_ZONE_ID
```

Verify in: **Repository Settings → Secrets and variables → Actions**

## Part 2: GitHub Actions Workflows

GitHub Actions workflows are YAML files stored in `.github/workflows/`. Due to permissions, you'll need to create these files manually.

### Workflow 1: PR Stack Deploy (B Stack)

**Purpose**: Deploy ephemeral testing stack on PR open/update

**File**: `.github/workflows/pr-stack-deploy.yml`

**When to Create**: Immediately (enables PR-based testing)

**Trigger Events**:
- Pull request opened
- Pull request synchronized (new commits pushed)

**Content**:

```yaml
name: Deploy PR Stack (B Stack)

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches:
      - main

env:
  AWS_REGION: us-east-1
  STACK_NAME: silvermoat-pr-${{ github.event.pull_request.number }}

jobs:
  deploy-pr-stack:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Package Lambda functions
        run: ./scripts/package-lambda.sh

      - name: Deploy CloudFormation stack
        run: |
          STACK_NAME="${{ env.STACK_NAME }}" \
          APP_NAME="silvermoat-pr-${{ github.event.pull_request.number }}" \
          STAGE_NAME="pr${{ github.event.pull_request.number }}" \
          UI_SEEDING_MODE="external" \
          DOMAIN_NAME="" \
          ./scripts/deploy-stack.sh

      - name: Install UI dependencies
        working-directory: ui
        run: npm ci

      - name: Deploy UI to S3
        run: STACK_NAME="${{ env.STACK_NAME }}" ./scripts/deploy-ui.sh

      - name: Get stack outputs
        id: outputs
        run: |
          API_URL=$(aws cloudformation describe-stacks \
            --stack-name "${{ env.STACK_NAME }}" \
            --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" \
            --output text)
          UI_URL=$(aws cloudformation describe-stacks \
            --stack-name "${{ env.STACK_NAME }}" \
            --query "Stacks[0].Outputs[?OutputKey=='UiUrl'].OutputValue" \
            --output text)
          echo "api_url=$API_URL" >> $GITHUB_OUTPUT
          echo "ui_url=$UI_URL" >> $GITHUB_OUTPUT

      - name: Run smoke tests
        run: |
          API_BASE_URL="${{ steps.outputs.outputs.api_url }}" \
          ./scripts/smoke-test.sh

      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            const apiUrl = '${{ steps.outputs.outputs.api_url }}';
            const uiUrl = '${{ steps.outputs.outputs.ui_url }}';
            const body = `## PR Stack Deployed ✅

            **Stack Name**: \`${{ env.STACK_NAME }}\`

            **URLs**:
            - UI: ${uiUrl}
            - API: ${apiUrl}

            **Tests**: Smoke tests passed

            Stack will persist until PR is closed.`;

            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: body
            });
```

**Key Points**:
- Stack name includes PR number for isolation
- No CloudFront (fast deployment)
- No custom domain (HTTP S3 only)
- Runs smoke tests automatically
- Posts results as PR comment

### Workflow 2: PR Stack Cleanup

**Purpose**: Delete ephemeral stack when PR closes

**File**: `.github/workflows/pr-stack-cleanup.yml`

**When to Create**: Immediately (prevents orphaned stacks)

**Trigger Events**:
- Pull request closed (merged or not)

**Content**:

```yaml
name: Cleanup PR Stack

on:
  pull_request:
    types: [closed]
    branches:
      - main

env:
  AWS_REGION: us-east-1
  STACK_NAME: silvermoat-pr-${{ github.event.pull_request.number }}

jobs:
  cleanup-pr-stack:
    runs-on: ubuntu-latest

    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Delete CloudFormation stack
        run: |
          echo "Deleting stack: ${{ env.STACK_NAME }}"
          aws cloudformation delete-stack --stack-name "${{ env.STACK_NAME }}"

          echo "Waiting for stack deletion to complete..."
          aws cloudformation wait stack-delete-complete \
            --stack-name "${{ env.STACK_NAME }}" \
            || echo "Stack deletion completed (or stack not found)"

      - name: Verify deletion
        run: |
          STATUS=$(aws cloudformation describe-stacks \
            --stack-name "${{ env.STACK_NAME }}" \
            --query "Stacks[0].StackStatus" \
            --output text 2>/dev/null || echo "DELETED")

          if [ "$STATUS" == "DELETED" ] || [ "$STATUS" == "DELETE_COMPLETE" ]; then
            echo "✓ Stack successfully deleted"
          else
            echo "✗ Stack deletion failed or in progress: $STATUS"
            exit 1
          fi
```

**Key Points**:
- Automatically deletes stack when PR closes
- Waits for deletion to complete
- SeederFunction Lambda handles S3 bucket cleanup
- Fails workflow if deletion unsuccessful

### Workflow 3: Production Deploy (A Stack)

**Purpose**: Deploy production stack with CloudFront + DNS on merge to main

**File**: `.github/workflows/deploy-production.yml`

**When to Create**: After testing B stack workflows (Phase 3)

**Trigger Events**:
- Push to main branch (typically after PR merge)

**Content**:

```yaml
name: Deploy Production (A Stack)

on:
  push:
    branches:
      - main

env:
  AWS_REGION: us-east-1
  STACK_NAME: silvermoat
  DOMAIN_NAME: silvermoat.net

jobs:
  deploy-production:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Package Lambda functions
        run: ./scripts/package-lambda.sh

      - name: Deploy CloudFormation stack
        run: |
          STACK_NAME="${{ env.STACK_NAME }}" \
          APP_NAME="silvermoat" \
          STAGE_NAME="prod" \
          UI_SEEDING_MODE="external" \
          DOMAIN_NAME="${{ env.DOMAIN_NAME }}" \
          ./scripts/deploy-stack.sh

      - name: Smart Cloudflare DNS update
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          CLOUDFLARE_ZONE_ID: ${{ secrets.CLOUDFLARE_ZONE_ID }}
          STACK_NAME: ${{ env.STACK_NAME }}
          DOMAIN_NAME: ${{ env.DOMAIN_NAME }}
        run: ./scripts/update-cloudflare-dns.sh

      - name: Get CloudFront distribution ID
        id: cloudfront
        run: |
          DISTRIBUTION_ID=$(aws cloudformation describe-stacks \
            --stack-name "${{ env.STACK_NAME }}" \
            --query "Stacks[0].Outputs[?OutputKey=='CloudFrontDistributionId'].OutputValue" \
            --output text)
          echo "distribution_id=$DISTRIBUTION_ID" >> $GITHUB_OUTPUT

      - name: Invalidate CloudFront cache
        run: |
          aws cloudfront create-invalidation \
            --distribution-id "${{ steps.cloudfront.outputs.distribution_id }}" \
            --paths "/*"

      - name: Install UI dependencies
        working-directory: ui
        run: npm ci

      - name: Deploy UI to S3
        run: STACK_NAME="${{ env.STACK_NAME }}" ./scripts/deploy-ui.sh

      - name: Get production URLs
        id: outputs
        run: |
          API_URL=$(aws cloudformation describe-stacks \
            --stack-name "${{ env.STACK_NAME }}" \
            --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" \
            --output text)
          CLOUDFRONT_URL=$(aws cloudformation describe-stacks \
            --stack-name "${{ env.STACK_NAME }}" \
            --query "Stacks[0].Outputs[?OutputKey=='CloudFrontUrl'].OutputValue" \
            --output text)
          echo "api_url=$API_URL" >> $GITHUB_OUTPUT
          echo "cloudfront_url=$CLOUDFRONT_URL" >> $GITHUB_OUTPUT

      - name: Run smoke tests
        run: |
          API_BASE_URL="${{ steps.outputs.outputs.api_url }}" \
          ./scripts/smoke-test.sh

      - name: Deployment summary
        run: |
          echo "✓ Production deployment complete"
          echo "  API: ${{ steps.outputs.outputs.api_url }}"
          echo "  CloudFront: ${{ steps.outputs.outputs.cloudfront_url }}"
          echo "  Custom Domain: https://${{ env.DOMAIN_NAME }}"
```

**Key Points**:
- Fixed stack name (not PR-specific)
- Includes CloudFront distribution
- Smart DNS update (skips if CloudFront domain unchanged)
- Invalidates CloudFront cache after UI deployment
- Runs smoke tests against production

## Part 3: Cloudflare DNS Setup

Before running production workflow, configure DNS records in Cloudflare.

### Required DNS Records

**Record 1: ACM Certificate Validation** (One-time, manual setup)

This record validates the SSL certificate. CloudFormation creates the cert, but you must add the validation CNAME to Cloudflare.

1. Deploy stack once (workflow will create ACM certificate request)
2. Get validation details from AWS Console:
   - Navigate to: **Certificate Manager → Certificates**
   - Find certificate for `silvermoat.net`
   - Copy CNAME name and value from validation section
3. Add CNAME to Cloudflare:
   - Type: `CNAME`
   - Name: `_<validation-subdomain>` (e.g., `_abc123.silvermoat.net`)
   - Target: `_<validation-value>.acm-validations.aws.`
   - Proxy status: **DNS only** (gray cloud, not orange)
   - TTL: Auto
4. Wait 5-15 minutes for validation to complete
5. Subsequent deployments reuse validated certificate

**Record 2: Site Access** (Automated by workflow)

This record points your domain to CloudFront. The workflow's DNS update script manages this automatically.

- Type: `CNAME`
- Name: `silvermoat.net` (root domain or subdomain)
- Target: `<cloudfront-distribution>.cloudfront.net` (updated by workflow)
- Proxy status: **DNS only** (gray cloud, not orange)
- TTL: Auto

**Critical**: Cloudflare proxy must be **disabled** (gray cloud) for both records. Orange cloud (proxied) conflicts with CloudFront's SSL/caching.

### Verifying DNS Configuration

After workflow runs:

1. Check workflow logs for DNS update confirmation
2. Verify DNS record in Cloudflare dashboard:
   - Should point to CloudFront domain (e.g., `d111111abcdef8.cloudfront.net`)
3. Test access:
   - `curl -I https://silvermoat.net` (should return 200 OK)
   - Browser: `https://silvermoat.net` (should load UI)

## Part 4: Testing the Workflows

### Testing B Stack (PR Workflow)

1. Create test branch: `git checkout -b test-ab-deployment`
2. Make small change (e.g., update README)
3. Push branch: `git push origin test-ab-deployment`
4. Open PR against main
5. Observe workflow in Actions tab:
   - **Deploy PR Stack** should trigger
   - Check logs for deployment progress
   - Verify PR comment with stack URLs
6. Visit UI URL (HTTP S3 website)
7. Close PR to trigger cleanup workflow
8. Verify stack deletion in AWS Console

### Testing A Stack (Production Workflow)

1. Merge PR to main (or push directly to main)
2. Observe workflow in Actions tab:
   - **Deploy Production** should trigger
   - Check logs for:
     - Stack deployment
     - DNS update (or skip message)
     - Cache invalidation
     - UI deployment
3. Visit production URLs:
   - CloudFront default: `https://<distribution>.cloudfront.net`
   - Custom domain: `https://silvermoat.net`
4. Verify smoke tests passed in workflow logs

## Part 5: Troubleshooting

### Common Issues

**Issue**: `AWS credentials not configured`
**Solution**: Verify `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` secrets are set correctly

**Issue**: `Cloudflare API error: Invalid request`
**Solution**: Verify `CLOUDFLARE_API_TOKEN` has DNS edit permissions and `CLOUDFLARE_ZONE_ID` is correct

**Issue**: `Stack deployment failed: Certificate not validated`
**Solution**: Add ACM validation CNAME to Cloudflare (see Part 3, Record 1)

**Issue**: `DNS update skipped, but domain not accessible`
**Solution**: Manually verify Cloudflare CNAME points to correct CloudFront domain. Force update: add `FORCE_UPDATE=true` to workflow env

**Issue**: `PR stack not deleted`
**Solution**: Check cleanup workflow logs. Manual deletion: `aws cloudformation delete-stack --stack-name silvermoat-pr-{PR_NUMBER}`

**Issue**: `CloudFront returns 403 Forbidden`
**Solution**: S3 bucket policy may be incorrect. Verify bucket policy allows CloudFront access.

### Monitoring

**GitHub Actions**: Check workflow run history in Actions tab
**AWS CloudFormation**: Monitor stack events in AWS Console
**AWS CloudWatch**: Check Lambda logs for runtime errors
**Cloudflare**: Verify DNS records in dashboard

## Part 6: Next Steps

After completing this setup:

1. ✅ GitHub secrets configured
2. ✅ Three workflows created
3. ✅ Cloudflare DNS records configured
4. ✅ Workflows tested (PR + production)

**Recommended enhancements**:
- Add Slack/email notifications for deployment status
- Configure CloudWatch alarms for production errors
- Implement automated rollback on test failures
- Add E2E test suite (beyond smoke tests)

## Summary Checklist

Use this checklist to verify complete setup:

- [ ] AWS IAM user created with CloudFormation/S3/Lambda permissions
- [ ] `AWS_ACCESS_KEY_ID` secret added to GitHub
- [ ] `AWS_SECRET_ACCESS_KEY` secret added to GitHub
- [ ] Cloudflare API token created with DNS edit permissions
- [ ] `CLOUDFLARE_API_TOKEN` secret added to GitHub
- [ ] `CLOUDFLARE_ZONE_ID` secret added to GitHub
- [ ] `.github/workflows/pr-stack-deploy.yml` created
- [ ] `.github/workflows/pr-stack-cleanup.yml` created
- [ ] `.github/workflows/deploy-production.yml` created
- [ ] ACM validation CNAME added to Cloudflare (manual, one-time)
- [ ] Site access CNAME configured in Cloudflare (automated by workflow)
- [ ] Cloudflare proxy disabled (gray cloud) for both records
- [ ] Test PR created and B stack deployed successfully
- [ ] Test PR closed and B stack cleaned up successfully
- [ ] Production deployment tested (merge to main)
- [ ] Custom domain accessible via HTTPS

**Total Setup Time**: ~30-60 minutes (including certificate validation wait)

## Reference Links

- [GitHub Actions Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Cloudflare API Token Guide](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
- [ACM Certificate Validation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html)
- [CloudFront Custom Domains](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/CNAMEs.html)
