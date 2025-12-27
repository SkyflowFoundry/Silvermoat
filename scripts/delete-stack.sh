#!/bin/bash
# Delete CloudFormation stack for Silvermoat MVP

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

echo "Deleting CloudFormation stack: $STACK_NAME"
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
  echo "Deletion cancelled."
  exit 0
fi

echo ""
echo "Deleting stack..."

$AWS_CMD cloudformation delete-stack --stack-name "$STACK_NAME"

echo "Stack deletion initiated."
echo "Waiting for deletion to complete..."

$AWS_CMD cloudformation wait stack-delete-complete --stack-name "$STACK_NAME"

echo ""
echo "Stack deletion complete!"

