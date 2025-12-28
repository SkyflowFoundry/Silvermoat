import * as cdk from 'aws-cdk-lib';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export interface CdnConstructProps {
  appName: string;
  stageName: string;
  uiBucket: s3.Bucket;
  domainName?: string;
  createCloudFront: boolean;
}

export class CdnConstruct extends Construct {
  public readonly distribution?: cloudfront.Distribution;
  public readonly certificate?: acm.Certificate;

  constructor(scope: Construct, id: string, props: CdnConstructProps) {
    super(scope, id);

    if (!props.createCloudFront) {
      return;
    }

    const hasDomain = props.domainName && props.domainName.length > 0;

    // Create ACM certificate if domain name provided
    if (hasDomain) {
      this.certificate = new acm.Certificate(this, 'UiCertificate', {
        domainName: props.domainName!,
        validation: acm.CertificateValidation.fromDns(),
      });

      new cdk.CfnOutput(this, 'CertificateArn', {
        description: 'ACM certificate ARN (for reference)',
        value: this.certificate.certificateArn,
      });
    }

    // Extract domain from S3 website URL
    const websiteUrl = props.uiBucket.bucketWebsiteUrl;
    const websiteDomain = cdk.Fn.select(2, cdk.Fn.split('/', websiteUrl));

    // Create CloudFront distribution
    this.distribution = new cloudfront.Distribution(this, 'UiDistribution', {
      comment: `${props.appName}-${props.stageName} UI Distribution`,
      defaultBehavior: {
        origin: new origins.HttpOrigin(websiteDomain, {
          protocolPolicy: cloudfront.OriginProtocolPolicy.HTTP_ONLY,
        }),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        allowedMethods: cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
        cachedMethods: cloudfront.CachedMethods.CACHE_GET_HEAD_OPTIONS,
        compress: true,
        cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
        originRequestPolicy: cloudfront.OriginRequestPolicy.CORS_S3_ORIGIN,
      },
      domainNames: hasDomain ? [props.domainName!] : undefined,
      certificate: this.certificate,
      defaultRootObject: 'index.html',
      errorResponses: [
        {
          httpStatus: 404,
          responseHttpStatus: 200,
          responsePagePath: '/index.html',
          ttl: cdk.Duration.minutes(5),
        },
        {
          httpStatus: 403,
          responseHttpStatus: 200,
          responsePagePath: '/index.html',
          ttl: cdk.Duration.minutes(5),
        },
      ],
      httpVersion: cloudfront.HttpVersion.HTTP2_AND_3,
      enableIpv6: true,
      priceClass: cloudfront.PriceClass.PRICE_CLASS_100,
    });

    // Output CloudFront URL
    new cdk.CfnOutput(this, 'CloudFrontUrl', {
      description: 'CloudFront distribution URL (HTTPS) - Primary access method',
      value: `https://${this.distribution.distributionDomainName}`,
      exportName: `${cdk.Stack.of(this).stackName}-CloudFrontUrl`,
    });

    // Output CloudFront domain for DNS CNAME
    new cdk.CfnOutput(this, 'CloudFrontDomain', {
      description: 'CloudFront domain name (for DNS CNAME record)',
      value: this.distribution.distributionDomainName,
      exportName: `${cdk.Stack.of(this).stackName}-CloudFrontDomain`,
    });

    // Output custom domain URL if configured
    if (hasDomain) {
      new cdk.CfnOutput(this, 'CustomDomainUrl', {
        description: 'Custom domain URL (if DomainName parameter provided and CloudFront enabled)',
        value: `https://${props.domainName}`,
      });
    }
  }
}
