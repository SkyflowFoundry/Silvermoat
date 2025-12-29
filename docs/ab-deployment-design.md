# A-B Stack Deployment Design

Comprehensive deployment strategy for Silvermoat with ephemeral test stacks (B) and production stack (A).

## Overview

**B Stack (PR Testing):**
- Ephemeral test environments per PR
- HTTP-only S3 website (no CloudFront)
- Full E2E test suite
- Automatic cleanup on PR close

**A Stack (Production):**
- Single production environment
- CloudFront + ACM certificate + custom domain
- Smart Cloudflare DNS updates (only when needed)
- Deployed on merge to main

## Architecture

### B Stack (Test Environment)

**Stack Name:** `silvermoat-pr-{PR_NUMBER}`

**Configuration:**
```bash
CREATE_CLOUDFRONT=false
DOMAIN_NAME=""
UI_SEEDING_MODE=external
```

**Infrastructure:**
- ✅ S3 website bucket (HTTP endpoint)
- ✅ API Gateway + Lambda
- ✅ DynamoDB tables
- ✅ S3 docs bucket
- ❌ CloudFront distribution
- ❌ ACM certificate
- ❌ Custom domain

**Access:** `http://{bucket-name}.s3-website-{region}.amazonaws.com`

**Lifecycle:**
1. Created/updated on PR open/update
2. E2E tests run against HTTP endpoint
3. Deleted automatically on PR close

### A Stack (Production Environment)

**Stack Name:** `silvermoat` (fixed)

**Configuration:**
```bash
CREATE_CLOUDFRONT=true
DOMAIN_NAME=silvermoat.net
UI_SEEDING_MODE=external
```

**Infrastructure:**
- ✅ S3 website bucket (origin)
- ✅ CloudFront distribution (HTTPS)
- ✅ ACM certificate (DNS validation)
- ✅ Custom domain (silvermoat.net)
- ✅ API Gateway + Lambda
- ✅ DynamoDB tables
- ✅ S3 docs bucket

**Access:**
- Primary: `https://silvermoat.net` (via Cloudflare DNS → CloudFront)
- Fallback: `https://{distribution-id}.cloudfront.net`

**Deployment Triggers:**
- Merge to `main` branch
- Manual workflow dispatch

## Smart DNS Updates

### Problem

CloudFront domain (`d111111abcdef8.cloudfront.net`) is stable and persistent. It only changes when the CloudFront distribution is deleted and recreated—which happens rarely in CloudFormation (only when immutable properties change).

Most deployments (Lambda updates, S3 content, DynamoDB changes, cache behavior tweaks) don't recreate CloudFront, so DNS doesn't need updating.

### Solution

**Conditional DNS Update Logic:**

1. **Fetch current DNS:** Query Cloudflare API for existing CNAME record
2. **Fetch CloudFront domain:** Get from CloudFormation stack outputs
3. **Compare:** If current DNS target ≠ CloudFront domain → update
4. **Skip:** If they match → skip update (fast deployment)

**Script:** `scripts/update-cloudflare-dns.sh`

**Behavior:**
```bash
# Standard call (checks first, only updates if needed)
./scripts/update-cloudflare-dns.sh

# Force update even if unchanged
FORCE_UPDATE=true ./scripts/update-cloudflare-dns.sh
```

**Output Examples:**

```
# When DNS matches (most deployments)
✓ DNS already points to correct CloudFront domain
  Current: d111111abcdef8.cloudfront.net
  Target:  d111111abcdef8.cloudfront.net

No DNS update needed. Skipping.
```

```
# When DNS needs updating (rare)
DNS target mismatch detected:
  Current: d111111abcdef8.cloudfront.net
  Target:  d222222abcdef9.cloudfront.net

Updating existing CNAME record...
✓ DNS record updated successfully
```

### When DNS Updates Run

**Always skipped:** Lambda code changes, S3 content, DynamoDB updates, cache settings
**Update needed:** CloudFront recreation (origin changes, certificate changes, distribution replacement)

## GitHub Actions Workflows

### 1. PR Stack Deploy & Test (`.github/workflows/pr-stack-deploy.yml`)

**Triggers:**
- `pull_request` (opened, synchronize, reopened)

**Jobs:**

**`deploy-b-stack`:**
- Checkout code
- Package Lambda functions
- Deploy CloudFormation stack with `CREATE_CLOUDFRONT=false`
- Upload outputs as artifact
- Set PR comment with stack URL

**`run-e2e-tests`:**
- Depends on: `deploy-b-stack`
- Download stack outputs
- Run E2E test suite against HTTP S3 endpoint
- Report results in PR comment

**Environment Variables:**
```bash
STACK_NAME: silvermoat-pr-${{ github.event.pull_request.number }}
CREATE_CLOUDFRONT: false
DOMAIN_NAME: ""
```

**Stack Persistence:** B stacks remain until PR is closed (allows iterative testing)

### 2. PR Stack Cleanup (`.github/workflows/pr-stack-cleanup.yml`)

**Triggers:**
- `pull_request` (closed)

**Jobs:**

**`cleanup-b-stack`:**
- Identify stack name from PR number
- Delete CloudFormation stack
- Report completion

**Environment Variables:**
```bash
STACK_NAME: silvermoat-pr-${{ github.event.pull_request.number }}
```

### 3. Production Deploy (`.github/workflows/deploy-production.yml`)

**Triggers:**
- `push` to `main` branch
- `workflow_dispatch` (manual)

**Jobs:**

**`deploy-a-stack`:**
- Checkout code
- Package Lambda functions
- Deploy CloudFormation stack with `CREATE_CLOUDFRONT=true`
- **Smart DNS update:** Run `update-cloudflare-dns.sh` (checks first, only updates if needed)
- Invalidate CloudFront cache
- Run smoke tests
- Report deployment status

**Environment Variables:**
```bash
STACK_NAME: silvermoat
CREATE_CLOUDFRONT: true
DOMAIN_NAME: silvermoat.net
```

**Secrets Required:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ZONE_ID`

## Cloudflare Configuration

### Required DNS Records

**1. ACM Certificate Validation (one-time setup):**
```
Type: CNAME
Name: _validation-subdomain.silvermoat.net
Target: _validation-target.acm-validations.aws.
Proxy: Disabled (DNS only, gray cloud)
```

**2. Site Access (managed by workflow):**
```
Type: CNAME
Name: silvermoat.net
Target: d111111abcdef8.cloudfront.net (from CloudFormation output)
Proxy: Disabled (DNS only, gray cloud)
TTL: Auto
```

### API Token Permissions

**Required scopes:**
- Zone.DNS (Read, Edit)

**Zone resources:**
- Include: `silvermoat.net`

### Initial Setup Steps

1. **Deploy production stack (first time):**
   ```bash
   ./scripts/deploy-stack.sh
   ```

2. **Get ACM validation CNAME:**
   ```bash
   aws cloudformation describe-stacks \
     --stack-name silvermoat \
     --query "Stacks[0].Outputs[?OutputKey=='CertificateArn'].OutputValue" \
     --output text

   aws acm describe-certificate \
     --certificate-arn <arn-from-above> \
     --query "Certificate.DomainValidationOptions[0].ResourceRecord"
   ```

3. **Add validation CNAME to Cloudflare** (DNS only, gray cloud)

4. **Wait for certificate validation** (~5-15 minutes)

5. **First DNS update (manual or via workflow):**
   ```bash
   CLOUDFLARE_API_TOKEN=xxx \
   CLOUDFLARE_ZONE_ID=xxx \
   ./scripts/update-cloudflare-dns.sh
   ```

6. **Subsequent deployments:** DNS updates automatically (only when needed)

## Rollback Strategy

### Code/Lambda Rollback

**Git revert + redeploy:**
```bash
git revert <commit-sha>
git push origin main
# Production workflow auto-triggers
```

### Infrastructure Rollback

**CloudFormation stack rollback:**
```bash
aws cloudformation cancel-update-stack --stack-name silvermoat
# or
aws cloudformation rollback-stack --stack-name silvermoat
```

### Emergency DNS Rollback

**Manual Cloudflare update (if DNS change caused issue):**
```bash
# Update DNS to previous CloudFront domain
CLOUDFLARE_API_TOKEN=xxx \
CLOUDFLARE_ZONE_ID=xxx \
FORCE_UPDATE=true \
CLOUDFRONT_DOMAIN=<old-domain> \
./scripts/update-cloudflare-dns.sh
```

Or via Cloudflare dashboard: silvermoat.net → Edit CNAME → Change target

## Cost Optimization

**B Stacks (Ephemeral):**
- No CloudFront → saves $0.50/month base + data transfer costs per PR stack
- HTTP-only testing → no certificate fees
- Short-lived → minimal resource costs

**A Stack (Production):**
- CloudFront caching → reduces S3/API Gateway costs
- Smart DNS updates → faster deployments, no unnecessary API calls
- Single production environment → predictable costs

## Implementation Phases

### Phase 1: B Stack CI/CD (PR Testing)
- [x] Design document (this file)
- [ ] Create `pr-stack-deploy.yml` workflow
- [ ] Create `pr-stack-cleanup.yml` workflow
- [ ] Test PR deployment flow
- [ ] Verify E2E tests run correctly
- [ ] Confirm cleanup on PR close

### Phase 2: A Stack Production Deployment
- [x] Smart DNS update script (`update-cloudflare-dns.sh`)
- [ ] Create `deploy-production.yml` workflow
- [ ] Configure GitHub secrets (Cloudflare token, zone ID)
- [ ] Test production deployment
- [ ] Verify DNS updates (should skip on Lambda-only changes)
- [ ] Test force update scenario

### Phase 3: ACM Certificate Automation (Future)
- [ ] Investigate automated DNS validation
- [ ] Cloudflare API for creating validation CNAMEs
- [ ] Custom Resource Lambda for cert validation workflow

## Security Considerations

**GitHub Secrets:**
- `CLOUDFLARE_API_TOKEN`: Scoped to DNS edit only
- `CLOUDFLARE_ZONE_ID`: Public info, but keep in secrets for consistency
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`: IAM user with least privilege

**IAM Permissions (GitHub Actions user):**
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
        "apigateway:*",
        "dynamodb:*",
        "iam:*",
        "acm:*",
        "cloudfront:*",
        "sns:*"
      ],
      "Resource": "*"
    }
  ]
}
```

**Cloudflare Token Scoping:**
- Zone: `silvermoat.net` only
- Permissions: DNS read/edit (no other Cloudflare features)

## Testing Strategy

### B Stack (PR) Testing
- Full E2E test suite
- HTTP-only (no SSL/CORS complexity)
- Isolated environment per PR
- Parallel PR testing supported

### A Stack (Production) Testing
- Smoke tests after deployment
- Verify HTTPS/SSL cert
- Test custom domain access
- Check API Gateway endpoints
- Validate CloudFront caching

## Monitoring

**CloudFormation Stack Events:**
- Monitor for CREATE/UPDATE/DELETE failures
- Check Custom Resource logs for seed/cleanup issues

**CloudFront Metrics:**
- Cache hit ratio
- Error rates (4xx, 5xx)
- Data transfer volume

**Lambda Logs:**
- API errors
- Performance metrics
- Bedrock invocation costs

**DNS:**
- TTL expiration (~5 minutes)
- Cloudflare analytics (if needed)

## FAQ

**Q: Why not use CloudFront for B stacks?**
A: Cost optimization. CloudFront adds ~$0.50/month base cost per distribution. With multiple active PRs, this adds up. HTTP testing is sufficient for functional validation.

**Q: How long do DNS updates take?**
A: Cloudflare DNS typically propagates in 1-5 minutes. The CNAME record has TTL=1 (auto), so changes are quick. However, most deployments skip DNS updates entirely (smart check).

**Q: What if CloudFront distribution changes?**
A: The smart DNS script detects the mismatch and updates automatically. No manual intervention needed.

**Q: Can I force a DNS update?**
A: Yes. Set `FORCE_UPDATE=true` when running the script:
```bash
FORCE_UPDATE=true ./scripts/update-cloudflare-dns.sh
```

**Q: What happens if Cloudflare API fails?**
A: DNS update step fails, but stack deployment succeeds. Manual fix: run DNS script locally or update via Cloudflare dashboard. CloudFront default domain still works.

**Q: Why not use Route 53?**
A: Project already uses Cloudflare for domain management. Keeping DNS in one place simplifies operations. Could migrate to Route 53 in future if needed.

## Future Enhancements

1. **Blue-Green Deployments:** Maintain two A stacks, switch DNS between them
2. **Canary Deployments:** Route 10% traffic to new version via CloudFront behaviors
3. **Automated Rollback:** Detect errors and auto-revert within workflow
4. **Slack Notifications:** Deployment status updates in team channel
5. **Cost Tracking:** Tag resources, monitor per-PR and production costs
6. **Preview URLs:** Unique subdomains for each PR (e.g., `pr-123.silvermoat.net`)
