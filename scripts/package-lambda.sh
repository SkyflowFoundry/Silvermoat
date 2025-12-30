#!/usr/bin/env bash
set -euo pipefail

# Package Lambda functions for CloudFormation deployment
# Creates ZIP files for each Lambda function and uploads to S3

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LAMBDA_DIR="${PROJECT_ROOT}/lambda"

# Get stack name (required)
STACK_NAME="${STACK_NAME:-silvermoat}"

# Get Lambda code bucket name from stack outputs
echo "Fetching Lambda code bucket from stack outputs..."
LAMBDA_BUCKET=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --query 'Stacks[0].Outputs[?OutputKey==`LambdaCodeBucketName`].OutputValue' \
  --output text 2>/dev/null || echo "")

if [ -z "${LAMBDA_BUCKET}" ]; then
  echo "ERROR: Could not find LambdaCodeBucketName output in stack ${STACK_NAME}"
  echo "The stack must be deployed with the updated template first (which creates the bucket)"
  exit 1
fi

echo "Lambda code bucket: ${LAMBDA_BUCKET}"

# Package mvp_service Lambda
echo ""
echo "Packaging mvp_service Lambda..."
cd "${LAMBDA_DIR}"
rm -f mvp_service/mvp-service.zip
# Package handler and chatbot from mvp_service/, plus shared/ directory
zip -r mvp_service/mvp-service.zip mvp_service/handler.py mvp_service/chatbot.py shared/
echo "Created mvp-service.zip ($(du -h mvp_service/mvp-service.zip | cut -f1))"

echo "Uploading mvp-service.zip to s3://${LAMBDA_BUCKET}/"
aws s3 cp mvp_service/mvp-service.zip "s3://${LAMBDA_BUCKET}/mvp-service.zip"
echo "✓ Uploaded mvp-service.zip"

# Package seeder Lambda
echo ""
echo "Packaging seeder Lambda..."
cd "${LAMBDA_DIR}/seeder"
rm -f seeder.zip
zip -r seeder.zip handler.py
echo "Created seeder.zip ($(du -h seeder.zip | cut -f1))"

echo "Uploading seeder.zip to s3://${LAMBDA_BUCKET}/"
aws s3 cp seeder.zip "s3://${LAMBDA_BUCKET}/seeder.zip"
echo "✓ Uploaded seeder.zip"

echo ""
echo "✓ Lambda packaging complete"
echo ""
echo "Next steps:"
echo "  1. Update CloudFormation stack to use new Lambda code:"
echo "     ./scripts/deploy-stack.sh"
echo "  2. Or manually trigger stack update via AWS Console"
