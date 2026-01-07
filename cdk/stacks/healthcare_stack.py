"""Healthcare vertical CDK stack - completely independent"""
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as lambda_,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
)
from constructs import Construct
from config.base import SilvermoatConfig
from .vertical_stack import VerticalStack


class HealthcareStack(Stack):
    """Healthcare vertical stack - completely self-contained"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        config: SilvermoatConfig,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # Healthcare-specific Lambda Layer
        self.layer = lambda_.LayerVersion(
            self,
            "HealthcareLayer",
            code=lambda_.Code.from_asset("../lambda/layer"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_12],
            description="Shared utilities for Healthcare Lambda functions",
        )

        # Healthcare Vertical Stack
        self.healthcare = VerticalStack(
            self,
            "HealthcareVertical",
            vertical_name="healthcare",
            app_name=config.app_name,
            stage_name=config.stage_name,
            layer=self.layer,
            api_deployment_token=config.api_deployment_token,
        )

        # ========================================
        # CloudFront Distribution (Production Only)
        # ========================================
        self.certificate = None
        self.distribution = None

        if config.create_cloudfront and config.domain_name:
            # Determine the domain for this vertical
            if config.domain_name.startswith("*"):
                base_domain = config.domain_name.lstrip("*").lstrip(".")
                cert_domain = f"healthcare.{base_domain}"
            else:
                cert_domain = config.domain_name

            # Create certificate for this vertical
            self.certificate = acm.Certificate(
                self,
                "HealthcareCertificate",
                domain_name=cert_domain,
                validation=acm.CertificateValidation.from_dns(),
            )

            # CloudFront origin pointing to S3 website endpoint
            s3_origin = origins.HttpOrigin(
                self.healthcare.ui_bucket.bucket_website_domain_name,
                protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
            )

            # CloudFront distribution using shared certificate
            self.distribution = cloudfront.Distribution(
                self,
                "HealthcareDistribution",
                default_behavior=cloudfront.BehaviorOptions(
                    origin=s3_origin,
                    viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                    allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
                    cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                ),
                domain_names=[cert_domain],
                certificate=self.certificate,
                minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
                price_class=cloudfront.PriceClass.PRICE_CLASS_100,
                error_responses=[
                    cloudfront.ErrorResponse(
                        http_status=403,
                        response_http_status=200,
                        response_page_path="/index.html",
                    ),
                    cloudfront.ErrorResponse(
                        http_status=404,
                        response_http_status=200,
                        response_page_path="/index.html",
                    ),
                ],
            )

        # ========================================
        # Outputs
        # ========================================

        CfnOutput(
            self,
            "HealthcareApiUrl",
            value=self.healthcare.api_url,
            description="Healthcare API Base URL",
            export_name=f"{self.stack_name}-HealthcareApiUrl",
        )

        CfnOutput(
            self,
            "HealthcareUiBucketName",
            value=self.healthcare.ui_bucket.bucket_name,
            description="Healthcare UI S3 Bucket",
            export_name=f"{self.stack_name}-HealthcareUiBucketName",
        )

        CfnOutput(
            self,
            "HealthcareUiBucketWebsiteURL",
            value=self.healthcare.ui_bucket.bucket_website_url,
            description="Healthcare UI S3 Website URL",
            export_name=f"{self.stack_name}-HealthcareUiBucketWebsiteURL",
        )

        # WebUrl: Use CloudFront if available, otherwise S3
        web_url = self.healthcare.ui_bucket.bucket_website_url
        if self.distribution:
            web_url = f"https://{self.distribution.distribution_domain_name}"

        CfnOutput(
            self,
            "WebUrl",
            value=web_url,
            description="Healthcare Web URL",
        )

        # CloudFront Outputs (if enabled)
        if self.certificate:
            CfnOutput(
                self,
                "HealthcareCertificateArn",
                value=self.certificate.certificate_arn,
                description="Healthcare ACM Certificate ARN",
                export_name=f"{self.stack_name}-CertificateArn",
            )

        if self.distribution:
            CfnOutput(
                self,
                "HealthcareCloudFrontDomain",
                value=self.distribution.distribution_domain_name,
                description="Healthcare CloudFront Domain",
                export_name=f"{self.stack_name}-CloudFrontDomain",
            )
            CfnOutput(
                self,
                "HealthcareCloudFrontUrl",
                value=f"https://{self.distribution.distribution_domain_name}",
                description="Healthcare CloudFront URL",
                export_name=f"{self.stack_name}-CloudFrontUrl",
            )
            CfnOutput(
                self,
                "HealthcareCloudFrontDistributionId",
                value=self.distribution.distribution_id,
                description="Healthcare CloudFront Distribution ID",
                export_name=f"{self.stack_name}-CloudFrontDistributionId",
            )

        # Custom Domain Output (if configured)
        if config.domain_name:
            if config.domain_name.startswith("*"):
                base_domain = config.domain_name.lstrip("*").lstrip(".")
                CfnOutput(
                    self,
                    "CustomDomainUrl",
                    value=f"https://healthcare.{base_domain}",
                    description="Healthcare vertical custom domain URL",
                )
            else:
                CfnOutput(
                    self,
                    "CustomDomainUrl",
                    value=f"https://{config.domain_name}",
                    export_name=f"{self.stack_name}-CustomDomainUrl",
                )
