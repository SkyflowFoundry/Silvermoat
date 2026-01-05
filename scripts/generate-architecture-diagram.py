#!/usr/bin/env python3
"""
Generate multiple documentation diagrams for Silvermoat platform using the diagrams library.

This script creates professional diagrams with official AWS icons:
- Architecture: Infrastructure layout
- Data Flow: Request/response flows
- User Journey: Customer and agent workflows

Requirements:
    - pip install diagrams
    - brew install graphviz (macOS) or apt install graphviz (Ubuntu/Debian)

Usage:
    python scripts/generate-architecture-diagram.py

Outputs:
    docs/architecture.png
    docs/data-flow.png
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
        "pad": "1.0",
        "ranksep": "1.5",
        "nodesep": "1.0",
        "splines": "ortho",
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

        # Data Layer - DynamoDB Tables
        with Cluster("Data Layer"):
            customers_table = Dynamodb("Customers")
            quotes_table = Dynamodb("Quotes")
            policies_table = Dynamodb("Policies")
            claims_table = Dynamodb("Claims")
            payments_table = Dynamodb("Payments")
            cases_table = Dynamodb("Cases")
            conversations_table = Dynamodb("Conversations")

        # External Services
        with Cluster("External Services"):
            docs_bucket = S3("Documents Bucket")
            sns_topic = SNS("SNS Topic")
            eventbridge = Eventbridge("EventBridge")
            bedrock = Bedrock("Claude API")
            lambda_role = IAM("Lambda Role")

        # DNS routing to CloudFront
        cloudflare >> cloudfront

        # Frontend to API flow
        cloudfront >> apigw

        # Simplified connections - use lists for cleaner code
        apigw >> [customer_fn, claims_fn, docs_fn, ai_fn]

        # Lambda handlers to data (simplified - show representative connections)
        customer_fn >> [customers_table, quotes_table]
        claims_fn >> [policies_table, claims_table, payments_table, cases_table]
        ai_fn >> [conversations_table, bedrock]
        docs_fn >> docs_bucket

        # External services
        [customer_fn, claims_fn, docs_fn] >> sns_topic
        eventbridge >> customer_fn
        lambda_role >> [customer_fn, claims_fn, docs_fn, ai_fn]

def generate_data_flow_diagram():
    """Generate detailed data flow diagram showing request flows."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "1.0",
        "ranksep": "1.5",
        "nodesep": "1.0",
        "splines": "ortho",
    }

    with Diagram(
        "Silvermoat Data Flow",
        filename="docs/data-flow",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # User
        customer = User("Customer")

        # Frontend
        with Cluster("Frontend"):
            react_app = CloudFront("CloudFront")

        # API
        api_gw = APIGateway("API Gateway")

        # Lambda Handlers
        with Cluster("Lambda Handlers"):
            customer_fn = Lambda("customer-handler")
            claims_fn = Lambda("claims-handler")
            docs_fn = Lambda("documents-handler")
            ai_fn = Lambda("ai-handler")

        # Data Layer - DynamoDB Tables
        with Cluster("Data Layer"):
            customers_db = Dynamodb("Customers")
            quotes_db = Dynamodb("Quotes")
            policies_db = Dynamodb("Policies")
            claims_db = Dynamodb("Claims")
            payments_db = Dynamodb("Payments")
            cases_db = Dynamodb("Cases")
            conversations_db = Dynamodb("Conversations")

        # External Services
        with Cluster("External Services"):
            docs_bucket = S3("Documents")
            bedrock = Bedrock("Claude API")
            sns = SNS("SNS")

        # Simplified flow - representative connections
        customer >> react_app >> api_gw
        api_gw >> [customer_fn, claims_fn, docs_fn, ai_fn]

        # Lambda to data (show key connections)
        customer_fn >> [customers_db, quotes_db]
        claims_fn >> [policies_db, claims_db, payments_db, cases_db]
        ai_fn >> [conversations_db, bedrock]
        docs_fn >> docs_bucket

        # External services
        [customer_fn, claims_fn, docs_fn] >> sns


def generate_user_journey_diagram():
    """Generate user journey map for customer and agent workflows."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "1.0",
        "ranksep": "1.5",
        "nodesep": "1.0",
        "splines": "ortho",
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

    print("1/3 Generating architecture diagram...")
    generate_architecture_diagram()
    print("    ✓ docs/architecture.png")

    print("2/3 Generating data flow diagram...")
    generate_data_flow_diagram()
    print("    ✓ docs/data-flow.png")

    print("3/3 Generating user journey diagram...")
    generate_user_journey_diagram()
    print("    ✓ docs/user-journey.png")

    print("\n✓ All diagrams generated successfully!")
