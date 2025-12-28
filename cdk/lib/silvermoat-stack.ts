import * as cdk from 'aws-cdk-lib';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as cr from 'aws-cdk-lib/custom-resources';
import { Construct } from 'constructs';
import { StorageConstruct } from './constructs/storage';
import { ComputeConstruct } from './constructs/compute';
import { ApiConstruct } from './constructs/api';
import { CdnConstruct } from './constructs/cdn';

export interface SilvermoatStackProps extends cdk.StackProps {
  appName?: string;
  stageName?: string;
  apiDeploymentToken?: string;
  uiSeedingMode?: string;
  domainName?: string;
  createCloudFront?: string;
}

export class SilvermoatStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: SilvermoatStackProps) {
    super(scope, id, props);

    // Parameters with defaults
    const appName = props?.appName || 'silvermoat';
    const stageName = props?.stageName || 'demo';
    const apiDeploymentToken = props?.apiDeploymentToken || 'v1';
    const uiSeedingMode = props?.uiSeedingMode || 'seeded';
    const domainName = props?.domainName || 'silvermoat.net';
    const createCloudFront = props?.createCloudFront !== 'false';

    // Create SNS topic
    const notificationsTopic = new sns.Topic(this, 'DemoNotificationsTopic', {
      displayName: `${appName}-${stageName}-demo-notifications`,
    });

    // Create storage resources
    const storage = new StorageConstruct(this, 'Storage', {
      appName,
      stageName,
    });

    // Create compute resources
    const compute = new ComputeConstruct(this, 'Compute', {
      appName,
      stageName,
      quotesTable: storage.quotesTable,
      policiesTable: storage.policiesTable,
      claimsTable: storage.claimsTable,
      paymentsTable: storage.paymentsTable,
      casesTable: storage.casesTable,
      docsBucket: storage.docsBucket,
      uiBucket: storage.uiBucket,
      notificationsTopic,
    });

    // Create API Gateway
    const api = new ApiConstruct(this, 'Api', {
      appName,
      stageName,
      mvpServiceFunction: compute.mvpServiceFunction,
      apiDeploymentToken,
    });

    // Update seeder Lambda environment with API URL
    compute.seederFunction.addEnvironment('API_BASE', api.apiUrl);

    // Create CloudFront distribution
    const cdn = new CdnConstruct(this, 'Cdn', {
      appName,
      stageName,
      uiBucket: storage.uiBucket,
      domainName: domainName && domainName.length > 0 ? domainName : undefined,
      createCloudFront,
    });

    // Create Custom Resources for seeding and cleanup
    const seedProvider = new cr.Provider(this, 'SeedProvider', {
      onEventHandler: compute.seederFunction,
    });

    const seedResource = new cdk.CustomResource(this, 'SeedCustomResource', {
      serviceToken: seedProvider.serviceToken,
      properties: {
        Mode: 'seed',
        UiSeedingMode: uiSeedingMode,
      },
    });

    // Ensure seed runs after API stage is deployed
    seedResource.node.addDependency(api.api);
    seedResource.node.addDependency(storage.uiBucket);
    seedResource.node.addDependency(storage.docsBucket);

    const cleanupProvider = new cr.Provider(this, 'CleanupProvider', {
      onEventHandler: compute.seederFunction,
    });

    const cleanupResource = new cdk.CustomResource(this, 'CleanupCustomResource', {
      serviceToken: cleanupProvider.serviceToken,
      properties: {
        Mode: 'cleanup',
      },
    });

    cleanupResource.node.addDependency(storage.uiBucket);
    cleanupResource.node.addDependency(storage.docsBucket);
    cleanupResource.node.addDependency(compute.seederFunction);

    // Outputs
    new cdk.CfnOutput(this, 'WebUrl', {
      description: 'S3 Website URL (HTTP) - Use CloudFrontUrl for production, or this for test stacks',
      value: storage.uiBucket.bucketWebsiteUrl,
    });

    new cdk.CfnOutput(this, 'UiBucketName', {
      value: storage.uiBucket.bucketName,
    });

    new cdk.CfnOutput(this, 'DocsBucketName', {
      value: storage.docsBucket.bucketName,
    });

    new cdk.CfnOutput(this, 'QuotesTableName', {
      value: storage.quotesTable.tableName,
    });

    new cdk.CfnOutput(this, 'PoliciesTableName', {
      value: storage.policiesTable.tableName,
    });

    new cdk.CfnOutput(this, 'ClaimsTableName', {
      value: storage.claimsTable.tableName,
    });

    new cdk.CfnOutput(this, 'PaymentsTableName', {
      value: storage.paymentsTable.tableName,
    });

    new cdk.CfnOutput(this, 'CasesTableName', {
      value: storage.casesTable.tableName,
    });

    new cdk.CfnOutput(this, 'DemoNotificationsTopicArn', {
      value: notificationsTopic.topicArn,
    });
  }
}
