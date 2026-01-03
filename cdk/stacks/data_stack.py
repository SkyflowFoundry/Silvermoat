from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_sns as sns,
    RemovalPolicy,
)
from constructs import Construct


class DataStack(Construct):
    """Data layer: DynamoDB tables and SNS topic"""

    def __init__(self, scope: Construct, id: str, app_name: str, stage_name: str):
        super().__init__(scope, id)

        # Create DynamoDB tables
        self.tables = {}
        table_types = ["Customers", "Quotes", "Policies", "Claims", "Payments", "Cases"]

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

            # Add GSIs for efficient querying
            if table_type == "Customers":
                # GSI for querying by email
                table.add_global_secondary_index(
                    index_name="EmailIndex",
                    partition_key=dynamodb.Attribute(
                        name="email", type=dynamodb.AttributeType.STRING
                    ),
                    projection_type=dynamodb.ProjectionType.ALL,
                )
            elif table_type == "Policies":
                # GSI for querying by customerId
                table.add_global_secondary_index(
                    index_name="CustomerIdIndex",
                    partition_key=dynamodb.Attribute(
                        name="customerId", type=dynamodb.AttributeType.STRING
                    ),
                    projection_type=dynamodb.ProjectionType.ALL,
                )
            elif table_type == "Claims":
                # GSI for querying by customerId
                table.add_global_secondary_index(
                    index_name="CustomerIdIndex",
                    partition_key=dynamodb.Attribute(
                        name="customerId", type=dynamodb.AttributeType.STRING
                    ),
                    projection_type=dynamodb.ProjectionType.ALL,
                )

            self.tables[table_type.lower()] = table

        # SNS Topic
        self.topic = sns.Topic(
            self,
            "DemoNotificationsTopic",
            display_name=f"{app_name}-{stage_name}-demo-notifications",
        )

        # Note: Outputs must be defined in parent Stack, not here in Construct
