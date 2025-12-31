import os
from dataclasses import dataclass


@dataclass
class SilvermoatConfig:
    """Configuration for Silvermoat CDK stack"""

    app_name: str
    stage_name: str
    api_deployment_token: str
    ui_seeding_mode: str
    domain_name: str
    create_cloudfront: bool

    @staticmethod
    def from_env():
        """Load configuration from environment variables"""
        return SilvermoatConfig(
            app_name=os.getenv("APP_NAME", "silvermoat"),
            stage_name=os.getenv("STAGE_NAME", "demo"),
            api_deployment_token=os.getenv("API_DEPLOYMENT_TOKEN", "v1"),
            ui_seeding_mode=os.getenv("UI_SEEDING_MODE", "external"),
            domain_name=os.getenv("DOMAIN_NAME", "silvermoat.net"),
            create_cloudfront=os.getenv("CREATE_CLOUDFRONT", "true").lower() == "true",
        )
