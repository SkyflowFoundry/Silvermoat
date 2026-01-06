"""Frontend layer: Multi-vertical CloudFront distribution with subdomain-based routing"""
from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_s3 as s3,
    Duration,
)
from constructs import Construct


class FrontendStack(Construct):
    """
    Frontend layer: CloudFront distribution with subdomain-based routing to vertical-specific origins.

    Routes:
    - insurance.domain.com → Insurance UI S3 + Insurance API
    - retail.domain.com → Retail UI S3 + Retail API
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        verticals: dict,  # {"insurance": {"ui_bucket": bucket, "api_url": url}, "retail": {...}}
        domain_name: str,
        create_cloudfront: bool,
    ):
        super().__init__(scope, id)

        self.distribution = None
        self.certificate = None
        self.verticals = verticals

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

        # Build CloudFront distribution with multi-vertical origins and behaviors
        self._create_distribution(domain_name)

    def _create_distribution(self, domain_name: str):
        """Create CloudFront distribution with subdomain-based routing"""

        # Create origins for each vertical
        origins_map = {}
        for vertical_name, vertical_config in self.verticals.items():
            ui_bucket = vertical_config["ui_bucket"]

            # UI origin (S3 website endpoint)
            origins_map[f"{vertical_name}_ui"] = origins.HttpOrigin(
                ui_bucket.bucket_website_domain_name,
                protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
                origin_id=f"{vertical_name}-ui-origin",
            )

        # Default behavior (insurance UI - for apex domain and unknown subdomains)
        default_ui_origin = origins_map["insurance_ui"]

        # Build distribution properties
        distribution_props = {
            "default_behavior": cloudfront.BehaviorOptions(
                origin=default_ui_origin,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                compress=True,
                # Cache varies by Host header for subdomain routing
                cache_key_parameters=cloudfront.CacheQueryStringBehavior.none(),
                origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
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
                    base_domain,  # Also support apex domain (defaults to insurance)
                ]
            else:
                distribution_props["domain_names"] = [domain_name]

            distribution_props["minimum_protocol_version"] = cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021

        # Create distribution
        # Note: CloudFront doesn't natively support subdomain-based origin selection.
        # We use CloudFront Functions to route based on Host header.
        # For now, use default origin (insurance) and rely on client-side detection.
        # Future enhancement: Add CloudFront Functions for server-side routing.

        self.distribution = cloudfront.Distribution(
            self, "UiDistribution", **distribution_props
        )

        # TODO: Add CloudFront Function to route requests based on subdomain
        # Currently relies on client-side vertical detection in App.jsx
        # This means all requests go to insurance S3, but client-side JS
        # detects subdomain and loads vertical-specific code.
        # For true server-side routing, need CloudFront Functions to rewrite origin.
