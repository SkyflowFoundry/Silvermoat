#!/usr/bin/env python3
# CDK Application Entry Point - v2.0.0 (Multi-Vertical Parallel)
import os
from aws_cdk import App, Environment
from stacks.insurance_stack import InsuranceStack
from stacks.retail_stack import RetailStack
from stacks.healthcare_stack import HealthcareStack
from stacks.landing_stack import LandingStack
from config.environments import get_config

app = App()

# Get deployment configuration
stack_name = app.node.try_get_context("stack_name") or os.getenv("STACK_NAME", "silvermoat")
stage_name = app.node.try_get_context("stage_name") or os.getenv("STAGE_NAME", "demo")
vertical = os.getenv("VERTICAL")  # Optional: deploy specific vertical only

# AWS environment
env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-1"),
)

# Determine which stacks to deploy
deploy_insurance = vertical is None or vertical == "insurance"
deploy_retail = vertical is None or vertical == "retail"
deploy_healthcare = vertical is None or vertical == "healthcare"
deploy_landing = vertical is None or vertical == "landing"

# ========================================
# Vertical Stacks (Each manages its own certificate)
# ========================================

if deploy_insurance:
    insurance_config = get_config(f"{stack_name}-insurance", stage_name)
    InsuranceStack(
        app,
        f"{stack_name}-insurance",
        config=insurance_config,
        env=env,
    )

if deploy_retail:
    retail_config = get_config(f"{stack_name}-retail", stage_name)
    RetailStack(
        app,
        f"{stack_name}-retail",
        config=retail_config,
        env=env,
    )

if deploy_healthcare:
    healthcare_config = get_config(f"{stack_name}-healthcare", stage_name)
    HealthcareStack(
        app,
        f"{stack_name}-healthcare",
        config=healthcare_config,
        env=env,
    )

if deploy_landing:
    landing_config = get_config(f"{stack_name}-landing", stage_name)
    LandingStack(
        app,
        f"{stack_name}-landing",
        config=landing_config,
        env=env,
    )

app.synth()
