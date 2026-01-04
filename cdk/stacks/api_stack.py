from aws_cdk import (
    aws_apigateway as apigw,
    aws_lambda as lambda_,
)
from constructs import Construct


class ApiStack(Construct):
    """API layer: API Gateway REST API with path-based routing to Lambda functions"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        app_name: str,
        stage_name: str,
        customer_function: lambda_.Function,
        claims_function: lambda_.Function,
        documents_function: lambda_.Function,
        ai_function: lambda_.Function,
        api_deployment_token: str,
    ):
        super().__init__(scope, id)

        # REST API
        self.api = apigw.RestApi(
            self,
            "Api",
            rest_api_name=f"{app_name}-{stage_name}-api",
            deploy_options=apigw.StageOptions(
                stage_name=stage_name,
                description=f"Deployment token: {api_deployment_token}",
            ),
        )

        # Create Lambda integrations
        customer_integration = apigw.LambdaIntegration(customer_function)
        claims_integration = apigw.LambdaIntegration(claims_function)
        documents_integration = apigw.LambdaIntegration(documents_function)
        ai_integration = apigw.LambdaIntegration(ai_function)

        # Root endpoint (/) -> customer handler
        self.api.root.add_method("ANY", customer_integration)

        # /customer resource
        customer_resource = self.api.root.add_resource("customer")
        customer_resource.add_method("ANY", customer_integration)
        customer_id_resource = customer_resource.add_resource("{id}")
        customer_id_resource.add_method("ANY", customer_integration)

        # /quote resource
        quote_resource = self.api.root.add_resource("quote")
        quote_resource.add_method("ANY", customer_integration)
        quote_id_resource = quote_resource.add_resource("{id}")
        quote_id_resource.add_method("ANY", customer_integration)

        # /policy resource -> claims handler
        policy_resource = self.api.root.add_resource("policy")
        policy_resource.add_method("ANY", claims_integration)
        policy_id_resource = policy_resource.add_resource("{id}")
        policy_id_resource.add_method("ANY", claims_integration)

        # /claim resource -> claims handler (except /claim/{id}/doc)
        claim_resource = self.api.root.add_resource("claim")
        claim_resource.add_method("ANY", claims_integration)
        claim_id_resource = claim_resource.add_resource("{id}")
        claim_id_resource.add_method("ANY", claims_integration)

        # /claim/{id}/status -> claims handler
        claim_status_resource = claim_id_resource.add_resource("status")
        claim_status_resource.add_method("POST", claims_integration)

        # /claim/{id}/doc -> documents handler
        claim_doc_resource = claim_id_resource.add_resource("doc")
        claim_doc_resource.add_method("POST", documents_integration)

        # /payment resource -> claims handler
        payment_resource = self.api.root.add_resource("payment")
        payment_resource.add_method("ANY", claims_integration)
        payment_id_resource = payment_resource.add_resource("{id}")
        payment_id_resource.add_method("ANY", claims_integration)

        # /case resource -> claims handler
        case_resource = self.api.root.add_resource("case")
        case_resource.add_method("ANY", claims_integration)
        case_id_resource = case_resource.add_resource("{id}")
        case_id_resource.add_method("ANY", claims_integration)

        # /chat -> AI handler
        chat_resource = self.api.root.add_resource("chat")
        chat_resource.add_method("POST", ai_integration)
        chat_resource.add_method("OPTIONS", ai_integration)  # CORS preflight

        # /customer-chat -> AI handler
        customer_chat_resource = self.api.root.add_resource("customer-chat")
        customer_chat_resource.add_method("POST", ai_integration)
        customer_chat_resource.add_method("OPTIONS", ai_integration)  # CORS preflight

        # API URL (exact match to CloudFormation)
        self.api_url = self.api.url

        # Note: Outputs must be defined in parent Stack, not here in Construct
