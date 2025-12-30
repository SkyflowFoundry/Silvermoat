from aws_cdk import (
    aws_apigateway as apigw,
    aws_lambda as lambda_,
    CfnOutput,
    Stack,
)
from constructs import Construct


class ApiStack(Construct):
    """API layer: API Gateway REST API with Lambda proxy integration"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        app_name: str,
        stage_name: str,
        mvp_function: lambda_.Function,
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

        # Lambda integration
        integration = apigw.LambdaIntegration(mvp_function)

        # Root method (/)
        self.api.root.add_method("ANY", integration)

        # Proxy resource (/{proxy+})
        self.api.root.add_proxy(
            default_integration=integration,
            any_method=True,
        )

        # API URL (exact match to CloudFormation)
        self.api_url = self.api.url

        # Outputs
        CfnOutput(
            self,
            "ApiBaseUrl",
            value=self.api_url,
            export_name=f"{Stack.of(self).stack_name}-ApiBaseUrl",
        )

        CfnOutput(
            self,
            "ApiId",
            value=self.api.rest_api_id,
            export_name=f"{Stack.of(self).stack_name}-ApiId",
        )
