# Silvermoat MVP - E2E Demo Project

A one-shot deployable insurance MVP demo built on AWS CDK, featuring a React SPA frontend and serverless backend.

## Overview

Silvermoat is a complete end-to-end demo MVP that showcases:

- **Infrastructure as Code**: AWS CDK (TypeScript) for all AWS resources
- **Static Website Hosting**: S3 website hosting with CloudFront CDN (HTTPS)
- **Serverless API**: API Gateway REST API proxying to a single Lambda function
- **Data Storage**: DynamoDB tables for domain entities (quotes, policies, claims, payments, cases)
- **Document Storage**: S3 bucket for documents/attachments
- **Notifications**: SNS topic for demo notifications
- **Automated Cleanup**: Custom Resource Lambda that empties buckets on stack deletion

## Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  CloudFront │─────▶│  S3 Website  │      │ API Gateway │─────▶│   Lambda    │
│    (CDN)    │      │     (UI)     │      │   (REST)    │      │  (Handler)  │
└─────────────┘      └──────────────┘      └──────────────┘      └──────┬──────┘
                                                                          │
       ┌───────────────────────────────────────────┼─────────────┐
       │                                           │             │
       ▼                                           ▼             ▼
┌─────────────┐                          ┌─────────────┐  ┌─────────────┐
│   S3 Docs   │                          │  DynamoDB   │  │     SNS     │
│   Bucket    │                          │   Tables    │  │    Topic    │
└─────────────┘                          └─────────────┘  └─────────────┘
```

## Project Structure

```
Silvermoat/
├── cdk/                            # AWS CDK infrastructure (TypeScript)
│   ├── bin/
│   │   └── silvermoat.ts           # CDK app entry point
│   ├── lib/
│   │   ├── silvermoat-stack.ts     # Main stack
│   │   ├── constructs/             # Reusable CDK constructs
│   │   │   ├── storage.ts          # DynamoDB, S3
│   │   │   ├── compute.ts          # Lambda, IAM
│   │   │   ├── api.ts              # API Gateway
│   │   │   └── cdn.ts              # CloudFront, ACM
│   │   └── lambda/                 # Lambda function code
│   │       ├── mvp-service/        # API handler (Python)
│   │       └── seeder/             # Custom resource (Python)
│   ├── package.json                # Node dependencies
│   ├── cdk.json                    # CDK configuration
│   └── README.md                   # CDK-specific docs
├── ui/                             # React SPA frontend
│   ├── src/                        # React components
│   ├── package.json                # UI dependencies
│   └── vite.config.js              # Vite build config
├── scripts/                        # Helper scripts
│   ├── deploy-ui.sh                # Build and deploy UI
│   ├── get-outputs.sh              # Get stack outputs
│   └── smoke-test.sh               # Run smoke tests
└── README.md                       # This file
```

## Prerequisites

- **Node.js** 20+ and npm
- **AWS CLI** configured with credentials
- **AWS CDK CLI**: `npm install -g aws-cdk`
- **AWS account bootstrapped**: `cdk bootstrap`
- **AWS Permissions** to create:
  - S3 buckets, Lambda functions, DynamoDB tables
  - API Gateway, CloudFront, ACM certificates
  - IAM roles, SNS topics

## Quick Start

### 1. Deploy Infrastructure

```bash
cd cdk
npm install
npm run deploy
```

Or with custom parameters:

```bash
cd cdk
export APP_NAME=silvermoat
export STAGE_NAME=demo
export UI_SEEDING_MODE=external
export DOMAIN_NAME=silvermoat.net
npm run deploy
```

**Parameters:**
- `APP_NAME`: Application name (default: `silvermoat`)
- `STAGE_NAME`: API Gateway stage (default: `demo`)
- `API_DEPLOYMENT_TOKEN`: Force API redeployment (default: `v1`)
- `UI_SEEDING_MODE`: `seeded` (Lambda HTML) or `external` (React SPA) (default: `external`)
- `DOMAIN_NAME`: Custom domain for CloudFront (default: `silvermoat.net`)
- `CREATE_CLOUDFRONT`: Create CloudFront (default: `true`)

Wait for deployment to complete (~15-20 minutes, including CloudFront).

### 2. Get Stack Outputs

```bash
./scripts/get-outputs.sh
```

Key outputs:
- `CloudFrontUrl`: HTTPS URL for production access
- `WebUrl`: S3 website URL (HTTP, for testing)
- `ApiBaseUrl`: API Gateway base URL
- `UiBucketName`, `DocsBucketName`: S3 bucket names

### 3. Deploy UI

```bash
./scripts/deploy-ui.sh
```

This will:
1. Install npm dependencies
2. Build the React app
3. Sync to S3 with proper cache headers
4. Display the CloudFront URL

### 4. Verify Deployment

Run smoke tests:

```bash
./scripts/smoke-test.sh
```

Or manually test:
- Open the `CloudFrontUrl` in a browser
- Create a quote using the form
- Check API responses

## Development

### Infrastructure Changes

Edit CDK code in `cdk/lib/`, then:

```bash
cd cdk
npm run build   # Compile TypeScript
npm run diff    # Show changes
npm run deploy  # Deploy updates
```

### Lambda Function Changes

Edit Python code in `cdk/lib/lambda/`, then:

```bash
cd cdk
npm run deploy  # CDK handles Lambda packaging
```

### Local UI Development

```bash
cd ui
npm install
npm run dev
```

UI available at `http://localhost:5173`.

**Note**: Set `VITE_API_BASE_URL` environment variable or modify `ui/src/App.jsx` to use your deployed API URL.

### Building UI

```bash
cd ui
npm run build
```

Output in `ui/dist/`.

## UI Architecture

### Technology Stack

- **React 18**: Functional components with hooks
- **React Router v6**: Client-side routing with lazy loading
- **React Query (TanStack Query v5)**: Server state management
- **Ant Design v5**: Enterprise component library
- **Vite**: Fast build tool and dev server

### Design System

**Insurance Industry Standard**: Conservative, trustworthy, professional interface

**Colors**:
- Primary Blue: `#003d82` (trust, stability)
- Primary Dark: `#002855` (header/footer)
- Accent Gold: `#c5a572` (premium feel)

### Component Patterns

Every entity follows consistent pattern:
- **EntityList.jsx**: Page wrapper, routing
- **EntityTable.jsx**: Data table with sorting, filtering
- **EntityForm.jsx**: Create form with validation
- **EntityDetail.jsx**: Detail view with related entities

See full UI architecture documentation in the UI section below.

## API Endpoints

### Create Quote
```bash
POST /quote
Content-Type: application/json

{
  "name": "Jane Doe",
  "zip": "33431"
}
```

### Get Quote
```bash
GET /quote/{id}
```

### Other Endpoints
- `POST /policy`, `GET /policy/{id}`
- `POST /claim`, `GET /claim/{id}`
- `POST /payment`, `GET /payment/{id}`
- `POST /case`, `GET /case/{id}`
- `POST /chat` (Bedrock AI assistant)

### Update Claim Status
```bash
POST /claim/{id}/status
Content-Type: application/json

{
  "status": "APPROVED"
}
```

## Custom Domain Setup with Cloudflare

The stack creates CloudFront with custom domain (`silvermoat.net` by default).

### Step 1: Deploy Stack

```bash
cd cdk
npm run deploy
```

Stack creates ACM certificate and waits for DNS validation.

### Step 2: Get DNS Validation Record

```bash
aws acm describe-certificate \
  --certificate-arn $(aws cloudformation describe-stacks \
    --stack-name SilvermoatStack \
    --query "Stacks[0].Outputs[?OutputKey=='CertificateArn'].OutputValue" \
    --output text) \
  --query "Certificate.DomainValidationOptions[0].ResourceRecord" \
  --output table
```

### Step 3: Add DNS Validation CNAME in Cloudflare

1. Log in to Cloudflare dashboard
2. Select domain (`silvermoat.net`)
3. Go to **DNS** → **Records** → **Add record**
4. Configure:
   - **Type**: `CNAME`
   - **Name**: `_abc123def456` (validation subdomain)
   - **Target**: `_xyz789.acm-validations.aws.` (validation target)
   - **Proxy status**: **DNS only** (gray cloud, NOT orange)

Wait 5-15 minutes for validation.

### Step 4: Add CloudFront Alias CNAME

```bash
./scripts/get-outputs.sh
# Look for "CloudFrontDomain" output
```

Add CNAME in Cloudflare:
- **Type**: `CNAME`
- **Name**: `@` (apex domain)
- **Target**: `xyz123.cloudfront.net` (CloudFront domain)
- **Proxy status**: **DNS only** (gray cloud)

### Step 5: Test

Visit `https://silvermoat.net`.

**Critical**: Cloudflare proxy must be **disabled** (DNS only, gray cloud) for both records.

## Stack Deletion

```bash
cd cdk
npm run destroy
```

Cleanup Lambda automatically:
- Empties both S3 buckets
- Wipes all DynamoDB tables
- Ensures clean deletion

## Troubleshooting

### Stack Deployment Fails

- Check CloudWatch logs: `/aws/lambda/SilvermoatStack-*`
- Verify AWS credentials: `aws sts get-caller-identity`
- Ensure CDK bootstrap: `cdk bootstrap`

### API Returns 403/404

- Verify API Gateway deployment token updated
- Check Lambda logs: `/aws/lambda/SilvermoatStack-Compute-MvpServiceFunction-*`

### UI Not Loading

- Check CloudFront distribution status (takes 10-20 min to deploy)
- Verify UI files in S3: `aws s3 ls s3://<ui-bucket-name>/`
- Clear browser cache

### Custom Domain Issues

- Verify DNS records in Cloudflare (DNS only, gray cloud)
- Check ACM certificate validation status
- Wait for CloudFront distribution to fully deploy

## Configuration

CDK parameters via environment variables or CDK context:

```bash
# Via environment variables
export APP_NAME=silvermoat
export STAGE_NAME=demo
cd cdk && npm run deploy
```

```bash
# Via CDK context
cd cdk
cdk deploy -c appName=silvermoat -c stageName=demo
```

See `cdk/README.md` for detailed CDK documentation.

## UI Development Guide

Full UI architecture and development guide available in original README (UI Architecture section).

Key sections:
- Technology Stack
- Design System
- State Management (React Query + Context API)
- Component Patterns
- How to Add a New Entity
- Demo Data Seeding
- Best Practices

## Important Notes

1. **CDK Bootstrap**: Required before first deployment: `cdk bootstrap`
2. **Lambda Packaging**: CDK handles automatically (no manual ZIP files)
3. **Type Safety**: TypeScript catches errors at compile time
4. **DynamoDB Data**: Use integers for currency (e.g., `premium_cents: 12550`)
5. **API Deployment**: Change `API_DEPLOYMENT_TOKEN` to force redeployment

## License

Demo project for educational purposes.

## Support

For issues:
1. Check CloudWatch logs for Lambda functions
2. Review CloudFormation stack events in AWS Console
3. Run `./scripts/smoke-test.sh`
4. Check `cdk/README.md` for CDK-specific troubleshooting
