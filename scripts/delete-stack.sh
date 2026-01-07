#!/bin/bash
# Delete CDK stack for Silvermoat MVP

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

STACK_NAME="${STACK_NAME:-silvermoat}"

# Extract vertical from stack name if present
# Format: silvermoat-{vertical} or silvermoat-test-pr-{N}-{vertical}
BASE_STACK_NAME="$STACK_NAME"

if [[ "$STACK_NAME" == *-insurance ]]; then
    export VERTICAL="insurance"
    # Remove vertical suffix to get base name for CDK
    BASE_STACK_NAME="${STACK_NAME%-insurance}"
elif [[ "$STACK_NAME" == *-retail ]]; then
    export VERTICAL="retail"
    BASE_STACK_NAME="${STACK_NAME%-retail}"
elif [[ "$STACK_NAME" == *-landing ]]; then
    export VERTICAL="landing"
    BASE_STACK_NAME="${STACK_NAME%-landing}"
elif [[ "$STACK_NAME" == *-certificate ]]; then
    export VERTICAL="certificate"
    BASE_STACK_NAME="${STACK_NAME%-certificate}"
fi

echo "Stack to delete: $STACK_NAME"
if [[ -n "$VERTICAL" ]]; then
    echo "Detected vertical: $VERTICAL"
    echo "Base stack name (for CDK): $BASE_STACK_NAME"
fi
echo ""

# Parse command line arguments
SKIP_CONFIRM=false
while [[ $# -gt 0 ]]; do
  case $1 in
    --yes|-y)
      SKIP_CONFIRM=true
      shift
      ;;
    *)
      shift
      ;;
  esac
done

# Check AWS CLI and credentials
check_aws_configured

echo "Deleting CDK stack: $STACK_NAME"
echo ""
echo "WARNING: This will delete all resources in the stack, including:"
echo "  - S3 buckets (will be emptied automatically)"
echo "  - DynamoDB tables (will be wiped automatically)"
echo "  - Lambda functions"
echo "  - API Gateway"
echo "  - All other resources"
echo ""

# Skip confirmation if --yes flag or non-interactive
if [ "$SKIP_CONFIRM" = false ] && [ -t 0 ]; then
  read -p "Are you sure you want to continue? (yes/no): " confirm
  if [ "$confirm" != "yes" ]; then
    echo "Deletion cancelled."
    exit 0
  fi
else
  echo "Skipping confirmation (non-interactive or --yes flag)"
fi

# Check if CDK CLI is installed
if ! command -v cdk >/dev/null 2>&1; then
  echo "Error: AWS CDK CLI not found. Install with:"
  echo "  npm install -g aws-cdk"
  exit 1
fi

echo ""
echo "Deleting stack..."

cd "$PROJECT_ROOT/cdk"

# Export BASE_STACK_NAME for CDK (app.py will append vertical suffix)
export STACK_NAME="$BASE_STACK_NAME"

# Determine which stack to destroy
if [[ -n "$VERTICAL" ]]; then
  # CDK will find the stack by reconstructing: {BASE_STACK_NAME}-{VERTICAL}
  DESTROY_TARGET="$BASE_STACK_NAME-$VERTICAL"
else
  # No vertical detected - destroy all stacks matching base name
  DESTROY_TARGET="$BASE_STACK_NAME*"
fi

echo "CDK destroy target: $DESTROY_TARGET"
cdk destroy "$DESTROY_TARGET" --force

echo ""
echo "Stack deletion complete!"

