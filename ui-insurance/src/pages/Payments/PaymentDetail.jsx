/**
 * Payment Detail Page
 */

import { Card, Descriptions, Button, Space, Typography, Spin, Alert } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { usePayment } from '../../hooks/queries/usePayment';
import { formatTimestamp, formatDate, formatCurrency } from '../../utils/formatters';
import StatusTag from '../../components/common/StatusTag';

const { Title } = Typography;

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

          <Descriptions.Item label="Payment Date">
            -
          </Descriptions.Item>

          <Descriptions.Item label="Amount">
            {formatCurrency(payment.data?.amount)}
          </Descriptions.Item>

          <Descriptions.Item label="Method">
            {payment.data?.paymentMethod ? payment.data.paymentMethod.replace('_', ' ') : '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Status">
            <StatusTag type="payment" value={payment.status} />
          </Descriptions.Item>

          {payment.data?.policyId && (
            <Descriptions.Item label="Related Policy ID" span={2}>
              <Button
                type="link"
                onClick={() => navigate(`/policies/${payment.data.policyId}`)}
                style={{ padding: 0 }}
              >
                {payment.data.policyId}
              </Button>
            </Descriptions.Item>
          )}

          <Descriptions.Item label="Created At" span={2}>
            {formatTimestamp(payment.createdAt)}
          </Descriptions.Item>
        </Descriptions>

        <Card
          type="inner"
          title="Raw Data"
          size="small"
          style={{ marginTop: 24 }}
        >
          <pre
            style={{
              background: '#f5f5f5',
              padding: 16,
              borderRadius: 4,
              overflow: 'auto',
              maxHeight: 400,
            }}
          >
            {JSON.stringify(payment, null, 2)}
          </pre>
        </Card>
      </Card>
    </div>
  );
};

export default PaymentDetail;
