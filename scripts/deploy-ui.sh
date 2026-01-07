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

# Get Healthcare outputs
HEALTHCARE_BUCKET=""
HEALTHCARE_API_URL=""
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "healthcare" ]; then
  echo "Fetching healthcare stack outputs..."
  HEALTHCARE_OUTPUTS=$(get_stack_outputs "${BASE_STACK_NAME}-healthcare")

  if [ "$HEALTHCARE_OUTPUTS" = "null" ] || [ -z "$HEALTHCARE_OUTPUTS" ]; then
    echo "Error: Could not get outputs from ${BASE_STACK_NAME}-healthcare"
    echo "Make sure the healthcare stack is deployed."
    exit 1
  fi

  HEALTHCARE_BUCKET=$(echo "$HEALTHCARE_OUTPUTS" | jq -r '.[] | select(.OutputKey=="HealthcareUiBucketName") | .OutputValue')
  HEALTHCARE_API_URL=$(echo "$HEALTHCARE_OUTPUTS" | jq -r '.[] | select(.OutputKey=="HealthcareApiUrl") | .OutputValue')

  echo "Healthcare UI Bucket: $HEALTHCARE_BUCKET"
  echo "Healthcare API URL: $HEALTHCARE_API_URL"
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

# Generate architecture diagrams based on vertical being deployed
# Only if Graphviz is installed (optional, non-blocking)
if command -v dot >/dev/null 2>&1; then
  # Determine which diagrams to generate based on VERTICAL
  # - insurance: Generate only insurance diagrams (2 files)
  # - retail: Generate only retail diagrams (2 files)
  # - landing: Generate all diagrams (6 files, but landing only uses multi-vertical ones)
  # - all: Generate all diagrams (6 files)
  DIAGRAM_VERTICAL="$VERTICAL"
  if [ "$VERTICAL" = "landing" ]; then
    DIAGRAM_VERTICAL="all"  # Landing needs multi-vertical diagrams from --vertical all
  fi

  echo "Generating architecture diagrams for: $DIAGRAM_VERTICAL"
  pip install -q -r "$PROJECT_ROOT/requirements-docs.txt" || echo "Warning: Failed to install diagram dependencies"
  cd "$PROJECT_ROOT"
  python3 "$PROJECT_ROOT/scripts/generate-architecture-diagram.py" --vertical "$DIAGRAM_VERTICAL" || echo "Warning: Failed to generate diagrams"
  echo ""
else
  echo "Skipping architecture diagram generation (Graphviz not installed)"
  echo ""
fi

# Deploy Insurance UI
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "insurance" ]; then
  deploy_vertical_ui "Insurance" "$PROJECT_ROOT/ui-insurance" "$INSURANCE_BUCKET" "$INSURANCE_API_URL"

  # Copy insurance-specific architecture diagrams to insurance UI bucket
  if [ -f "$PROJECT_ROOT/docs/architecture-insurance.png" ]; then
    echo "Copying insurance architecture diagrams to insurance UI..."
    $AWS_CMD s3 cp "$PROJECT_ROOT/docs/architecture-insurance.png" "s3://$INSURANCE_BUCKET/architecture-insurance.png"
    $AWS_CMD s3 cp "$PROJECT_ROOT/docs/data-flow-insurance.png" "s3://$INSURANCE_BUCKET/data-flow-insurance.png"
    echo ""
  fi
fi

# Deploy Retail UI
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "retail" ]; then
  deploy_vertical_ui "Retail" "$PROJECT_ROOT/ui-retail" "$RETAIL_BUCKET" "$RETAIL_API_URL"

  # Copy retail-specific architecture diagrams to retail UI bucket
  if [ -f "$PROJECT_ROOT/docs/architecture-retail.png" ]; then
    echo "Copying retail architecture diagrams to retail UI..."
    $AWS_CMD s3 cp "$PROJECT_ROOT/docs/architecture-retail.png" "s3://$RETAIL_BUCKET/architecture-retail.png"
    $AWS_CMD s3 cp "$PROJECT_ROOT/docs/data-flow-retail.png" "s3://$RETAIL_BUCKET/data-flow-retail.png"
    echo ""
  fi
fi

# Deploy Healthcare UI
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "healthcare" ]; then
  deploy_vertical_ui "Healthcare" "$PROJECT_ROOT/ui-healthcare" "$HEALTHCARE_BUCKET" "$HEALTHCARE_API_URL"

  # Copy healthcare-specific architecture diagrams to healthcare UI bucket
  if [ -f "$PROJECT_ROOT/docs/architecture-healthcare.png" ]; then
    echo "Copying healthcare architecture diagrams to healthcare UI..."
    $AWS_CMD s3 cp "$PROJECT_ROOT/docs/architecture-healthcare.png" "s3://$HEALTHCARE_BUCKET/architecture-healthcare.png"
    $AWS_CMD s3 cp "$PROJECT_ROOT/docs/data-flow-healthcare.png" "s3://$HEALTHCARE_BUCKET/data-flow-healthcare.png"
    echo ""
  fi
fi

# Deploy Landing UI
if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "landing" ]; then
  # Get insurance, retail, and healthcare WebUrls for landing page links
  INSURANCE_WEB_URL=""
  RETAIL_WEB_URL=""
  HEALTHCARE_WEB_URL=""

  # Fetch insurance URL if stack exists (prefer CustomDomainUrl over WebUrl)
  if aws cloudformation describe-stacks --stack-name "${BASE_STACK_NAME}-insurance" &>/dev/null; then
    # Try CustomDomainUrl first (DNS name like insurance.silvermoat.net)
    INSURANCE_WEB_URL=$(aws cloudformation describe-stacks \
      --stack-name "${BASE_STACK_NAME}-insurance" \
      --query 'Stacks[0].Outputs[?OutputKey==`CustomDomainUrl`].OutputValue' \
      --output text 2>/dev/null || echo "")

    # Fallback to WebUrl if CustomDomainUrl not available (CloudFront or S3 URL)
    if [ -z "$INSURANCE_WEB_URL" ]; then
      INSURANCE_WEB_URL=$(aws cloudformation describe-stacks \
        --stack-name "${BASE_STACK_NAME}-insurance" \
        --query 'Stacks[0].Outputs[?OutputKey==`WebUrl`].OutputValue' \
        --output text 2>/dev/null || echo "")
    fi
  fi

  # Fetch retail URL if stack exists (prefer CustomDomainUrl over WebUrl)
  if aws cloudformation describe-stacks --stack-name "${BASE_STACK_NAME}-retail" &>/dev/null; then
    # Try CustomDomainUrl first (DNS name like retail.silvermoat.net)
    RETAIL_WEB_URL=$(aws cloudformation describe-stacks \
      --stack-name "${BASE_STACK_NAME}-retail" \
      --query 'Stacks[0].Outputs[?OutputKey==`CustomDomainUrl`].OutputValue' \
      --output text 2>/dev/null || echo "")

    # Fallback to WebUrl if CustomDomainUrl not available (CloudFront or S3 URL)
    if [ -z "$RETAIL_WEB_URL" ]; then
      RETAIL_WEB_URL=$(aws cloudformation describe-stacks \
        --stack-name "${BASE_STACK_NAME}-retail" \
        --query 'Stacks[0].Outputs[?OutputKey==`WebUrl`].OutputValue' \
        --output text 2>/dev/null || echo "")
    fi
  fi

  # Fetch healthcare URL if stack exists (prefer CustomDomainUrl over WebUrl)
  if aws cloudformation describe-stacks --stack-name "${BASE_STACK_NAME}-healthcare" &>/dev/null; then
    # Try CustomDomainUrl first (DNS name like healthcare.silvermoat.net)
    HEALTHCARE_WEB_URL=$(aws cloudformation describe-stacks \
      --stack-name "${BASE_STACK_NAME}-healthcare" \
      --query 'Stacks[0].Outputs[?OutputKey==`CustomDomainUrl`].OutputValue' \
      --output text 2>/dev/null || echo "")

    # Fallback to WebUrl if CustomDomainUrl not available (CloudFront or S3 URL)
    if [ -z "$HEALTHCARE_WEB_URL" ]; then
      HEALTHCARE_WEB_URL=$(aws cloudformation describe-stacks \
        --stack-name "${BASE_STACK_NAME}-healthcare" \
        --query 'Stacks[0].Outputs[?OutputKey==`WebUrl`].OutputValue' \
        --output text 2>/dev/null || echo "")
    fi
  fi

  # Export as environment variables for Vite build
  export VITE_INSURANCE_URL="$INSURANCE_WEB_URL"
  export VITE_RETAIL_URL="$RETAIL_WEB_URL"
  export VITE_HEALTHCARE_URL="$HEALTHCARE_WEB_URL"

  deploy_vertical_ui "Landing" "$PROJECT_ROOT/ui-landing" "$LANDING_BUCKET" ""

  # Copy multi-vertical architecture diagrams to landing UI bucket
  if [ -f "$PROJECT_ROOT/docs/architecture.png" ]; then
    echo "Copying multi-vertical architecture diagrams to landing UI..."
    $AWS_CMD s3 cp "$PROJECT_ROOT/docs/architecture.png" "s3://$LANDING_BUCKET/architecture.png"
    $AWS_CMD s3 cp "$PROJECT_ROOT/docs/data-flow.png" "s3://$LANDING_BUCKET/data-flow.png"
    echo ""
  fi
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
