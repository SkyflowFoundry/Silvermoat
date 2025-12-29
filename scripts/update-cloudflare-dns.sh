#!/bin/bash
set -e

# Smart Cloudflare DNS update script
# Only updates DNS when CloudFront domain changes (rare)
# Skips update for Lambda/S3/DynamoDB changes (common)

# Usage:
#   ./scripts/update-cloudflare-dns.sh
#   FORCE_UPDATE=true ./scripts/update-cloudflare-dns.sh

# Required environment variables:
# - CLOUDFLARE_API_TOKEN: API token with DNS edit permissions
# - CLOUDFLARE_ZONE_ID: Zone ID for target domain
# - STACK_NAME: CloudFormation stack name (default: silvermoat)
# - DOMAIN_NAME: Domain name to update (default: silvermoat.net)

# Optional:
# - FORCE_UPDATE: Set to "true" to force update regardless of comparison

STACK_NAME="${STACK_NAME:-silvermoat}"
DOMAIN_NAME="${DOMAIN_NAME:-silvermoat.net}"
FORCE_UPDATE="${FORCE_UPDATE:-false}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

error() {
    echo -e "${RED}✗ $1${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Validate required environment variables
if [[ -z "$CLOUDFLARE_API_TOKEN" ]]; then
    error "CLOUDFLARE_API_TOKEN environment variable not set"
fi

if [[ -z "$CLOUDFLARE_ZONE_ID" ]]; then
    error "CLOUDFLARE_ZONE_ID environment variable not set"
fi

# Get CloudFront domain from CloudFormation stack outputs
info "Fetching CloudFront domain from stack: $STACK_NAME"
CLOUDFRONT_DOMAIN=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='CloudFrontDomain'].OutputValue" \
    --output text 2>/dev/null)

if [[ -z "$CLOUDFRONT_DOMAIN" || "$CLOUDFRONT_DOMAIN" == "None" ]]; then
    error "Could not fetch CloudFront domain from stack outputs"
fi

success "CloudFront domain: $CLOUDFRONT_DOMAIN"

# Get current DNS record from Cloudflare
info "Fetching current DNS record for: $DOMAIN_NAME"
DNS_RECORD_RESPONSE=$(curl -s -X GET \
    "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records?name=$DOMAIN_NAME&type=CNAME" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: application/json")

# Check for API errors
if echo "$DNS_RECORD_RESPONSE" | jq -e '.success == false' >/dev/null 2>&1; then
    ERRORS=$(echo "$DNS_RECORD_RESPONSE" | jq -r '.errors[] | .message' 2>/dev/null || echo "Unknown error")
    error "Cloudflare API error: $ERRORS"
fi

# Extract current DNS target
CURRENT_DNS_TARGET=$(echo "$DNS_RECORD_RESPONSE" | jq -r '.result[0].content // empty')
DNS_RECORD_ID=$(echo "$DNS_RECORD_RESPONSE" | jq -r '.result[0].id // empty')

if [[ -z "$CURRENT_DNS_TARGET" ]]; then
    info "No existing DNS record found. Will create new record."
    CREATE_NEW_RECORD=true
else
    success "Current DNS target: $CURRENT_DNS_TARGET"
    CREATE_NEW_RECORD=false
fi

# Compare current vs target (skip update if identical, unless forced)
if [[ "$FORCE_UPDATE" != "true" && "$CURRENT_DNS_TARGET" == "$CLOUDFRONT_DOMAIN" ]]; then
    success "DNS already points to correct CloudFront domain"
    echo "  Current: $CURRENT_DNS_TARGET"
    echo "  Target:  $CLOUDFRONT_DOMAIN"
    echo ""
    info "No DNS update needed. Skipping."
    exit 0
fi

# DNS update required
if [[ "$FORCE_UPDATE" == "true" ]]; then
    info "Force update enabled. Updating DNS record..."
elif [[ "$CREATE_NEW_RECORD" == "true" ]]; then
    info "Creating new DNS record..."
else
    info "CloudFront domain changed. Updating DNS record..."
    echo "  Old: $CURRENT_DNS_TARGET"
    echo "  New: $CLOUDFRONT_DOMAIN"
fi

# Prepare DNS record data
DNS_RECORD_DATA=$(jq -n \
    --arg name "$DOMAIN_NAME" \
    --arg content "$CLOUDFRONT_DOMAIN" \
    '{
        type: "CNAME",
        name: $name,
        content: $content,
        ttl: 1,
        proxied: false
    }')

# Create or update DNS record
if [[ "$CREATE_NEW_RECORD" == "true" ]]; then
    # Create new record
    UPDATE_RESPONSE=$(curl -s -X POST \
        "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "$DNS_RECORD_DATA")
else
    # Update existing record
    UPDATE_RESPONSE=$(curl -s -X PUT \
        "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records/$DNS_RECORD_ID" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "$DNS_RECORD_DATA")
fi

# Check update success
if echo "$UPDATE_RESPONSE" | jq -e '.success == true' >/dev/null 2>&1; then
    success "DNS record updated successfully"
    echo "  Domain: $DOMAIN_NAME"
    echo "  Target: $CLOUDFRONT_DOMAIN"
    echo "  Proxied: No (DNS only)"
    echo ""
    info "DNS propagation may take a few minutes"
else
    ERRORS=$(echo "$UPDATE_RESPONSE" | jq -r '.errors[] | .message' 2>/dev/null || echo "Unknown error")
    error "Failed to update DNS record: $ERRORS"
fi
