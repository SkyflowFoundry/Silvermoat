"""
AWS Helper Functions
Utilities for fetching CloudFormation stack outputs
"""

import boto3
from botocore.exceptions import ClientError


def get_stack_output(stack_name, output_key):
    """
    Fetch a specific output from a CloudFormation stack

    Args:
        stack_name: Name of the CloudFormation stack
        output_key: Key of the output to fetch (e.g., 'WebUrl', 'ApiBaseUrl')

    Returns:
        Output value or None if not found
    """
    try:
        cf_client = boto3.client('cloudformation')
        response = cf_client.describe_stacks(StackName=stack_name)

        if not response['Stacks']:
            return None

        stack = response['Stacks'][0]
        outputs = stack.get('Outputs', [])

        for output in outputs:
            if output['OutputKey'] == output_key:
                return output['OutputValue']

        return None

    except ClientError as e:
        print(f"Error fetching stack outputs: {e}")
        return None


def get_all_stack_outputs(stack_name):
    """
    Fetch all outputs from a CloudFormation stack

    Args:
        stack_name: Name of the CloudFormation stack

    Returns:
        Dictionary of output key-value pairs, or empty dict if error
    """
    try:
        cf_client = boto3.client('cloudformation')
        response = cf_client.describe_stacks(StackName=stack_name)

        if not response['Stacks']:
            return {}

        stack = response['Stacks'][0]
        outputs = stack.get('Outputs', [])

        return {
            output['OutputKey']: output['OutputValue']
            for output in outputs
        }

    except ClientError as e:
        print(f"Error fetching stack outputs: {e}")
        return {}


def get_stack_status(stack_name):
    """
    Get the status of a CloudFormation stack

    Args:
        stack_name: Name of the CloudFormation stack

    Returns:
        Stack status string or None if not found
    """
    try:
        cf_client = boto3.client('cloudformation')
        response = cf_client.describe_stacks(StackName=stack_name)

        if not response['Stacks']:
            return None

        return response['Stacks'][0]['StackStatus']

    except ClientError as e:
        print(f"Error fetching stack status: {e}")
        return None
