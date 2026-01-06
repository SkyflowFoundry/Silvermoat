#!/bin/bash
# Build and deploy multi-vertical React UIs to S3 buckets

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

BASE_STACK_NAME="${STACK_NAME:-silvermoat}"
VERTICAL="${VERTICAL:-all}"  # Can be: all, insurance, retail, landing

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
echo "Base Stack: $BASE_STACK_NAME"
echo "Deploying: $VERTICAL"
echo ""

# Function to get stack outputs
get_stack_outputs() {
  local stack_name=$1
  $AWS_CMD cloudformation describe-stacks \
    --stack-name "$stack_name" \
    --query "Stacks[0].Outputs" \
    --output json 2>/dev/null || echo "null"
}

# Get Insurance outputs
INSURANCE_BUCKET=""
INSURANCE_API_URL=""
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "insurance" ]; then
  echo "Fetching insurance stack outputs..."
  INSURANCE_OUTPUTS=$(get_stack_outputs "${BASE_STACK_NAME}-insurance")

  if [ "$INSURANCE_OUTPUTS" = "null" ] || [ -z "$INSURANCE_OUTPUTS" ]; then
    echo "Error: Could not get outputs from ${BASE_STACK_NAME}-insurance"
    echo "Make sure the insurance stack is deployed."
    exit 1
  fi

  INSURANCE_BUCKET=$(echo "$INSURANCE_OUTPUTS" | jq -r '.[] | select(.OutputKey=="InsuranceUiBucketName") | .OutputValue')
  INSURANCE_API_URL=$(echo "$INSURANCE_OUTPUTS" | jq -r '.[] | select(.OutputKey=="InsuranceApiUrl") | .OutputValue')

  echo "Insurance UI Bucket: $INSURANCE_BUCKET"
  echo "Insurance API URL: $INSURANCE_API_URL"
  echo ""
fi

# Get Retail outputs
RETAIL_BUCKET=""
RETAIL_API_URL=""
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "retail" ]; then
  echo "Fetching retail stack outputs..."
  RETAIL_OUTPUTS=$(get_stack_outputs "${BASE_STACK_NAME}-retail")

  if [ "$RETAIL_OUTPUTS" = "null" ] || [ -z "$RETAIL_OUTPUTS" ]; then
    echo "Error: Could not get outputs from ${BASE_STACK_NAME}-retail"
    echo "Make sure the retail stack is deployed."
    exit 1
  fi

  RETAIL_BUCKET=$(echo "$RETAIL_OUTPUTS" | jq -r '.[] | select(.OutputKey=="RetailUiBucketName") | .OutputValue')
  RETAIL_API_URL=$(echo "$RETAIL_OUTPUTS" | jq -r '.[] | select(.OutputKey=="RetailApiUrl") | .OutputValue')

  echo "Retail UI Bucket: $RETAIL_BUCKET"
  echo "Retail API URL: $RETAIL_API_URL"
  echo ""
fi

# Get Landing outputs
LANDING_BUCKET=""
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "landing" ]; then
  echo "Fetching landing stack outputs..."
  LANDING_OUTPUTS=$(get_stack_outputs "${BASE_STACK_NAME}-landing")

  if [ "$LANDING_OUTPUTS" = "null" ] || [ -z "$LANDING_OUTPUTS" ]; then
    echo "Error: Could not get outputs from ${BASE_STACK_NAME}-landing"
    echo "Make sure the landing stack is deployed."
    exit 1
  fi

  LANDING_BUCKET=$(echo "$LANDING_OUTPUTS" | jq -r '.[] | select(.OutputKey=="LandingUiBucketName") | .OutputValue')

  echo "Landing UI Bucket: $LANDING_BUCKET"
  echo ""
fi

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

  # Build with API URL (if provided)
  echo "Building React app..."
  if [ -n "$API_URL" ]; then
    export VITE_API_BASE_URL="$API_URL"
  fi
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
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "insurance" ]; then
  deploy_vertical_ui "Insurance" "$PROJECT_ROOT/ui-insurance" "$INSURANCE_BUCKET" "$INSURANCE_API_URL"

  # Copy architecture diagram to insurance UI bucket
  echo "Copying architecture diagram to insurance UI..."
  $AWS_CMD s3 cp "$PROJECT_ROOT/docs/architecture.png" "s3://$INSURANCE_BUCKET/architecture.png"
  echo ""
fi

# Deploy Retail UI
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "retail" ]; then
  deploy_vertical_ui "Retail" "$PROJECT_ROOT/ui-retail" "$RETAIL_BUCKET" "$RETAIL_API_URL"
  echo ""
fi

# Deploy Landing UI
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "landing" ]; then
  deploy_vertical_ui "Landing" "$PROJECT_ROOT/ui-landing" "$LANDING_BUCKET" ""
  echo ""
fi

echo "========================================="
echo "✅ UI Deployment Complete"
echo "========================================="
echo ""
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "insurance" ]; then
  echo "Insurance UI: http://$INSURANCE_BUCKET.s3-website-us-east-1.amazonaws.com"
fi
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "retail" ]; then
  echo "Retail UI: http://$RETAIL_BUCKET.s3-website-us-east-1.amazonaws.com"
fi
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "landing" ]; then
  echo "Landing UI: http://$LANDING_BUCKET.s3-website-us-east-1.amazonaws.com"
fi
echo ""
