"""Vertical-specific CDK stack construct - complete isolation per vertical"""
from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_sns as sns,
    Duration,
    RemovalPolicy,
)
from constructs import Construct


class VerticalStack(Construct):
    """
    Complete vertical stack: API Gateway, Lambda, DynamoDB tables, S3 buckets.
    Each vertical is fully isolated with its own resources.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        vertical_name: str,  # "insurance" or "retail"
        app_name: str,
        stage_name: str,
        layer: lambda_.LayerVersion,
        api_deployment_token: str,
    ):
        super().__init__(scope, id)

        self.vertical_name = vertical_name
        self.app_name = app_name
        self.stage_name = stage_name

        # Create vertical-specific resources
        self._create_dynamodb_tables()
        self._create_s3_buckets()
        self._create_sns_topic()
        self._create_lambda_function(layer)
        self._create_api_gateway(api_deployment_token)

    def _create_dynamodb_tables(self):
        """Create DynamoDB tables for this vertical"""
        # Table configuration
        table_config = {
            "billing_mode": dynamodb.BillingMode.PAY_PER_REQUEST,
            "removal_policy": RemovalPolicy.DESTROY,  # For demo - use RETAIN in prod
            "point_in_time_recovery": False,  # Enable in prod
        }

        # Customer table (shared schema across verticals)
        self.customers_table = dynamodb.Table(
            self,
            "CustomersTable",
            table_name=f"{self.app_name}-{self.vertical_name}-customers-{self.stage_name}",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            **table_config,
        )
        # GSI for email lookup
        self.customers_table.add_global_secondary_index(
            index_name="EmailIndex",
            partition_key=dynamodb.Attribute(name="email", type=dynamodb.AttributeType.STRING),
        )

        # Quotes table (insurance) / Products table (retail)
        self.quotes_table = dynamodb.Table(
            self,
            "QuotesTable",
            table_name=f"{self.app_name}-{self.vertical_name}-quotes-{self.stage_name}",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            **table_config,
        )

        # Policies table (insurance) / Orders table (retail)
        self.policies_table = dynamodb.Table(
            self,
            "PoliciesTable",
            table_name=f"{self.app_name}-{self.vertical_name}-policies-{self.stage_name}",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            **table_config,
        )
        # GSI for customer lookup
        self.policies_table.add_global_secondary_index(
            index_name="CustomerIdIndex",
            partition_key=dynamodb.Attribute(name="customerId", type=dynamodb.AttributeType.STRING),
        )

        # Claims table (insurance) / Inventory table (retail)
        self.claims_table = dynamodb.Table(
            self,
            "ClaimsTable",
            table_name=f"{self.app_name}-{self.vertical_name}-claims-{self.stage_name}",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            **table_config,
        )
        # GSI for customer lookup
        self.claims_table.add_global_secondary_index(
            index_name="CustomerIdIndex",
            partition_key=dynamodb.Attribute(name="customerId", type=dynamodb.AttributeType.STRING),
        )

        # Payments table (shared schema)
        self.payments_table = dynamodb.Table(
            self,
            "PaymentsTable",
            table_name=f"{self.app_name}-{self.vertical_name}-payments-{self.stage_name}",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            **table_config,
        )

        # Cases table (support cases, shared schema)
        self.cases_table = dynamodb.Table(
            self,
            "CasesTable",
            table_name=f"{self.app_name}-{self.vertical_name}-cases-{self.stage_name}",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            **table_config,
        )

    def _create_s3_buckets(self):
        """Create S3 buckets for this vertical"""
        # UI bucket with website hosting
        self.ui_bucket = s3.Bucket(
            self,
            "UiBucket",
            bucket_name=f"{self.app_name}-{self.vertical_name}-ui-{self.stage_name}",
            website_index_document="index.html",
            website_error_document="index.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Documents bucket (for claims, etc.)
        self.docs_bucket = s3.Bucket(
            self,
            "DocsBucket",
            bucket_name=f"{self.app_name}-{self.vertical_name}-docs-{self.stage_name}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

    def _create_sns_topic(self):
        """Create SNS topic for events"""
        self.topic = sns.Topic(
            self,
            "EventsTopic",
            topic_name=f"{self.app_name}-{self.vertical_name}-events-{self.stage_name}",
        )

    def _create_lambda_function(self, layer: lambda_.LayerVersion):
        """Create Lambda function for this vertical"""
        self.function = lambda_.Function(
            self,
            "ApiFunction",
            function_name=f"{self.app_name}-{self.vertical_name}-api-{self.stage_name}",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset(f"../lambda/{self.vertical_name}"),
            handler="handler.handler",
            layers=[layer],
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={
                "CUSTOMERS_TABLE": self.customers_table.table_name,
                "QUOTES_TABLE": self.quotes_table.table_name,
                "POLICIES_TABLE": self.policies_table.table_name,
                "CLAIMS_TABLE": self.claims_table.table_name,
                "PAYMENTS_TABLE": self.payments_table.table_name,
                "CASES_TABLE": self.cases_table.table_name,
                "DOCS_BUCKET": self.docs_bucket.bucket_name,
                "SNS_TOPIC_ARN": self.topic.topic_arn,
                "VERTICAL": self.vertical_name,
            },
        )

        # Grant permissions
        self.customers_table.grant_read_write_data(self.function)
        self.quotes_table.grant_read_write_data(self.function)
        self.policies_table.grant_read_write_data(self.function)
        self.claims_table.grant_read_write_data(self.function)
        self.payments_table.grant_read_write_data(self.function)
        self.cases_table.grant_read_write_data(self.function)
        self.docs_bucket.grant_read_write(self.function)
        self.topic.grant_publish(self.function)

        # Grant Bedrock access for chatbot
        self.function.add_to_role_policy(
            statement={
                "Effect": "Allow",
                "Action": ["bedrock:InvokeModel"],
                "Resource": "arn:aws:bedrock:*:*:foundation-model/*",
            }
        )

    def _create_api_gateway(self, api_deployment_token: str):
        """Create API Gateway for this vertical"""
        self.api = apigateway.RestApi(
            self,
            "Api",
            rest_api_name=f"{self.app_name}-{self.vertical_name}-api-{self.stage_name}",
            description=f"API for {self.vertical_name} vertical",
            deploy_options=apigateway.StageOptions(
                stage_name=self.stage_name,
                throttling_rate_limit=100,
                throttling_burst_limit=200,
            ),
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["*"],
            ),
        )

        # Add proxy integration
        integration = apigateway.LambdaIntegration(
            self.function,
            proxy=True,
            allow_test_invoke=True,
        )

        # Add {proxy+} resource for all routes
        proxy_resource = self.api.root.add_resource("{proxy+}")
        proxy_resource.add_method("ANY", integration)

        # Also handle root path
        self.api.root.add_method("ANY", integration)

        # Store API URL
        self.api_url = f"{self.api.url}{self.stage_name}/"
