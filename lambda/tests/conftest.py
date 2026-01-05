"""
Shared pytest fixtures for Lambda unit tests.

Provides mocked AWS services, storage backends, and Lambda event/context objects.
"""
import os
import json
import pytest
import boto3
from moto import mock_aws
from unittest.mock import MagicMock


# Mock AWS environment - must be set before importing Lambda code
@pytest.fixture(scope="function")
def aws_credentials():
    """Mock AWS credentials for moto"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def dynamodb_tables(aws_credentials):
    """Create mocked DynamoDB tables with all required tables and indexes"""
    with mock_aws():
        # Set table name environment variables
        os.environ["CUSTOMERS_TABLE"] = "test-customers"
        os.environ["QUOTES_TABLE"] = "test-quotes"
        os.environ["POLICIES_TABLE"] = "test-policies"
        os.environ["CLAIMS_TABLE"] = "test-claims"
        os.environ["PAYMENTS_TABLE"] = "test-payments"
        os.environ["CASES_TABLE"] = "test-cases"

        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

        # Create customers table with EmailIndex GSI
        dynamodb.create_table(
            TableName="test-customers",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "email", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "EmailIndex",
                    "KeySchema": [{"AttributeName": "email", "KeyType": "HASH"}],
                    "Projection": {"ProjectionType": "ALL"},
                }
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        # Create quotes table with CustomerIdIndex GSI
        dynamodb.create_table(
            TableName="test-quotes",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "customerId", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "CustomerIdIndex",
                    "KeySchema": [{"AttributeName": "customerId", "KeyType": "HASH"}],
                    "Projection": {"ProjectionType": "ALL"},
                }
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        # Create other tables (policies, claims, payments, cases) with CustomerIdIndex
        for table_name in ["test-policies", "test-claims", "test-payments", "test-cases"]:
            dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[
                    {"AttributeName": "id", "AttributeType": "S"},
                    {"AttributeName": "customerId", "AttributeType": "S"},
                ],
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "CustomerIdIndex",
                        "KeySchema": [{"AttributeName": "customerId", "KeyType": "HASH"}],
                        "Projection": {"ProjectionType": "ALL"},
                    }
                ],
                BillingMode="PAY_PER_REQUEST",
            )

        yield dynamodb


@pytest.fixture
def storage_backend(dynamodb_tables):
    """Create a mocked DynamoDBBackend instance"""
    # Import here to ensure environment variables are set
    from shared.storage import DynamoDBBackend
    return DynamoDBBackend()


@pytest.fixture
def lambda_context():
    """Mock Lambda context object"""
    context = MagicMock()
    context.function_name = "test-function"
    context.function_version = "$LATEST"
    context.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    context.memory_limit_in_mb = 128
    context.aws_request_id = "test-request-id"
    context.log_group_name = "/aws/lambda/test-function"
    context.log_stream_name = "2024/01/01/[$LATEST]test"
    context.get_remaining_time_in_millis = MagicMock(return_value=30000)
    return context


@pytest.fixture
def api_gateway_event():
    """Factory fixture to create API Gateway events"""
    def _make_event(
        method="GET",
        path="/",
        body=None,
        query_params=None,
        path_params=None,
        headers=None,
    ):
        """
        Create an API Gateway proxy event.

        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            path: Request path (e.g., "/customer/123")
            body: Request body (dict or string)
            query_params: Query string parameters (dict)
            path_params: Path parameters (dict)
            headers: HTTP headers (dict)
        """
        event = {
            "resource": path,
            "path": path,
            "httpMethod": method,
            "headers": headers or {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            "queryStringParameters": query_params,
            "pathParameters": path_params,
            "body": json.dumps(body) if isinstance(body, dict) else body,
            "isBase64Encoded": False,
            "requestContext": {
                "requestId": "test-request-id",
                "stage": "test",
                "identity": {
                    "sourceIp": "127.0.0.1",
                    "userAgent": "test-agent",
                },
            },
        }
        return event

    return _make_event


@pytest.fixture
def sample_customer_data():
    """Sample customer data for testing"""
    return {
        "email": "test@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "phone": "555-1234",
        "address": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip": "12345",
    }


@pytest.fixture
def sample_quote_data():
    """Sample quote data for testing"""
    return {
        "customerEmail": "test@example.com",
        "coverageType": "AUTO",
        "coverageAmount": 100000,
        "premium": 1200,
        "deductible": 500,
    }


@pytest.fixture
def sample_policy_data(sample_customer_data):
    """Sample policy data for testing"""
    return {
        "customer": sample_customer_data,
        "policyNumber": "POL-12345",
        "coverageType": "AUTO",
        "premium": 1200,
        "deductible": 500,
        "startDate": "2024-01-01",
        "endDate": "2025-01-01",
    }


@pytest.fixture
def sample_claim_data():
    """Sample claim data for testing"""
    return {
        "policyId": "test-policy-id",
        "claimNumber": "CLM-12345",
        "incidentDate": "2024-06-15",
        "description": "Vehicle accident",
        "claimAmount": 5000,
    }
