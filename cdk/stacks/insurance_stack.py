"""Insurance vertical CDK stack - completely independent"""
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
        # CloudFront Distribution (Production Only)
        # ========================================
        self.certificate = None
        self.distribution = None

        if config.create_cloudfront and config.domain_name:
            # Determine the domain for this vertical
            if config.domain_name.startswith("*"):
                base_domain = config.domain_name.lstrip("*").lstrip(".")
                cert_domain = f"insurance.{base_domain}"
            else:
                cert_domain = config.domain_name

            # Create certificate for this vertical
            self.certificate = acm.Certificate(
                self,
                "InsuranceCertificate",
                domain_name=cert_domain,
                validation=acm.CertificateValidation.from_dns(),
            )

            # CloudFront origin pointing to S3 website endpoint
            s3_origin = origins.HttpOrigin(
                self.insurance.ui_bucket.bucket_website_domain_name,
                protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
            )

            # CloudFront distribution using shared certificate
            self.distribution = cloudfront.Distribution(
                self,
                "InsuranceDistribution",
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

        # WebUrl: Use CloudFront if available, otherwise S3
        web_url = self.insurance.ui_bucket.bucket_website_url
        if self.distribution:
            web_url = f"https://{self.distribution.distribution_domain_name}"

        CfnOutput(
            self,
            "WebUrl",
            value=web_url,
            description="Insurance Web URL",
        )

        # CloudFront Outputs (if enabled)
        if self.certificate:
            CfnOutput(
                self,
                "InsuranceCertificateArn",
                value=self.certificate.certificate_arn,
                description="Insurance ACM Certificate ARN",
                export_name=f"{self.stack_name}-CertificateArn",
            )

        if self.distribution:
            CfnOutput(
                self,
                "InsuranceCloudFrontDomain",
                value=self.distribution.distribution_domain_name,
                description="Insurance CloudFront Domain",
                export_name=f"{self.stack_name}-CloudFrontDomain",
            )
            CfnOutput(
                self,
                "InsuranceCloudFrontUrl",
                value=f"https://{self.distribution.distribution_domain_name}",
                description="Insurance CloudFront URL",
                export_name=f"{self.stack_name}-CloudFrontUrl",
            )
            CfnOutput(
                self,
                "InsuranceCloudFrontDistributionId",
                value=self.distribution.distribution_id,
                description="Insurance CloudFront Distribution ID",
                export_name=f"{self.stack_name}-CloudFrontDistributionId",
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
