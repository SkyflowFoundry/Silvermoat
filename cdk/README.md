# Silvermoat CDK

AWS CDK infrastructure for Silvermoat Insurance MVP.

## Prerequisites

- Node.js 20+ and npm
- AWS CLI configured with credentials
- AWS CDK CLI: `npm install -g aws-cdk`
- AWS account bootstrapped for CDK: `cdk bootstrap`

## Quick Start

```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Synthesize CloudFormation template
npm run synth

# Deploy stack
npm run deploy

# Destroy stack
npm run destroy
```

## Configuration

Set parameters via environment variables or CDK context:

```bash
# Via environment variables
export APP_NAME=silvermoat
export STAGE_NAME=demo
export API_DEPLOYMENT_TOKEN=v1
export UI_SEEDING_MODE=external
export DOMAIN_NAME=silvermoat.net
export CREATE_CLOUDFRONT=true

npm run deploy
```

```bash
# Via CDK context
cdk deploy \
  -c appName=silvermoat \
  -c stageName=demo \
  -c apiDeploymentToken=v1 \
  -c uiSeedingMode=external \
  -c domainName=silvermoat.net \
  -c createCloudFront=true
```

## Parameters

- `appName` (default: `silvermoat`): Application name used in resource naming
- `stageName` (default: `demo`): API Gateway stage name
- `apiDeploymentToken` (default: `v1`): Change to force API redeployment
- `uiSeedingMode` (default: `external`):
  - `seeded`: Lambda uploads basic index.html
  - `external`: Deploy React SPA separately
- `domainName` (default: `silvermoat.net`): Custom domain for CloudFront (empty = CloudFront default domain only)
- `createCloudFront` (default: `true`): Create CloudFront distribution (false = S3 website URL only)

## Architecture

### Resources Created

- **DynamoDB Tables**: Quotes, Policies, Claims, Payments, Cases (PAY_PER_REQUEST)
- **S3 Buckets**: UI (public website), Docs (private)
- **Lambda Functions**: MvpService (API logic), Seeder (custom resource)
- **API Gateway**: REST API with Lambda proxy integration
- **CloudFront**: CDN with optional custom domain
- **ACM Certificate**: For custom domain (if configured)
- **SNS Topic**: Demo notifications
- **Custom Resources**: Seed demo data, cleanup on delete

### Lambda Functions

Lambda code is in `lib/lambda/`:

- `mvp-service/index.py`: Main API handler (routes, CRUD, Bedrock chat)
- `seeder/index.py`: Custom resource handler (seed/cleanup)

CDK automatically packages Lambda code and uploads to S3 during deployment.

## Deployment Workflow

1. **Build**: `npm run build` (compiles TypeScript)
2. **Synth**: `npm run synth` (generates CloudFormation template in `cdk.out/`)
3. **Deploy**: `npm run deploy` (deploys stack to AWS)
4. **Get Outputs**: `cdk deploy` prints outputs (API URL, S3 bucket names, etc.)

## UI Deployment

After infrastructure deployment, deploy the React UI:

```bash
cd ../ui
npm install
npm run build

# Deploy to S3 (requires stack outputs)
../scripts/deploy-ui.sh
```

## Custom Domain Setup

1. Set `domainName` parameter to your domain (e.g., `silvermoat.net`)
2. Deploy stack: `cdk deploy`
3. Stack creates ACM certificate and waits for DNS validation
4. Add ACM validation CNAME to Cloudflare (DNS only, gray cloud)
5. Wait for cert validation (~5-15min)
6. Stack completes, CloudFront gets custom domain alias
7. Add CloudFront alias CNAME to Cloudflare (DNS only, gray cloud)
8. Access via `https://silvermoat.net`

**Critical**: Cloudflare proxy must be **disabled** (DNS only, gray cloud) for both records.

## Troubleshooting

### Stack Deployment Fails

- Check CloudWatch logs: `/aws/lambda/SilvermoatStack-*`
- Verify AWS credentials: `aws sts get-caller-identity`
- Ensure CDK bootstrap: `cdk bootstrap`

### Stack Deletion Fails

- Cleanup Lambda should empty S3 buckets automatically
- Manual cleanup: `aws s3 rm s3://<bucket-name> --recursive`

### API Returns 403/404

- Verify API Gateway deployment token was updated
- Check Lambda logs: `/aws/lambda/SilvermoatStack-Compute-MvpServiceFunction-*`

## Development

### Project Structure

```
cdk/
├── bin/
│   └── silvermoat.ts        # CDK app entry point
├── lib/
│   ├── silvermoat-stack.ts  # Main stack
│   ├── constructs/
│   │   ├── storage.ts       # DynamoDB, S3
│   │   ├── compute.ts       # Lambda, IAM
│   │   ├── api.ts           # API Gateway
│   │   └── cdn.ts           # CloudFront, ACM
│   └── lambda/
│       ├── mvp-service/     # API Lambda code
│       └── seeder/          # Seeder Lambda code
├── cdk.json                 # CDK config
├── package.json             # Node dependencies
└── tsconfig.json            # TypeScript config
```

### Adding Resources

Edit `lib/silvermoat-stack.ts` or create new constructs in `lib/constructs/`.

### Modifying Lambda Code

Edit Python files in `lib/lambda/`, then redeploy:

```bash
npm run build
npm run deploy
```

CDK detects code changes and updates Lambda functions automatically.

## Useful Commands

- `npm run build`: Compile TypeScript
- `npm run watch`: Watch for changes and compile
- `npm run synth`: Generate CloudFormation template
- `npm run deploy`: Deploy stack to AWS
- `npm run diff`: Show differences between deployed and local
- `npm run destroy`: Delete stack from AWS
- `cdk ls`: List all stacks in app
- `cdk docs`: Open CDK documentation

## Migration from CloudFormation

This CDK project replaced the raw CloudFormation template (previously at `infra/silvermoat-mvp-s3-website.yaml`, now removed).

**Key improvements:**

- **Type safety**: TypeScript catches errors at compile time
- **Reusable constructs**: DynamoDB tables, Lambda functions follow DRY principle
- **Automatic Lambda packaging**: No manual ZIP + S3 upload
- **Cleaner syntax**: Less verbose than YAML
- **Better maintainability**: Organized constructs by architectural concern

**Old deployment scripts** (CloudFormation-based) have been archived to `scripts/legacy/` and are no longer needed.
