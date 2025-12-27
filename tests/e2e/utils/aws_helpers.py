"""
AWS helper functions for E2E tests.
"""
import os
import boto3
from botocore.exceptions import ClientError


def get_stack_outputs(stack_name=None):
    """
    Fetch CloudFormation stack outputs.

    Args:
        stack_name: Name of the CloudFormation stack. If not provided,
                   uses STACK_NAME environment variable.

    Returns:
        dict: Dictionary of output key-value pairs
    """
    if not stack_name:
        stack_name = os.getenv("STACK_NAME", "silvermoat")

    try:
        cfn = boto3.client("cloudformation")
        response = cfn.describe_stacks(StackName=stack_name)

        if not response["Stacks"]:
            return {}

        stack = response["Stacks"][0]
        outputs = stack.get("Outputs", [])

        return {
            output["OutputKey"]: output["OutputValue"]
            for output in outputs
        }
    except ClientError as e:
        print(f"Error fetching stack outputs: {e}")
        return {}


def get_api_url(stack_name=None):
    """Get API Gateway URL from stack outputs."""
    outputs = get_stack_outputs(stack_name)
    return outputs.get("ApiUrl", "")


def get_ui_url(stack_name=None):
    """Get UI URL from stack outputs (S3 website or CloudFront)."""
    outputs = get_stack_outputs(stack_name)
    # Prefer CloudFront URL, fallback to S3 website URL
    return outputs.get("CloudFrontUrl") or outputs.get("UiUrl", "")
