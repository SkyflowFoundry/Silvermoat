/**
 * Payments Statistics Component
 * Mini-dashboard showing payment-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import {
  DollarOutlined,
  CreditCardOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import { usePayments } from '../../hooks/queries/usePayments';
import { formatCurrency } from '../../utils/formatters';

const { Text } = Typography;

const PaymentsStats = () => {
  const { data: paymentsData, isLoading } = usePayments();
  const payments = paymentsData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalPayments = payments.length;
  const totalAmount = payments.reduce((sum, payment) => sum + (payment.data?.amount || 0), 0);
  const completedPayments = payments.filter(p => p.data?.status === 'COMPLETED');
  const completedAmount = completedPayments.reduce((sum, p) => sum + (p.data?.amount || 0), 0);
  const failedPayments = payments.filter(p => p.data?.status === 'FAILED').length;
  const pendingPayments = payments.filter(p => p.data?.status === 'PENDING').length;

  // Payment method distribution
  const methods = {};
  payments.forEach(p => {
    const method = p.data?.method || 'Unknown';
    methods[method] = (methods[method] || 0) + 1;
  });
  const topMethod = Object.entries(methods).sort((a, b) => b[1] - a[1])[0];

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Payments */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Total Payments</Text>}
              value={totalPayments}
              prefix={<CreditCardOutlined style={{ color: '#531dab' }} />}
              valueStyle={{ color: '#531dab' }}
            />
          </Card>
        </Col>

        {/* Total Amount */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Total Amount</Text>}
              value={totalAmount}
              prefix={<DollarOutlined style={{ color: '#13c2c2' }} />}
              valueStyle={{ color: '#13c2c2' }}
              precision={2}
            />
          </Card>
        </Col>

        {/* Completed Amount */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Completed</Text>}
              value={completedAmount}
              prefix={<CheckCircleOutlined style={{ color: '#13c2c2' }} />}
              valueStyle={{ color: '#13c2c2' }}
              precision={2}
              suffix={`(${completedPayments.length})`}
            />
          </Card>
        </Col>

        {/* Failed Payments */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: failedPayments > 0 ? '#fff1f0' : '#f6ffed' }}>
            <Statistic
              title={<Text strong>Failed</Text>}
              value={failedPayments}
              prefix={failedPayments > 0 ? <CloseCircleOutlined style={{ color: '#ff4d4f' }} /> : null}
              valueStyle={{ color: failedPayments > 0 ? '#ff4d4f' : '#13c2c2' }}
              suffix={`/ ${totalPayments}`}
            />
          </Card>
        </Col>
      </Row>

      {/* Payment Methods */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24}>
          <Card size="small" bordered={false}>
            <Space direction="horizontal" size="large" wrap>
              <div>
                <Text type="secondary">Pending</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#faad14' }}>
                    {pendingPayments}
                  </Text>
                </div>
              </div>
              {topMethod && (
                <div>
                  <Text type="secondary">Top Method</Text>
                  <div>
                    <Text strong style={{ fontSize: 16, color: '#531dab' }}>
                      {topMethod[0]} ({topMethod[1]})
                    </Text>
                  </div>
                </div>
              )}
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default PaymentsStats;
