/**
 * Customer Medical Transactions Page
 * Patient view of their medical transactions
 */

import { Card, Typography, Button, Space, Alert } from 'antd';
import { useNavigate } from 'react-router-dom';
import { ArrowLeftOutlined, FileTextOutlined } from '@ant-design/icons';

const { Title, Paragraph, Text } = Typography;

const CustomerTransactions = () => {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', background: '#f5f5f5', padding: '24px' }}>
      <Card style={{ maxWidth: 1200, margin: '0 auto' }}>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <Button
              icon={<ArrowLeftOutlined />}
              onClick={() => navigate('/customer/dashboard')}
              style={{ marginBottom: 16 }}
            >
              Back to Dashboard
            </Button>
            <Title level={2}>
              <FileTextOutlined /> My Medical Transactions
            </Title>
            <Paragraph type="secondary">
              Access your medical history and test results.
            </Paragraph>
          </div>

          <Alert
            message="Coming Soon"
            description="Medical transactions viewing functionality will be available soon. You will be able to view test results, diagnoses, and visit summaries here."
            type="info"
            showIcon
          />

          <Card title="Record Types" size="small">
            <Space direction="vertical">
              <div>
                <Text strong>Visit Notes</Text>
                <br />
                <Text type="secondary">Summary of doctor visits</Text>
              </div>
              <div>
                <Text strong>Lab Results</Text>
                <br />
                <Text type="secondary">Blood work and other test results</Text>
              </div>
              <div>
                <Text strong>Imaging</Text>
                <br />
                <Text type="secondary">X-rays, MRIs, and other scans</Text>
              </div>
              <div>
                <Text strong>Immunizations</Text>
                <br />
                <Text type="secondary">Vaccination history</Text>
              </div>
            </Space>
          </Card>
        </Space>
      </Card>
    </div>
  );
};

export default CustomerTransactions;
