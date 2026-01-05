#!/usr/bin/env python3
"""
Generate documentation diagrams for Silvermoat platform using the diagrams library.

This script creates professional diagrams with official AWS icons:
- Architecture: Infrastructure layout (top-bottom)
- Data Flow: Request/response flows (top-bottom)

PNGs are cached for 1 hour (no immutable directive) to allow updates without hard refresh.

Requirements:
    - pip install diagrams
    - brew install graphviz (macOS) or apt install graphviz (Ubuntu/Debian)

Usage:
    python scripts/generate-architecture-diagram.py

Outputs:
    docs/architecture.png
    docs/data-flow.png
"""

from diagrams import Diagram, Cluster
from diagrams.aws.network import CloudFront, APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import SNS, Eventbridge
from diagrams.aws.security import CertificateManager, IAM
from diagrams.aws.ml import Bedrock
from diagrams.saas.cdn import Cloudflare
from diagrams.onprem.client import User

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

        # Storage Layer
        with Cluster("Storage"):
            docs_bucket = S3("Documents")

        # Notifications & Events
        with Cluster("Notifications & Events"):
            sns_topic = SNS("SNS")
            eventbridge = Eventbridge("EventBridge")

        # AI Integration
        with Cluster("AI Integration"):
            bedrock = Bedrock("Bedrock")

        # Security & Permissions
        with Cluster("Security & Permissions"):
            lambda_role = IAM("IAM Role")

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
        direction="TB",
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

        # Storage
        with Cluster("Storage"):
            docs_bucket = S3("Documents")

        # AI Integration
        with Cluster("AI Integration"):
            bedrock = Bedrock("Bedrock")

        # Notifications
        with Cluster("Notifications"):
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


if __name__ == "__main__":
    print("Generating Silvermoat documentation diagrams...\n")

    print("1/2 Generating architecture diagram...")
    generate_architecture_diagram()
    print("    ✓ docs/architecture.png")

    print("2/2 Generating data flow diagram...")
    generate_data_flow_diagram()
    print("    ✓ docs/data-flow.png")

    print("\n✓ All diagrams generated successfully!")
