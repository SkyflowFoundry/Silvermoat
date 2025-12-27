"""
Pytest configuration and fixtures for infrastructure tests.
"""
import os
import pytest
import boto3
from botocore.exceptions import ClientError


@pytest.fixture(scope="session")
def stack_name():
    """Get stack name from environment variable."""
    name = os.environ.get("TEST_STACK_NAME", os.environ.get("STACK_NAME", "silvermoat"))
    return name


@pytest.fixture(scope="session")
def aws_region():
    """Get AWS region from environment or default to us-east-1."""
    return os.environ.get("AWS_REGION", "us-east-1")


@pytest.fixture(scope="session")
def cfn_client(aws_region):
    """CloudFormation client."""
    return boto3.client("cloudformation", region_name=aws_region)


@pytest.fixture(scope="session")
def dynamodb_client(aws_region):
    """DynamoDB client."""
    return boto3.client("dynamodb", region_name=aws_region)


@pytest.fixture(scope="session")
def s3_client(aws_region):
    """S3 client."""
    return boto3.client("s3", region_name=aws_region)


@pytest.fixture(scope="session")
def lambda_client(aws_region):
    """Lambda client."""
    return boto3.client("lambda", region_name=aws_region)


@pytest.fixture(scope="session")
def apigateway_client(aws_region):
    """API Gateway client."""
    return boto3.client("apigateway", region_name=aws_region)


@pytest.fixture(scope="session")
def cloudfront_client():
    """CloudFront client (always us-east-1)."""
    return boto3.client("cloudfront", region_name="us-east-1")


@pytest.fixture(scope="session")
def stack_outputs(cfn_client, stack_name):
    """
    Get all stack outputs as a dictionary.

    Returns:
        dict: {OutputKey: OutputValue}
    """
    try:
        response = cfn_client.describe_stacks(StackName=stack_name)
        stacks = response.get("Stacks", [])
        if not stacks:
            pytest.fail(f"Stack {stack_name} not found")

        outputs = stacks[0].get("Outputs", [])
        return {o["OutputKey"]: o["OutputValue"] for o in outputs}
    except ClientError as e:
        pytest.fail(f"Failed to get stack outputs: {e}")


@pytest.fixture(scope="session")
def stack_resources(cfn_client, stack_name):
    """
    Get all stack resources as a dictionary.

    Returns:
        dict: {LogicalResourceId: PhysicalResourceId}
    """
    try:
        response = cfn_client.describe_stack_resources(StackName=stack_name)
        resources = response.get("StackResources", [])
        return {r["LogicalResourceId"]: r["PhysicalResourceId"] for r in resources}
    except ClientError as e:
        pytest.fail(f"Failed to get stack resources: {e}")


@pytest.fixture(scope="session")
def api_base_url(stack_outputs):
    """Get API Gateway base URL from stack outputs."""
    return stack_outputs.get("ApiBaseUrl")


@pytest.fixture(scope="session")
def web_url(stack_outputs):
    """Get S3 website URL from stack outputs."""
    return stack_outputs.get("WebUrl")


@pytest.fixture(scope="session")
def ui_bucket_name(stack_outputs):
    """Get UI bucket name from stack outputs."""
    return stack_outputs.get("UiBucketName")


@pytest.fixture(scope="session")
def docs_bucket_name(stack_outputs):
    """Get docs bucket name from stack outputs."""
    return stack_outputs.get("DocsBucketName")
