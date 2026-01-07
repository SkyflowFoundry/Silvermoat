/**
 * Payment Detail Page
 * Displays detailed information about a specific payment
 */

import { Card, Descriptions, Button, Space, Typography, Spin, Alert, Tag } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { usePayment } from '../../hooks/queries/usePayment';
import { formatTimestamp, formatCurrency } from '../../utils/formatters';

const { Title, Paragraph } = Typography;

const PaymentDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: payment, isLoading, error } = usePayment(id);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading payment details..." />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error Loading Payment"
        description={error.message || 'Failed to load payment details'}
        type="error"
        showIcon
      />
    );
  }

  if (!payment) {
    return (
      <Alert
        message="Payment Not Found"
        description="The requested payment could not be found."
        type="warning"
        showIcon
      />
    );
  }

  const statusColor = payment.data?.status === 'COMPLETED' ? 'green'
    : payment.data?.status === 'FAILED' ? 'red'
    : 'orange';

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/payments')}
        >
          Back to Payments
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Payment Details
            </Title>
          </Space>
        }
      >
        <Descriptions
          bordered
          column={{ xs: 1, sm: 1, md: 2, lg: 2, xl: 2 }}
          size="middle"
        >
          <Descriptions.Item label="Payment ID" span={2}>
            {payment.id}
          </Descriptions.Item>
          <Descriptions.Item label="Order ID" span={2}>
            {payment.data?.orderId || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Amount">
            <strong>
              {payment.data?.amount !== undefined
                ? formatCurrency(payment.data.amount * 100)
                : '-'}
            </strong>
          </Descriptions.Item>
          <Descriptions.Item label="Method">
            <Tag color="blue">{payment.data?.method || '-'}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={statusColor}>{payment.data?.status || 'PENDING'}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Transaction ID">
            {payment.data?.transactionId || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Notes" span={2}>
            {payment.data?.notes ? (
              <Paragraph style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
                {payment.data.notes}
              </Paragraph>
            ) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(payment.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Status">
            {payment.status || 'ACTIVE'}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {/* Raw Data (for debugging) */}
      <Card title="Raw Data" style={{ marginTop: 24 }} size="small">
        <pre style={{ maxHeight: '400px', overflow: 'auto', fontSize: '12px' }}>
          {JSON.stringify(payment, null, 2)}
        </pre>
      </Card>
    </div>
  );
};

export default PaymentDetail;
