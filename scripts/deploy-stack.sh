#!/bin/bash
# Deploy CDK stack for Silvermoat MVP

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

BASE_STACK_NAME="${STACK_NAME:-silvermoat}"

# Check AWS CLI and credentials
check_aws_configured

# Default parameters (exported as environment variables for CDK)
export APP_NAME="${APP_NAME:-silvermoat}"
export STAGE_NAME="${STAGE_NAME:-demo}"
export API_DEPLOYMENT_TOKEN="${API_DEPLOYMENT_TOKEN:-v1}"
export UI_SEEDING_MODE="${UI_SEEDING_MODE:-external}"
export CREATE_CLOUDFRONT="${CREATE_CLOUDFRONT:-false}"  # Disabled for multi-vertical
export DOMAIN_NAME="${DOMAIN_NAME:-silvermoat.net}"
export STACK_NAME="$BASE_STACK_NAME"

# Determine which verticals to deploy
VERTICAL="${VERTICAL:-all}"  # Can be: all, insurance, retail

echo "Deploying Multi-Vertical CDK Stacks"
echo "Parameters:"
echo "  Base Stack Name: $BASE_STACK_NAME"
echo "  Vertical: $VERTICAL"
echo "  AppName: $APP_NAME"
echo "  StageName: $STAGE_NAME"
echo "  ApiDeploymentToken: $API_DEPLOYMENT_TOKEN"
echo "  UiSeedingMode: $UI_SEEDING_MODE"
echo "  CreateCloudFront: $CREATE_CLOUDFRONT"
echo "  DomainName: $DOMAIN_NAME"
echo ""

# Install CDK dependencies (first time only)
if [ ! -d "$PROJECT_ROOT/cdk/cdk.out" ]; then
  echo "Installing CDK dependencies..."
  cd "$PROJECT_ROOT/cdk"
  pip install -q -r requirements.txt
  echo "✓ CDK dependencies installed"
  echo ""
fi

# Check if CDK CLI is installed
if ! command -v cdk >/dev/null 2>&1; then
  echo "Error: AWS CDK CLI not found. Install with:"
  echo "  npm install -g aws-cdk"
  exit 1
fi

# Deploy CDK stacks
echo "Deploying CDK stacks..."
cd "$PROJECT_ROOT/cdk"

if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "insurance" ]; then
  echo "→ Deploying Insurance Stack..."
  cdk deploy "${BASE_STACK_NAME}-insurance" --require-approval never
  echo "✓ Insurance stack deployed"
  echo ""
fi

if [ "$VERTICAL" = "all" ] || [ "$VERTICAL" = "retail" ]; then
  echo "→ Deploying Retail Stack..."
  cdk deploy "${BASE_STACK_NAME}-retail" --require-approval never
  echo "✓ Retail stack deployed"
  echo ""
fi

echo ""
echo "✅ All stack deployments complete!"
echo ""
echo "To get stack outputs, run:"
echo "  ./scripts/get-outputs.sh"
echo ""
echo "To deploy the UI, run:"
echo "  ./scripts/deploy-ui.sh"
