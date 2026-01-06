#!/bin/bash
# Delete and redeploy complete Silvermoat stack (infrastructure + UI) using CDK

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

STACK_NAME="${STACK_NAME:-silvermoat}"
export STACK_NAME

# AWS Profile support
AWS_PROFILE="${AWS_PROFILE:-}"
AWS_CMD="aws"
if [ -n "$AWS_PROFILE" ]; then
  AWS_CMD="aws --profile $AWS_PROFILE"
  echo "Using AWS profile: $AWS_PROFILE"
fi

# Check AWS CLI and credentials
check_aws_configured

echo "=========================================="
echo "Silvermoat Full Redeployment (CDK)"
echo "=========================================="
echo ""
echo "This will:"
echo "  1. Delete the existing CDK stack: $STACK_NAME"
echo "  2. Redeploy everything from scratch"
echo ""

# ==========================================
# Step 1: Delete existing stack
# ==========================================
echo "Step 1: Deleting existing CDK stack"
echo "----------------------------------------"
echo ""

# Check if stack exists
STACK_STATUS=$($AWS_CMD cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].StackStatus" \
  --output text 2>/dev/null || echo "DOES_NOT_EXIST")

if [ "$STACK_STATUS" = "DOES_NOT_EXIST" ]; then
  echo "Stack '$STACK_NAME' does not exist. Skipping deletion."
  echo ""
else
  echo "Stack '$STACK_NAME' exists (Status: $STACK_STATUS)"
  echo ""
  echo "WARNING: This will delete all resources in the stack, including:"
  echo "  - S3 buckets (will be emptied automatically)"
  echo "  - DynamoDB tables (will be wiped automatically)"
  echo "  - Lambda functions"
  echo "  - API Gateway"
  echo "  - All other resources"
  echo ""
  read -p "Are you sure you want to continue? (yes/no): " confirm

  if [ "$confirm" != "yes" ]; then
    echo "Redeployment cancelled."
    exit 0
  fi

  echo ""
  echo "Deleting CDK stack..."

  # Check if CDK CLI is installed
  if ! command -v cdk >/dev/null 2>&1; then
    echo "Warning: CDK CLI not found. Falling back to CloudFormation delete."
    $AWS_CMD cloudformation delete-stack --stack-name "$STACK_NAME"
  else
    cd "$PROJECT_ROOT/cdk"
    cdk destroy "$STACK_NAME" --force
  fi

  echo "Stack deletion initiated."
  echo "Waiting for deletion to complete..."

  $AWS_CMD cloudformation wait stack-delete-complete --stack-name "$STACK_NAME"

  echo ""
  echo "Stack deletion complete!"
  echo ""
fi

# ==========================================
# Step 2: Deploy everything
# ==========================================
echo "Step 2: Deploying fresh stack"
echo "----------------------------------------"
echo ""

# Call deploy-all.sh with the same environment variables
"$SCRIPT_DIR/deploy-all.sh"

echo ""
echo "=========================================="
echo "Redeployment Complete!"
echo "=========================================="
echo ""
