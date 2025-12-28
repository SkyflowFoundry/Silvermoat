# AWS OIDC Setup for GitHub Actions

This guide explains how to set up AWS OIDC (OpenID Connect) authentication for GitHub Actions, eliminating the need for long-lived AWS access keys.

## Why OIDC?

**Traditional approach (❌ Not recommended):**
- Create IAM user with access keys
- Store keys in GitHub Secrets
- Keys are long-lived and can be compromised
- Requires manual rotation

**OIDC approach (✅ Recommended):**
- No access keys stored in GitHub
- Short-lived tokens (1 hour)
- Automatic token rotation
- More secure and compliant

## Prerequisites

- AWS account with administrator access
- GitHub repository admin access
- AWS CLI configured locally

## Step 1: Create GitHub OIDC Provider in AWS

Run this AWS CLI command to create the OIDC provider:

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1 \
  --tags Key=Name,Value=GitHubActions
```

**Note:** The thumbprint `6938fd4d98bab03faadb97b34396831e3780aea1` is GitHub's OIDC provider certificate thumbprint (valid as of 2024).

Verify the provider was created:

```bash
aws iam list-open-id-connect-providers
```

You should see: `arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com`

## Step 2: Create IAM Role for GitHub Actions

Create a trust policy file `github-trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<AWS_ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:<GITHUB_ORG>/<GITHUB_REPO>:*"
        }
      }
    }
  ]
}
```

**Replace placeholders:**
- `<AWS_ACCOUNT_ID>`: Your AWS account ID (e.g., `123456789012`)
- `<GITHUB_ORG>`: Your GitHub organization (e.g., `SkyflowFoundry`)
- `<GITHUB_REPO>`: Your repository name (e.g., `Silvermoat`)

Create the IAM role:

```bash
aws iam create-role \
  --role-name GitHubActionsDeploymentRole \
  --assume-role-policy-document file://github-trust-policy.json \
  --description "Role for GitHub Actions to deploy Silvermoat"
```

## Step 3: Attach Permissions to the Role

### Option A: Admin Access (Easiest, for dev/staging)

```bash
aws iam attach-role-policy \
  --role-name GitHubActionsDeploymentRole \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

### Option B: Least Privilege (Recommended for production)

Create a custom policy `github-deploy-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CDKDeploy",
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "s3:*",
        "lambda:*",
        "iam:*",
        "dynamodb:*",
        "apigateway:*",
        "cloudfront:*",
        "acm:*",
        "sns:*",
        "events:*",
        "logs:*",
        "ec2:DescribeAvailabilityZones",
        "ec2:DescribeVpcs",
        "ec2:DescribeSubnets",
        "ec2:DescribeSecurityGroups",
        "ssm:GetParameter",
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    }
  ]
}
```

Create and attach the policy:

```bash
aws iam create-policy \
  --policy-name GitHubActionsCDKDeployPolicy \
  --policy-document file://github-deploy-policy.json

aws iam attach-role-policy \
  --role-name GitHubActionsDeploymentRole \
  --policy-arn arn:aws:iam::<AWS_ACCOUNT_ID>:policy/GitHubActionsCDKDeployPolicy
```

## Step 4: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secret:

**Secret name:** `AWS_ROLE_ARN`
**Secret value:** `arn:aws:iam::<AWS_ACCOUNT_ID>:role/GitHubActionsDeploymentRole`

### For Production Deployments (Optional)

If using a separate AWS account or role for production:

**Secret name:** `AWS_ROLE_ARN_PROD`
**Secret value:** `arn:aws:iam::<PROD_ACCOUNT_ID>:role/GitHubActionsProductionRole`

## Step 5: Configure GitHub Environments

GitHub Environments add approval gates and environment-specific secrets.

Go to: Repository → Settings → Environments

### Create Dev Environment

1. Click "New environment"
2. Name: `dev`
3. No protection rules (deploys automatically)

### Create Staging Environment

1. Click "New environment"
2. Name: `staging`
3. Protection rules:
   - ✅ Required reviewers: (optional)
   - Wait timer: 0 minutes

### Create Production Environment

1. Click "New environment"
2. Name: `production`
3. Protection rules:
   - ✅ Required reviewers: Add yourself or team members
   - ✅ Prevent administrators from bypassing configured protection rules
   - Wait timer: 0 minutes
4. Environment secrets:
   - `AWS_ROLE_ARN_PROD`: Production role ARN (if different from dev/staging)

## Step 6: Test the Setup

Create a test workflow run:

```bash
git checkout -b test-oidc-setup
git push origin test-oidc-setup
```

Open a PR and check the "PR Checks" workflow. If OIDC is configured correctly, you should see:

✅ Configure AWS credentials (OIDC) - Success

## Troubleshooting

### Error: "Not authorized to perform sts:AssumeRoleWithWebIdentity"

**Cause:** Trust policy doesn't match the GitHub repository.

**Fix:** Update trust policy with correct `<GITHUB_ORG>/<GITHUB_REPO>`:

```bash
aws iam update-assume-role-policy \
  --role-name GitHubActionsDeploymentRole \
  --policy-document file://github-trust-policy.json
```

### Error: "OIDC provider not found"

**Cause:** OIDC provider wasn't created in AWS.

**Fix:** Run Step 1 again to create the provider.

### Error: "Access Denied" during CDK deployment

**Cause:** IAM role doesn't have sufficient permissions.

**Fix:** Attach `AdministratorAccess` policy (for testing) or review CDK deployment logs to identify missing permissions.

### Verify OIDC Configuration

Check the OIDC provider exists:

```bash
aws iam get-open-id-connect-provider \
  --open-id-connect-provider-arn arn:aws:iam::<AWS_ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com
```

Check the role trust policy:

```bash
aws iam get-role --role-name GitHubActionsDeploymentRole --query 'Role.AssumeRolePolicyDocument'
```

Check attached policies:

```bash
aws iam list-attached-role-policies --role-name GitHubActionsDeploymentRole
```

## Security Best Practices

1. **Scope OIDC to specific branches** (optional):
   ```json
   "token.actions.githubusercontent.com:sub": "repo:<ORG>/<REPO>:ref:refs/heads/main"
   ```

2. **Use separate roles for environments**:
   - Dev: `GitHubActionsDevRole`
   - Staging: `GitHubActionsStagingRole`
   - Production: `GitHubActionsProductionRole` (with stricter permissions)

3. **Enable CloudTrail**: Monitor all API calls made by GitHub Actions.

4. **Use AWS Organizations**: Restrict deployments to specific AWS accounts.

5. **Rotate OIDC thumbprints**: GitHub may update their certificate. Monitor AWS IAM for updates.

## Additional Resources

- [GitHub OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [AWS IAM OIDC Providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)
- [CDK Bootstrap](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html)

## Summary

After completing this setup:

✅ No AWS access keys stored in GitHub
✅ Short-lived tokens (1 hour expiry)
✅ Automatic token rotation
✅ Scoped permissions per repository
✅ Approval gates for production deployments

Your GitHub Actions workflows will now authenticate to AWS securely using OIDC!
