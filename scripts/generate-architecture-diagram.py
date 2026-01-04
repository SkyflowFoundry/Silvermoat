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
            lambda_fn = Lambda("Lambda Handler\nPython 3.12")

            apigw >> Edge(label="proxy+") >> lambda_fn

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

        # External Integration
        with Cluster("AI Integration"):
            claude_api = Lambda("Claude API\nChatbot Engine")

        # Frontend to API flow
        cloudfront >> Edge(label="HTTPS\nAPI requests") >> apigw

        # Lambda to Data Layer
        lambda_fn >> Edge(label="read/write", style="dashed") >> customers_table
        lambda_fn >> Edge(label="read/write", style="dashed") >> quotes_table
        lambda_fn >> Edge(label="read/write", style="dashed") >> policies_table
        lambda_fn >> Edge(label="read/write", style="dashed") >> claims_table
        lambda_fn >> Edge(label="read/write", style="dashed") >> payments_table
        lambda_fn >> Edge(label="read/write", style="dashed") >> cases_table
        lambda_fn >> Edge(label="read/write", style="dashed") >> conversations_table

        # Lambda to Storage
        lambda_fn >> Edge(label="upload/download", style="dashed") >> docs_bucket

        # Lambda to Notifications
        lambda_fn >> Edge(label="publish") >> sns_topic

        # EventBridge triggers
        eventbridge >> Edge(label="schedule") >> lambda_fn

        # IAM permissions
        lambda_role >> Edge(label="grants", style="dotted", color="gray") >> lambda_fn

        # Claude API integration
        lambda_fn >> Edge(label="chatbot\nrequests") >> claude_api

if __name__ == "__main__":
    print("Generating Silvermoat architecture diagram...")
    generate_architecture_diagram()
    print("✓ Diagram generated: docs/architecture.png")
