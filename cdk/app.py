#!/usr/bin/env python3
# CDK Application Entry Point - v1.0.0
import os
from aws_cdk import App, Environment
from stacks.silvermoat_stack import SilvermoatStack
from config.environments import get_config

app = App()

# Get stack name from context or environment
stack_name = app.node.try_get_context("stack_name") or os.getenv("STACK_NAME", "silvermoat")
stage_name = app.node.try_get_context("stage_name") or os.getenv("STAGE_NAME", "demo")

# Get configuration
config = get_config(stack_name, stage_name)

# Create stack
SilvermoatStack(
    app,
    stack_name,
    config=config,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION", "us-east-1"),
    ),
)

app.synth()
