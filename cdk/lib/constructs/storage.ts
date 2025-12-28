import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export interface StorageConstructProps {
  appName: string;
  stageName: string;
}

export class StorageConstruct extends Construct {
  public readonly quotesTable: dynamodb.Table;
  public readonly policiesTable: dynamodb.Table;
  public readonly claimsTable: dynamodb.Table;
  public readonly paymentsTable: dynamodb.Table;
  public readonly casesTable: dynamodb.Table;
  public readonly uiBucket: s3.Bucket;
  public readonly docsBucket: s3.Bucket;

  constructor(scope: Construct, id: string, props: StorageConstructProps) {
    super(scope, id);

    // Create DynamoDB tables
    const tables = ['Quotes', 'Policies', 'Claims', 'Payments', 'Cases'];
    const tableMap: { [key: string]: dynamodb.Table } = {};

    tables.forEach((tableName) => {
      const table = new dynamodb.Table(this, `${tableName}Table`, {
        partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
        billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
      });
      tableMap[tableName] = table;
    });

    this.quotesTable = tableMap['Quotes'];
    this.policiesTable = tableMap['Policies'];
    this.claimsTable = tableMap['Claims'];
    this.paymentsTable = tableMap['Payments'];
    this.casesTable = tableMap['Cases'];

    // Create S3 bucket for UI (public website hosting)
    this.uiBucket = new s3.Bucket(this, 'UiBucket', {
      websiteIndexDocument: 'index.html',
      websiteErrorDocument: 'index.html',
      publicReadAccess: true,
      blockPublicAccess: new s3.BlockPublicAccess({
        blockPublicAcls: false,
        blockPublicPolicy: false,
        ignorePublicAcls: false,
        restrictPublicBuckets: false,
      }),
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      versioned: false,
    });

    // Create S3 bucket for documents (private)
    this.docsBucket = new s3.Bucket(this, 'DocsBucket', {
      publicReadAccess: false,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      versioned: false,
    });
  }
}
