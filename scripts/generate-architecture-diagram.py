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
        # User
        customer = User("Customer")

        # Frontend
        react_app = CloudFront("React UI\n(CloudFront)")

        # API Gateway
        api_gw = APIGateway("API Gateway")

        # Lambda Handler (simplified - one node)
        lambda_fn = Lambda("Lambda\nHandlers")

        # Data Layer (grouped)
        dynamodb = Dynamodb("DynamoDB\nTables")

        # External Services (only show key ones)
        s3_docs = S3("Document\nStorage")
        bedrock_ai = Bedrock("Claude AI")

        # Main flow: Customer → UI → API → Lambda → DB
        customer >> Edge(label="1. Request", color="blue") >> react_app
        react_app >> Edge(label="2. API call", color="blue") >> api_gw
        api_gw >> Edge(label="3. Route", color="blue") >> lambda_fn
        lambda_fn >> Edge(label="4. Query/Write", color="blue") >> dynamodb
        dynamodb >> Edge(label="5. Response", color="blue") >> lambda_fn
        lambda_fn >> Edge(label="6. Return", color="blue") >> api_gw
        api_gw >> Edge(label="7. Data", color="blue") >> react_app
        react_app >> Edge(label="8. Display", color="blue") >> customer

        # Document upload flow
        lambda_fn >> Edge(label="Upload docs", color="orange", style="dashed") >> s3_docs

        # AI chatbot flow
        lambda_fn >> Edge(label="Query AI", color="purple", style="dashed") >> bedrock_ai
        lambda_fn >> Edge(label="Read context", color="purple", style="dotted") >> dynamodb


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
    """Generate CI/CD pipeline diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "0.5",
    }

    with Diagram(
        "Silvermoat CI/CD Pipeline",
        filename="docs/cicd-pipeline",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # Source
        with Cluster("Source"):
            github = Github("GitHub\nRepository")
            pr = GithubActions("Pull Request")

        # CI/CD
        with Cluster("CI/CD (GitHub Actions)"):
            with Cluster("Test Matrix"):
                api_tests = GithubActions("API Tests\n(pytest)")
                e2e_tests = GithubActions("E2E Tests\n(Selenium)")

            with Cluster("Build"):
                cdk_synth = GithubActions("CDK Synth\n(CloudFormation)")
                validate = GithubActions("Validate\nTemplate")

            with Cluster("Deploy"):
                deploy_stack = GithubActions("Deploy Stack\n(Lambda, API, DB)")
                deploy_ui = GithubActions("Deploy UI\n(S3, CloudFront)")

            with Cluster("Post-Deploy"):
                seed_data = GithubActions("Seed Demo\nData")
                invalidate = GithubActions("Invalidate\nCloudFront")

        # AWS Services
        with Cluster("AWS Production"):
            lambda_fn = Lambda("Lambda\nFunctions")
            cloudfront = CloudFront("CloudFront\nDistribution")

        # Flow
        github >> pr
        pr >> [api_tests, e2e_tests]
        api_tests >> cdk_synth
        e2e_tests >> cdk_synth
        cdk_synth >> validate
        validate >> deploy_stack
        deploy_stack >> deploy_ui
        deploy_stack >> lambda_fn
        deploy_ui >> cloudfront
        deploy_ui >> seed_data
        deploy_ui >> invalidate
        invalidate >> cloudfront


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
