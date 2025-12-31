#!/bin/bash
# Fix CloudFront CNAME conflict during CDK migration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

STACK_NAME="${STACK_NAME:-silvermoat}"
CNAME="${CNAME:-silvermoat.net}"

# Check AWS CLI and credentials
check_aws_configured

echo "================================================"
echo "CloudFront CNAME Conflict Resolver"
echo "================================================"
echo ""
echo "Stack: $STACK_NAME"
echo "CNAME: $CNAME"
echo ""

# Step 1: List all CloudFront distributions with the CNAME
echo "Step 1: Finding CloudFront distributions with CNAME '$CNAME'..."
DISTRIBUTIONS=$(aws cloudfront list-distributions --query "DistributionList.Items[?Aliases.Items && contains(Aliases.Items, '$CNAME')].{Id:Id,Status:Status,Enabled:Enabled}" --output json)

if [ "$DISTRIBUTIONS" == "[]" ]; then
  echo "✓ No CloudFront distributions found with CNAME '$CNAME'"
  echo ""
  echo "The CNAME conflict may have been resolved already."
  exit 0
fi

echo "Found CloudFront distribution(s):"
echo "$DISTRIBUTIONS" | jq -r '.[] | "  - ID: \(.Id), Status: \(.Status), Enabled: \(.Enabled)"'
echo ""

# Step 2: Check which distribution belongs to the stack
echo "Step 2: Checking which distribution belongs to stack '$STACK_NAME'..."
STACK_DISTRIBUTION=$(aws cloudformation describe-stack-resources \
  --stack-name "$STACK_NAME" \
  --query 'StackResources[?ResourceType==`AWS::CloudFront::Distribution`].PhysicalResourceId' \
  --output text 2>/dev/null || echo "")

if [ -z "$STACK_DISTRIBUTION" ]; then
  echo "⚠️  No CloudFront distribution found in current stack"
  echo ""
  echo "This means the distribution with the CNAME is orphaned or from a previous stack."
else
  echo "✓ Current stack distribution: $STACK_DISTRIBUTION"
  echo ""
fi

# Step 3: Show action options
echo "Step 3: Choose an action:"
echo ""
echo "OPTIONS:"
echo "  1. List all distributions in detail (for manual inspection)"
echo "  2. Remove CNAME from distribution (requires distribution ID)"
echo "  3. Disable and delete distribution (requires distribution ID)"
echo "  4. Update stack without CloudFront (temporary workaround)"
echo "  5. Exit and handle manually"
echo ""

# For now, just show info and let user decide
echo "================================================"
echo "RECOMMENDED ACTIONS:"
echo "================================================"
echo ""

if [ -n "$STACK_DISTRIBUTION" ]; then
  echo "The stack already has a CloudFront distribution: $STACK_DISTRIBUTION"
  echo ""
  echo "To resolve the conflict:"
  echo "  1. Check if there are multiple distributions with the same CNAME"
  echo "  2. If yes, remove the CNAME from the old/orphaned distribution"
  echo ""
  echo "Commands to remove CNAME from a distribution:"
  echo "  DIST_ID=<old-distribution-id>"
  echo "  aws cloudfront get-distribution-config --id \$DIST_ID > config.json"
  echo "  # Edit config.json: Remove '$CNAME' from Aliases.Items"
  echo "  # Update ETag and DistributionConfig, then:"
  echo "  aws cloudfront update-distribution-config --id \$DIST_ID --if-match <etag> --distribution-config file://config.json"
else
  echo "No CloudFront distribution in current stack."
  echo ""
  echo "The CNAME conflict is from an orphaned distribution."
  echo ""
  echo "To resolve:"
  echo "  1. Find the orphaned distribution ID from the list above"
  echo "  2. Either remove the CNAME or delete the distribution"
  echo ""
  echo "To temporarily deploy without CloudFront:"
  echo "  CREATE_CLOUDFRONT=false ./scripts/deploy-stack.sh"
fi

echo ""
echo "================================================"
echo ""

# Show distribution details
echo "All distributions with CNAME '$CNAME':"
echo "$DISTRIBUTIONS" | jq '.'
