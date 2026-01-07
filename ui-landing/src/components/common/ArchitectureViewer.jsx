import { Modal, Typography, Divider, List } from 'antd';

const { Title, Paragraph, Text } = Typography;

const ArchitectureViewer = ({ open, onClose }) => {
  return (
    <Modal
      title="About Silvermoat Platform"
      open={open}
      onCancel={onClose}
      footer={null}
      width="90%"
      style={{ top: 20 }}
      bodyStyle={{
        maxHeight: 'calc(100vh - 200px)',
        overflow: 'auto',
        padding: '24px',
      }}
    >
      {/* Project Overview */}
      <div style={{ marginBottom: 48 }}>
        <Title level={3} style={{ marginBottom: 16 }}>
          Project Overview
        </Title>
        <Paragraph style={{ fontSize: 15, color: 'rgba(0, 0, 0, 0.65)', marginBottom: 16 }}>
          Silvermoat is a comprehensive cloud-native multi-vertical platform built entirely on AWS serverless
          infrastructure. It demonstrates enterprise-grade patterns including Infrastructure as Code (IaC), continuous
          deployment, automated testing, vertical isolation, and AI-powered customer service across multiple business domains.
        </Paragraph>
        <Paragraph style={{ fontSize: 15, color: 'rgba(0, 0, 0, 0.65)' }}>
          The platform supports both Insurance and Retail verticals, each with complete isolation at the infrastructure level.
          Each vertical manages its full lifecycle—from customer onboarding through transaction processing and support—all
          through intuitive web interfaces powered by Claude AI for intelligent assistance.
        </Paragraph>
      </div>

      <Divider />

      {/* Key Features */}
      <div style={{ marginBottom: 48 }}>
        <Title level={3} style={{ marginBottom: 16 }}>
          Key Features
        </Title>
        <List
          size="small"
          dataSource={[
            { title: 'Multi-Vertical Architecture', description: 'Complete infrastructure isolation between Insurance and Retail verticals' },
            { title: 'Insurance: Quote Management', description: 'Generate and manage insurance quotes with automated pricing' },
            { title: 'Insurance: Policy Lifecycle', description: 'Complete policy creation, renewal, and management workflows' },
            { title: 'Insurance: Claims Processing', description: 'End-to-end claims filing, document upload, and status tracking' },
            { title: 'Retail: Product Catalog', description: 'Browse and manage product inventory with search and filtering' },
            { title: 'Retail: Order Processing', description: 'Complete order lifecycle from cart to fulfillment' },
            { title: 'Retail: Inventory Tracking', description: 'Real-time stock levels and warehouse management' },
            { title: 'Retail: Payment Processing', description: 'Secure payment capture and transaction tracking' },
            { title: 'AI-Powered Support', description: 'Claude AI chatbot for customer and employee assistance across all verticals' },
            { title: 'Document Management', description: 'Secure S3-based storage for policies, claims, receipts, and documents' },
            { title: 'Multi-Role Access', description: 'Separate interfaces for customers and employees in each vertical' },
            { title: 'Real-time Notifications', description: 'SNS-based alerts for policy, claim, and order updates' },
            { title: 'Shared AI Service', description: 'Centralized AWS Bedrock integration serving all verticals' },
            { title: 'Vertical Isolation', description: 'Complete data and infrastructure separation ensuring security and scalability' },
          ]}
          renderItem={(item) => (
            <List.Item>
              <Text strong>{item.title}:</Text> {item.description}
            </List.Item>
          )}
        />
      </div>

      <Divider />

      {/* Technology Stack */}
      <div style={{ marginBottom: 48 }}>
        <Title level={3} style={{ marginBottom: 16 }}>
          Technology Stack
        </Title>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
          <div>
            <Text strong style={{ display: 'block', marginBottom: 8 }}>Frontend</Text>
            <Text style={{ fontSize: 14, color: 'rgba(0, 0, 0, 0.65)' }}>
              React, Ant Design, Vite
            </Text>
          </div>
          <div>
            <Text strong style={{ display: 'block', marginBottom: 8 }}>Backend</Text>
            <Text style={{ fontSize: 14, color: 'rgba(0, 0, 0, 0.65)' }}>
              AWS Lambda (Python), API Gateway
            </Text>
          </div>
          <div>
            <Text strong style={{ display: 'block', marginBottom: 8 }}>Database</Text>
            <Text style={{ fontSize: 14, color: 'rgba(0, 0, 0, 0.65)' }}>
              DynamoDB (14 tables across verticals)
            </Text>
          </div>
          <div>
            <Text strong style={{ display: 'block', marginBottom: 8 }}>Storage</Text>
            <Text style={{ fontSize: 14, color: 'rgba(0, 0, 0, 0.65)' }}>
              S3, CloudFront CDN
            </Text>
          </div>
          <div>
            <Text strong style={{ display: 'block', marginBottom: 8 }}>AI/ML</Text>
            <Text style={{ fontSize: 14, color: 'rgba(0, 0, 0, 0.65)' }}>
              AWS Bedrock (Claude 3.5 Sonnet)
            </Text>
          </div>
          <div>
            <Text strong style={{ display: 'block', marginBottom: 8 }}>Infrastructure</Text>
            <Text style={{ fontSize: 14, color: 'rgba(0, 0, 0, 0.65)' }}>
              AWS CDK, CloudFormation
            </Text>
          </div>
          <div>
            <Text strong style={{ display: 'block', marginBottom: 8 }}>CI/CD</Text>
            <Text style={{ fontSize: 14, color: 'rgba(0, 0, 0, 0.65)' }}>
              GitHub Actions
            </Text>
          </div>
          <div>
            <Text strong style={{ display: 'block', marginBottom: 8 }}>Security</Text>
            <Text style={{ fontSize: 14, color: 'rgba(0, 0, 0, 0.65)' }}>
              IAM, ACM (SSL/TLS)
            </Text>
          </div>
        </div>
      </div>

      <Divider />

      {/* Architecture Diagram Section */}
      <div style={{ marginBottom: 48, textAlign: 'center' }}>
        <Title level={3} style={{ marginBottom: 16 }}>
          AWS Infrastructure Architecture
        </Title>
        <Paragraph style={{ marginBottom: 24, fontSize: 15, color: 'rgba(0, 0, 0, 0.65)' }}>
          Silvermoat multi-vertical platform is built on AWS serverless infrastructure with complete vertical isolation.
          Each vertical (Insurance and Retail) has its own CloudFront distribution, API Gateway, Lambda handlers, and
          DynamoDB tables. The only shared service is AWS Bedrock for AI capabilities, ensuring maximum scalability
          and security through infrastructure separation.
        </Paragraph>

        <img
          src="/architecture.png"
          alt="Silvermoat Multi-Vertical AWS Architecture"
          style={{
            width: '100%',
            height: 'auto',
            maxWidth: '1200px',
            border: '1px solid #e0e0e0',
            borderRadius: '8px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          }}
        />
      </div>

      <Divider />

      {/* Data Flow Diagram Section */}
      <div style={{ marginBottom: 24, textAlign: 'center' }}>
        <Title level={3} style={{ marginBottom: 16 }}>
          Request/Response Data Flow
        </Title>
        <Paragraph style={{ marginBottom: 24, fontSize: 15, color: 'rgba(0, 0, 0, 0.65)' }}>
          Shows how requests flow through each vertical independently, from the React UI through CloudFront and
          API Gateway to vertical-specific Lambda handlers. Each vertical maintains its own DynamoDB tables and
          S3 storage, with only the Claude AI service shared across verticals for intelligent assistance.
        </Paragraph>

        <img
          src="/data-flow.png"
          alt="Silvermoat Multi-Vertical Data Flow"
          style={{
            width: '100%',
            height: 'auto',
            maxWidth: '1200px',
            border: '1px solid #e0e0e0',
            borderRadius: '8px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          }}
        />
      </div>

      <Paragraph
        style={{
          marginTop: 24,
          fontSize: 13,
          color: 'rgba(0, 0, 0, 0.45)',
          fontStyle: 'italic',
          textAlign: 'center',
        }}
      >
        Diagrams generated with official AWS service icons using the Diagrams library
      </Paragraph>
    </Modal>
  );
};

export default ArchitectureViewer;
