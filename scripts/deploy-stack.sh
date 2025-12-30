#!/bin/bash
# Deploy CDK stack for Silvermoat MVP

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load AWS CLI check utility
source "$SCRIPT_DIR/lib/check-aws.sh"

STACK_NAME="${STACK_NAME:-silvermoat}"

# Check AWS CLI and credentials
check_aws_configured

# Default parameters (exported as environment variables for CDK)
export APP_NAME="${APP_NAME:-silvermoat}"
export STAGE_NAME="${STAGE_NAME:-demo}"
export API_DEPLOYMENT_TOKEN="${API_DEPLOYMENT_TOKEN:-v1}"
export UI_SEEDING_MODE="${UI_SEEDING_MODE:-external}"
export CREATE_CLOUDFRONT="${CREATE_CLOUDFRONT:-true}"
export DOMAIN_NAME="${DOMAIN_NAME:-silvermoat.net}"
export STACK_NAME

echo "Deploying CDK stack: $STACK_NAME"
echo "Parameters:"
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

# Deploy CDK stack
echo "Deploying CDK stack..."
cd "$PROJECT_ROOT/cdk"
cdk deploy "$STACK_NAME" --require-approval never

echo ""
echo "Stack deployment complete!"
echo ""
echo "To get stack outputs, run:"
echo "  ./scripts/get-outputs.sh"
echo ""
echo "To deploy the UI, run:"
echo "  ./scripts/deploy-ui.sh"
