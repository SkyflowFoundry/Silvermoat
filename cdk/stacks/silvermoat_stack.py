from aws_cdk import Stack, CfnOutput
from constructs import Construct
from config.base import SilvermoatConfig
from .data_stack import DataStack
from .storage_stack import StorageStack
from .compute_stack import ComputeStack
from .api_stack import ApiStack
from .frontend_stack import FrontendStack


class SilvermoatStack(Stack):
    """Main Silvermoat CDK stack - orchestrates all nested constructs"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        config: SilvermoatConfig,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # Instantiate nested stacks as constructs
        data = DataStack(self, "DataStack", config.app_name, config.stage_name)

        storage = StorageStack(self, "StorageStack")

        compute = ComputeStack(
            self,
            "ComputeStack",
            config.app_name,
            config.stage_name,
            data,
            storage,
        )

        api = ApiStack(
            self,
            "ApiStack",
            config.app_name,
            config.stage_name,
            compute.customer_function,
            compute.claims_function,
            compute.documents_function,
            compute.ai_function,
            config.api_deployment_token,
        )

        frontend = FrontendStack(
            self,
            "FrontendStack",
            storage.ui_bucket,
            config.domain_name,
            config.create_cloudfront,
        )

        # Top-level outputs (used by scripts)
        # All outputs must be at Stack level for CloudFormation compatibility

        # Data Stack outputs
        for table_type in ["Quotes", "Policies", "Claims", "Payments", "Cases"]:
            table = data.tables[table_type.lower()]
            CfnOutput(
                self,
                f"{table_type}TableName",
                value=table.table_name,
                export_name=f"{self.stack_name}-{table_type}TableName",
            )
            CfnOutput(
                self,
                f"{table_type}TableArn",
                value=table.table_arn,
                export_name=f"{self.stack_name}-{table_type}TableArn",
            )

        CfnOutput(
            self,
            "SnsTopicArn",
            value=data.topic.topic_arn,
            export_name=f"{self.stack_name}-SnsTopicArn",
        )

        # Storage Stack outputs
        CfnOutput(
            self,
            "UiBucketName",
            value=storage.ui_bucket.bucket_name,
            export_name=f"{self.stack_name}-UiBucketName",
        )
        CfnOutput(
            self,
            "UiBucketArn",
            value=storage.ui_bucket.bucket_arn,
            export_name=f"{self.stack_name}-UiBucketArn",
        )
        CfnOutput(
            self,
            "UiBucketWebsiteURL",
            value=storage.ui_bucket.bucket_website_url,
            export_name=f"{self.stack_name}-UiBucketWebsiteURL",
        )
        CfnOutput(
            self,
            "UiBucketWebsiteDomain",
            value=storage.ui_bucket.bucket_website_domain_name,
            export_name=f"{self.stack_name}-UiBucketWebsiteDomain",
        )
        CfnOutput(
            self,
            "DocsBucketName",
            value=storage.docs_bucket.bucket_name,
            export_name=f"{self.stack_name}-DocsBucketName",
        )
        CfnOutput(
            self,
            "DocsBucketArn",
            value=storage.docs_bucket.bucket_arn,
            export_name=f"{self.stack_name}-DocsBucketArn",
        )

        # API Stack outputs
        CfnOutput(
            self,
            "ApiBaseUrl",
            value=api.api_url,
            export_name=f"{self.stack_name}-ApiBaseUrl",
        )
        CfnOutput(
            self,
            "ApiId",
            value=api.api.rest_api_id,
            export_name=f"{self.stack_name}-ApiId",
        )

        # Compute Stack outputs
        CfnOutput(
            self,
            "MvpServiceFunctionArn",
            value=compute.mvp_function.function_arn,
            export_name=f"{self.stack_name}-MvpServiceFunctionArn",
        )
        CfnOutput(
            self,
            "MvpServiceFunctionName",
            value=compute.mvp_function.function_name,
            export_name=f"{self.stack_name}-MvpServiceFunctionName",
        )

        # Frontend Stack outputs (conditional)
        if frontend.certificate:
            CfnOutput(
                self,
                "CertificateArn",
                value=frontend.certificate.certificate_arn,
                export_name=f"{self.stack_name}-CertificateArn",
            )

        if frontend.distribution:
            CfnOutput(
                self,
                "CloudFrontUrl",
                value=f"https://{frontend.distribution.distribution_domain_name}",
                export_name=f"{self.stack_name}-CloudFrontUrl",
            )
            CfnOutput(
                self,
                "CloudFrontDomain",
                value=frontend.distribution.distribution_domain_name,
                export_name=f"{self.stack_name}-CloudFrontDomain",
            )
            CfnOutput(
                self,
                "CloudFrontDistributionId",
                value=frontend.distribution.distribution_id,
                export_name=f"{self.stack_name}-CloudFrontDistributionId",
                description="CloudFront distribution ID for cache invalidation",
            )

        if config.domain_name:
            CfnOutput(
                self,
                "CustomDomainUrl",
                value=f"https://{config.domain_name}",
                export_name=f"{self.stack_name}-CustomDomainUrl",
            )

        # WebUrl is either CloudFront URL or S3 website URL
        if frontend.distribution:
            web_url = f"https://{frontend.distribution.distribution_domain_name}"
        else:
            web_url = storage.ui_bucket.bucket_website_url

        CfnOutput(
            self,
            "WebUrl",
            value=web_url,
            description="Primary web URL for the application",
        )
