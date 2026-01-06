#!/bin/bash
set -e

# Smart Cloudflare DNS update script for multi-vertical architecture
# Creates/updates:
# - Vertical-specific subdomain (insurance.silvermoat.net, retail.silvermoat.net)
# - Wildcard subdomain (*.silvermoat.net) pointing to insurance vertical

# Usage:
#   STACK_NAME=silvermoat-insurance ./scripts/update-cloudflare-dns.sh
#   STACK_NAME=silvermoat-retail ./scripts/update-cloudflare-dns.sh
#   FORCE_UPDATE=true ./scripts/update-cloudflare-dns.sh

# Required environment variables:
# - CLOUDFLARE_API_TOKEN: API token with DNS edit permissions
# - CLOUDFLARE_ZONE_ID: Zone ID for target domain
# - STACK_NAME: CloudFormation stack name (e.g., silvermoat-insurance)
# - DOMAIN_NAME: Base domain name (default: silvermoat.net)

# Optional:
# - FORCE_UPDATE: Set to "true" to force update regardless of comparison
# - CREATE_WILDCARD: Set to "true" to create/update wildcard record (default: true for insurance)

STACK_NAME="${STACK_NAME:-silvermoat}"
DOMAIN_NAME="${DOMAIN_NAME:-silvermoat.net}"
FORCE_UPDATE="${FORCE_UPDATE:-false}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

header() {
    echo -e "${BLUE}▶ $1${NC}"
}

# Validate required environment variables
if [[ -z "$CLOUDFLARE_API_TOKEN" ]]; then
    error "CLOUDFLARE_API_TOKEN environment variable not set"
fi

if [[ -z "$CLOUDFLARE_ZONE_ID" ]]; then
    error "CLOUDFLARE_ZONE_ID environment variable not set"
fi

# Detect vertical from stack name
if [[ "$STACK_NAME" == *-insurance ]]; then
    VERTICAL="insurance"
    CREATE_WILDCARD="${CREATE_WILDCARD:-true}"  # Default: create wildcard for insurance
elif [[ "$STACK_NAME" == *-retail ]]; then
    VERTICAL="retail"
    CREATE_WILDCARD="${CREATE_WILDCARD:-false}"  # Default: no wildcard for retail
else
    # Legacy single-stack behavior
    VERTICAL=""
    CREATE_WILDCARD="${CREATE_WILDCARD:-false}"
fi

# Determine subdomain
if [[ -n "$VERTICAL" ]]; then
    SUBDOMAIN="${VERTICAL}.${DOMAIN_NAME}"
    CLOUDFRONT_OUTPUT_KEY="${VERTICAL^}CloudFrontDomain"  # InsuranceCloudFrontDomain or RetailCloudFrontDomain
else
    SUBDOMAIN="$DOMAIN_NAME"
    CLOUDFRONT_OUTPUT_KEY="CloudFrontDomain"
fi

header "DNS Configuration for $STACK_NAME"
echo "  Vertical: ${VERTICAL:-none}"
echo "  Subdomain: $SUBDOMAIN"
echo "  Wildcard: $CREATE_WILDCARD"
echo ""

# Function to update a single DNS record
update_dns_record() {
    local record_name="$1"
    local cloudfront_domain="$2"

    header "Processing DNS record: $record_name"

    # Get current DNS record from Cloudflare
    info "Fetching current DNS record..."
    local dns_response=$(curl -s -X GET \
        "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records?name=$record_name&type=CNAME" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json")

    # Check for API errors
    if echo "$dns_response" | jq -e '.success == false' >/dev/null 2>&1; then
        local errors=$(echo "$dns_response" | jq -r '.errors[] | .message' 2>/dev/null || echo "Unknown error")
        error "Cloudflare API error: $errors"
    fi

    # Extract current DNS target
    local current_target=$(echo "$dns_response" | jq -r '.result[0].content // empty')
    local record_id=$(echo "$dns_response" | jq -r '.result[0].id // empty')

    local create_new=false
    if [[ -z "$current_target" ]]; then
        info "No existing DNS record found. Will create new record."
        create_new=true
    else
        success "Current DNS target: $current_target"
    fi

    # Compare current vs target (skip update if identical, unless forced)
    if [[ "$FORCE_UPDATE" != "true" && "$current_target" == "$cloudfront_domain" ]]; then
        success "DNS already points to correct CloudFront domain"
        echo "  Current: $current_target"
        echo "  Target:  $cloudfront_domain"
        echo ""
        info "No DNS update needed. Skipping."
        return 0
    fi

    # DNS update required
    if [[ "$FORCE_UPDATE" == "true" ]]; then
        info "Force update enabled. Updating DNS record..."
    elif [[ "$create_new" == "true" ]]; then
        info "Creating new DNS record..."
    else
        info "CloudFront domain changed. Updating DNS record..."
        echo "  Old: $current_target"
        echo "  New: $cloudfront_domain"
    fi

    # Prepare DNS record data
    local dns_data=$(jq -n \
        --arg name "$record_name" \
        --arg content "$cloudfront_domain" \
        '{
            type: "CNAME",
            name: $name,
            content: $content,
            ttl: 1,
            proxied: false
        }')

    # Create or update DNS record
    local update_response
    if [[ "$create_new" == "true" ]]; then
        update_response=$(curl -s -X POST \
            "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
            -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
            -H "Content-Type: application/json" \
            --data "$dns_data")
    else
        update_response=$(curl -s -X PUT \
            "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records/$record_id" \
            -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
            -H "Content-Type: application/json" \
            --data "$dns_data")
    fi

    # Check update success
    if echo "$update_response" | jq -e '.success == true' >/dev/null 2>&1; then
        success "DNS record updated successfully"
        echo "  Domain: $record_name"
        echo "  Target: $cloudfront_domain"
        echo "  Proxied: No (DNS only)"
        echo ""
    else
        local errors=$(echo "$update_response" | jq -r '.errors[] | .message' 2>/dev/null || echo "Unknown error")
        error "Failed to update DNS record: $errors"
    fi
}

# Get CloudFront domain from CloudFormation stack outputs
info "Fetching CloudFront domain from stack: $STACK_NAME"

# Try vertical-specific output key first
CLOUDFRONT_DOMAIN=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='$CLOUDFRONT_OUTPUT_KEY'].OutputValue" \
    --output text 2>/dev/null)

# Fallback to generic CloudFrontDomain for backwards compatibility
if [[ -z "$CLOUDFRONT_DOMAIN" || "$CLOUDFRONT_DOMAIN" == "None" ]]; then
    CLOUDFRONT_DOMAIN=$(aws cloudformation describe-stacks \
        --stack-name "$STACK_NAME" \
        --query "Stacks[0].Outputs[?OutputKey=='CloudFrontDomain'].OutputValue" \
        --output text 2>/dev/null)
fi

if [[ -z "$CLOUDFRONT_DOMAIN" || "$CLOUDFRONT_DOMAIN" == "None" ]]; then
    error "Could not fetch CloudFront domain from stack outputs (tried $CLOUDFRONT_OUTPUT_KEY and CloudFrontDomain)"
fi

success "CloudFront domain: $CLOUDFRONT_DOMAIN"
echo ""

# Update vertical-specific subdomain
update_dns_record "$SUBDOMAIN" "$CLOUDFRONT_DOMAIN"

# Update wildcard subdomain (if enabled)
if [[ "$CREATE_WILDCARD" == "true" ]]; then
    WILDCARD_DOMAIN="*.${DOMAIN_NAME}"
    update_dns_record "$WILDCARD_DOMAIN" "$CLOUDFRONT_DOMAIN"
fi

# Summary
header "DNS Update Complete"
echo "  Updated: $SUBDOMAIN → $CLOUDFRONT_DOMAIN"
if [[ "$CREATE_WILDCARD" == "true" ]]; then
    echo "  Updated: *.${DOMAIN_NAME} → $CLOUDFRONT_DOMAIN"
fi
echo ""
info "DNS propagation may take a few minutes"
