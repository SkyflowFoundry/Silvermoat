#!/bin/bash
# Deploy complete Silvermoat stack (infrastructure + UI) using CDK

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

STACK_NAME="${STACK_NAME:-silvermoat}"
UI_DIR="$PROJECT_ROOT/ui"
BUILD_DIR="$UI_DIR/dist"

# AWS Profile support
AWS_PROFILE="${AWS_PROFILE:-}"
AWS_CMD="aws"
if [ -n "$AWS_PROFILE" ]; then
  AWS_CMD="aws --profile $AWS_PROFILE"
  echo "Using AWS profile: $AWS_PROFILE"
fi

# Check AWS CLI and credentials
check_aws_configured

# Default parameters (exported as environment variables for CDK)
export APP_NAME="${APP_NAME:-silvermoat}"
export STAGE_NAME="${STAGE_NAME:-demo}"
export API_DEPLOYMENT_TOKEN="${API_DEPLOYMENT_TOKEN:-v1}"
export UI_SEEDING_MODE="${UI_SEEDING_MODE:-external}"
export CREATE_CLOUDFRONT="${CREATE_CLOUDFRONT:-true}"
export DOMAIN_NAME="${DOMAIN_NAME:-silvermoat.net}"
export STACK_NAME

echo "=========================================="
echo "Silvermoat Full Deployment (CDK)"
echo "=========================================="
echo ""

# ==========================================
# Step 1: Deploy CDK Stack
# ==========================================
echo "Step 1: Deploying CDK stack"
echo "----------------------------------------"
echo "Stack Name: $STACK_NAME"
echo "Parameters:"
echo "  AppName: $APP_NAME"
echo "  StageName: $STAGE_NAME"
echo "  ApiDeploymentToken: $API_DEPLOYMENT_TOKEN"
echo "  UiSeedingMode: $UI_SEEDING_MODE"
echo "  CreateCloudFront: $CREATE_CLOUDFRONT"
echo "  DomainName: $DOMAIN_NAME"
echo ""

# Install CDK dependencies (first time only)
if [ ! -d "$PROJECT_ROOT/cdk/cdk.out" ]; then
  echo "Installing CDK dependencies..."
  cd "$PROJECT_ROOT/cdk"
  pip install -q -r requirements.txt
  echo "✓ CDK dependencies installed"
  echo ""
fi

# Check if CDK CLI is installed
if ! command -v cdk >/dev/null 2>&1; then
  echo "Error: AWS CDK CLI not found. Install with:"
  echo "  npm install -g aws-cdk"
  exit 1
fi

# Deploy CDK stack
echo "Deploying CDK stack..."
cd "$PROJECT_ROOT/cdk"
cdk deploy "$STACK_NAME" --require-approval never

echo ""
echo "Stack deployment complete!"
echo ""

# ==========================================
# Step 2: Build and Deploy UI
# ==========================================
echo "Step 2: Building and deploying React UI"
echo "----------------------------------------"
echo ""

# Check if UI directory exists
if [ ! -d "$UI_DIR" ]; then
  echo "Error: UI directory not found: $UI_DIR"
  exit 1
fi

# Get UI bucket name from CDK stack outputs
echo "Getting stack outputs..."
UI_BUCKET=$($AWS_CMD cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='UiBucketName'].OutputValue" \
  --output text 2>/dev/null || echo "")

if [ -z "$UI_BUCKET" ]; then
  echo "Error: Could not get UiBucketName from stack '$STACK_NAME'"
  echo "Make sure the CDK stack is deployed and has the UiBucketName output."
  exit 1
fi

echo "UI Bucket: $UI_BUCKET"
echo ""

# Get API base URL for build-time injection
API_BASE=$($AWS_CMD cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='ApiBaseUrl'].OutputValue" \
  --output text 2>/dev/null || echo "")

if [ -n "$API_BASE" ]; then
  echo "API Base URL: $API_BASE"
  export VITE_API_BASE_URL="$API_BASE"
fi

# Build React app
cd "$UI_DIR"
echo "Installing dependencies (if needed)..."

# Use npm ci if package-lock.json exists, otherwise use npm install
if [ -f "package-lock.json" ]; then
  npm ci --silent
else
  echo "No package-lock.json found, running npm install..."
  npm install --silent
fi

echo "Building React app..."
npm run build

if [ ! -d "$BUILD_DIR" ]; then
  echo "Error: Build output directory not found: $BUILD_DIR"
  exit 1
fi

echo ""
echo "Syncing build output to S3 bucket..."

# Sync with proper cache headers
# index.html: no-cache (always fetch fresh)
# PNG diagrams: 1-hour cache (updates visible on reload)
# Static assets (JS/CSS): long cache (immutable, hash-based filenames)
$AWS_CMD s3 sync "$BUILD_DIR" "s3://$UI_BUCKET/" \
  --delete \
  --exclude "*.html" \
  --exclude "*.png" \
  --cache-control "public, max-age=31536000, immutable"

# Upload PNG diagrams with 1-hour cache (no immutable)
$AWS_CMD s3 sync "$BUILD_DIR" "s3://$UI_BUCKET/" \
  --exclude "*" \
  --include "*.png" \
  --cache-control "public, max-age=3600"

# Upload index.html separately with no-cache
$AWS_CMD s3 cp "$BUILD_DIR/index.html" "s3://$UI_BUCKET/index.html" \
  --cache-control "no-cache"

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "CloudFront URL (HTTPS - Recommended):"
CF_URL=$($AWS_CMD cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='CloudFrontUrl'].OutputValue" \
  --output text 2>/dev/null || echo "")

if [ -n "$CF_URL" ]; then
  echo "  $CF_URL"
else
  echo "  (Get from: ./scripts/get-outputs.sh)"
fi

echo ""
echo "Custom Domain URL:"
CUSTOM_URL=$($AWS_CMD cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='CustomDomainUrl'].OutputValue" \
  --output text 2>/dev/null || echo "")

if [ -n "$CUSTOM_URL" ]; then
  echo "  $CUSTOM_URL"
  echo ""
  echo "  Note: Ensure DNS CNAME is configured in Cloudflare:"
  echo "    Type: CNAME"
  echo "    Name: your-subdomain (e.g., silvermoat or app)"
  CF_DOMAIN=$($AWS_CMD cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='CloudFrontDomain'].OutputValue" \
    --output text 2>/dev/null || echo "")
  if [ -n "$CF_DOMAIN" ]; then
    echo "    Target: $CF_DOMAIN"
  fi
else
  echo "  (Not configured - domain may be disabled or cert validation pending)"
  echo "  Default domain is silvermoat.net"
  echo "  To disable: DOMAIN_NAME=\"\" ./scripts/deploy-stack.sh"
fi

echo ""
echo "S3 Website URL (HTTP, legacy):"
WEB_URL=$($AWS_CMD cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='WebUrl'].OutputValue" \
  --output text 2>/dev/null || echo "")

if [ -n "$WEB_URL" ]; then
  echo "  $WEB_URL"
else
  echo "  (Get from: ./scripts/get-outputs.sh)"
fi

echo ""
echo "API Base URL:"
if [ -n "$API_BASE" ]; then
  echo "  $API_BASE"
else
  echo "  (Get from: ./scripts/get-outputs.sh)"
fi

echo ""
echo "To run smoke tests:"
echo "  ./scripts/smoke-test.sh"
echo ""
