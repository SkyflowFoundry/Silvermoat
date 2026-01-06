from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_s3 as s3,
    Duration,
)
from constructs import Construct


class FrontendStack(Construct):
    """Frontend layer: CloudFront distribution and ACM certificate (conditional)"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        ui_bucket: s3.Bucket,
        domain_name: str,
        create_cloudfront: bool,
    ):
        super().__init__(scope, id)

        self.distribution = None
        self.certificate = None

        if not create_cloudfront:
            # Test stacks skip CloudFront for fast deployment
            return

        # ACM Certificate (only if domain_name provided)
        # Support wildcard for multi-vertical subdomains
        if domain_name:
            # If domain starts with wildcard, use as-is; otherwise use exact domain
            cert_domain = domain_name if domain_name.startswith("*") else domain_name

            self.certificate = acm.Certificate(
                self,
                "UiCertificate",
                domain_name=cert_domain,
                validation=acm.CertificateValidation.from_dns(),
            )

            # Note: Outputs defined in parent Stack

        # CloudFront Distribution
        # Use HTTP origin for S3 website endpoint (not S3 origin)
        origin = origins.HttpOrigin(
            ui_bucket.bucket_website_domain_name,
            protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
        )

        # Build distribution properties based on whether we have a custom domain
        distribution_props = {
            "default_behavior": cloudfront.BehaviorOptions(
                origin=origin,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                compress=True,
            ),
            "default_root_object": "index.html",
            "error_responses": [
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(5),
                ),
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(5),
                ),
            ],
            "price_class": cloudfront.PriceClass.PRICE_CLASS_100,
        }

        # Add certificate and domain if provided
        if self.certificate and domain_name:
            distribution_props["certificate"] = self.certificate

            # If wildcard cert, add specific subdomains as alternate domains
            if domain_name.startswith("*"):
                # Extract base domain (e.g., "silvermoat.net" from "*.silvermoat.net")
                base_domain = domain_name.lstrip("*").lstrip(".")
                distribution_props["domain_names"] = [
                    f"insurance.{base_domain}",
                    f"retail.{base_domain}",
                    base_domain,  # Also support apex domain
                ]
            else:
                distribution_props["domain_names"] = [domain_name]

            distribution_props["minimum_protocol_version"] = cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021

        self.distribution = cloudfront.Distribution(
            self, "UiDistribution", **distribution_props
        )

        # Note: Outputs must be defined in parent Stack, not here in Construct
