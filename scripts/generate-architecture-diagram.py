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
    """Generate data flow diagram showing request/response flows."""

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
        with Cluster("Frontend"):
            react_app = React("React App\n(CloudFront)")

        # API Gateway
        api_gw = APIGateway("API Gateway")

        # Lambda Handlers
        with Cluster("Lambda Handlers"):
            customer_handler = Lambda("customer-handler")
            claims_handler = Lambda("claims-handler")
            docs_handler = Lambda("documents-handler")
            ai_handler = Lambda("ai-handler")

        # Data Stores
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
            bedrock = Bedrock("Claude 3.5")

        # Flow 1: Quote Creation
        customer >> Edge(label="1. Request quote", color="blue") >> react_app
        react_app >> Edge(label="POST /quote", color="blue") >> api_gw
        api_gw >> Edge(color="blue") >> customer_handler
        customer_handler >> Edge(label="save", color="blue") >> quotes_db
        quotes_db >> Edge(label="response", color="blue") >> customer_handler
        customer_handler >> Edge(color="blue") >> api_gw
        api_gw >> Edge(color="blue") >> react_app
        react_app >> Edge(label="2. Show quote", color="blue") >> customer

        # Flow 2: Policy Creation
        customer_handler >> Edge(label="create policy", color="green", style="dashed") >> policies_db

        # Flow 3: Claim Filing
        claims_handler >> Edge(label="file claim", color="orange") >> claims_db
        docs_handler >> Edge(label="upload doc", color="orange") >> docs_bucket

        # Flow 4: AI Chatbot
        ai_handler >> Edge(label="query context", color="purple", style="dotted") >> [
            customers_db, quotes_db, policies_db, claims_db
        ]
        ai_handler >> Edge(label="invoke", color="purple") >> bedrock
        bedrock >> Edge(label="response", color="purple") >> ai_handler
        ai_handler >> Edge(label="store", color="purple") >> conversations_db


def generate_erd_diagram():
    """Generate Entity Relationship Diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "0.5",
        "rankdir": "TB",
    }

    with Diagram(
        "Silvermoat Entity Relationships",
        filename="docs/erd",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # Entities as DynamoDB tables
        customer = Dynamodb("Customer\n---\nid\nname\nemail\naddress\nphone")
        quote = Dynamodb("Quote\n---\nid\ncustomerEmail\npropertyAddress\ncoverageAmount\npropertyType")
        policy = Dynamodb("Policy\n---\nid\nquoteId\npolicyNumber\nholderEmail\npremium\neffectiveDate")
        claim = Dynamodb("Claim\n---\nid\npolicyId\nclaimNumber\nlossType\namount\nincidentDate")
        payment = Dynamodb("Payment\n---\nid\npolicyId\namount\npaymentMethod")
        case = Dynamodb("Case\n---\nid\ntitle\nrelatedEntityType\nrelatedEntityId\nassignee")
        conversation = Dynamodb("Conversation\n---\nid\ncustomerEmail\nmessages\ntimestamp")

        # Relationships
        customer >> Edge(label="1:M", style="bold") >> quote
        quote >> Edge(label="1:M", style="bold") >> policy
        policy >> Edge(label="1:M", style="bold") >> claim
        policy >> Edge(label="1:M", style="bold") >> payment
        policy >> Edge(label="1:M", style="bold") >> case
        customer >> Edge(label="1:M", style="bold") >> conversation


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
