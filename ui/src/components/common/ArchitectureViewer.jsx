import { Modal, Typography } from 'antd';

const { Paragraph } = Typography;

const ArchitectureViewer = ({ open, onClose }) => {
  return (
    <Modal
      title="System Architecture"
      open={open}
      onCancel={onClose}
      footer={null}
      width="90%"
      style={{ top: 20 }}
      bodyStyle={{
        maxHeight: 'calc(100vh - 200px)',
        overflow: 'auto',
        padding: '24px',
        textAlign: 'center',
      }}
    >
      <Paragraph style={{ marginBottom: 24, fontSize: 16, color: 'rgba(0, 0, 0, 0.65)' }}>
        Silvermoat is built on AWS serverless infrastructure, featuring CloudFront CDN,
        API Gateway, Lambda functions, DynamoDB tables for data persistence, S3 for storage,
        and integration with Claude AI for intelligent customer service.
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

      <Paragraph
        style={{
          marginTop: 24,
          fontSize: 14,
          color: 'rgba(0, 0, 0, 0.45)',
          fontStyle: 'italic',
        }}
      >
        Architecture diagram generated with official AWS service icons
      </Paragraph>
    </Modal>
  );
};

export default ArchitectureViewer;
