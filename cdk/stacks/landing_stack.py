"""Landing page CDK stack - static content only"""
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
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
        # CloudFront Distribution (Production Only)
        # ========================================
        self.certificate = None
        self.distribution = None

        if config.create_cloudfront and config.domain_name:
            # ACM Certificate for custom domain (must be in us-east-1 for CloudFront)
            # Landing uses apex domain (silvermoat.com) instead of subdomain
            if config.domain_name.startswith("*"):
                # Extract base domain for apex
                base_domain = config.domain_name.lstrip("*").lstrip(".")
                cert_domain = base_domain  # Apex domain
            else:
                cert_domain = config.domain_name

            self.certificate = acm.Certificate(
                self,
                "LandingCertificate",
                domain_name=cert_domain,
                validation=acm.CertificateValidation.from_dns(),
            )

            # CloudFront origin pointing to S3 website endpoint
            s3_origin = origins.HttpOrigin(
                self.ui_bucket.bucket_website_domain_name,
                protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
            )

            # CloudFront distribution
            self.distribution = cloudfront.Distribution(
                self,
                "LandingDistribution",
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

        # WebUrl: Use CloudFront if available, otherwise S3
        web_url = self.ui_bucket.bucket_website_url
        if self.distribution:
            web_url = f"https://{self.distribution.distribution_domain_name}"

        CfnOutput(
            self,
            "WebUrl",
            value=web_url,
            description="Landing page Web URL",
        )

        # CloudFront Outputs (if enabled)
        if self.certificate:
            CfnOutput(
                self,
                "LandingCertificateArn",
                value=self.certificate.certificate_arn,
                description="Landing ACM Certificate ARN",
                export_name=f"{self.stack_name}-CertificateArn",
            )

        if self.distribution:
            CfnOutput(
                self,
                "LandingCloudFrontDomain",
                value=self.distribution.distribution_domain_name,
                description="Landing CloudFront Domain",
                export_name=f"{self.stack_name}-CloudFrontDomain",
            )
            CfnOutput(
                self,
                "LandingCloudFrontUrl",
                value=f"https://{self.distribution.distribution_domain_name}",
                description="Landing CloudFront URL",
                export_name=f"{self.stack_name}-CloudFrontUrl",
            )
            CfnOutput(
                self,
                "LandingCloudFrontDistributionId",
                value=self.distribution.distribution_id,
                description="Landing CloudFront Distribution ID",
                export_name=f"{self.stack_name}-CloudFrontDistributionId",
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
