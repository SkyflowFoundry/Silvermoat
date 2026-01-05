#!/usr/bin/env python3
"""
Generate multiple documentation diagrams for Silvermoat platform using the diagrams library.

This script creates professional diagrams with official AWS icons:
- Architecture: Infrastructure layout
- Data Flow: Request/response flows
- ERD: Entity relationship diagram
- User Journey: Customer and agent workflows

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
    """Generate the Silvermoat AWS architecture diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "0.5",
    }

    with Diagram(
        "Silvermoat AWS Architecture",
        filename="docs/architecture",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # DNS Layer
        with Cluster("DNS Management"):
            cloudflare = Cloudflare("Cloudflare")

        # Frontend Layer
        with Cluster("Frontend Distribution"):
            cloudfront = CloudFront("CloudFront")
            acm = CertificateManager("ACM Certificate")
            ui_bucket = S3("UI Bucket")

            cloudfront >> acm
            cloudfront >> ui_bucket

        # API Layer
        with Cluster("API Layer"):
            apigw = APIGateway("API Gateway")

        # Lambda Handlers (Split by domain)
        with Cluster("Lambda Handlers"):
            customer_fn = Lambda("customer-handler")
            claims_fn = Lambda("claims-handler")
            docs_fn = Lambda("documents-handler")
            ai_fn = Lambda("ai-handler")

        # API Gateway routing
        apigw >> customer_fn
        apigw >> claims_fn
        apigw >> docs_fn
        apigw >> ai_fn

        # Data Layer - DynamoDB Tables
        with Cluster("Data Layer"):
            with Cluster("Core Entities"):
                customers_table = Dynamodb("Customers")
                quotes_table = Dynamodb("Quotes")
                policies_table = Dynamodb("Policies")

            with Cluster("Operations"):
                claims_table = Dynamodb("Claims")
                payments_table = Dynamodb("Payments")
                cases_table = Dynamodb("Cases")

            with Cluster("AI Context"):
                conversations_table = Dynamodb("Conversations")

        # Storage Layer
        with Cluster("Document Storage"):
            docs_bucket = S3("Documents Bucket")

        # Notifications & Events
        with Cluster("Notifications & Events"):
            sns_topic = SNS("SNS Topic")
            eventbridge = Eventbridge("EventBridge")

        # Security & IAM
        with Cluster("Security & Permissions"):
            lambda_role = IAM("Lambda Role")

        # AI Integration
        with Cluster("AI Integration"):
            bedrock = Bedrock("Claude API")

        # DNS routing to CloudFront
        cloudflare >> cloudfront

        # Frontend to API flow
        cloudfront >> apigw

        # Customer Handler Data Access
        customer_fn >> customers_table
        customer_fn >> quotes_table
        customer_fn >> sns_topic

        # Claims Handler Data Access
        claims_fn >> customers_table
        claims_fn >> policies_table
        claims_fn >> claims_table
        claims_fn >> payments_table
        claims_fn >> cases_table
        claims_fn >> sns_topic

        # Documents Handler Access
        docs_fn >> claims_table
        docs_fn >> docs_bucket
        docs_fn >> sns_topic

        # AI Handler Data Access (read-only)
        ai_fn >> customers_table
        ai_fn >> quotes_table
        ai_fn >> policies_table
        ai_fn >> claims_table
        ai_fn >> payments_table
        ai_fn >> cases_table
        ai_fn >> conversations_table
        ai_fn >> bedrock

        # EventBridge triggers
        eventbridge >> customer_fn

        # IAM permissions
        lambda_role >> customer_fn
        lambda_role >> claims_fn
        lambda_role >> docs_fn
        lambda_role >> ai_fn

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




if __name__ == "__main__":
    print("Generating Silvermoat documentation diagrams...\n")

    print("1/4 Generating architecture diagram...")
    generate_architecture_diagram()
    print("    ✓ docs/architecture.png")

    print("2/4 Generating data flow diagram...")
    generate_data_flow_diagram()
    print("    ✓ docs/data-flow.png")

    print("3/4 Generating ERD diagram...")
    generate_erd_diagram()
    print("    ✓ docs/erd.png")

    print("4/4 Generating user journey diagram...")
    generate_user_journey_diagram()
    print("    ✓ docs/user-journey.png")

    print("\n✓ All diagrams generated successfully!")
