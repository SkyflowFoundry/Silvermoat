#!/bin/bash
# Delete CloudFormation stack for Silvermoat MVP

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

STACK_NAME="${STACK_NAME:-silvermoat}"

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

# Build AWS command with profile if set
AWS_CMD="aws"
if [ -n "${AWS_PROFILE:-}" ]; then
  AWS_CMD="aws --profile $AWS_PROFILE"
fi

echo "Deleting CloudFormation stack: $STACK_NAME"
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

echo ""
echo "Deleting stack..."

$AWS_CMD cloudformation delete-stack --stack-name "$STACK_NAME"

echo "Stack deletion initiated."
echo "Waiting for deletion to complete..."

$AWS_CMD cloudformation wait stack-delete-complete --stack-name "$STACK_NAME"

echo ""
echo "Stack deletion complete!"

