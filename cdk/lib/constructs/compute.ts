import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as sns from 'aws-cdk-lib/aws-sns';
import { Construct } from 'constructs';
import * as path from 'path';

export interface ComputeConstructProps {
  appName: string;
  stageName: string;
  quotesTable: dynamodb.Table;
  policiesTable: dynamodb.Table;
  claimsTable: dynamodb.Table;
  paymentsTable: dynamodb.Table;
  casesTable: dynamodb.Table;
  docsBucket: s3.Bucket;
  uiBucket: s3.Bucket;
  notificationsTopic: sns.Topic;
}

export class ComputeConstruct extends Construct {
  public readonly mvpServiceFunction: lambda.Function;
  public readonly seederFunction: lambda.Function;

  constructor(scope: Construct, id: string, props: ComputeConstructProps) {
    super(scope, id);

    const region = cdk.Stack.of(this).region;
    const account = cdk.Stack.of(this).account;
    const bedrockModelId = 'anthropic.claude-3-5-sonnet-20240620-v1:0';

    // Create IAM role for MVP Lambda
    const mvpLambdaRole = new iam.Role(this, 'MvpLambdaRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
      ],
    });

    // Add policies for MVP Lambda
    mvpLambdaRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          'dynamodb:GetItem',
          'dynamodb:PutItem',
          'dynamodb:UpdateItem',
          'dynamodb:DeleteItem',
          'dynamodb:Scan',
        ],
        resources: [
          props.quotesTable.tableArn,
          props.policiesTable.tableArn,
          props.claimsTable.tableArn,
          props.paymentsTable.tableArn,
          props.casesTable.tableArn,
        ],
      })
    );

    mvpLambdaRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['s3:ListBucket'],
        resources: [props.docsBucket.bucketArn],
      })
    );

    mvpLambdaRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['s3:GetObject', 's3:PutObject', 's3:DeleteObject'],
        resources: [`${props.docsBucket.bucketArn}/*`],
      })
    );

    mvpLambdaRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['events:PutEvents'],
        resources: ['*'],
      })
    );

    mvpLambdaRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['sns:Publish'],
        resources: [props.notificationsTopic.topicArn],
      })
    );

    mvpLambdaRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['bedrock:InvokeModel'],
        resources: [`arn:aws:bedrock:${region}::foundation-model/${bedrockModelId}`],
      })
    );

    // Create MVP Service Lambda
    this.mvpServiceFunction = new lambda.Function(this, 'MvpServiceFunction', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/mvp-service')),
      role: mvpLambdaRole,
      timeout: cdk.Duration.seconds(30),
      memorySize: 256,
      environment: {
        QUOTES_TABLE: props.quotesTable.tableName,
        POLICIES_TABLE: props.policiesTable.tableName,
        CLAIMS_TABLE: props.claimsTable.tableName,
        PAYMENTS_TABLE: props.paymentsTable.tableName,
        CASES_TABLE: props.casesTable.tableName,
        DOCS_BUCKET: props.docsBucket.bucketName,
        SNS_TOPIC_ARN: props.notificationsTopic.topicArn,
        BEDROCK_MODEL_ID: bedrockModelId,
        BEDROCK_REGION: region,
      },
    });

    // Create IAM role for Seeder Lambda
    const seederLambdaRole = new iam.Role(this, 'SeederLambdaRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
      ],
    });

    // Add policies for Seeder Lambda
    seederLambdaRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['s3:ListBucket', 's3:ListBucketVersions'],
        resources: [props.uiBucket.bucketArn, props.docsBucket.bucketArn],
      })
    );

    seederLambdaRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['s3:PutObject', 's3:GetObject', 's3:DeleteObject', 's3:DeleteObjectVersion'],
        resources: [`${props.uiBucket.bucketArn}/*`, `${props.docsBucket.bucketArn}/*`],
      })
    );

    seederLambdaRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['dynamodb:PutItem', 'dynamodb:Scan', 'dynamodb:DeleteItem'],
        resources: [
          props.quotesTable.tableArn,
          props.policiesTable.tableArn,
          props.claimsTable.tableArn,
          props.paymentsTable.tableArn,
          props.casesTable.tableArn,
        ],
      })
    );

    // Create Seeder Lambda
    this.seederFunction = new lambda.Function(this, 'SeederFunction', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/seeder')),
      role: seederLambdaRole,
      timeout: cdk.Duration.seconds(120),
      memorySize: 256,
      environment: {
        UI_BUCKET: props.uiBucket.bucketName,
        DOCS_BUCKET: props.docsBucket.bucketName,
        QUOTES_TABLE: props.quotesTable.tableName,
        POLICIES_TABLE: props.policiesTable.tableName,
        CLAIMS_TABLE: props.claimsTable.tableName,
        PAYMENTS_TABLE: props.paymentsTable.tableName,
        CASES_TABLE: props.casesTable.tableName,
        // API_BASE and WEB_BASE will be set by custom resource
        API_BASE: '',
        WEB_BASE: props.uiBucket.bucketWebsiteUrl,
      },
    });
  }
}
