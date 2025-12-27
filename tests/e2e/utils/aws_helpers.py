"""AWS helper functions for fetching stack outputs."""
import boto3
import os


def get_stack_outputs(stack_name=None):
    """Get CloudFormation stack outputs.

    Args:
        stack_name: Stack name (defaults to STACK_NAME env var or 'silvermoat')

    Returns:
        dict: Key-value pairs of stack outputs
    """
    if not stack_name:
        stack_name = os.getenv("STACK_NAME", "silvermoat")

    try:
        cfn = boto3.client("cloudformation")
        response = cfn.describe_stacks(StackName=stack_name)

        if not response["Stacks"]:
            return {}

        outputs = {}
        for output in response["Stacks"][0].get("Outputs", []):
            outputs[output["OutputKey"]] = output["OutputValue"]

        return outputs
    except Exception as e:
        print(f"Error fetching stack outputs: {e}")
        return {}


def get_api_url(stack_name=None):
    """Get API Gateway URL from stack outputs."""
    outputs = get_stack_outputs(stack_name)
    return outputs.get("ApiUrl", "")


def get_ui_url(stack_name=None):
    """Get UI URL from stack outputs."""
    outputs = get_stack_outputs(stack_name)
    # Try custom domain first, then CloudFront, then S3 website
    return (
        outputs.get("CustomDomainUrl") or
        outputs.get("CloudFrontUrl") or
        outputs.get("UiUrl", "")
    )
