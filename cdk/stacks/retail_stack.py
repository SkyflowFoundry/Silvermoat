"""Retail vertical CDK stack - completely independent"""
from aws_cdk import Stack, CfnOutput, aws_lambda as lambda_
from constructs import Construct
from config.base import SilvermoatConfig
from .vertical_stack import VerticalStack


class RetailStack(Stack):
    """Retail vertical stack - completely self-contained"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        config: SilvermoatConfig,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # Retail-specific Lambda Layer
        self.layer = lambda_.LayerVersion(
            self,
            "RetailLayer",
            code=lambda_.Code.from_asset("../lambda/layer"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_12],
            description="Shared utilities for Retail Lambda functions",
        )

        # Retail Vertical Stack
        self.retail = VerticalStack(
            self,
            "RetailVertical",
            vertical_name="retail",
            app_name=config.app_name,
            stage_name=config.stage_name,
            layer=self.layer,
            api_deployment_token=config.api_deployment_token,
        )

        # ========================================
        # Outputs
        # ========================================

        CfnOutput(
            self,
            "RetailApiUrl",
            value=self.retail.api_url,
            description="Retail API Base URL",
            export_name=f"{self.stack_name}-RetailApiUrl",
        )

        CfnOutput(
            self,
            "RetailUiBucketName",
            value=self.retail.ui_bucket.bucket_name,
            description="Retail UI S3 Bucket",
            export_name=f"{self.stack_name}-RetailUiBucketName",
        )

        CfnOutput(
            self,
            "RetailUiBucketWebsiteURL",
            value=self.retail.ui_bucket.bucket_website_url,
            description="Retail UI S3 Website URL",
            export_name=f"{self.stack_name}-RetailUiBucketWebsiteURL",
        )

        CfnOutput(
            self,
            "WebUrl",
            value=self.retail.ui_bucket.bucket_website_url,
            description="Retail Web URL",
        )

        # Custom Domain Output (if configured)
        if config.domain_name:
            if config.domain_name.startswith("*"):
                base_domain = config.domain_name.lstrip("*").lstrip(".")
                CfnOutput(
                    self,
                    "CustomDomainUrl",
                    value=f"https://retail.{base_domain}",
                    description="Retail vertical custom domain URL",
                )
            else:
                CfnOutput(
                    self,
                    "CustomDomainUrl",
                    value=f"https://{config.domain_name}",
                    export_name=f"{self.stack_name}-CustomDomainUrl",
                )
