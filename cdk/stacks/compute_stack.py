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

        # MVP Service Lambda
        self.mvp_function = PythonFunction(
            self,
            "MvpServiceFunction",
            entry="../lambda/mvp_service",
            index="handler.py",
            handler="handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            timeout=Duration.seconds(30),
            memory_size=256,
            layers=[shared_layer],
            environment={
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

        # Grant permissions to MVP function
        for table in data_stack.tables.values():
            table.grant_read_write_data(self.mvp_function)

        storage_stack.docs_bucket.grant_read_write(self.mvp_function)
        data_stack.topic.grant_publish(self.mvp_function)

        # Bedrock permissions
        self.mvp_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel"],
                resources=[
                    f"arn:aws:bedrock:{Stack.of(self).region}::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
                ],
            )
        )

        # EventBridge permissions
        self.mvp_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["events:PutEvents"],
                resources=[f"arn:aws:events:{Stack.of(self).region}:{Stack.of(self).account}:event-bus/default"],
            )
        )

        # Note: Outputs must be defined in parent Stack, not here in Construct
