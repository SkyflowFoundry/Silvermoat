"""Shared SSL/TLS Certificate Stack for CloudFront distributions"""
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_certificatemanager as acm,
)
from constructs import Construct
from config.base import SilvermoatConfig


class CertificateStack(Stack):
    """
    Shared certificate stack - creates a single wildcard certificate
    that covers all vertical subdomains and apex domain.

    This certificate is used by all CloudFront distributions across
    insurance, retail, and landing verticals.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        config: SilvermoatConfig,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        self.certificate = None

        # Only create certificate for production stacks with CloudFront
        if config.create_cloudfront and config.domain_name:
            # Determine domains based on configuration
            if config.domain_name.startswith("*"):
                # Wildcard config: extract base domain
                base_domain = config.domain_name.lstrip("*").lstrip(".")
                primary_domain = base_domain  # silvermoat.net
                wildcard_domain = f"*.{base_domain}"  # *.silvermoat.net
            else:
                # Direct domain config
                primary_domain = config.domain_name
                wildcard_domain = f"*.{config.domain_name}"

            # Create single certificate with SANs (Subject Alternative Names)
            # This covers:
            # - silvermoat.com (apex domain for landing)
            # - *.silvermoat.net (wildcard for insurance, retail, future verticals)
            self.certificate = acm.Certificate(
                self,
                "SharedCertificate",
                domain_name=primary_domain,  # Primary: silvermoat.com or silvermoat.net
                subject_alternative_names=[wildcard_domain],  # SAN: *.silvermoat.net
                validation=acm.CertificateValidation.from_dns(),
            )

            # Export certificate ARN for other stacks to import
            CfnOutput(
                self,
                "SharedCertificateArn",
                value=self.certificate.certificate_arn,
                description="Shared wildcard certificate ARN for all CloudFront distributions",
                export_name=f"{self.stack_name}-CertificateArn",
            )

            CfnOutput(
                self,
                "CertificateDomain",
                value=primary_domain,
                description="Primary domain name for certificate",
            )
