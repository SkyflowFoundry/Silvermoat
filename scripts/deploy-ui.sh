#!/bin/bash
# Build and deploy multi-vertical React UIs to S3 buckets

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

STACK_NAME="${STACK_NAME:-silvermoat}"

# Check AWS CLI and credentials
check_aws_configured

# Build AWS command with profile if set
AWS_CMD="aws"
if [ -n "${AWS_PROFILE:-}" ]; then
  AWS_CMD="aws --profile $AWS_PROFILE"
fi

echo "========================================="
echo "Multi-Vertical UI Deployment"
echo "========================================="
echo ""
echo "Stack: $STACK_NAME"
echo ""

# Get all stack outputs
echo "Fetching stack outputs..."
OUTPUTS=$($AWS_CMD cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs" \
  --output json 2>/dev/null)

if [ -z "$OUTPUTS" ] || [ "$OUTPUTS" == "null" ]; then
  echo "Error: Could not get outputs from CDK stack '$STACK_NAME'"
  echo "Make sure the CDK stack is deployed."
  exit 1
fi

# Extract insurance vertical outputs
INSURANCE_BUCKET=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="InsuranceUiBucketName") | .OutputValue')
INSURANCE_API_URL=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="InsuranceApiUrl") | .OutputValue')

# Extract retail vertical outputs
RETAIL_BUCKET=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="RetailUiBucketName") | .OutputValue')
RETAIL_API_URL=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="RetailApiUrl") | .OutputValue')

# Validate outputs
if [ -z "$INSURANCE_BUCKET" ] || [ "$INSURANCE_BUCKET" == "null" ]; then
  echo "Error: Could not get InsuranceUiBucketName from stack"
  exit 1
fi

if [ -z "$RETAIL_BUCKET" ] || [ "$RETAIL_BUCKET" == "null" ]; then
  echo "Error: Could not get RetailUiBucketName from stack"
  exit 1
fi

echo "Insurance UI Bucket: $INSURANCE_BUCKET"
echo "Insurance API URL: $INSURANCE_API_URL"
echo "Retail UI Bucket: $RETAIL_BUCKET"
echo "Retail API URL: $RETAIL_API_URL"
echo ""

# Function to deploy a vertical UI
deploy_vertical_ui() {
  local VERTICAL=$1
  local UI_DIR=$2
  local BUCKET=$3
  local API_URL=$4

  echo "========================================="
  echo "Deploying $VERTICAL Vertical UI"
  echo "========================================="
  echo ""

  if [ ! -d "$UI_DIR" ]; then
    echo "Error: UI directory not found: $UI_DIR"
    exit 1
  fi

  cd "$UI_DIR"

  # Install dependencies
  echo "Installing dependencies..."
  if [ -f "package-lock.json" ]; then
    npm ci --silent
  else
    echo "No package-lock.json found, running npm install..."
    npm install --silent
  fi

  # Build with API URL
  echo "Building React app..."
  export VITE_API_BASE_URL="$API_URL"
  npm run build

  BUILD_DIR="$UI_DIR/dist"
  if [ ! -d "$BUILD_DIR" ]; then
    echo "Error: Build directory not found: $BUILD_DIR"
    exit 1
  fi

  # Deploy to S3
  echo "Deploying to S3 bucket: $BUCKET"
  $AWS_CMD s3 sync "$BUILD_DIR" "s3://$BUCKET" --delete

  # Set proper content types for index.html
  $AWS_CMD s3 cp "s3://$BUCKET/index.html" "s3://$BUCKET/index.html" \
    --metadata-directive REPLACE \
    --content-type "text/html" \
    --cache-control "no-cache"

  echo "✅ $VERTICAL UI deployed successfully"
  echo ""
}

# Generate architecture diagram (shared across verticals)
echo "Generating architecture diagram..."
pip install -q -r "$PROJECT_ROOT/requirements-docs.txt"
cd "$PROJECT_ROOT"
python3 "$PROJECT_ROOT/scripts/generate-architecture-diagram.py"
echo ""

# Deploy Insurance UI
deploy_vertical_ui "Insurance" "$PROJECT_ROOT/ui-insurance" "$INSURANCE_BUCKET" "$INSURANCE_API_URL"

# Copy architecture diagram to insurance UI bucket
echo "Copying architecture diagram to insurance UI..."
$AWS_CMD s3 cp "$PROJECT_ROOT/docs/architecture.png" "s3://$INSURANCE_BUCKET/architecture.png"
echo ""

# Deploy Retail UI
deploy_vertical_ui "Retail" "$PROJECT_ROOT/ui-retail" "$RETAIL_BUCKET" "$RETAIL_API_URL"

echo "========================================="
echo "✅ All UIs deployed successfully"
echo "========================================="
echo ""
echo "Insurance UI: http://$INSURANCE_BUCKET.s3-website-us-east-1.amazonaws.com"
echo "Retail UI: http://$RETAIL_BUCKET.s3-website-us-east-1.amazonaws.com"
echo ""
