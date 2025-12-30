from aws_cdk import (
    aws_lambda as lambda_,
    CustomResource,
)
from aws_cdk import custom_resources as cr
from constructs import Construct


class SeederCustomResource(Construct):
    """Custom resource for seeding demo data and cleanup"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        seeder_function: lambda_.Function,
        ui_seeding_mode: str,
        api_base_url: str,
    ):
        super().__init__(scope, id)

        # Create custom resource provider
        provider = cr.Provider(
            self,
            "SeederProvider",
            on_event_handler=seeder_function,
        )

        # Seed Custom Resource (CREATE/UPDATE)
        self.seed_resource = CustomResource(
            self,
            "SeedCustomResource",
            service_token=provider.service_token,
            properties={
                "Mode": "seed",
                "UiSeedingMode": ui_seeding_mode,
                "ApiBaseUrl": api_base_url,
            },
        )

        # Cleanup Custom Resource (DELETE)
        # Note: With CDK auto_delete_objects on S3 buckets,
        # the cleanup Lambda is primarily needed for DynamoDB
        self.cleanup_resource = CustomResource(
            self,
            "CleanupCustomResource",
            service_token=provider.service_token,
            properties={
                "Mode": "cleanup",
            },
        )
