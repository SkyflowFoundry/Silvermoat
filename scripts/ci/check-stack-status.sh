#!/bin/bash
# Check CloudFormation stack status and handle failed states
# Usage: ./check-stack-status.sh <stack_name>
# Outputs: stack_status=<status> and stack_deleted=<true|false> in GitHub Actions format

set -euo pipefail

STACK_NAME="${1:?Stack name required}"

echo "Checking if CDK stack ${STACK_NAME} exists..."

# Check CDK stack status
STACK_STATUS=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --query 'Stacks[0].StackStatus' \
  --output text 2>/dev/null || echo "NOT_FOUND")

echo "Stack status: ${STACK_STATUS}"

# Output for GitHub Actions
if [ -n "${GITHUB_OUTPUT:-}" ]; then
  echo "stack_status=${STACK_STATUS}" >> "${GITHUB_OUTPUT}"
fi

# Handle failed rollback states - delete stack before redeploying
if [[ "${STACK_STATUS}" == "ROLLBACK_COMPLETE" ]] || \
   [[ "${STACK_STATUS}" == "ROLLBACK_FAILED" ]] || \
   [[ "${STACK_STATUS}" == "UPDATE_ROLLBACK_COMPLETE" ]] || \
   [[ "${STACK_STATUS}" == "UPDATE_ROLLBACK_FAILED" ]]; then
  echo "🗑️ Stack in failed state (${STACK_STATUS}), deleting before redeployment..."
  cd cdk
  cdk destroy "${STACK_NAME}" --force || true
  echo "✅ Stack deleted"
  if [ -n "${GITHUB_OUTPUT:-}" ]; then
    echo "stack_deleted=true" >> "${GITHUB_OUTPUT}"
  fi
elif [[ "${STACK_STATUS}" == "NOT_FOUND" ]]; then
  echo "Stack does not exist, will create"
  if [ -n "${GITHUB_OUTPUT:-}" ]; then
    echo "stack_deleted=false" >> "${GITHUB_OUTPUT}"
    echo "stack_exists=false" >> "${GITHUB_OUTPUT}"
  fi
else
  echo "✅ Stack exists (${STACK_STATUS})"
  if [ -n "${GITHUB_OUTPUT:-}" ]; then
    echo "stack_deleted=false" >> "${GITHUB_OUTPUT}"
    echo "stack_exists=true" >> "${GITHUB_OUTPUT}"
  fi
fi
