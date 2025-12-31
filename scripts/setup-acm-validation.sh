#!/bin/bash
set -e

# Automated ACM Certificate DNS Validation via Cloudflare
# Fetches validation records from ACM and creates them in Cloudflare

STACK_NAME="${STACK_NAME:-silvermoat}"

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

info "Fetching ACM certificate ARN from stack: $STACK_NAME"

# Get ACM certificate ARN from CloudFormation outputs
CERT_ARN=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='CertificateArn'].OutputValue" \
    --output text 2>/dev/null)

if [[ -z "$CERT_ARN" || "$CERT_ARN" == "None" ]]; then
    info "No ACM certificate found in stack outputs (CloudFront may not be enabled)"
    exit 0
fi

success "Certificate ARN: $CERT_ARN"

# Get certificate validation records from ACM
info "Fetching DNS validation records from ACM..."

VALIDATION_RECORDS=$(aws acm describe-certificate \
    --certificate-arn "$CERT_ARN" \
    --query 'Certificate.DomainValidationOptions[0].ResourceRecord' \
    --output json 2>/dev/null)

if [[ -z "$VALIDATION_RECORDS" || "$VALIDATION_RECORDS" == "null" ]]; then
    error "Could not fetch validation records from ACM certificate"
fi

# Extract validation record details
VALIDATION_NAME=$(echo "$VALIDATION_RECORDS" | jq -r '.Name')
VALIDATION_VALUE=$(echo "$VALIDATION_RECORDS" | jq -r '.Value')
VALIDATION_TYPE=$(echo "$VALIDATION_RECORDS" | jq -r '.Type')

if [[ -z "$VALIDATION_NAME" || "$VALIDATION_NAME" == "null" ]]; then
    error "Invalid validation record data from ACM"
fi

# Remove trailing dot from validation name if present
VALIDATION_NAME="${VALIDATION_NAME%.}"

success "Validation record details:"
echo "  Name:  $VALIDATION_NAME"
echo "  Value: $VALIDATION_VALUE"
echo "  Type:  $VALIDATION_TYPE"

# Check if validation record already exists in Cloudflare
info "Checking if validation record exists in Cloudflare..."

EXISTING_RECORD=$(curl -s -X GET \
    "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records?name=$VALIDATION_NAME&type=$VALIDATION_TYPE" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: application/json")

EXISTING_VALUE=$(echo "$EXISTING_RECORD" | jq -r '.result[0].content // empty')
RECORD_ID=$(echo "$EXISTING_RECORD" | jq -r '.result[0].id // empty')

# Check if record exists and matches
if [[ -n "$EXISTING_VALUE" ]]; then
    if [[ "$EXISTING_VALUE" == "$VALIDATION_VALUE" ]]; then
        success "Validation record already exists with correct value"
        echo "  Record ID: $RECORD_ID"
        info "ACM validation DNS setup complete. Waiting for AWS to validate..."
        exit 0
    else
        info "Validation record exists but value differs. Updating..."
        echo "  Old: $EXISTING_VALUE"
        echo "  New: $VALIDATION_VALUE"
        UPDATE_EXISTING=true
    fi
else
    info "Validation record not found. Creating new record..."
    UPDATE_EXISTING=false
fi

# Prepare DNS record data
DNS_RECORD_DATA=$(jq -n \
    --arg name "$VALIDATION_NAME" \
    --arg content "$VALIDATION_VALUE" \
    --arg type "$VALIDATION_TYPE" \
    '{
        type: $type,
        name: $name,
        content: $content,
        ttl: 1,
        proxied: false
    }')

# Create or update DNS record
if [[ "$UPDATE_EXISTING" == "true" ]]; then
    # Update existing record
    RESPONSE=$(curl -s -X PUT \
        "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records/$RECORD_ID" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "$DNS_RECORD_DATA")
else
    # Create new record
    RESPONSE=$(curl -s -X POST \
        "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "$DNS_RECORD_DATA")
fi

# Check success
if echo "$RESPONSE" | jq -e '.success == true' >/dev/null 2>&1; then
    success "ACM validation record created/updated successfully"
    echo "  Name:  $VALIDATION_NAME"
    echo "  Value: $VALIDATION_VALUE"
    echo "  Proxied: No (DNS only)"
    echo ""
    info "ACM validation may take 5-15 minutes to complete"
    info "CloudFormation stack will proceed automatically once validated"
else
    ERRORS=$(echo "$RESPONSE" | jq -r '.errors[] | .message' 2>/dev/null || echo "Unknown error")
    error "Failed to create/update validation record: $ERRORS"
fi
