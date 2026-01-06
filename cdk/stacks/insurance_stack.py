"""Insurance vertical CDK stack - completely independent"""
from aws_cdk import Stack, CfnOutput, aws_lambda as lambda_
from constructs import Construct
from config.base import SilvermoatConfig
from .vertical_stack import VerticalStack


class InsuranceStack(Stack):
    """Insurance vertical stack - completely self-contained"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        config: SilvermoatConfig,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # Insurance-specific Lambda Layer
        self.layer = lambda_.LayerVersion(
            self,
            "InsuranceLayer",
            code=lambda_.Code.from_asset("../lambda/layer"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_12],
            description="Shared utilities for Insurance Lambda functions",
        )

        # Insurance Vertical Stack
        self.insurance = VerticalStack(
            self,
            "InsuranceVertical",
            vertical_name="insurance",
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
            "InsuranceApiUrl",
            value=self.insurance.api_url,
            description="Insurance API Base URL",
            export_name=f"{self.stack_name}-InsuranceApiUrl",
        )

        CfnOutput(
            self,
            "InsuranceUiBucketName",
            value=self.insurance.ui_bucket.bucket_name,
            description="Insurance UI S3 Bucket",
            export_name=f"{self.stack_name}-InsuranceUiBucketName",
        )

        CfnOutput(
            self,
            "InsuranceUiBucketWebsiteURL",
            value=self.insurance.ui_bucket.bucket_website_url,
            description="Insurance UI S3 Website URL",
            export_name=f"{self.stack_name}-InsuranceUiBucketWebsiteURL",
        )

        CfnOutput(
            self,
            "WebUrl",
            value=self.insurance.ui_bucket.bucket_website_url,
            description="Insurance Web URL",
        )

        # Custom Domain Output (if configured)
        if config.domain_name:
            if config.domain_name.startswith("*"):
                base_domain = config.domain_name.lstrip("*").lstrip(".")
                CfnOutput(
                    self,
                    "CustomDomainUrl",
                    value=f"https://insurance.{base_domain}",
                    description="Insurance vertical custom domain URL",
                )
            else:
                CfnOutput(
                    self,
                    "CustomDomainUrl",
                    value=f"https://{config.domain_name}",
                    export_name=f"{self.stack_name}-CustomDomainUrl",
                )
