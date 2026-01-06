#!/bin/bash
# Get test stack name based on PR number or run ID
# Usage: ./get-stack-name.sh [pr_number] [run_id]
# Outputs stack name to stdout

set -euo pipefail

PR_NUMBER="${1:-}"
RUN_ID="${2:-}"

if [ -n "${PR_NUMBER}" ]; then
  STACK_NAME="silvermoat-test-pr-${PR_NUMBER}"
elif [ -n "${RUN_ID}" ]; then
  STACK_NAME="silvermoat-test-${RUN_ID}"
else
  echo "Error: Either PR_NUMBER or RUN_ID must be provided" >&2
  exit 1
fi

echo "${STACK_NAME}"
