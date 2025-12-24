#!/bin/bash
# Deploy complete Silvermoat stack (infrastructure + UI)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

STACK_NAME="${STACK_NAME:-silvermoat}"
TEMPLATE_FILE="$PROJECT_ROOT/infra/silvermoat-mvp-s3-website.yaml"
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

# Default parameters
APP_NAME="${APP_NAME:-silvermoat}"
STAGE_NAME="${STAGE_NAME:-demo}"
API_DEPLOYMENT_TOKEN="${API_DEPLOYMENT_TOKEN:-v1}"
UI_SEEDING_MODE="${UI_SEEDING_MODE:-external}"

echo "=========================================="
echo "Silvermoat Full Deployment"
echo "=========================================="
echo ""

# ==========================================
# Step 1: Deploy CloudFormation Stack
# ==========================================
echo "Step 1: Deploying CloudFormation stack"
echo "----------------------------------------"
echo "Stack Name: $STACK_NAME"
echo "Template: $TEMPLATE_FILE"
echo "Parameters:"
echo "  AppName: $APP_NAME"
echo "  StageName: $STAGE_NAME"
echo "  ApiDeploymentToken: $API_DEPLOYMENT_TOKEN"
echo "  UiSeedingMode: $UI_SEEDING_MODE"
echo ""

# Check if template file exists
if [ ! -f "$TEMPLATE_FILE" ]; then
  echo "Error: Template file not found: $TEMPLATE_FILE"
  exit 1
fi

# Deploy stack
$AWS_CMD cloudformation deploy \
  --stack-name "$STACK_NAME" \
  --template-file "$TEMPLATE_FILE" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    AppName="$APP_NAME" \
    StageName="$STAGE_NAME" \
    ApiDeploymentToken="$API_DEPLOYMENT_TOKEN" \
    UiSeedingMode="$UI_SEEDING_MODE" \
  --no-fail-on-empty-changeset

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

# Get UI bucket name from stack outputs
echo "Getting stack outputs..."
UI_BUCKET=$($AWS_CMD cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='UiBucketName'].OutputValue" \
  --output text 2>/dev/null || echo "")

if [ -z "$UI_BUCKET" ]; then
  echo "Error: Could not get UiBucketName from stack '$STACK_NAME'"
  echo "Make sure the stack is deployed and has the UiBucketName output."
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
# Static assets: long cache (immutable)
$AWS_CMD s3 sync "$BUILD_DIR" "s3://$UI_BUCKET/" \
  --delete \
  --exclude "*.html" \
  --cache-control "public, max-age=31536000, immutable"

# Upload index.html separately with no-cache
$AWS_CMD s3 cp "$BUILD_DIR/index.html" "s3://$UI_BUCKET/index.html" \
  --cache-control "no-cache"

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Website URL:"
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
