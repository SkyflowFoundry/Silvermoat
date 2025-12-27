"""
Cleanup utilities for test data.
"""
import boto3
from botocore.exceptions import ClientError


def delete_test_items(table_name, test_ids, region="us-east-1"):
    """
    Delete test items from DynamoDB table.

    Args:
        table_name: DynamoDB table name
        test_ids: List of item IDs to delete
        region: AWS region
    """
    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table_name)

    for item_id in test_ids:
        try:
            table.delete_item(Key={"id": item_id})
        except ClientError as e:
            print(f"Failed to delete item {item_id} from {table_name}: {e}")


def cleanup_test_stack(stack_name, region="us-east-1", skip_confirmation=False):
    """
    Delete a test CloudFormation stack.

    Args:
        stack_name: Stack name to delete
        region: AWS region
        skip_confirmation: If True, skip confirmation prompt
    """
    cfn_client = boto3.client("cloudformation", region_name=region)

    if not skip_confirmation:
        response = input(f"Delete stack {stack_name}? (yes/no): ")
        if response.lower() != "yes":
            print("Deletion cancelled")
            return

    try:
        print(f"Deleting stack {stack_name}...")
        cfn_client.delete_stack(StackName=stack_name)
        print("Stack deletion initiated")
        print("Waiting for deletion to complete...")
        waiter = cfn_client.get_waiter("stack_delete_complete")
        waiter.wait(StackName=stack_name)
        print("Stack deletion complete")
    except ClientError as e:
        print(f"Failed to delete stack {stack_name}: {e}")
