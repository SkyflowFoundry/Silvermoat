"""Main Silvermoat CDK stack - multi-vertical platform with isolated resources per vertical"""
from aws_cdk import Stack, CfnOutput, aws_lambda as lambda_
from constructs import Construct
from config.base import SilvermoatConfig
from .vertical_stack import VerticalStack
from .frontend_stack import FrontendStack


class SilvermoatStack(Stack):
    """Main Silvermoat CDK stack - orchestrates all vertical stacks"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        config: SilvermoatConfig,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # Shared Lambda Layer (contains shared/ directory used by all verticals)
        shared_layer = lambda_.LayerVersion(
            self,
            "SharedLayer",
            code=lambda_.Code.from_asset("../lambda/layer"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_12],
            description="Shared utilities for Lambda functions across all verticals",
        )

        # Insurance Vertical Stack
        self.insurance = VerticalStack(
            self,
            "InsuranceVertical",
            vertical_name="insurance",
            app_name=config.app_name,
            stage_name=config.stage_name,
            layer=shared_layer,
            api_deployment_token=config.api_deployment_token,
        )

        # Retail Vertical Stack
        self.retail = VerticalStack(
            self,
            "RetailVertical",
            vertical_name="retail",
            app_name=config.app_name,
            stage_name=config.stage_name,
            layer=shared_layer,
            api_deployment_token=config.api_deployment_token,
        )

        # Frontend Stack with multi-vertical CloudFront distribution
        self.frontend = FrontendStack(
            self,
            "FrontendStack",
            verticals={
                "insurance": {
                    "ui_bucket": self.insurance.ui_bucket,
                    "api_url": self.insurance.api_url,
                },
                "retail": {
                    "ui_bucket": self.retail.ui_bucket,
                    "api_url": self.retail.api_url,
                },
            },
            domain_name=config.domain_name,
            create_cloudfront=config.create_cloudfront,
        )

        # ========================================
        # Outputs
        # ========================================

        # Insurance Vertical Outputs
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

        # Retail Vertical Outputs
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

        # CloudFront Outputs (if enabled)
        if self.frontend.certificate:
            CfnOutput(
                self,
                "CertificateArn",
                value=self.frontend.certificate.certificate_arn,
                export_name=f"{self.stack_name}-CertificateArn",
            )

        if self.frontend.distribution:
            CfnOutput(
                self,
                "CloudFrontUrl",
                value=f"https://{self.frontend.distribution.distribution_domain_name}",
                export_name=f"{self.stack_name}-CloudFrontUrl",
            )
            CfnOutput(
                self,
                "CloudFrontDomain",
                value=self.frontend.distribution.distribution_domain_name,
                export_name=f"{self.stack_name}-CloudFrontDomain",
            )
            CfnOutput(
                self,
                "CloudFrontDistributionId",
                value=self.frontend.distribution.distribution_id,
                export_name=f"{self.stack_name}-CloudFrontDistributionId",
                description="CloudFront distribution ID for cache invalidation",
            )

        # Custom Domain Outputs
        if config.domain_name:
            if config.domain_name.startswith("*"):
                base_domain = config.domain_name.lstrip("*").lstrip(".")
                CfnOutput(
                    self,
                    "InsuranceDomainUrl",
                    value=f"https://insurance.{base_domain}",
                    description="Insurance vertical custom domain URL",
                )
                CfnOutput(
                    self,
                    "RetailDomainUrl",
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

        # Primary Web URL (CloudFront or Insurance S3)
        if self.frontend.distribution:
            web_url = f"https://{self.frontend.distribution.distribution_domain_name}"
        else:
            web_url = self.insurance.ui_bucket.bucket_website_url

        CfnOutput(
            self,
            "WebUrl",
            value=web_url,
            description="Primary web URL (defaults to insurance vertical)",
        )
