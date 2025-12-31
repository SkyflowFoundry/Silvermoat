from .base import SilvermoatConfig


def get_config(stack_name: str, stage_name: str) -> SilvermoatConfig:
    """Get configuration based on stack name and stage"""

    # Production stack
    if stack_name == "silvermoat":
        return SilvermoatConfig(
            app_name="silvermoat",
            stage_name="prod",
            api_deployment_token="v1",
            ui_seeding_mode="external",
            domain_name="silvermoat.net",
            create_cloudfront=True,
        )

    # Test stacks (PR ephemeral stacks)
    elif stack_name.startswith("silvermoat-test-pr-"):
        return SilvermoatConfig(
            app_name="silvermoat-test",
            stage_name="test",
            api_deployment_token="v1",
            ui_seeding_mode="external",
            domain_name="",  # No custom domain for test stacks
            create_cloudfront=False,  # Fast deployment, HTTP only
        )

    # Default/fallback - load from environment
    else:
        return SilvermoatConfig.from_env()
