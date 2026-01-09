#!/usr/bin/env python3
"""
Generate documentation diagrams for Silvermoat multi-vertical platform using the diagrams library.

This script creates professional diagrams with official AWS icons showing the multi-vertical architecture:
- Architecture: Infrastructure layout with separate Insurance and Retail verticals (top-bottom)
- Data Flow: Request/response flows showing vertical isolation (top-bottom)

PNGs are cached for 1 hour (no immutable directive) to allow updates without hard refresh.

Requirements:
    - pip install diagrams
    - brew install graphviz (macOS) or apt install graphviz (Ubuntu/Debian)

Usage:
    python scripts/generate-architecture-diagram.py [--vertical {insurance,retail,all}]

Outputs:
    --vertical insurance: docs/architecture-insurance.png, docs/data-flow-insurance.png
    --vertical retail: docs/architecture-retail.png, docs/data-flow-retail.png
    --vertical all (default): All 6 diagrams above + docs/architecture.png, docs/data-flow.png
"""

import argparse
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import CloudFront, APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import SNS, Eventbridge
from diagrams.aws.security import CertificateManager, IAM
from diagrams.aws.ml import Bedrock
from diagrams.saas.cdn import Cloudflare
from diagrams.onprem.client import User

def generate_shared_services():
    """Create shared Bedrock AI service node."""
    bedrock = Bedrock("Bedrock\\n(Shared)")
    return bedrock


def generate_multi_vertical_architecture_diagram():
    """Generate the Silvermoat multi-vertical AWS architecture diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "1.0",
        "ranksep": "1.5",
        "nodesep": "1.0",
        "splines": "ortho",
    }

    with Diagram(
        "Silvermoat Multi-Vertical AWS Architecture",
        filename="docs/architecture",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # DNS Layer
        with Cluster("DNS Management"):
            cloudflare = Cloudflare("Cloudflare\n*.silvermoat.net")

        # Landing Page
        with Cluster("Landing Page"):
            with Cluster("Frontend Distribution"):
                landing_cloudfront = CloudFront("CloudFront\nsilvermoat.net")
                landing_ui_bucket = S3("UI Bucket")

            landing_cloudfront >> landing_ui_bucket

        # Insurance Vertical
        with Cluster("Insurance Vertical"):
            with Cluster("Frontend Distribution"):
                ins_cloudfront = CloudFront("CloudFront\ninsurance.silvermoat.net")
                ins_acm = CertificateManager("ACM Cert")
                ins_ui_bucket = S3("UI Bucket")

                ins_cloudfront >> ins_acm
                ins_cloudfront >> ins_ui_bucket

            with Cluster("API Layer"):
                ins_apigw = APIGateway("API Gateway")

            with Cluster("Lambda Handlers"):
                ins_customer_fn = Lambda("customer-handler")
                ins_claims_fn = Lambda("claims-handler")
                ins_docs_fn = Lambda("documents-handler")
                ins_ai_fn = Lambda("ai-handler")

            with Cluster("Data Layer"):
                ins_customers_table = Dynamodb("Customers")
                ins_quotes_table = Dynamodb("Quotes")
                ins_policies_table = Dynamodb("Policies")
                ins_claims_table = Dynamodb("Claims")
                ins_payments_table = Dynamodb("Payments")
                ins_cases_table = Dynamodb("Cases")
                ins_conversations_table = Dynamodb("Conversations")

            with Cluster("Storage"):
                ins_docs_bucket = S3("Documents")

            # Insurance connections
            cloudflare >> ins_cloudfront
            ins_cloudfront >> ins_apigw
            ins_apigw >> [ins_customer_fn, ins_claims_fn, ins_docs_fn, ins_ai_fn]
            ins_customer_fn >> [ins_customers_table, ins_quotes_table]
            ins_claims_fn >> [ins_policies_table, ins_claims_table, ins_payments_table, ins_cases_table]
            ins_ai_fn >> ins_conversations_table
            ins_docs_fn >> ins_docs_bucket

        # Retail Vertical
        with Cluster("Retail Vertical"):
            with Cluster("Frontend Distribution"):
                ret_cloudfront = CloudFront("CloudFront\nretail.silvermoat.net")
                ret_acm = CertificateManager("ACM Cert")
                ret_ui_bucket = S3("UI Bucket")

                ret_cloudfront >> ret_acm
                ret_cloudfront >> ret_ui_bucket

            with Cluster("API Layer"):
                ret_apigw = APIGateway("API Gateway")

            with Cluster("Lambda Handlers"):
                ret_products_fn = Lambda("products-handler")
                ret_orders_fn = Lambda("orders-handler")
                ret_inventory_fn = Lambda("inventory-handler")
                ret_ai_fn = Lambda("ai-handler")

            with Cluster("Data Layer"):
                ret_customers_table = Dynamodb("Customers")
                ret_products_table = Dynamodb("Products")
                ret_orders_table = Dynamodb("Orders")
                ret_inventory_table = Dynamodb("Inventory")
                ret_payments_table = Dynamodb("Payments")
                ret_cases_table = Dynamodb("Cases")
                ret_conversations_table = Dynamodb("Conversations")

            with Cluster("Storage"):
                ret_docs_bucket = S3("Documents")

            # Retail connections
            cloudflare >> ret_cloudfront
            ret_cloudfront >> ret_apigw
            ret_apigw >> [ret_products_fn, ret_orders_fn, ret_inventory_fn, ret_ai_fn]
            ret_products_fn >> ret_products_table
            ret_orders_fn >> [ret_orders_table, ret_payments_table]
            ret_inventory_fn >> ret_inventory_table
            ret_ai_fn >> ret_conversations_table
            [ret_products_fn, ret_orders_fn, ret_inventory_fn] >> ret_cases_table

        # Shared Services
        with Cluster("Shared AI Service"):
            bedrock = Bedrock("Bedrock\n(Shared)")

        # AI handlers to Bedrock
        ins_ai_fn >> bedrock
        ret_ai_fn >> bedrock

        # DNS to Landing
        cloudflare >> landing_cloudfront

def generate_multi_vertical_data_flow_diagram():
    """Generate detailed data flow diagram showing request flows with vertical isolation."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "1.0",
        "ranksep": "1.5",
        "nodesep": "1.0",
        "splines": "ortho",
    }

    with Diagram(
        "Silvermoat Multi-Vertical Data Flow",
        filename="docs/data-flow",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # Users
        ins_user = User("Insurance\nCustomer")
        ret_user = User("Retail\nCustomer")

        # Insurance Vertical Flow
        with Cluster("Insurance Vertical"):
            ins_cf = CloudFront("CloudFront")
            ins_api = APIGateway("API Gateway")

            with Cluster("Lambda Handlers"):
                ins_customer_fn = Lambda("customer-handler")
                ins_claims_fn = Lambda("claims-handler")
                ins_ai_fn = Lambda("ai-handler")

            with Cluster("Data Layer"):
                ins_customers_db = Dynamodb("Customers")
                ins_quotes_db = Dynamodb("Quotes")
                ins_policies_db = Dynamodb("Policies")
                ins_claims_db = Dynamodb("Claims")
                ins_conversations_db = Dynamodb("Conversations")

            # Insurance flow
            ins_user >> ins_cf >> ins_api
            ins_api >> [ins_customer_fn, ins_claims_fn, ins_ai_fn]
            ins_customer_fn >> [ins_customers_db, ins_quotes_db]
            ins_claims_fn >> [ins_policies_db, ins_claims_db]
            ins_ai_fn >> ins_conversations_db

        # Retail Vertical Flow
        with Cluster("Retail Vertical"):
            ret_cf = CloudFront("CloudFront")
            ret_api = APIGateway("API Gateway")

            with Cluster("Lambda Handlers"):
                ret_products_fn = Lambda("products-handler")
                ret_orders_fn = Lambda("orders-handler")
                ret_ai_fn = Lambda("ai-handler")

            with Cluster("Data Layer"):
                ret_products_db = Dynamodb("Products")
                ret_orders_db = Dynamodb("Orders")
                ret_inventory_db = Dynamodb("Inventory")
                ret_conversations_db = Dynamodb("Conversations")

            # Retail flow
            ret_user >> ret_cf >> ret_api
            ret_api >> [ret_products_fn, ret_orders_fn, ret_ai_fn]
            ret_products_fn >> ret_products_db
            ret_orders_fn >> [ret_orders_db, ret_inventory_db]
            ret_ai_fn >> ret_conversations_db

        # Shared AI Service
        with Cluster("Shared AI Service"):
            bedrock = Bedrock("Bedrock\n(Shared)")

        # AI handlers to Bedrock
        ins_ai_fn >> bedrock
        ret_ai_fn >> bedrock


def generate_insurance_only_architecture_diagram():
    """Generate insurance-only AWS architecture diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "1.0",
        "ranksep": "1.5",
        "nodesep": "1.0",
        "splines": "ortho",
    }

    with Diagram(
        "Silvermoat Insurance AWS Architecture",
        filename="docs/architecture-insurance",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # DNS Layer
        with Cluster("DNS Management"):
            cloudflare = Cloudflare("Cloudflare\ninsurance.silvermoat.net")

        # Insurance Vertical
        with Cluster("Insurance Vertical"):
            with Cluster("Frontend Distribution"):
                ins_cloudfront = CloudFront("CloudFront\ninsurance.silvermoat.net")
                ins_acm = CertificateManager("ACM Cert")
                ins_ui_bucket = S3("UI Bucket")

                ins_cloudfront >> ins_acm
                ins_cloudfront >> ins_ui_bucket

            with Cluster("API Layer"):
                ins_apigw = APIGateway("API Gateway")

            with Cluster("Lambda Handlers"):
                ins_customer_fn = Lambda("customer-handler")
                ins_claims_fn = Lambda("claims-handler")
                ins_docs_fn = Lambda("documents-handler")
                ins_ai_fn = Lambda("ai-handler")

            with Cluster("Data Layer"):
                ins_customers_table = Dynamodb("Customers")
                ins_quotes_table = Dynamodb("Quotes")
                ins_policies_table = Dynamodb("Policies")
                ins_claims_table = Dynamodb("Claims")
                ins_payments_table = Dynamodb("Payments")
                ins_cases_table = Dynamodb("Cases")
                ins_conversations_table = Dynamodb("Conversations")

            with Cluster("Storage"):
                ins_docs_bucket = S3("Documents")

            # Insurance connections
            cloudflare >> ins_cloudfront
            ins_cloudfront >> ins_apigw
            ins_apigw >> [ins_customer_fn, ins_claims_fn, ins_docs_fn, ins_ai_fn]
            ins_customer_fn >> [ins_customers_table, ins_quotes_table]
            ins_claims_fn >> [ins_policies_table, ins_claims_table, ins_payments_table, ins_cases_table]
            ins_ai_fn >> ins_conversations_table
            ins_docs_fn >> ins_docs_bucket

        # Shared AI Service
        with Cluster("Shared AI Service"):
            bedrock = Bedrock("Bedrock")

        # AI handler to Bedrock
        ins_ai_fn >> bedrock


def generate_insurance_only_data_flow_diagram():
    """Generate insurance-only data flow diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "1.0",
        "ranksep": "1.5",
        "nodesep": "1.0",
        "splines": "ortho",
    }

    with Diagram(
        "Silvermoat Insurance Data Flow",
        filename="docs/data-flow-insurance",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # User
        ins_user = User("Insurance\nCustomer")

        # Insurance Vertical Flow
        with Cluster("Insurance Vertical"):
            ins_cf = CloudFront("CloudFront")
            ins_api = APIGateway("API Gateway")

            with Cluster("Lambda Handlers"):
                ins_customer_fn = Lambda("customer-handler")
                ins_claims_fn = Lambda("claims-handler")
                ins_ai_fn = Lambda("ai-handler")

            with Cluster("Data Layer"):
                ins_customers_db = Dynamodb("Customers")
                ins_quotes_db = Dynamodb("Quotes")
                ins_policies_db = Dynamodb("Policies")
                ins_claims_db = Dynamodb("Claims")
                ins_conversations_db = Dynamodb("Conversations")

            # Insurance flow
            ins_user >> ins_cf >> ins_api
            ins_api >> [ins_customer_fn, ins_claims_fn, ins_ai_fn]
            ins_customer_fn >> [ins_customers_db, ins_quotes_db]
            ins_claims_fn >> [ins_policies_db, ins_claims_db]
            ins_ai_fn >> ins_conversations_db

        # Shared AI Service
        with Cluster("Shared AI Service"):
            bedrock = Bedrock("Bedrock")

        # AI handler to Bedrock
        ins_ai_fn >> bedrock


def generate_retail_only_architecture_diagram():
    """Generate retail-only AWS architecture diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "1.0",
        "ranksep": "1.5",
        "nodesep": "1.0",
        "splines": "ortho",
    }

    with Diagram(
        "Silvermoat Retail AWS Architecture",
        filename="docs/architecture-retail",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # DNS Layer
        with Cluster("DNS Management"):
            cloudflare = Cloudflare("Cloudflare\nretail.silvermoat.net")

        # Retail Vertical
        with Cluster("Retail Vertical"):
            with Cluster("Frontend Distribution"):
                ret_cloudfront = CloudFront("CloudFront\nretail.silvermoat.net")
                ret_acm = CertificateManager("ACM Cert")
                ret_ui_bucket = S3("UI Bucket")

                ret_cloudfront >> ret_acm
                ret_cloudfront >> ret_ui_bucket

            with Cluster("API Layer"):
                ret_apigw = APIGateway("API Gateway")

            with Cluster("Lambda Handlers"):
                ret_products_fn = Lambda("products-handler")
                ret_orders_fn = Lambda("orders-handler")
                ret_inventory_fn = Lambda("inventory-handler")
                ret_ai_fn = Lambda("ai-handler")

            with Cluster("Data Layer"):
                ret_customers_table = Dynamodb("Customers")
                ret_products_table = Dynamodb("Products")
                ret_orders_table = Dynamodb("Orders")
                ret_inventory_table = Dynamodb("Inventory")
                ret_payments_table = Dynamodb("Payments")
                ret_cases_table = Dynamodb("Cases")
                ret_conversations_table = Dynamodb("Conversations")

            with Cluster("Storage"):
                ret_docs_bucket = S3("Documents")

            # Retail connections
            cloudflare >> ret_cloudfront
            ret_cloudfront >> ret_apigw
            ret_apigw >> [ret_products_fn, ret_orders_fn, ret_inventory_fn, ret_ai_fn]
            ret_products_fn >> ret_products_table
            ret_orders_fn >> [ret_orders_table, ret_payments_table]
            ret_inventory_fn >> ret_inventory_table
            ret_ai_fn >> ret_conversations_table
            [ret_products_fn, ret_orders_fn, ret_inventory_fn] >> ret_cases_table

        # Shared AI Service
        with Cluster("Shared AI Service"):
            bedrock = Bedrock("Bedrock")

        # AI handler to Bedrock
        ret_ai_fn >> bedrock


def generate_retail_only_data_flow_diagram():
    """Generate retail-only data flow diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "1.0",
        "ranksep": "1.5",
        "nodesep": "1.0",
        "splines": "ortho",
    }

    with Diagram(
        "Silvermoat Retail Data Flow",
        filename="docs/data-flow-retail",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # User
        ret_user = User("Retail\nCustomer")

        # Retail Vertical Flow
        with Cluster("Retail Vertical"):
            ret_cf = CloudFront("CloudFront")
            ret_api = APIGateway("API Gateway")

            with Cluster("Lambda Handlers"):
                ret_products_fn = Lambda("products-handler")
                ret_orders_fn = Lambda("orders-handler")
                ret_ai_fn = Lambda("ai-handler")

            with Cluster("Data Layer"):
                ret_products_db = Dynamodb("Products")
                ret_orders_db = Dynamodb("Orders")
                ret_inventory_db = Dynamodb("Inventory")
                ret_conversations_db = Dynamodb("Conversations")

            # Retail flow
            ret_user >> ret_cf >> ret_api
            ret_api >> [ret_products_fn, ret_orders_fn, ret_ai_fn]
            ret_products_fn >> ret_products_db
            ret_orders_fn >> [ret_orders_db, ret_inventory_db]
            ret_ai_fn >> ret_conversations_db

        # Shared AI Service
        with Cluster("Shared AI Service"):
            bedrock = Bedrock("Bedrock")

        # AI handler to Bedrock
        ret_ai_fn >> bedrock


def generate_healthcare_only_architecture_diagram():
    """Generate healthcare-only AWS architecture diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "1.0",
        "ranksep": "1.5",
        "nodesep": "1.0",
        "splines": "ortho",
    }

    with Diagram(
        "Silvermoat Healthcare AWS Architecture",
        filename="docs/architecture-healthcare",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # DNS Layer
        with Cluster("DNS Management"):
            cloudflare = Cloudflare("Cloudflare\nhealthcare.silvermoat.net")

        # Healthcare Vertical
        with Cluster("Healthcare Vertical"):
            with Cluster("Frontend Distribution"):
                hc_cloudfront = CloudFront("CloudFront\nhealthcare.silvermoat.net")
                hc_acm = CertificateManager("ACM Cert")
                hc_ui_bucket = S3("UI Bucket")

                hc_cloudfront >> hc_acm
                hc_cloudfront >> hc_ui_bucket

            with Cluster("API Layer"):
                hc_apigw = APIGateway("API Gateway")

            with Cluster("Lambda Handlers"):
                hc_patient_fn = Lambda("patient-handler")
                hc_appointment_fn = Lambda("appointment-handler")
                hc_docs_fn = Lambda("documents-handler")
                hc_ai_fn = Lambda("ai-handler")

            with Cluster("Data Layer"):
                hc_patients_table = Dynamodb("Patients")
                hc_appointments_table = Dynamodb("Appointments")
                hc_prescriptions_table = Dynamodb("Prescriptions")
                hc_providers_table = Dynamodb("Providers")
                hc_cases_table = Dynamodb("Cases")
                hc_conversations_table = Dynamodb("Conversations")
                hc_documents_table = Dynamodb("Documents")

            with Cluster("Storage"):
                hc_docs_bucket = S3("Medical Records")

            # Healthcare connections
            cloudflare >> hc_cloudfront
            hc_cloudfront >> hc_apigw
            hc_apigw >> [hc_patient_fn, hc_appointment_fn, hc_docs_fn, hc_ai_fn]
            hc_patient_fn >> [hc_patients_table, hc_prescriptions_table]
            hc_appointment_fn >> [hc_appointments_table, hc_providers_table, hc_cases_table]
            hc_ai_fn >> hc_conversations_table
            hc_docs_fn >> [hc_docs_bucket, hc_documents_table]

        # Shared AI Service
        with Cluster("Shared AI Service"):
            bedrock = Bedrock("Bedrock")

        # AI handler to Bedrock
        hc_ai_fn >> bedrock


def generate_healthcare_only_data_flow_diagram():
    """Generate healthcare-only data flow diagram."""

    graph_attr = {
        "fontsize": "14",
        "bgcolor": "white",
        "pad": "1.0",
        "ranksep": "1.5",
        "nodesep": "1.0",
        "splines": "ortho",
    }

    with Diagram(
        "Silvermoat Healthcare Data Flow",
        filename="docs/data-flow-healthcare",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        outformat="png"
    ):
        # User
        hc_user = User("Healthcare\nPatient")

        # Healthcare Vertical Flow
        with Cluster("Healthcare Vertical"):
            hc_cf = CloudFront("CloudFront")
            hc_api = APIGateway("API Gateway")

            with Cluster("Lambda Handlers"):
                hc_patient_fn = Lambda("patient-handler")
                hc_appointment_fn = Lambda("appointment-handler")
                hc_ai_fn = Lambda("ai-handler")

            with Cluster("Data Layer"):
                hc_patients_db = Dynamodb("Patients")
                hc_appointments_db = Dynamodb("Appointments")
                hc_prescriptions_db = Dynamodb("Prescriptions")
                hc_providers_db = Dynamodb("Providers")
                hc_conversations_db = Dynamodb("Conversations")

            # Healthcare flow
            hc_user >> hc_cf >> hc_api
            hc_api >> [hc_patient_fn, hc_appointment_fn, hc_ai_fn]
            hc_patient_fn >> [hc_patients_db, hc_prescriptions_db]
            hc_appointment_fn >> [hc_appointments_db, hc_providers_db]
            hc_ai_fn >> hc_conversations_db

        # Shared AI Service
        with Cluster("Shared AI Service"):
            bedrock = Bedrock("Bedrock")

        # AI handler to Bedrock
        hc_ai_fn >> bedrock


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Silvermoat architecture diagrams")
    parser.add_argument(
        "--vertical",
        choices=["insurance", "retail", "healthcare", "fintech", "all"],
        default="all",
        help="Which vertical to generate diagrams for (default: all)"
    )
    args = parser.parse_args()

    if args.vertical == "insurance":
        print("Generating Insurance vertical documentation diagrams...\n")
        print("1/2 Generating architecture diagram...")
        generate_insurance_only_architecture_diagram()
        print("    ✓ docs/architecture-insurance.png")
        print("2/2 Generating data flow diagram...")
        generate_insurance_only_data_flow_diagram()
        print("    ✓ docs/data-flow-insurance.png")
        print("\n✓ Insurance diagrams generated successfully!")

    elif args.vertical == "retail":
        print("Generating Retail vertical documentation diagrams...\n")
        print("1/2 Generating architecture diagram...")
        generate_retail_only_architecture_diagram()
        print("    ✓ docs/architecture-retail.png")
        print("2/2 Generating data flow diagram...")
        generate_retail_only_data_flow_diagram()
        print("    ✓ docs/data-flow-retail.png")
        print("\n✓ Retail diagrams generated successfully!")

    elif args.vertical == "healthcare":
        print("Generating Healthcare vertical documentation diagrams...\n")
        print("1/2 Generating architecture diagram...")
        generate_healthcare_only_architecture_diagram()
        print("    ✓ docs/architecture-healthcare.png")
        print("2/2 Generating data flow diagram...")
        generate_healthcare_only_data_flow_diagram()
        print("    ✓ docs/data-flow-healthcare.png")
        print("\n✓ Healthcare diagrams generated successfully!")

    elif args.vertical == "fintech":
        print("Generating Fintech vertical documentation diagrams...\n")
        print("⚠️  Fintech diagram generation not yet implemented - skipping")
        print("    (Fintech can use multi-vertical diagrams from --vertical all)")

    else:  # all
        print("Generating Silvermoat multi-vertical documentation diagrams...\n")

        print("1/8 Generating insurance architecture diagram...")
        generate_insurance_only_architecture_diagram()
        print("    ✓ docs/architecture-insurance.png")

        print("2/8 Generating insurance data flow diagram...")
        generate_insurance_only_data_flow_diagram()
        print("    ✓ docs/data-flow-insurance.png")

        print("3/8 Generating retail architecture diagram...")
        generate_retail_only_architecture_diagram()
        print("    ✓ docs/architecture-retail.png")

        print("4/8 Generating retail data flow diagram...")
        generate_retail_only_data_flow_diagram()
        print("    ✓ docs/data-flow-retail.png")

        print("5/8 Generating healthcare architecture diagram...")
        generate_healthcare_only_architecture_diagram()
        print("    ✓ docs/architecture-healthcare.png")

        print("6/8 Generating healthcare data flow diagram...")
        generate_healthcare_only_data_flow_diagram()
        print("    ✓ docs/data-flow-healthcare.png")

        print("7/8 Generating multi-vertical architecture diagram...")
        generate_multi_vertical_architecture_diagram()
        print("    ✓ docs/architecture.png")

        print("8/8 Generating multi-vertical data flow diagram...")
        generate_multi_vertical_data_flow_diagram()
        print("    ✓ docs/data-flow.png")

        print("\n✓ All diagrams generated successfully!")
        print("   Showing multi-vertical architecture with:")
        print("   - Insurance vertical (insurance.silvermoat.net)")
        print("   - Retail vertical (retail.silvermoat.net)")
        print("   - Healthcare vertical (healthcare.silvermoat.net)")
        print("   - Shared Bedrock AI service")
