import { Modal, Typography, Divider } from 'antd';

const { Title, Paragraph } = Typography;

const ArchitectureViewer = ({ open, onClose }) => {
  return (
    <Modal
      title="System Architecture & Data Flow"
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
      {/* Architecture Diagram Section */}
      <div style={{ marginBottom: 48, textAlign: 'center' }}>
        <Title level={3} style={{ marginBottom: 16 }}>
          AWS Infrastructure Architecture
        </Title>
        <Paragraph style={{ marginBottom: 24, fontSize: 15, color: 'rgba(0, 0, 0, 0.65)' }}>
          Silvermoat is built on AWS serverless infrastructure with CloudFront CDN for global content delivery,
          API Gateway for REST APIs, four domain-based Lambda handlers, seven DynamoDB tables for data persistence,
          S3 for document storage, and AWS Bedrock integration with Claude AI for intelligent customer service.
        </Paragraph>

        <img
          src="/architecture.png"
          alt="Silvermoat AWS Architecture"
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
          Shows how customer requests flow through the system from the React UI through CloudFront and
          API Gateway to the Lambda handlers, which interact with DynamoDB tables, S3 storage, Claude AI,
          and SNS notifications to process and respond to requests.
        </Paragraph>

        <img
          src="/data-flow.png"
          alt="Silvermoat Data Flow"
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
