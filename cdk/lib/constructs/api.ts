import * as cdk from 'aws-cdk-lib';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

export interface ApiConstructProps {
  appName: string;
  stageName: string;
  mvpServiceFunction: lambda.Function;
  apiDeploymentToken: string;
}

export class ApiConstruct extends Construct {
  public readonly api: apigateway.RestApi;
  public readonly apiUrl: string;

  constructor(scope: Construct, id: string, props: ApiConstructProps) {
    super(scope, id);

    // Create REST API
    this.api = new apigateway.RestApi(this, 'Api', {
      restApiName: `${props.appName}-${props.stageName}-api`,
      description: `Silvermoat MVP API (deployment: ${props.apiDeploymentToken})`,
      endpointConfiguration: {
        types: [apigateway.EndpointType.REGIONAL],
      },
      deployOptions: {
        stageName: props.stageName,
        description: `API deployment token: ${props.apiDeploymentToken}`,
      },
    });

    // Create Lambda integration
    const integration = new apigateway.LambdaIntegration(props.mvpServiceFunction, {
      proxy: true,
    });

    // Add ANY method to root resource
    this.api.root.addMethod('ANY', integration);

    // Add proxy resource for all paths
    const proxyResource = this.api.root.addProxy({
      defaultIntegration: integration,
      anyMethod: true,
    });

    // Store API URL
    this.apiUrl = this.api.urlForPath('/');

    // Output API URL
    new cdk.CfnOutput(this, 'ApiBaseUrl', {
      description: 'API base URL (HTTPS)',
      value: this.apiUrl,
    });
  }
}
