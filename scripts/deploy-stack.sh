#!/bin/bash
# Deploy CloudFormation stack for Silvermoat MVP

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

STACK_NAME="${STACK_NAME:-silvermoat}"
TEMPLATE_FILE="$PROJECT_ROOT/infra/silvermoat-mvp-s3-website.yaml"

# Check AWS CLI and credentials
check_aws_configured

# Build AWS command with profile if set
AWS_CMD="aws"
if [ -n "${AWS_PROFILE:-}" ]; then
  AWS_CMD="aws --profile $AWS_PROFILE"
fi

# Default parameters
APP_NAME="${APP_NAME:-silvermoat}"
STAGE_NAME="${STAGE_NAME:-demo}"
API_DEPLOYMENT_TOKEN="${API_DEPLOYMENT_TOKEN:-v1}"
UI_SEEDING_MODE="${UI_SEEDING_MODE:-external}"
CREATE_CLOUDFRONT="${CREATE_CLOUDFRONT:-true}"
DOMAIN_NAME="${DOMAIN_NAME:-silvermoat.net}"

echo "Deploying CloudFormation stack: $STACK_NAME"
echo "Template: $TEMPLATE_FILE"
echo "Parameters:"
echo "  AppName: $APP_NAME"
echo "  StageName: $STAGE_NAME"
echo "  ApiDeploymentToken: $API_DEPLOYMENT_TOKEN"
echo "  UiSeedingMode: $UI_SEEDING_MODE"
echo "  CreateCloudFront: $CREATE_CLOUDFRONT"
echo "  DomainName: $DOMAIN_NAME"
echo ""

# Check if template file exists
if [ ! -f "$TEMPLATE_FILE" ]; then
  echo "Error: Template file not found: $TEMPLATE_FILE"
  exit 1
fi

# Get AWS account ID and region for S3 bucket name
AWS_ACCOUNT_ID=$($AWS_CMD sts get-caller-identity --query Account --output text)
AWS_REGION=$($AWS_CMD configure get region || echo "us-east-1")
S3_BUCKET="${CFN_S3_BUCKET:-cf-templates-${STACK_NAME}-${AWS_ACCOUNT_ID}-${AWS_REGION}}"

echo "S3 Bucket for templates: $S3_BUCKET"
echo ""

# Create S3 bucket if it doesn't exist
if ! $AWS_CMD s3 ls "s3://$S3_BUCKET" 2>/dev/null; then
  echo "Creating S3 bucket: $S3_BUCKET"
  if [ "$AWS_REGION" = "us-east-1" ]; then
    $AWS_CMD s3 mb "s3://$S3_BUCKET"
  else
    $AWS_CMD s3 mb "s3://$S3_BUCKET" --region "$AWS_REGION"
  fi
  echo "S3 bucket created"
else
  echo "S3 bucket already exists"
fi

# Check if Lambda code has changed (optimization)
echo ""
echo "Checking Lambda code for changes..."
LAMBDA_DIR="$PROJECT_ROOT/lambda"

# Calculate hash of all Lambda source files
if command -v md5sum >/dev/null 2>&1; then
  LAMBDA_HASH=$(find "$LAMBDA_DIR" -type f -name "*.py" -exec md5sum {} \; 2>/dev/null | sort | md5sum | cut -d' ' -f1)
else
  # macOS fallback (uses md5 instead of md5sum)
  LAMBDA_HASH=$(find "$LAMBDA_DIR" -type f -name "*.py" -exec md5 {} \; 2>/dev/null | sort | md5 | cut -d' ' -f1)
fi

# Try to get stored hash from S3
STORED_HASH=$($AWS_CMD s3 cp "s3://$S3_BUCKET/.lambda-hash" - 2>/dev/null || echo "")

if [ -n "$LAMBDA_HASH" ] && [ "$LAMBDA_HASH" = "$STORED_HASH" ]; then
  echo "✅ Lambda code unchanged (hash: $LAMBDA_HASH), skipping repackage"
  SKIP_LAMBDA_PACKAGING=true
else
  echo "Lambda code changed (current: $LAMBDA_HASH, stored: $STORED_HASH)"
  SKIP_LAMBDA_PACKAGING=false
fi
echo ""

# Package Lambda functions (only if code changed)
if [ "$SKIP_LAMBDA_PACKAGING" = "false" ]; then
  echo "Packaging Lambda functions..."

  # Package mvp_service Lambda
  echo "Packaging mvp_service..."
  cd "$LAMBDA_DIR/mvp_service"
  rm -f mvp-service.zip
  zip -q mvp-service.zip handler.py
  $AWS_CMD s3 cp mvp-service.zip "s3://$S3_BUCKET/lambda/mvp-service.zip"
  echo "✓ Uploaded mvp-service.zip"

  # Package seeder Lambda
  echo "Packaging seeder..."
  cd "$LAMBDA_DIR/seeder"
  rm -f seeder.zip
  zip -q seeder.zip handler.py
  $AWS_CMD s3 cp seeder.zip "s3://$S3_BUCKET/lambda/seeder.zip"
  echo "✓ Uploaded seeder.zip"

  cd "$PROJECT_ROOT"

  # Save new hash to S3
  echo "$LAMBDA_HASH" | $AWS_CMD s3 cp - "s3://$S3_BUCKET/.lambda-hash"
  echo "✓ Saved Lambda hash to S3"
  echo "Lambda packaging complete"
else
  echo "Skipping Lambda packaging (code unchanged)"
fi
echo ""

# Upload nested stack templates to S3
echo "Uploading nested stack templates to S3..."
NESTED_TEMPLATE_DIR="$PROJECT_ROOT/infra/nested"
if [ -d "$NESTED_TEMPLATE_DIR" ]; then
  $AWS_CMD s3 cp "$NESTED_TEMPLATE_DIR/" "s3://$S3_BUCKET/nested/" --recursive --exclude ".*"
  echo "✓ Nested templates uploaded to s3://$S3_BUCKET/nested/"
else
  echo "Warning: Nested template directory not found: $NESTED_TEMPLATE_DIR"
fi
echo ""

# Deploy stack
$AWS_CMD cloudformation deploy \
  --stack-name "$STACK_NAME" \
  --template-file "$TEMPLATE_FILE" \
  --s3-bucket "$S3_BUCKET" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    AppName="$APP_NAME" \
    StageName="$STAGE_NAME" \
    ApiDeploymentToken="$API_DEPLOYMENT_TOKEN" \
    UiSeedingMode="$UI_SEEDING_MODE" \
    CreateCloudFront="$CREATE_CLOUDFRONT" \
    DomainName="$DOMAIN_NAME" \
    LambdaCodeS3Bucket="$S3_BUCKET" \
    MvpServiceCodeS3Key="lambda/mvp-service.zip" \
    SeederCodeS3Key="lambda/seeder.zip" \
  --no-fail-on-empty-changeset

echo ""
echo "Stack deployment complete!"
echo ""
echo "To get stack outputs, run:"
echo "  ./scripts/get-outputs.sh"
echo ""
echo "To deploy the UI, run:"
echo "  ./scripts/deploy-ui.sh"

