from aws_cdk import (
    aws_lambda as lambda_,
    aws_iam as iam,
    Duration,
    Stack,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct
from .data_stack import DataStack
from .storage_stack import StorageStack


class ComputeStack(Construct):
    """Compute layer: Lambda functions and IAM roles"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        app_name: str,
        stage_name: str,
        data_stack: DataStack,
        storage_stack: StorageStack,
    ):
        super().__init__(scope, id)

        # Shared Lambda Layer (contains shared/ directory used by both Lambdas)
        shared_layer = lambda_.LayerVersion(
            self,
            "SharedLayer",
            code=lambda_.Code.from_asset("../lambda/layer"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_12],
            description="Shared utilities for Lambda functions",
        )

        # Customer Handler - Manages customer and quote operations
        self.customer_function = PythonFunction(
            self,
            "CustomerFunction",
            entry="../lambda/customer_handler",
            index="handler.py",
            handler="handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            timeout=Duration.seconds(30),
            memory_size=256,
            layers=[shared_layer],
            environment={
                "CUSTOMERS_TABLE": data_stack.tables["customers"].table_name,
                "QUOTES_TABLE": data_stack.tables["quotes"].table_name,
                "POLICIES_TABLE": data_stack.tables["policies"].table_name,
                "CLAIMS_TABLE": data_stack.tables["claims"].table_name,
                "PAYMENTS_TABLE": data_stack.tables["payments"].table_name,
                "CASES_TABLE": data_stack.tables["cases"].table_name,
                "DOCS_BUCKET": storage_stack.docs_bucket.bucket_name,
                "SNS_TOPIC_ARN": data_stack.topic.topic_arn,
            },
        )

        # Customer handler permissions - full access for demo platform
        for table in data_stack.tables.values():
            table.grant_read_write_data(self.customer_function)
        storage_stack.docs_bucket.grant_read_write(self.customer_function)
        data_stack.topic.grant_publish(self.customer_function)
        self.customer_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["events:PutEvents"],
                resources=[f"arn:aws:events:{Stack.of(self).region}:{Stack.of(self).account}:event-bus/default"],
            )
        )

        # Claims Handler - Manages policies, claims, payments, and cases
        self.claims_function = PythonFunction(
            self,
            "ClaimsFunction",
            entry="../lambda/claims_handler",
            index="handler.py",
            handler="handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            timeout=Duration.seconds(30),
            memory_size=256,
            layers=[shared_layer],
            environment={
                "CUSTOMERS_TABLE": data_stack.tables["customers"].table_name,
                "QUOTES_TABLE": data_stack.tables["quotes"].table_name,
                "POLICIES_TABLE": data_stack.tables["policies"].table_name,
                "CLAIMS_TABLE": data_stack.tables["claims"].table_name,
                "PAYMENTS_TABLE": data_stack.tables["payments"].table_name,
                "CASES_TABLE": data_stack.tables["cases"].table_name,
                "DOCS_BUCKET": storage_stack.docs_bucket.bucket_name,
                "SNS_TOPIC_ARN": data_stack.topic.topic_arn,
            },
        )

        # Claims handler permissions - full access for demo platform
        for table in data_stack.tables.values():
            table.grant_read_write_data(self.claims_function)
        storage_stack.docs_bucket.grant_read_write(self.claims_function)
        data_stack.topic.grant_publish(self.claims_function)
        self.claims_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["events:PutEvents"],
                resources=[f"arn:aws:events:{Stack.of(self).region}:{Stack.of(self).account}:event-bus/default"],
            )
        )

        # Documents Handler - Manages document uploads to S3
        self.documents_function = PythonFunction(
            self,
            "DocumentsFunction",
            entry="../lambda/documents_handler",
            index="handler.py",
            handler="handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            timeout=Duration.seconds(30),
            memory_size=256,
            layers=[shared_layer],
            environment={
                "CUSTOMERS_TABLE": data_stack.tables["customers"].table_name,
                "QUOTES_TABLE": data_stack.tables["quotes"].table_name,
                "POLICIES_TABLE": data_stack.tables["policies"].table_name,
                "CLAIMS_TABLE": data_stack.tables["claims"].table_name,
                "PAYMENTS_TABLE": data_stack.tables["payments"].table_name,
                "CASES_TABLE": data_stack.tables["cases"].table_name,
                "DOCS_BUCKET": storage_stack.docs_bucket.bucket_name,
                "SNS_TOPIC_ARN": data_stack.topic.topic_arn,
            },
        )

        # Documents handler permissions - full access for demo platform
        for table in data_stack.tables.values():
            table.grant_read_write_data(self.documents_function)
        storage_stack.docs_bucket.grant_read_write(self.documents_function)
        data_stack.topic.grant_publish(self.documents_function)
        self.documents_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["events:PutEvents"],
                resources=[f"arn:aws:events:{Stack.of(self).region}:{Stack.of(self).account}:event-bus/default"],
            )
        )

        # AI Handler - Manages AI chatbot operations
        self.ai_function = PythonFunction(
            self,
            "AiFunction",
            entry="../lambda/ai_handler",
            index="handler.py",
            handler="handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            timeout=Duration.seconds(30),
            memory_size=256,
            layers=[shared_layer],
            environment={
                "CUSTOMERS_TABLE": data_stack.tables["customers"].table_name,
                "QUOTES_TABLE": data_stack.tables["quotes"].table_name,
                "POLICIES_TABLE": data_stack.tables["policies"].table_name,
                "CLAIMS_TABLE": data_stack.tables["claims"].table_name,
                "PAYMENTS_TABLE": data_stack.tables["payments"].table_name,
                "CASES_TABLE": data_stack.tables["cases"].table_name,
                "DOCS_BUCKET": storage_stack.docs_bucket.bucket_name,
                "SNS_TOPIC_ARN": data_stack.topic.topic_arn,
                "BEDROCK_MODEL_ID": "anthropic.claude-3-5-sonnet-20240620-v1:0",
                "BEDROCK_REGION": Stack.of(self).region,
            },
        )

        # AI handler permissions - full access for demo platform
        for table in data_stack.tables.values():
            table.grant_read_write_data(self.ai_function)
        storage_stack.docs_bucket.grant_read_write(self.ai_function)
        data_stack.topic.grant_publish(self.ai_function)
        self.ai_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["events:PutEvents"],
                resources=[f"arn:aws:events:{Stack.of(self).region}:{Stack.of(self).account}:event-bus/default"],
            )
        )
        self.ai_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel"],
                resources=[
                    f"arn:aws:bedrock:{Stack.of(self).region}::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
                ],
            )
        )

        # Add Function URL with streaming support for AI handler
        self.ai_function_url = self.ai_function.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.NONE,
            invoke_mode=lambda_.InvokeMode.RESPONSE_STREAM,
            cors=lambda_.FunctionUrlCorsOptions(
                allowed_origins=["*"],  # Will be restricted in production
                allowed_methods=[lambda_.HttpMethod.POST],
                allowed_headers=["Content-Type", "Accept"],
                max_age=Duration.seconds(300),
            ),
        )

        # Keep mvp_function reference for backwards compatibility during transition
        # This can be removed once all references are updated
        self.mvp_function = self.customer_function

        # Note: Outputs must be defined in parent Stack, not here in Construct
