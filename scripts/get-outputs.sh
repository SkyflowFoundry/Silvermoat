#!/bin/bash
# Get and display CloudFormation stack outputs

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

STACK_NAME="${STACK_NAME:-silvermoat}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-table}"

# AWS Profile support
AWS_PROFILE="${AWS_PROFILE:-}"
AWS_CMD="aws"
if [ -n "$AWS_PROFILE" ]; then
  AWS_CMD="aws --profile $AWS_PROFILE"
fi

# Check AWS CLI and credentials
check_aws_configured

echo "Stack: $STACK_NAME"
echo ""

# Check if stack exists
if ! $AWS_CMD cloudformation describe-stacks --stack-name "$STACK_NAME" > /dev/null 2>&1; then
  echo "Error: Stack '$STACK_NAME' not found"
  exit 1
fi

# Get outputs
if [ "$OUTPUT_FORMAT" = "json" ]; then
  $AWS_CMD cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs" \
    --output json
else
  # Table format (default)
  $AWS_CMD cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs" \
    --output table
  
  echo ""
  echo "Key outputs (for use in scripts):"
  echo ""

  # Export as environment variables
  CF_URL=$($AWS_CMD cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='CloudFrontUrl'].OutputValue" \
    --output text 2>/dev/null || echo "")

  CUSTOM_URL=$($AWS_CMD cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='CustomDomainUrl'].OutputValue" \
    --output text 2>/dev/null || echo "")

  CF_DOMAIN=$($AWS_CMD cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='CloudFrontDomain'].OutputValue" \
    --output text 2>/dev/null || echo "")

  WEB_URL=$($AWS_CMD cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='WebUrl'].OutputValue" \
    --output text 2>/dev/null || echo "")

  API_BASE=$($AWS_CMD cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='ApiBaseUrl'].OutputValue" \
    --output text 2>/dev/null || echo "")

  UI_BUCKET=$($AWS_CMD cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='UiBucketName'].OutputValue" \
    --output text 2>/dev/null || echo "")

  DOCS_BUCKET=$($AWS_CMD cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='DocsBucketName'].OutputValue" \
    --output text 2>/dev/null || echo "")

  if [ -n "$CF_URL" ]; then
    echo "export CF_URL=\"$CF_URL\""
  fi

  if [ -n "$CUSTOM_URL" ]; then
    echo "export CUSTOM_URL=\"$CUSTOM_URL\""
  fi

  if [ -n "$CF_DOMAIN" ]; then
    echo "export CF_DOMAIN=\"$CF_DOMAIN\""
  fi

  if [ -n "$WEB_URL" ]; then
    echo "export WEB_URL=\"$WEB_URL\""
  fi

  if [ -n "$API_BASE" ]; then
    echo "export API_BASE=\"$API_BASE\""
  fi

  if [ -n "$UI_BUCKET" ]; then
    echo "export UI_BUCKET=\"$UI_BUCKET\""
  fi

  if [ -n "$DOCS_BUCKET" ]; then
    echo "export DOCS_BUCKET=\"$DOCS_BUCKET\""
  fi
fi

