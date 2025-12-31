from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy,
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

        # Note: Outputs must be defined in parent Stack, not here in Construct
