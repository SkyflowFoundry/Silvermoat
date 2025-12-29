#!/bin/bash
# Update Cloudflare DNS record to point to CloudFront distribution
# Only updates if the CloudFront domain has changed (smart update)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

# Required environment variables
: "${CLOUDFLARE_API_TOKEN:?Environment variable CLOUDFLARE_API_TOKEN is required}"
: "${CLOUDFLARE_ZONE_ID:?Environment variable CLOUDFLARE_ZONE_ID is required}"

# Configuration
STACK_NAME="${STACK_NAME:-silvermoat}"
DOMAIN_NAME="${DOMAIN_NAME:-silvermoat.net}"
FORCE_UPDATE="${FORCE_UPDATE:-false}"

# Check AWS CLI and credentials
check_aws_configured

# Build AWS command with profile if set
AWS_CMD="aws"
if [ -n "${AWS_PROFILE:-}" ]; then
  AWS_CMD="aws --profile $AWS_PROFILE"
fi

echo "Checking CloudFront distribution for stack: $STACK_NAME"
echo "Domain: $DOMAIN_NAME"
echo ""

# Get CloudFront domain from stack outputs
CLOUDFRONT_DOMAIN=$($AWS_CMD cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='CloudFrontDomain'].OutputValue" \
  --output text)

if [ -z "$CLOUDFRONT_DOMAIN" ] || [ "$CLOUDFRONT_DOMAIN" = "None" ]; then
  echo "Error: CloudFront domain not found in stack outputs"
  echo "Ensure CreateCloudFront=true and stack deployment succeeded"
  exit 1
fi

echo "CloudFront domain: $CLOUDFRONT_DOMAIN"
echo ""

# Get existing DNS record from Cloudflare
echo "Fetching current DNS record from Cloudflare..."
CURRENT_DNS=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records?name=$DOMAIN_NAME&type=CNAME" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json")

# Parse current DNS target
CURRENT_TARGET=$(echo "$CURRENT_DNS" | grep -o '"content":"[^"]*"' | head -1 | sed 's/"content":"//;s/"//')
RECORD_ID=$(echo "$CURRENT_DNS" | grep -o '"id":"[^"]*"' | head -1 | sed 's/"id":"//;s/"//')

if [ -z "$CURRENT_TARGET" ]; then
  echo "No existing DNS record found for $DOMAIN_NAME"
  ACTION="create"
elif [ "$CURRENT_TARGET" = "$CLOUDFRONT_DOMAIN" ]; then
  if [ "$FORCE_UPDATE" = "true" ]; then
    echo "Current DNS target matches CloudFront domain, but FORCE_UPDATE=true"
    echo "  Current: $CURRENT_TARGET"
    ACTION="update"
  else
    echo "✓ DNS already points to correct CloudFront domain"
    echo "  Current: $CURRENT_TARGET"
    echo "  Target:  $CLOUDFRONT_DOMAIN"
    echo ""
    echo "No DNS update needed. Skipping."
    exit 0
  fi
else
  echo "DNS target mismatch detected:"
  echo "  Current: $CURRENT_TARGET"
  echo "  Target:  $CLOUDFRONT_DOMAIN"
  ACTION="update"
fi

echo ""

# Create or update DNS record
if [ "$ACTION" = "create" ]; then
  echo "Creating new CNAME record..."
  RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data "{
      \"type\": \"CNAME\",
      \"name\": \"$DOMAIN_NAME\",
      \"content\": \"$CLOUDFRONT_DOMAIN\",
      \"ttl\": 1,
      \"proxied\": false
    }")
else
  echo "Updating existing CNAME record..."
  RESPONSE=$(curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records/$RECORD_ID" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data "{
      \"type\": \"CNAME\",
      \"name\": \"$DOMAIN_NAME\",
      \"content\": \"$CLOUDFRONT_DOMAIN\",
      \"ttl\": 1,
      \"proxied\": false
    }")
fi

# Check response
SUCCESS=$(echo "$RESPONSE" | grep -o '"success":[^,]*' | sed 's/"success"://')

if [ "$SUCCESS" = "true" ]; then
  echo "✓ DNS record updated successfully"
  echo ""
  echo "DNS Configuration:"
  echo "  Type:    CNAME"
  echo "  Name:    $DOMAIN_NAME"
  echo "  Target:  $CLOUDFRONT_DOMAIN"
  echo "  Proxied: No (DNS only)"
  echo ""
  echo "Note: DNS propagation may take a few minutes"
else
  echo "Error updating DNS record:"
  echo "$RESPONSE" | grep -o '"message":"[^"]*"' | sed 's/"message":"//;s/"//'
  exit 1
fi
