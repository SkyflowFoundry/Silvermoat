#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { SilvermoatStack } from '../lib/silvermoat-stack';

const app = new cdk.App();

// Get context values or use defaults
const stackName = app.node.tryGetContext('stackName') || process.env.STACK_NAME || 'SilvermoatStack';
const appName = app.node.tryGetContext('appName') || process.env.APP_NAME || 'silvermoat';
const stageName = app.node.tryGetContext('stageName') || process.env.STAGE_NAME || 'demo';
const apiDeploymentToken = app.node.tryGetContext('apiDeploymentToken') || process.env.API_DEPLOYMENT_TOKEN || 'v1';
const uiSeedingMode = app.node.tryGetContext('uiSeedingMode') || process.env.UI_SEEDING_MODE || 'external';
const domainName = app.node.tryGetContext('domainName') || process.env.DOMAIN_NAME || '';
const createCloudFront = app.node.tryGetContext('createCloudFront') || process.env.CREATE_CLOUDFRONT || 'false';

new SilvermoatStack(app, stackName, {
  appName,
  stageName,
  apiDeploymentToken,
  uiSeedingMode,
  domainName,
  createCloudFront,
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION || 'us-east-1',
  },
  description: 'Silvermoat Insurance MVP - CDK deployment',
});

app.synth();
