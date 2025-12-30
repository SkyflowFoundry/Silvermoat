from aws_cdk import (
    aws_s3 as s3,
    CfnOutput,
    RemovalPolicy,
    Stack,
)
from constructs import Construct


class StorageStack(Construct):
    """Storage layer: S3 buckets for UI and documents"""

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # UI Bucket (public website hosting)
        self.ui_bucket = s3.Bucket(
            self,
            "UiBucket",
            website_index_document="index.html",
            website_error_document="index.html",  # SPA routing
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,  # CDK handles cleanup automatically
        )

        # Docs Bucket (private)
        self.docs_bucket = s3.Bucket(
            self,
            "DocsBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Outputs (exact match to CloudFormation)
        CfnOutput(
            self,
            "UiBucketName",
            value=self.ui_bucket.bucket_name,
            export_name=f"{Stack.of(self).stack_name}-UiBucketName",
        )

        CfnOutput(
            self,
            "UiBucketArn",
            value=self.ui_bucket.bucket_arn,
            export_name=f"{Stack.of(self).stack_name}-UiBucketArn",
        )

        CfnOutput(
            self,
            "UiBucketWebsiteURL",
            value=self.ui_bucket.bucket_website_url,
            export_name=f"{Stack.of(self).stack_name}-UiBucketWebsiteURL",
        )

        CfnOutput(
            self,
            "UiBucketWebsiteDomain",
            value=self.ui_bucket.bucket_website_domain_name,
            export_name=f"{Stack.of(self).stack_name}-UiBucketWebsiteDomain",
        )

        CfnOutput(
            self,
            "DocsBucketName",
            value=self.docs_bucket.bucket_name,
            export_name=f"{Stack.of(self).stack_name}-DocsBucketName",
        )

        CfnOutput(
            self,
            "DocsBucketArn",
            value=self.docs_bucket.bucket_arn,
            export_name=f"{Stack.of(self).stack_name}-DocsBucketArn",
        )
