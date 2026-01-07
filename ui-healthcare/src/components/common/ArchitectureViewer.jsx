import { Modal, Typography, Divider, List } from 'antd';

const { Title, Paragraph, Text } = Typography;

const ArchitectureViewer = ({ open, onClose }) => {
  return (
    <Modal
      title="About Silvermoat Healthcare"
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
          Silvermoat Healthcare is a comprehensive cloud-native healthcare management platform built entirely on AWS serverless
          infrastructure. It demonstrates enterprise-grade patterns including Infrastructure as Code (IaC), continuous
          deployment, automated testing, and AI-powered patient support.
        </Paragraph>
        <Paragraph style={{ fontSize: 15, color: 'rgba(0, 0, 0, 0.65)' }}>
          The platform enables healthcare organizations to manage the complete patient care lifecycle—from appointment
          scheduling through patient records, prescription management, care coordination, and support—all through an
          intuitive web interface powered by Claude AI for intelligent assistance.
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
            { title: 'Patient Record Management', description: 'Complete EHR with secure access controls' },
            { title: 'Appointment Scheduling', description: 'Real-time calendar and availability management' },
            { title: 'Prescription Management', description: 'Track medications from prescribe to fulfillment' },
            { title: 'Care Coordination', description: 'Multi-provider communication and referrals' },
            { title: 'AI-Powered Support', description: 'Claude AI chatbot for patient and staff assistance' },
            { title: 'HIPAA Compliance', description: 'Secure document storage and audit trails' },
            { title: 'Multi-Role Access', description: 'Separate interfaces for patients and healthcare staff' },
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
              DynamoDB (7 tables)
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
          Silvermoat Healthcare is built on AWS serverless infrastructure with CloudFront CDN for global content delivery,
          API Gateway for REST APIs, four domain-based Lambda handlers, seven DynamoDB tables for data persistence,
          S3 for document storage, and AWS Bedrock integration with Claude AI for intelligent patient support.
        </Paragraph>

        <img
          src="/architecture-healthcare.png"
          alt="Silvermoat Healthcare AWS Architecture"
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
          Shows how patient requests flow through the system from the React UI through CloudFront and
          API Gateway to the Lambda handlers, which interact with DynamoDB tables, S3 storage, Claude AI,
          and healthcare systems to process and respond to requests.
        </Paragraph>

        <img
          src="/data-flow-healthcare.png"
          alt="Silvermoat Healthcare Data Flow"
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
