#!/usr/bin/env python3
"""
Generate AWS architecture diagram for Silvermoat platform using the diagrams library.

This script creates a professional architecture diagram with official AWS icons
showing the complete infrastructure layout including CloudFront, API Gateway,
Lambda, DynamoDB tables, S3 buckets, SNS, and EventBridge.

Requirements:
    - pip install diagrams
    - brew install graphviz (macOS) or apt install graphviz (Ubuntu/Debian)

Usage:
    python scripts/generate-architecture-diagram.py

Output:
    docs/architecture.png
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import CloudFront, APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import SNS, Eventbridge
from diagrams.aws.security import CertificateManager, IAM
from diagrams.aws.ml import Bedrock
from diagrams.saas.cdn import Cloudflare

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
            cloudflare = Cloudflare("Cloudflare DNS\nsilvermoat.net")

        # Frontend Layer
        with Cluster("Frontend Distribution"):
            cloudfront = CloudFront("CloudFront CDN")
            acm = CertificateManager("ACM Certificate\n*.silvermoat.net")
            ui_bucket = S3("UI Bucket\nStatic Assets")

            cloudfront >> Edge(label="SSL/TLS") << acm
            cloudfront >> Edge(label="origin") >> ui_bucket

        # API Layer
        with Cluster("API Layer"):
            apigw = APIGateway("API Gateway\nREST API")

        # Lambda Handlers (Split by domain)
        with Cluster("Lambda Handlers"):
            customer_fn = Lambda("customer-handler\nCustomer & Quotes")
            claims_fn = Lambda("claims-handler\nPolicies, Claims,\nPayments, Cases")
            docs_fn = Lambda("documents-handler\nDocument Uploads")
            ai_fn = Lambda("ai-handler\nChatbots (Claude)")

        # API Gateway routing
        apigw >> Edge(label="/customer, /quote") >> customer_fn
        apigw >> Edge(label="/policy, /claim,\n/payment, /case") >> claims_fn
        apigw >> Edge(label="/claim/{id}/doc") >> docs_fn
        apigw >> Edge(label="/chat,\n/customer-chat") >> ai_fn

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
            docs_bucket = S3("Documents Bucket\nPolicy/Claim Docs")

        # Notifications & Events
        with Cluster("Notifications & Events"):
            sns_topic = SNS("SNS Topic\nNotifications")
            eventbridge = Eventbridge("EventBridge\nScheduled Events")

        # Security & IAM
        with Cluster("Security & Permissions"):
            lambda_role = IAM("Lambda Execution\nRole")

        # AI Integration
        with Cluster("AI Integration"):
            bedrock = Bedrock("AWS Bedrock\nClaude 3.5 Sonnet")

        # DNS routing to CloudFront
        cloudflare >> Edge(label="CNAME\nDNS routing") >> cloudfront

        # Frontend to API flow
        cloudfront >> Edge(label="HTTPS\nAPI requests") >> apigw

        # Customer Handler Data Access
        customer_fn >> Edge(label="read/write", style="dashed", color="blue") >> customers_table
        customer_fn >> Edge(label="read/write", style="dashed", color="blue") >> quotes_table
        customer_fn >> Edge(label="publish", color="blue") >> sns_topic

        # Claims Handler Data Access
        claims_fn >> Edge(label="read-only", style="dotted", color="green") >> customers_table
        claims_fn >> Edge(label="read/write", style="dashed", color="green") >> policies_table
        claims_fn >> Edge(label="read/write", style="dashed", color="green") >> claims_table
        claims_fn >> Edge(label="read/write", style="dashed", color="green") >> payments_table
        claims_fn >> Edge(label="read/write", style="dashed", color="green") >> cases_table
        claims_fn >> Edge(label="publish", color="green") >> sns_topic

        # Documents Handler Access
        docs_fn >> Edge(label="read-only", style="dotted", color="orange") >> claims_table
        docs_fn >> Edge(label="upload (claims/*)", style="dashed", color="orange") >> docs_bucket
        docs_fn >> Edge(label="publish", color="orange") >> sns_topic

        # AI Handler Data Access (read-only)
        ai_fn >> Edge(label="read-only", style="dotted", color="purple") >> customers_table
        ai_fn >> Edge(label="read-only", style="dotted", color="purple") >> quotes_table
        ai_fn >> Edge(label="read-only", style="dotted", color="purple") >> policies_table
        ai_fn >> Edge(label="read-only", style="dotted", color="purple") >> claims_table
        ai_fn >> Edge(label="read-only", style="dotted", color="purple") >> payments_table
        ai_fn >> Edge(label="read-only", style="dotted", color="purple") >> cases_table
        ai_fn >> Edge(label="read-only", style="dotted", color="purple") >> conversations_table
        ai_fn >> Edge(label="InvokeModel\n(Claude 3.5)", color="purple") >> bedrock

        # EventBridge triggers (kept for potential scheduled tasks)
        eventbridge >> Edge(label="schedule") >> customer_fn

        # IAM permissions
        lambda_role >> Edge(label="grants", style="dotted", color="gray") >> customer_fn
        lambda_role >> Edge(label="grants", style="dotted", color="gray") >> claims_fn
        lambda_role >> Edge(label="grants", style="dotted", color="gray") >> docs_fn
        lambda_role >> Edge(label="grants", style="dotted", color="gray") >> ai_fn

if __name__ == "__main__":
    print("Generating Silvermoat architecture diagram...")
    generate_architecture_diagram()
    print("✓ Diagram generated: docs/architecture.png")
