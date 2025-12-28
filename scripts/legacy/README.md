# Legacy Scripts (Archived)

This directory contains scripts that were used with the old CloudFormation-based deployment approach.

**These scripts are no longer used** and have been replaced by:
- AWS CDK for infrastructure deployment
- GitHub Actions workflows for CI/CD automation

## Archived Scripts

### `deploy-stack.sh`
**Replaced by:** `cd cdk && npm run deploy` (or GitHub Actions workflows)

Old script that packaged Lambda code, uploaded to S3, and deployed CloudFormation template.

### `delete-stack.sh`
**Replaced by:** `cd cdk && npm run destroy`

Old script that deleted the CloudFormation stack.

### `deploy-all.sh`
**Replaced by:** GitHub Actions workflows (deploy-dev.yml, deploy-staging.yml, deploy-prod.yml)

Combined script that deployed infrastructure + UI in one command.

### `redeploy-all.sh`
**Replaced by:** GitHub Actions workflows

Script for redeploying the entire stack (delete + deploy).

## Why Archived?

These scripts were tightly coupled to the raw CloudFormation template at `infra/silvermoat-mvp-s3-website.yaml` which has been replaced by AWS CDK infrastructure code.

### Old Approach (CloudFormation + Shell Scripts)
```bash
./scripts/deploy-stack.sh    # Deploy infrastructure
./scripts/deploy-ui.sh        # Deploy UI
```

### New Approach (CDK + GitHub Actions)
```bash
# Manual deployment
cd cdk && npm run deploy      # Deploy infrastructure
./scripts/deploy-ui.sh        # Deploy UI (still used!)

# Automated deployment (preferred)
git push origin main          # Triggers deploy-dev.yml workflow
```

## Migration Date

Archived: 2024-12-28
Related Issue: #16 (Phase 1 & 2 - CDK migration + GitHub Actions CI/CD)
Related Commits:
- 143e34e: Migrate from CloudFormation to AWS CDK
- 8f8f1f2: Implement Phase 2 - GitHub Actions CI/CD workflows

## If You Need These Scripts

If you need to reference the old deployment approach:
1. Check git history: `git log scripts/legacy/`
2. View old version: `git show 143e34e^:scripts/deploy-stack.sh`
3. Checkout old commit: `git checkout 143e34e^` (before CDK migration)

For new deployments, use the CDK approach documented in:
- `cdk/README.md` - CDK deployment guide
- `README.md` - CI/CD workflows section
- `.github/AWS_OIDC_SETUP.md` - GitHub Actions setup
