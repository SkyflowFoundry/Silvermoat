# A-B Stack Deployment Design

## Overview

This document describes the A-B deployment model for Silvermoat, enabling safe PR-based testing (B stack) and automated production deployments (A stack) with intelligent Cloudflare DNS management.

## Architecture

### B Stack (PR Testing Environment)

**Purpose**: Ephemeral testing environment for pull requests

**Characteristics**:
- **Stack Name**: `silvermoat-pr-{PR_NUMBER}`
- **CloudFront**: None (HTTP S3 website only)
- **Custom Domain**: None
- **Lifecycle**: Created on PR open/update, deleted on PR close
- **Testing**: Full E2E test suite runs automatically
- **Access**: Via S3 website URL only (HTTP)

**Benefits**:
- Fast deployment (no CloudFront distribution creation)
- No DNS changes required
- Full isolated testing per PR
- Cost-effective (no CloudFront charges)
- Automatic cleanup

### A Stack (Production Environment)

**Purpose**: Live production environment

**Characteristics**:
- **Stack Name**: `silvermoat` (fixed)
- **CloudFront**: Full distribution with ACM certificate
- **Custom Domain**: `silvermoat.net` (or configured domain)
- **Lifecycle**: Persistent, updated on merge to main
- **Testing**: Smoke tests + CloudFront cache invalidation
- **Access**: Via CloudFront (HTTPS) + custom domain

**Benefits**:
- HTTPS with custom domain
- Global CDN caching
- Production-grade security
- Automated DNS updates only when needed

## Deployment Workflows

### 1. PR Stack Deploy (B Stack)

**Trigger**: PR opened or updated (push to PR branch)

**Workflow File**: `.github/workflows/pr-stack-deploy.yml`

**Steps**:
1. Checkout code
2. Configure AWS credentials
3. Package Lambda functions
4. Deploy CloudFormation stack:
   - Name: `silvermoat-pr-{PR_NUMBER}`
   - Parameters: `UiSeedingMode=external`, `DomainName=""` (no CloudFront)
5. Deploy React UI to S3
6. Run E2E test suite against S3 URL
7. Comment on PR with test results and URLs

**Key Points**:
- Stack persists until PR closed (not deleted on each push)
- Subsequent pushes update existing stack
- No CloudFront = faster deployments (~2-3 min vs ~15-20 min)
- Tests run against HTTP S3 website URL

### 2. PR Stack Cleanup (B Stack Deletion)

**Trigger**: PR closed or merged

**Workflow File**: `.github/workflows/pr-stack-cleanup.yml`

**Steps**:
1. Configure AWS credentials
2. Delete CloudFormation stack: `silvermoat-pr-{PR_NUMBER}`
3. Custom Resource handles S3 bucket cleanup automatically

**Key Points**:
- Automatic cleanup (no manual intervention)
- SeederFunction cleanup Lambda empties buckets before deletion
- If deletion fails, check CloudWatch logs: `/aws/lambda/silvermoat-pr-{PR_NUMBER}-SeederFunction-*`

### 3. Production Deploy (A Stack)

**Trigger**: Push to `main` branch (typically after PR merge)

**Workflow File**: `.github/workflows/deploy-production.yml`

**Steps**:
1. Checkout code
2. Configure AWS credentials
3. Package Lambda functions
4. Deploy CloudFormation stack:
   - Name: `silvermoat` (fixed)
   - Parameters: `UiSeedingMode=external`, `DomainName=silvermoat.net`
5. **Smart DNS Update**:
   - Check if CloudFront domain changed
   - Update Cloudflare DNS only if necessary
   - Skip update if CloudFront domain unchanged
6. Invalidate CloudFront cache: `/\*`
7. Deploy React UI to S3
8. Run smoke tests
9. Post deployment notification (optional)

**Key Points**:
- Fixed stack name (not PR-specific)
- CloudFront distribution included
- DNS updates only when CloudFront domain changes (rare)
- Cache invalidation ensures fresh content

## Cloudflare DNS Integration

### Smart DNS Update Strategy

**Script**: `scripts/update-cloudflare-dns.sh`

**How It Works**:
1. Fetch current DNS record from Cloudflare API
2. Fetch target CloudFront domain from CloudFormation outputs
3. Compare current vs target
4. **If identical**: Skip update (most common case)
5. **If different**: Update DNS record

**When DNS Updates Run**:
- ✅ CloudFront distribution recreated (origin/certificate changes)
- ❌ Lambda code updated (no DNS change needed)
- ❌ DynamoDB schema changed (no DNS change needed)
- ❌ S3 bucket content updated (no DNS change needed)

**CloudFront Domain Stability**:
CloudFront domains (e.g., `d111111abcdef8.cloudfront.net`) persist across stack updates. They only change when the distribution is deleted and recreated, which happens rarely (typically only when changing origin or certificate settings).

**Force Update Option**:
Set environment variable to force update regardless of comparison:
```bash
FORCE_UPDATE=true ./scripts/update-cloudflare-dns.sh
```

### Cloudflare API Requirements

**Required Secrets** (configured in GitHub Settings → Secrets):
- `CLOUDFLARE_API_TOKEN`: API token with DNS edit permissions
- `CLOUDFLARE_ZONE_ID`: Zone ID for target domain

**Script Configuration**:
- Domain name: Read from CloudFormation parameter or environment variable
- Record type: CNAME
- Proxied: No (DNS only, gray cloud in Cloudflare UI)
- TTL: Auto

### DNS Record Setup

**Two DNS records required** (one-time manual setup):

1. **ACM Certificate Validation** (one-time):
   - Type: CNAME
   - Name: `_<validation-subdomain>.silvermoat.net`
   - Target: `_<validation-target>.acm-validations.aws.`
   - Proxy: OFF (gray cloud)
   - Purpose: ACM certificate validation

2. **Site Access** (automated by workflow):
   - Type: CNAME
   - Name: `silvermoat.net` (or configured domain)
   - Target: `<cloudfront-distribution>.cloudfront.net`
   - Proxy: OFF (gray cloud)
   - Purpose: Route traffic to CloudFront

**Critical**: Cloudflare proxy must be disabled (DNS only, gray cloud) for both records. Orange cloud (proxied) conflicts with CloudFront's SSL/caching.

## Implementation Phases

### Phase 1: Enhance E2E Workflow for B Stack

**Goal**: Keep PR stacks running, add test suite

**Changes**:
- Modify existing E2E workflow to persist stacks
- Add full test suite (currently only smoke tests)
- Update stack naming to `silvermoat-pr-{PR_NUMBER}`
- Remove stack deletion step (move to cleanup workflow)

**Testing**: Open test PR, verify stack persists after workflow completes

### Phase 2: Create PR Cleanup Workflow

**Goal**: Auto-delete stacks when PRs close

**Changes**:
- Create `.github/workflows/pr-stack-cleanup.yml`
- Trigger on PR close/merge events
- Delete stack by name pattern

**Testing**: Close test PR, verify stack deletion

### Phase 3: Production Deployment Workflow

**Goal**: Deploy A stack on merge to main

**Changes**:
- Create `.github/workflows/deploy-production.yml`
- Fixed stack name: `silvermoat`
- Include CloudFront + custom domain parameters
- Add cache invalidation step
- Add smoke test step

**Testing**: Merge test PR to main, verify production deployment

### Phase 4: Cloudflare DNS Automation

**Goal**: Smart DNS updates only when needed

**Changes**:
- Create `scripts/update-cloudflare-dns.sh`
- Add Cloudflare secrets to GitHub
- Integrate script into production workflow
- Test both update and skip scenarios

**Testing**:
- Deploy with Lambda-only change (should skip DNS)
- Deploy with CloudFront change (should update DNS)

## Rollback Procedures

### Production Rollback Options

**Option 1: Git Revert + Redeploy** (Recommended)
```bash
git revert <commit-sha>
git push origin main
# Production workflow automatically redeploys
```

**Option 2: CloudFormation Stack Rollback**
```bash
aws cloudformation cancel-update-stack --stack-name silvermoat
# Rolls back to previous stable version
```

**Option 3: Emergency DNS Update** (Manual)
```bash
# Point DNS to known-good CloudFront distribution
FORCE_UPDATE=true \
CLOUDFRONT_DOMAIN=<previous-working-domain> \
./scripts/update-cloudflare-dns.sh
```

**Option 4: Previous Deployment**
```bash
# Redeploy specific git tag/commit
git checkout v1.2.3  # or commit SHA
./scripts/deploy-stack.sh
./scripts/deploy-ui.sh
```

### PR Stack Issues

**If B stack deployment fails**:
- Check workflow logs in GitHub Actions
- Check CloudWatch logs: `/aws/lambda/silvermoat-pr-{PR_NUMBER}-*`
- Manual cleanup: `aws cloudformation delete-stack --stack-name silvermoat-pr-{PR_NUMBER}`

**If B stack deletion fails**:
- Check cleanup Lambda logs: `/aws/lambda/silvermoat-pr-{PR_NUMBER}-SeederFunction-*`
- Manual S3 cleanup: `aws s3 rm s3://<bucket-name> --recursive`
- Retry deletion: `aws cloudformation delete-stack --stack-name silvermoat-pr-{PR_NUMBER}`

## Cost Optimization

**B Stack (per PR)**:
- S3 storage: ~$0.023/GB/month
- S3 requests: ~$0.005/1000 requests
- Lambda invocations: ~$0.20/1M requests
- DynamoDB: Pay-per-request (negligible for testing)
- **No CloudFront costs** (major savings)

**A Stack (production)**:
- All B stack costs +
- CloudFront data transfer: ~$0.085/GB (first 10TB)
- CloudFront requests: ~$0.0075/10k requests
- ACM certificate: Free

**Estimated monthly cost** (assuming 5 active PRs):
- B stacks: ~$5-10
- A stack: ~$20-50 (depending on traffic)
- **Total**: ~$25-60/month

## Security Considerations

### GitHub Secrets

Store sensitive credentials securely:
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`: AWS credentials with CloudFormation + S3 + Lambda + DynamoDB permissions
- `CLOUDFLARE_API_TOKEN`: Cloudflare DNS edit permissions (scoped to specific zone)
- `CLOUDFLARE_ZONE_ID`: Non-sensitive but stored for convenience

### IAM Permissions

GitHub Actions runner needs:
- `cloudformation:*` (stack operations)
- `s3:*` (bucket + object operations)
- `lambda:*` (function updates)
- `dynamodb:*` (table operations)
- `apigateway:*` (API operations)
- `iam:*` (role operations for Lambda)
- `cloudfront:*` (distribution + invalidation)
- `acm:*` (certificate operations)

**Best Practice**: Use dedicated IAM user with minimal permissions, not root credentials.

### Cloudflare Token Scoping

Create API token with:
- **Permissions**: Zone → DNS → Edit
- **Zone Resources**: Include → Specific zone (silvermoat.net)
- **IP filtering**: Optional (restrict to GitHub Actions IP ranges)

## Monitoring and Alerts

### CloudWatch Logs

**Lambda Functions**:
- `/aws/lambda/silvermoat-MvpServiceFunction-*` (production API)
- `/aws/lambda/silvermoat-pr-{PR_NUMBER}-MvpServiceFunction-*` (PR API)
- `/aws/lambda/silvermoat-SeederFunction-*` (production seeding/cleanup)
- `/aws/lambda/silvermoat-pr-{PR_NUMBER}-SeederFunction-*` (PR cleanup)

**Key Metrics**:
- Lambda errors (filter: `ERROR`)
- Lambda duration (watch for timeouts)
- DynamoDB throttling
- S3 4xx/5xx errors

### GitHub Actions

**Workflow Status**:
- PR stack deploy: Should complete in ~2-3 minutes
- PR stack cleanup: Should complete in ~1-2 minutes
- Production deploy: Should complete in ~20-25 minutes (including CloudFront)

**Alert on**:
- Repeated deployment failures
- Test failures in PR workflow
- Production deployment failures
- Stack deletion failures

## Future Enhancements

### Potential Improvements

1. **Blue-Green Deployment**:
   - Maintain two A stacks (blue/green)
   - Switch DNS between them for zero-downtime deploys
   - Requires DNS to point to Route53 (not directly to CloudFront)

2. **Canary Deployments**:
   - Route 10% traffic to new version
   - Monitor error rates
   - Gradually increase traffic or rollback

3. **Automated Rollback**:
   - Monitor error rates after deployment
   - Auto-rollback if threshold exceeded
   - Integrate with CloudWatch alarms

4. **Preview Environments per Commit**:
   - Deploy B stack on every commit (not just PR)
   - Useful for rapid iteration
   - Higher cost (more ephemeral stacks)

5. **Cross-Region Replication**:
   - Deploy A stack in multiple regions
   - Route53 latency-based routing
   - Improved global performance

## References

- [AWS CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
- [CloudFront Custom Domain Setup](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/CNAMEs.html)
- [Cloudflare API Documentation](https://developers.cloudflare.com/api/)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [ACM Certificate Validation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html)
