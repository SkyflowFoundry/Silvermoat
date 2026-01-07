#!/usr/bin/env python3
# CDK Application Entry Point - v2.0.0 (Multi-Vertical Parallel)
import os
from aws_cdk import App, Environment
from stacks.certificate_stack import CertificateStack
from stacks.insurance_stack import InsuranceStack
from stacks.retail_stack import RetailStack
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
deploy_landing = vertical is None or vertical == "landing"

# ========================================
# Certificate Stack (Shared - Production Only)
# ========================================
# Deploy shared certificate stack if any vertical needs CloudFront
# Always check certificate needs when deploying verticals (CDK handles dependencies)
certificate_stack = None

# Check if any vertical being deployed needs CloudFront
needs_cloudfront = False

if deploy_insurance:
    insurance_config = get_config(f"{stack_name}-insurance", stage_name)
    if insurance_config.create_cloudfront:
        needs_cloudfront = True

if deploy_retail and not needs_cloudfront:
    retail_config = get_config(f"{stack_name}-retail", stage_name)
    if retail_config.create_cloudfront:
        needs_cloudfront = True

if deploy_landing and not needs_cloudfront:
    landing_config = get_config(f"{stack_name}-landing", stage_name)
    if landing_config.create_cloudfront:
        needs_cloudfront = True

if needs_cloudfront:
    # Use insurance config for certificate (all verticals share same domain settings)
    cert_config = get_config(f"{stack_name}-certificate", stage_name)
    certificate_stack = CertificateStack(
        app,
        f"{stack_name}-certificate",
        config=cert_config,
        env=env,
    )

# ========================================
# Vertical Stacks (Pass shared certificate)
# ========================================

if deploy_insurance:
    insurance_config = get_config(f"{stack_name}-insurance", stage_name)
    InsuranceStack(
        app,
        f"{stack_name}-insurance",
        config=insurance_config,
        certificate_stack=certificate_stack,
        env=env,
    )

if deploy_retail:
    retail_config = get_config(f"{stack_name}-retail", stage_name)
    RetailStack(
        app,
        f"{stack_name}-retail",
        config=retail_config,
        certificate_stack=certificate_stack,
        env=env,
    )

if deploy_landing:
    landing_config = get_config(f"{stack_name}-landing", stage_name)
    LandingStack(
        app,
        f"{stack_name}-landing",
        config=landing_config,
        certificate_stack=certificate_stack,
        env=env,
    )

app.synth()
