"""
Deployment Smoke Test Configuration

Minimal infrastructure checks to verify deployment succeeded.
Does NOT validate specific AWS resources or implementation details.
"""

import os
import pytest


@pytest.fixture(scope="session")
def stack_name():
    """Get CloudFormation stack name from environment"""
    name = os.environ.get('STACK_NAME', os.environ.get('TEST_STACK_NAME'))
    if not name:
        pytest.skip("STACK_NAME or TEST_STACK_NAME environment variable required for smoke tests")
    return name


@pytest.fixture(scope="session")
def stack_outputs(stack_name):
    """
    Fetch CloudFormation stack outputs.
    Only used to verify deployment completed and get URLs.
    """
    try:
        import boto3
        cfn = boto3.client('cloudformation')
        response = cfn.describe_stacks(StackName=stack_name)
        stack = response['Stacks'][0]
        outputs = {o['OutputKey']: o['OutputValue'] for o in stack.get('Outputs', [])}
        return {
            'stack': stack,
            'outputs': outputs
        }
    except Exception as e:
        pytest.fail(f"Could not fetch stack outputs: {e}")
