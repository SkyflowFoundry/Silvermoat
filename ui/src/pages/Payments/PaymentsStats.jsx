/**
 * Payments Statistics Component
 * Mini-dashboard showing payment-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import { DollarOutlined, CheckCircleOutlined, CloseCircleOutlined, ClockCircleOutlined, CreditCardOutlined } from '@ant-design/icons';
import { usePayments } from '../../hooks/queries/usePayments';
import { formatCurrencyFromCents } from '../../utils/formatters';

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
  const pendingPayments = payments.filter(p => p.status === 'PENDING').length;
  const completedPayments = payments.filter(p => p.status === 'COMPLETED').length;
  const failedPayments = payments.filter(p => p.status === 'FAILED').length;
  const refundedPayments = payments.filter(p => p.status === 'REFUNDED').length;

  const successRate = totalPayments > 0 ? (completedPayments / totalPayments) * 100 : 0;

  // Financial metrics - amount is in dollars, convert to cents for formatCurrencyFromCents
  const totalAmount = payments.reduce((sum, p) => sum + ((p.data?.amount || 0) * 100), 0);
  const completedAmount = payments
    .filter(p => p.status === 'COMPLETED')
    .reduce((sum, p) => sum + ((p.data?.amount || 0) * 100), 0);
  const pendingAmount = payments
    .filter(p => p.status === 'PENDING')
    .reduce((sum, p) => sum + ((p.data?.amount || 0) * 100), 0);
  const avgPayment = totalPayments > 0 ? totalAmount / totalPayments : 0;

  // Payment method distribution
  const paymentMethods = {};
  payments.forEach(p => {
    const method = p.data?.paymentMethod || 'UNKNOWN';
    paymentMethods[method] = (paymentMethods[method] || 0) + 1;
  });
  const topMethod = Object.entries(paymentMethods).sort((a, b) => b[1] - a[1])[0];

  // Payment type distribution
  const paymentTypes = {};
  payments.forEach(p => {
    const type = p.data?.paymentType || 'UNKNOWN';
    paymentTypes[type] = (paymentTypes[type] || 0) + 1;
  });
  const premiumPayments = paymentTypes['PREMIUM'] || 0;
  const claimPayments = paymentTypes['CLAIM'] || 0;

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Payments */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#e6f7ff' }}>
            <Statistic
              title={<Text strong>Total Payments</Text>}
              value={totalPayments}
              prefix={<DollarOutlined style={{ color: '#0052A3' }} />}
              valueStyle={{ color: '#0052A3' }}
            />
            <Space split="|" size="small" style={{ marginTop: 8 }}>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#52c41a' }}>●</span> {completedPayments} Completed
              </Text>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#faad14' }}>●</span> {pendingPayments} Pending
              </Text>
            </Space>
          </Card>
        </Col>

        {/* Completed Payments */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Completed</Text>}
              value={completedPayments}
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {successRate.toFixed(1)}% success rate
            </Text>
          </Card>
        </Col>

        {/* Pending Payments */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff7e6' }}>
            <Statistic
              title={<Text strong>Pending</Text>}
              value={pendingPayments}
              prefix={<ClockCircleOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {totalPayments > 0 ? ((pendingPayments / totalPayments) * 100).toFixed(1) : 0}% pending
            </Text>
          </Card>
        </Col>

        {/* Failed Payments */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff1f0' }}>
            <Statistic
              title={<Text strong>Failed</Text>}
              value={failedPayments}
              prefix={<CloseCircleOutlined style={{ color: '#ff4d4f' }} />}
              valueStyle={{ color: '#ff4d4f' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {refundedPayments} refunded
            </Text>
          </Card>
        </Col>

        {/* Total Amount */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#e6fffb' }}>
            <Statistic
              title={<Text strong>Total Amount</Text>}
              value={formatCurrencyFromCents(totalAmount)}
              prefix={<DollarOutlined style={{ color: '#13c2c2' }} />}
              valueStyle={{ color: '#13c2c2', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              All payment attempts
            </Text>
          </Card>
        </Col>

        {/* Completed Amount */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Completed Amount</Text>}
              value={formatCurrencyFromCents(completedAmount)}
              prefix={<DollarOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {totalAmount > 0 ? ((completedAmount / totalAmount) * 100).toFixed(1) : 0}% of total
            </Text>
          </Card>
        </Col>

        {/* Pending Amount */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff7e6' }}>
            <Statistic
              title={<Text strong>Pending Amount</Text>}
              value={formatCurrencyFromCents(pendingAmount)}
              prefix={<DollarOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Awaiting processing
            </Text>
          </Card>
        </Col>

        {/* Average Payment */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Average Payment</Text>}
              value={formatCurrencyFromCents(avgPayment)}
              prefix={<DollarOutlined style={{ color: '#597ef7' }} />}
              valueStyle={{ color: '#597ef7', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Per transaction
            </Text>
          </Card>
        </Col>

        {/* Top Payment Method */}
        {topMethod && (
          <Col xs={24} sm={12} lg={6}>
            <Card size="small" bordered={false} style={{ background: '#f9f0ff' }}>
              <Statistic
                title={<Text strong>Top Payment Method</Text>}
                value={topMethod[0].replace('_', ' ')}
                prefix={<CreditCardOutlined style={{ color: '#722ed1' }} />}
                valueStyle={{ fontSize: 18, color: '#722ed1' }}
              />
              <Text type="secondary" style={{ fontSize: 12 }}>
                {topMethod[1]} payments ({totalPayments > 0 ? ((topMethod[1] / totalPayments) * 100).toFixed(1) : 0}%)
              </Text>
            </Card>
          </Col>
        )}

        {/* Premium vs Claim Payments */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff7e6' }}>
            <Statistic
              title={<Text strong>Premium Payments</Text>}
              value={premiumPayments}
              valueStyle={{ color: '#fa8c16' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {claimPayments} claim payments
            </Text>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default PaymentsStats;
