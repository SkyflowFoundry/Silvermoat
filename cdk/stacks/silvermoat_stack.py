from aws_cdk import Stack, CfnOutput
from constructs import Construct
from config.base import SilvermoatConfig
from .data_stack import DataStack
from .storage_stack import StorageStack
from .compute_stack import ComputeStack
from .api_stack import ApiStack
from .frontend_stack import FrontendStack
from custom_constructs.seeder_custom_resource import SeederCustomResource


class SilvermoatStack(Stack):
    """Main Silvermoat CDK stack - orchestrates all nested constructs"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        config: SilvermoatConfig,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # Instantiate nested stacks as constructs
        data = DataStack(self, "DataStack", config.app_name, config.stage_name)

        storage = StorageStack(self, "StorageStack")

        compute = ComputeStack(
            self,
            "ComputeStack",
            config.app_name,
            config.stage_name,
            data,
            storage,
        )

        api = ApiStack(
            self,
            "ApiStack",
            config.app_name,
            config.stage_name,
            compute.mvp_function,
            config.api_deployment_token,
        )

        frontend = FrontendStack(
            self,
            "FrontendStack",
            storage.ui_bucket,
            config.domain_name,
            config.create_cloudfront,
        )

        # Custom resources for seeding and cleanup
        seeder = SeederCustomResource(
            self,
            "Seeder",
            compute.seeder_function,
            config.ui_seeding_mode,
            api.api_url,
        )

        # Top-level outputs (used by scripts)
        # WebUrl is either CloudFront URL or S3 website URL
        if frontend.distribution:
            web_url = f"https://{frontend.distribution.distribution_domain_name}"
        else:
            web_url = storage.ui_bucket.bucket_website_url

        CfnOutput(
            self,
            "WebUrl",
            value=web_url,
            description="Primary web URL for the application",
        )
