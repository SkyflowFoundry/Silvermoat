/**
 * Claims Statistics Component
 * Mini-dashboard showing claims-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import { ExclamationCircleOutlined, DollarOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import { useClaims } from '../../hooks/queries/useClaims';
import { formatCurrencyFromCents } from '../../utils/formatters';

const { Text } = Typography;

const ClaimsStats = () => {
  const { data: claimsData, isLoading } = useClaims();
  const claims = claimsData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalClaims = claims.length;
  const pendingClaims = claims.filter(c => c.status === 'PENDING').length;
  const reviewClaims = claims.filter(c => c.status === 'REVIEW').length;
  const approvedClaims = claims.filter(c => c.status === 'APPROVED').length;
  const deniedClaims = claims.filter(c => c.status === 'DENIED').length;

  const totalEstimated = claims.reduce((sum, c) => sum + (c.data?.estimatedAmount_cents || 0), 0);
  const totalApproved = claims
    .filter(c => ['APPROVED', 'CLOSED'].includes(c.status))
    .reduce((sum, c) => sum + (c.data?.approvedAmount_cents || 0), 0);
  const totalPaid = claims.reduce((sum, c) => sum + (c.data?.paidAmount_cents || 0), 0);

  const avgClaimAmount = totalClaims > 0 ? totalEstimated / totalClaims : 0;
  const approvalRate = totalClaims > 0 ? (approvedClaims / totalClaims) * 100 : 0;

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Claims */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff7e6' }}>
            <Statistic
              title={<Text strong>Total Claims</Text>}
              value={totalClaims}
              prefix={<ExclamationCircleOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
            />
            <Space split="|" size="small" style={{ marginTop: 8 }}>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#d9d9d9' }}>●</span> {pendingClaims} Pending
              </Text>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#1890ff' }}>●</span> {reviewClaims} Review
              </Text>
            </Space>
          </Card>
        </Col>

        {/* Approved Claims */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Approved</Text>}
              value={approvedClaims}
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {approvalRate.toFixed(1)}% approval rate
            </Text>
          </Card>
        </Col>

        {/* Denied Claims */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff1f0' }}>
            <Statistic
              title={<Text strong>Denied</Text>}
              value={deniedClaims}
              prefix={<CloseCircleOutlined style={{ color: '#ff4d4f' }} />}
              valueStyle={{ color: '#ff4d4f' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {totalClaims > 0 ? ((deniedClaims / totalClaims) * 100).toFixed(1) : 0}% denial rate
            </Text>
          </Card>
        </Col>

        {/* Total Estimated */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#e6f7ff' }}>
            <Statistic
              title={<Text strong>Total Estimated</Text>}
              value={formatCurrencyFromCents(totalEstimated)}
              prefix={<DollarOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Avg: {formatCurrencyFromCents(avgClaimAmount)}
            </Text>
          </Card>
        </Col>

        {/* Total Approved Amount */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Total Approved</Text>}
              value={formatCurrencyFromCents(totalApproved)}
              prefix={<DollarOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {totalEstimated > 0 ? ((totalApproved / totalEstimated) * 100).toFixed(1) : 0}% of estimated
            </Text>
          </Card>
        </Col>

        {/* Total Paid */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#e6fffb' }}>
            <Statistic
              title={<Text strong>Total Paid</Text>}
              value={formatCurrencyFromCents(totalPaid)}
              prefix={<DollarOutlined style={{ color: '#13c2c2' }} />}
              valueStyle={{ color: '#13c2c2', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {totalApproved > 0 ? ((totalPaid / totalApproved) * 100).toFixed(1) : 0}% paid out
            </Text>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default ClaimsStats;
