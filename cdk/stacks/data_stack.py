from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_sns as sns,
    CfnOutput,
    RemovalPolicy,
    Stack,
)
from constructs import Construct


class DataStack(Construct):
    """Data layer: DynamoDB tables and SNS topic"""

    def __init__(self, scope: Construct, id: str, app_name: str, stage_name: str):
        super().__init__(scope, id)

        # Create DynamoDB tables
        self.tables = {}
        table_types = ["Quotes", "Policies", "Claims", "Payments", "Cases"]

        for table_type in table_types:
            table = dynamodb.Table(
                self,
                f"{table_type}Table",
                partition_key=dynamodb.Attribute(
                    name="id", type=dynamodb.AttributeType.STRING
                ),
                billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                removal_policy=RemovalPolicy.DESTROY,
            )
            self.tables[table_type.lower()] = table

            # Outputs (exact match to CloudFormation)
            CfnOutput(
                self,
                f"{table_type}TableName",
                value=table.table_name,
                export_name=f"{Stack.of(self).stack_name}-{table_type}TableName",
            )

            CfnOutput(
                self,
                f"{table_type}TableArn",
                value=table.table_arn,
                export_name=f"{Stack.of(self).stack_name}-{table_type}TableArn",
            )

        # SNS Topic
        self.topic = sns.Topic(
            self,
            "DemoNotificationsTopic",
            display_name=f"{app_name}-{stage_name}-demo-notifications",
        )

        CfnOutput(
            self,
            "SnsTopicArn",
            value=self.topic.topic_arn,
            export_name=f"{Stack.of(self).stack_name}-SnsTopicArn",
        )
