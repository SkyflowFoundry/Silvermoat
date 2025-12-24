/**
 * Quote Detail Page
 * Displays detailed information about a specific quote
 */

import { Card, Descriptions, Button, Space, Typography, Spin, Alert } from 'antd';
import { ArrowLeftOutlined, EditOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuote } from '../../hooks/queries/useQuote';
import { formatTimestamp } from '../../utils/formatters';

const { Title } = Typography;

const QuoteDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: quote, isLoading, error } = useQuote(id);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading quote details..." />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error Loading Quote"
        description={error.message || 'Failed to load quote details'}
        type="error"
        showIcon
      />
    );
  }

  if (!quote) {
    return (
      <Alert
        message="Quote Not Found"
        description="The requested quote could not be found."
        type="warning"
        showIcon
      />
    );
  }

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/quotes')}
        >
          Back to Quotes
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Quote Details
            </Title>
          </Space>
        }
        extra={
          <Space>
            {/* Future: Add edit functionality */}
          </Space>
        }
      >
        <Descriptions
          bordered
          column={{ xs: 1, sm: 1, md: 2, lg: 2, xl: 2 }}
          size="middle"
        >
          <Descriptions.Item label="Quote ID" span={2}>
            {quote.id}
          </Descriptions.Item>

          <Descriptions.Item label="Customer Name">
            {quote.data?.name || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="ZIP Code">
            {quote.data?.zip || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Created At" span={2}>
            {formatTimestamp(quote.createdAt)}
          </Descriptions.Item>
        </Descriptions>

        {/* Display raw data for debugging/demo purposes */}
        <Card
          type="inner"
          title="Raw Data"
          size="small"
          style={{ marginTop: 24 }}
        >
          <pre style={{
            background: '#f5f5f5',
            padding: 16,
            borderRadius: 4,
            overflow: 'auto',
            maxHeight: 400,
          }}>
            {JSON.stringify(quote, null, 2)}
          </pre>
        </Card>
      </Card>
    </div>
  );
};

export default QuoteDetail;
