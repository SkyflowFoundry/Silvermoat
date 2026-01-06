"""Landing page CDK stack - static content only"""
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_s3 as s3,
    RemovalPolicy,
)
from constructs import Construct
from config.base import SilvermoatConfig


class LandingStack(Stack):
    """Landing page stack - simplified S3-only deployment"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        config: SilvermoatConfig,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # S3 bucket for UI hosting (static website)
        self.ui_bucket = s3.Bucket(
            self,
            "LandingUiBucket",
            bucket_name=f"{config.app_name}-landing-ui-{config.stage_name}",
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

        # ========================================
        # Outputs
        # ========================================

        CfnOutput(
            self,
            "LandingUiBucketName",
            value=self.ui_bucket.bucket_name,
            description="Landing page UI S3 Bucket",
            export_name=f"{self.stack_name}-LandingUiBucketName",
        )

        CfnOutput(
            self,
            "LandingUiBucketWebsiteURL",
            value=self.ui_bucket.bucket_website_url,
            description="Landing page UI S3 Website URL",
            export_name=f"{self.stack_name}-LandingUiBucketWebsiteURL",
        )

        CfnOutput(
            self,
            "WebUrl",
            value=self.ui_bucket.bucket_website_url,
            description="Landing page Web URL",
        )

        # Custom Domain Output (if configured)
        if config.domain_name:
            if config.domain_name.startswith("*"):
                base_domain = config.domain_name.lstrip("*").lstrip(".")
                CfnOutput(
                    self,
                    "CustomDomainUrl",
                    value=f"https://{base_domain}",
                    description="Landing page custom domain URL (apex)",
                )
            else:
                CfnOutput(
                    self,
                    "CustomDomainUrl",
                    value=f"https://{config.domain_name}",
                    export_name=f"{self.stack_name}-CustomDomainUrl",
                )
