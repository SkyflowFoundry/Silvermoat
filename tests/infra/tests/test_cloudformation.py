"""
CloudFormation stack validation tests.
"""
import pytest
from botocore.exceptions import ClientError


@pytest.mark.infra
def test_stack_exists(cfn_client, stack_name):
    """Test that the CloudFormation stack exists."""
    try:
        response = cfn_client.describe_stacks(StackName=stack_name)
        stacks = response.get("Stacks", [])
        assert len(stacks) == 1, f"Expected 1 stack, found {len(stacks)}"
        assert stacks[0]["StackName"] == stack_name
    except ClientError as e:
        pytest.fail(f"Stack {stack_name} does not exist: {e}")


@pytest.mark.infra
def test_stack_status(cfn_client, stack_name):
    """Test that the stack is in a healthy state."""
    response = cfn_client.describe_stacks(StackName=stack_name)
    stack = response["Stacks"][0]
    status = stack["StackStatus"]

    healthy_statuses = [
        "CREATE_COMPLETE",
        "UPDATE_COMPLETE",
        "UPDATE_ROLLBACK_COMPLETE"
    ]

    assert status in healthy_statuses, f"Stack status is {status}, expected one of {healthy_statuses}"


@pytest.mark.infra
def test_stack_outputs_exist(stack_outputs):
    """Test that all expected stack outputs exist."""
    required_outputs = [
        "ApiBaseUrl",
        "WebUrl",
        "UiBucketName",
        "DocsBucketName",
    ]

    for output in required_outputs:
        assert output in stack_outputs, f"Missing required output: {output}"
        assert stack_outputs[output], f"Output {output} is empty"


@pytest.mark.infra
def test_stack_resources_exist(stack_resources):
    """Test that all expected stack resources exist."""
    required_resources = [
        "UiBucket",
        "DocsBucket",
        "QuotesTable",
        "PoliciesTable",
        "ClaimsTable",
        "PaymentsTable",
        "CasesTable",
        "MvpServiceFunction",
        "MvpApi",
        "UiDistribution",
    ]

    for resource in required_resources:
        assert resource in stack_resources, f"Missing required resource: {resource}"
        assert stack_resources[resource], f"Resource {resource} has no physical ID"


@pytest.mark.infra
def test_stack_parameters(cfn_client, stack_name):
    """Test that stack parameters are set correctly."""
    response = cfn_client.describe_stacks(StackName=stack_name)
    stack = response["Stacks"][0]
    parameters = {p["ParameterKey"]: p["ParameterValue"] for p in stack.get("Parameters", [])}

    # Verify key parameters exist
    assert "AppName" in parameters
    assert "StageName" in parameters
    assert "ApiDeploymentToken" in parameters
    assert "UiSeedingMode" in parameters


@pytest.mark.infra
@pytest.mark.slow
def test_no_stack_drift(cfn_client, stack_name):
    """Test that the stack has no configuration drift."""
    # Initiate drift detection
    response = cfn_client.detect_stack_drift(StackName=stack_name)
    drift_id = response["StackDriftDetectionId"]

    # Wait for drift detection to complete
    waiter = cfn_client.get_waiter("stack_drift_detection_complete")
    waiter.wait(StackDriftDetectionId=drift_id)

    # Check drift status
    response = cfn_client.describe_stack_drift_detection_status(
        StackDriftDetectionId=drift_id
    )

    drift_status = response["StackDriftStatus"]
    assert drift_status == "IN_SYNC", f"Stack has drift: {drift_status}"
