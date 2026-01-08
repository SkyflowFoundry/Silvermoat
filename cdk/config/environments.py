from .base import SilvermoatConfig


def get_config(stack_name: str, stage_name: str) -> SilvermoatConfig:
    """Get configuration based on stack name and stage"""

    # Production stacks
    if stack_name in ["silvermoat", "silvermoat-insurance", "silvermoat-retail", "silvermoat-healthcare", "silvermoat-fintech", "silvermoat-landing"]:
        return SilvermoatConfig(
            app_name="silvermoat",
            stage_name="prod",
            api_deployment_token="v1",
            ui_seeding_mode="external",
            domain_name="*.silvermoat.net",  # Wildcard for multi-vertical subdomains
            create_cloudfront=True,
        )

    # Test stacks (PR ephemeral stacks)
    elif stack_name.startswith("silvermoat-test-pr-"):
        # Extract PR number from stack name for unique resource naming
        # Format: silvermoat-test-pr-{N}-{vertical}
        pr_number = stack_name.split("-")[3]
        return SilvermoatConfig(
            app_name=f"silvermoat-test-pr-{pr_number}",
            stage_name="test",
            api_deployment_token="v1",
            ui_seeding_mode="external",
            domain_name="",  # No custom domain for test stacks
            create_cloudfront=False,  # Fast deployment, HTTP only
        )

    # Default/fallback - load from environment
    else:
        return SilvermoatConfig.from_env()
