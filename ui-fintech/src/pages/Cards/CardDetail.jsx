/**
 * Card Detail Page
 * Displays detailed information about a specific card
 */

import { Card, Descriptions, Button, Space, Typography, Spin, Alert, Tag } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { useCard } from '../../hooks/queries/useCard';
import { formatTimestamp, formatCurrency } from '../../utils/formatters';

const { Title, Paragraph } = Typography;

const CardDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: card, isLoading, error } = useCard(id);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading card details..." />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error Loading Card"
        description={error.message || 'Failed to load card details'}
        type="error"
        showIcon
      />
    );
  }

  if (!card) {
    return (
      <Alert
        message="Card Not Found"
        description="The requested card could not be found."
        type="warning"
        showIcon
      />
    );
  }

  const statusColor = card.data?.status === 'COMPLETED' ? 'green'
    : card.data?.status === 'FAILED' ? 'red'
    : 'orange';

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/cards')}
        >
          Back to Cards
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Card Details
            </Title>
          </Space>
        }
      >
        <Descriptions
          bordered
          column={{ xs: 1, sm: 1, md: 2, lg: 2, xl: 2 }}
          size="middle"
        >
          <Descriptions.Item label="Card ID" span={2}>
            {card.id}
          </Descriptions.Item>
          <Descriptions.Item label="Order ID" span={2}>
            {card.data?.orderId || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Amount">
            <strong>
              {card.data?.amount !== undefined
                ? formatCurrency(card.data.amount * 100)
                : '-'}
            </strong>
          </Descriptions.Item>
          <Descriptions.Item label="Method">
            <Tag color="blue">{card.data?.method || '-'}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={statusColor}>{card.data?.status || 'PENDING'}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Transaction ID">
            {card.data?.transactionId || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Notes" span={2}>
            {card.data?.notes ? (
              <Paragraph style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
                {card.data.notes}
              </Paragraph>
            ) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(card.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Status">
            {card.status || 'ACTIVE'}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {/* Raw Data (for debugging) */}
      <Card title="Raw Data" style={{ marginTop: 24 }} size="small">
        <pre style={{ maxHeight: '400px', overflow: 'auto', fontSize: '12px' }}>
          {JSON.stringify(card, null, 2)}
        </pre>
      </Card>
    </div>
  );
};

export default CardDetail;
