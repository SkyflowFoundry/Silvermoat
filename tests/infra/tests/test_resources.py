"""
AWS resource validation tests.
"""
import pytest
from botocore.exceptions import ClientError


# ----------------------------
# DynamoDB Tests
# ----------------------------

@pytest.mark.infra
def test_dynamodb_tables_exist(dynamodb_client, stack_resources):
    """Test that all DynamoDB tables exist."""
    table_resources = [
        "QuotesTable",
        "PoliciesTable",
        "ClaimsTable",
        "PaymentsTable",
        "CasesTable",
    ]

    for resource in table_resources:
        table_name = stack_resources[resource]
        try:
            response = dynamodb_client.describe_table(TableName=table_name)
            assert response["Table"]["TableStatus"] == "ACTIVE"
        except ClientError as e:
            pytest.fail(f"Table {table_name} does not exist or is not active: {e}")


@pytest.mark.infra
def test_dynamodb_table_schema(dynamodb_client, stack_resources):
    """Test that DynamoDB tables have correct key schema."""
    table_resources = [
        "QuotesTable",
        "PoliciesTable",
        "ClaimsTable",
        "PaymentsTable",
        "CasesTable",
    ]

    for resource in table_resources:
        table_name = stack_resources[resource]
        response = dynamodb_client.describe_table(TableName=table_name)

        key_schema = response["Table"]["KeySchema"]
        assert len(key_schema) == 1, f"Table {table_name} should have 1 key (partition key only)"
        assert key_schema[0]["AttributeName"] == "id"
        assert key_schema[0]["KeyType"] == "HASH"


@pytest.mark.infra
def test_dynamodb_billing_mode(dynamodb_client, stack_resources):
    """Test that DynamoDB tables use PAY_PER_REQUEST billing."""
    table_resources = [
        "QuotesTable",
        "PoliciesTable",
        "ClaimsTable",
        "PaymentsTable",
        "CasesTable",
    ]

    for resource in table_resources:
        table_name = stack_resources[resource]
        response = dynamodb_client.describe_table(TableName=table_name)

        billing_mode = response["Table"]["BillingModeSummary"]["BillingMode"]
        assert billing_mode == "PAY_PER_REQUEST", f"Table {table_name} should use PAY_PER_REQUEST"


@pytest.mark.infra
def test_dynamodb_seeded_data(dynamodb_client, stack_resources):
    """Test that DynamoDB tables have seeded data."""
    # Check quotes table has at least one item
    quotes_table = stack_resources["QuotesTable"]
    response = dynamodb_client.scan(TableName=quotes_table, Limit=1)
    assert response["Count"] > 0, "QuotesTable should have seeded data"


# ----------------------------
# S3 Tests
# ----------------------------

@pytest.mark.infra
def test_s3_buckets_exist(s3_client, ui_bucket_name, docs_bucket_name):
    """Test that S3 buckets exist."""
    # UI bucket
    try:
        s3_client.head_bucket(Bucket=ui_bucket_name)
    except ClientError as e:
        pytest.fail(f"UI bucket {ui_bucket_name} does not exist: {e}")

    # Docs bucket
    try:
        s3_client.head_bucket(Bucket=docs_bucket_name)
    except ClientError as e:
        pytest.fail(f"Docs bucket {docs_bucket_name} does not exist: {e}")


@pytest.mark.infra
def test_ui_bucket_website_config(s3_client, ui_bucket_name):
    """Test that UI bucket has website hosting enabled."""
    try:
        response = s3_client.get_bucket_website(Bucket=ui_bucket_name)
        assert response["IndexDocument"]["Suffix"] == "index.html"
        assert response["ErrorDocument"]["Key"] == "index.html"
    except ClientError as e:
        pytest.fail(f"UI bucket {ui_bucket_name} does not have website config: {e}")


@pytest.mark.infra
def test_ui_bucket_has_index_html(s3_client, ui_bucket_name):
    """Test that UI bucket has index.html."""
    try:
        response = s3_client.head_object(Bucket=ui_bucket_name, Key="index.html")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
    except ClientError as e:
        pytest.fail(f"index.html not found in UI bucket {ui_bucket_name}: {e}")


@pytest.mark.infra
def test_ui_bucket_public_policy(s3_client, ui_bucket_name):
    """Test that UI bucket has public read policy."""
    try:
        response = s3_client.get_bucket_policy(Bucket=ui_bucket_name)
        policy = response["Policy"]
        assert "s3:GetObject" in policy
        assert "*" in policy  # Public access
    except ClientError as e:
        pytest.fail(f"UI bucket {ui_bucket_name} does not have public policy: {e}")


# ----------------------------
# Lambda Tests
# ----------------------------

@pytest.mark.infra
def test_lambda_function_exists(lambda_client, stack_resources):
    """Test that Lambda function exists."""
    function_name = stack_resources["MvpServiceFunction"]

    try:
        response = lambda_client.get_function(FunctionName=function_name)
        config = response["Configuration"]
        assert config["State"] == "Active"
        assert config["Runtime"].startswith("python")
    except ClientError as e:
        pytest.fail(f"Lambda function {function_name} does not exist: {e}")


@pytest.mark.infra
def test_lambda_environment_variables(lambda_client, stack_resources):
    """Test that Lambda has required environment variables."""
    function_name = stack_resources["MvpServiceFunction"]

    response = lambda_client.get_function_configuration(FunctionName=function_name)
    env_vars = response.get("Environment", {}).get("Variables", {})

    required_vars = [
        "QUOTES_TABLE",
        "POLICIES_TABLE",
        "CLAIMS_TABLE",
        "PAYMENTS_TABLE",
        "CASES_TABLE",
        "DOCS_BUCKET",
        "SNS_TOPIC_ARN",
    ]

    for var in required_vars:
        assert var in env_vars, f"Lambda missing environment variable: {var}"
        assert env_vars[var], f"Lambda environment variable {var} is empty"


# ----------------------------
# CloudFront Tests
# ----------------------------

@pytest.mark.infra
def test_cloudfront_distribution_exists(cloudfront_client, stack_resources):
    """Test that CloudFront distribution exists and is deployed."""
    distribution_id = stack_resources["UiDistribution"]

    try:
        response = cloudfront_client.get_distribution(Id=distribution_id)
        distribution = response["Distribution"]
        assert distribution["Status"] == "Deployed"
        assert distribution["DistributionConfig"]["Enabled"] is True
    except ClientError as e:
        pytest.fail(f"CloudFront distribution {distribution_id} does not exist: {e}")


@pytest.mark.infra
def test_cloudfront_origin_config(cloudfront_client, stack_resources, ui_bucket_name):
    """Test that CloudFront origin points to S3 website endpoint."""
    distribution_id = stack_resources["UiDistribution"]

    response = cloudfront_client.get_distribution(Id=distribution_id)
    origins = response["Distribution"]["DistributionConfig"]["Origins"]["Items"]

    assert len(origins) > 0, "CloudFront should have at least one origin"

    # Check first origin points to S3 website
    origin = origins[0]
    assert ui_bucket_name in origin["DomainName"], "Origin should point to UI bucket"
    assert origin["DomainName"].endswith(".s3-website-us-east-1.amazonaws.com") or \
           origin["DomainName"].endswith(".s3.amazonaws.com"), "Origin should be S3 endpoint"
