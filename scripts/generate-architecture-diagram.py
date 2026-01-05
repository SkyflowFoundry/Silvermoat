#!/usr/bin/env python3
"""
Generate multiple documentation diagrams for Silvermoat platform using the diagrams library.

This script creates professional diagrams with official AWS icons:
- Architecture: Infrastructure layout
- Data Flow: Request/response flows
- ERD: Entity relationship diagram
- User Journey: Customer and agent workflows
- CI/CD: Deployment pipeline

Requirements:
    - pip install diagrams
    - brew install graphviz (macOS) or apt install graphviz (Ubuntu/Debian)

Usage:
    python scripts/generate-architecture-diagram.py

Outputs:
    docs/architecture.png
    docs/data-flow.png
    docs/erd.png
    docs/user-journey.png
    docs/cicd-pipeline.png
"""

from diagrams import Diagram, Cluster, Edge, Node
from diagrams.aws.network import CloudFront, APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import SNS, Eventbridge
from diagrams.aws.security import CertificateManager, IAM
from diagrams.aws.ml import Bedrock
from diagrams.saas.cdn import Cloudflare
from diagrams.onprem.client import User, Users
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import GithubActions
from diagrams.programming.framework import React

def generate_architecture_diagram():
    """Generate simplified Silvermoat AWS architecture diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "0.5",
    }

    with Diagram(
        "Silvermoat AWS Architecture",
        filename="docs/architecture",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # Frontend
        with Cluster("Frontend"):
            cloudflare = Cloudflare("Cloudflare\nDNS")
            cloudfront = CloudFront("CloudFront")
            ui_bucket = S3("UI Assets")

            cloudflare >> cloudfront >> ui_bucket

        # API Layer
        apigw = APIGateway("API Gateway")

        # Compute
        with Cluster("Compute"):
            lambda_fns = Lambda("Lambda\nHandlers\n(4 domain-based)")

        # Data Layer
        with Cluster("Data Storage"):
            dynamodb = Dynamodb("DynamoDB\nTables\n(7 tables)")
            docs_s3 = S3("Document\nStorage")

        # External Services
        with Cluster("External Services"):
            bedrock = Bedrock("AWS Bedrock\nClaude AI")
            sns = SNS("SNS\nNotifications")

        # Main flows
        cloudfront >> apigw
        apigw >> lambda_fns
        lambda_fns >> dynamodb
        lambda_fns >> docs_s3
        lambda_fns >> bedrock
        lambda_fns >> sns

def generate_data_flow_diagram():
    """Generate simplified data flow diagram showing key request flows."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "0.5",
    }

    with Diagram(
        "Silvermoat Data Flow",
        filename="docs/data-flow",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # Components
        customer = User("Customer")
        react_app = CloudFront("React UI")
        api_gw = APIGateway("API Gateway")
        lambda_fn = Lambda("Lambda")

        # Data stores
        with Cluster("Data Layer"):
            dynamodb = Dynamodb("DynamoDB")
            s3_docs = S3("Documents")

        bedrock_ai = Bedrock("Claude AI")

        # Simple left-to-right flow
        customer >> react_app >> api_gw >> lambda_fn
        lambda_fn >> dynamodb
        lambda_fn >> s3_docs
        lambda_fn >> bedrock_ai


def generate_erd_diagram():
    """Generate simplified Entity Relationship Diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "0.5",
        "rankdir": "LR",
    }

    with Diagram(
        "Silvermoat Entity Relationships",
        filename="docs/erd",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # Core entities (simplified - just entity name)
        customer = Dynamodb("Customer")
        quote = Dynamodb("Quote")
        policy = Dynamodb("Policy")
        claim = Dynamodb("Claim")
        payment = Dynamodb("Payment")
        case = Dynamodb("Case")

        # Main relationship chain
        customer >> Edge(label="has many") >> quote
        quote >> Edge(label="becomes") >> policy
        policy >> Edge(label="has") >> claim
        policy >> Edge(label="has") >> payment
        policy >> Edge(label="has") >> case


def generate_user_journey_diagram():
    """Generate user journey map for customer and agent workflows."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "0.5",
    }

    with Diagram(
        "Silvermoat User Journeys",
        filename="docs/user-journey",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        outformat="png"
    ):
        with Cluster("Customer Journey"):
            customer = User("Customer")

            with Cluster("Steps"):
                step1 = Lambda("1. Request\nQuote")
                step2 = Lambda("2. View\nQuote")
                step3 = Lambda("3. Accept &\nCreate Policy")
                step4 = Lambda("4. Make\nPayment")
                step5 = Lambda("5. File\nClaim")
                step6 = Lambda("6. Upload\nDocuments")
                step7 = Lambda("7. Chat with\nAI Support")

            customer >> step1 >> step2 >> step3 >> step4 >> step5 >> step6 >> step7

        with Cluster("Agent Journey"):
            agent = Users("Agent")

            with Cluster("Agent Steps"):
                agent1 = Lambda("1. View\nCustomers")
                agent2 = Lambda("2. Review\nClaims")
                agent3 = Lambda("3. Process\nClaim")
                agent4 = Lambda("4. Manage\nCases")
                agent5 = Lambda("5. Update\nStatus")

            agent >> agent1 >> agent2 >> agent3 >> agent4 >> agent5


def generate_cicd_pipeline_diagram():
    """Generate simplified CI/CD pipeline diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "0.5",
    }

    with Diagram(
        "Silvermoat CI/CD Pipeline",
        filename="docs/cicd-pipeline",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # Source
        github = Github("GitHub PR")

        # Pipeline stages
        with Cluster("Test (on PR)"):
            detect = GithubActions("Detect\nChanges")
            deploy_infra = GithubActions("Deploy Infra")
            deploy_ui = GithubActions("Deploy UI")
            tests = GithubActions("Run Tests\n(Unit/API/E2E)")
            seed = GithubActions("Seed Data")

        # Deployment target
        with Cluster("AWS Test Stack"):
            stack = Lambda("Lambda +\nDynamoDB")
            ui = CloudFront("S3 + UI")

        # Flow
        github >> detect
        detect >> deploy_infra >> stack
        detect >> deploy_ui >> ui
        deploy_infra >> deploy_ui
        deploy_ui >> tests
        tests >> seed


if __name__ == "__main__":
    print("Generating Silvermoat documentation diagrams...\n")

    print("1/5 Generating architecture diagram...")
    generate_architecture_diagram()
    print("    ✓ docs/architecture.png")

    print("2/5 Generating data flow diagram...")
    generate_data_flow_diagram()
    print("    ✓ docs/data-flow.png")

    print("3/5 Generating ERD diagram...")
    generate_erd_diagram()
    print("    ✓ docs/erd.png")

    print("4/5 Generating user journey diagram...")
    generate_user_journey_diagram()
    print("    ✓ docs/user-journey.png")

    print("5/5 Generating CI/CD pipeline diagram...")
    generate_cicd_pipeline_diagram()
    print("    ✓ docs/cicd-pipeline.png")

    print("\n✓ All diagrams generated successfully!")
