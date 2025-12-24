#!/bin/bash
# Smoke test for Silvermoat MVP

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

STACK_NAME="${STACK_NAME:-silvermoat}"

# AWS Profile support
AWS_PROFILE="${AWS_PROFILE:-}"
AWS_CMD="aws"
if [ -n "$AWS_PROFILE" ]; then
  AWS_CMD="aws --profile $AWS_PROFILE"
fi

# Check AWS CLI and credentials
check_aws_configured

echo "Running smoke tests for stack: $STACK_NAME"
echo ""

# Get API base URL
API_BASE=$($AWS_CMD cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='ApiBaseUrl'].OutputValue" \
  --output text 2>/dev/null || echo "")

if [ -z "$API_BASE" ]; then
  echo "Error: Could not get ApiBaseUrl from stack '$STACK_NAME'"
  exit 1
fi

echo "API Base URL: $API_BASE"
echo ""

# Test 1: Create a quote
echo "Test 1: Creating a quote..."
QUOTE_RESPONSE=$(curl -s -X POST "$API_BASE/quote" \
  -H "Content-Type: application/json" \
  -d '{"name":"Smoke Test User","zip":"12345"}')

if [ $? -ne 0 ]; then
  echo "❌ Failed to create quote"
  exit 1
fi

echo "Response: $QUOTE_RESPONSE"

# Extract quote ID (try jq first, then fallback to grep)
if command -v jq > /dev/null 2>&1; then
  QUOTE_ID=$(echo "$QUOTE_RESPONSE" | jq -r '.id // .item.id // empty' 2>/dev/null || echo "")
else
  # Fallback: extract using grep/sed
  QUOTE_ID=$(echo "$QUOTE_RESPONSE" | grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' || echo "")
  # If that didn't work, try the item.id path
  if [ -z "$QUOTE_ID" ]; then
    QUOTE_ID=$(echo "$QUOTE_RESPONSE" | grep -o '"item"[^}]*"id"[^}]*"[^"]*"' | sed 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' || echo "")
  fi
fi

if [ -z "$QUOTE_ID" ]; then
  echo "⚠️  Warning: Could not extract quote ID from response"
  echo "Response was: $QUOTE_RESPONSE"
else
  echo "✓ Quote created with ID: $QUOTE_ID"
  
  # Test 2: Get the quote
  echo ""
  echo "Test 2: Retrieving quote..."
  GET_RESPONSE=$(curl -s -X GET "$API_BASE/quote/$QUOTE_ID" \
    -H "Content-Type: application/json")
  
  if [ $? -ne 0 ]; then
    echo "❌ Failed to get quote"
    exit 1
  fi
  
  echo "Response: $GET_RESPONSE"
  
  if echo "$GET_RESPONSE" | grep -q "$QUOTE_ID"; then
    echo "✓ Quote retrieved successfully"
  else
    echo "⚠️  Warning: Quote ID not found in response"
  fi
fi

# Test 3: Check root endpoint
echo ""
echo "Test 3: Checking root endpoint..."
ROOT_RESPONSE=$(curl -s -X GET "$API_BASE/" \
  -H "Content-Type: application/json")

if [ $? -ne 0 ]; then
  echo "❌ Failed to access root endpoint"
  exit 1
fi

if echo "$ROOT_RESPONSE" | grep -q "Silvermoat"; then
  echo "✓ Root endpoint working"
else
  echo "⚠️  Warning: Unexpected root endpoint response"
fi

# Test 4: Check UI accessibility (if WebUrl is available)
WEB_URL=$($AWS_CMD cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='WebUrl'].OutputValue" \
  --output text 2>/dev/null || echo "")

if [ -n "$WEB_URL" ]; then
  echo ""
  echo "Test 4: Checking UI accessibility..."
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$WEB_URL" || echo "000")
  
  if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ UI is accessible (HTTP $HTTP_CODE)"
  else
    echo "⚠️  Warning: UI returned HTTP $HTTP_CODE"
  fi
fi

echo ""
echo "Smoke tests complete!"
echo ""
echo "To check CloudWatch logs for errors, run:"
echo "  $AWS_CMD logs tail /aws/lambda/\$($AWS_CMD cloudformation describe-stack-resources --stack-name $STACK_NAME --query 'StackResources[?LogicalResourceId==\`MvpServiceFunction\`].PhysicalResourceId' --output text) --follow"

