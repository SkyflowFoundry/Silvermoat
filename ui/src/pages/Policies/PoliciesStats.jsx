/**
 * Policies Statistics Component
 * Mini-dashboard showing policy-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import { SafetyCertificateOutlined, DollarOutlined, ClockCircleOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { usePolicies } from '../../hooks/queries/usePolicies';
import { formatCurrencyFromCents } from '../../utils/formatters';

const { Text } = Typography;

const PoliciesStats = () => {
  const { data: policiesData, isLoading } = usePolicies();
  const policies = policiesData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalPolicies = policies.length;
  const activePolicies = policies.filter(p => p.data?.status === 'ACTIVE').length;
  const expiredPolicies = policies.filter(p => p.data?.status === 'EXPIRED').length;
  const cancelledPolicies = policies.filter(p => p.data?.status === 'CANCELLED').length;

  // Expiring soon (within 30 days)
  const now = dayjs();
  const expiringSoon = policies.filter(p => {
    const expiryDate = p.data?.expiryDate;
    if (!expiryDate) return false;
    const daysUntilExpiry = dayjs(expiryDate).diff(now, 'day');
    return daysUntilExpiry > 0 && daysUntilExpiry <= 30;
  }).length;

  // Financial metrics
  const totalPremiumRevenue = policies.reduce((sum, p) => sum + (p.data?.premium_cents || 0), 0);
  const avgPremium = totalPolicies > 0 ? totalPremiumRevenue / totalPolicies : 0;

  // Coverage type distribution
  const coverageTypes = {};
  policies.forEach(p => {
    const type = p.data?.coverageType || 'UNKNOWN';
    coverageTypes[type] = (coverageTypes[type] || 0) + 1;
  });
  const topCoverage = Object.entries(coverageTypes).sort((a, b) => b[1] - a[1])[0];

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Policies */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Total Policies</Text>}
              value={totalPolicies}
              prefix={<SafetyCertificateOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
            <Space split="|" size="small" style={{ marginTop: 8 }}>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#52c41a' }}>●</span> {activePolicies} Active
              </Text>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#d9d9d9' }}>●</span> {expiredPolicies} Expired
              </Text>
            </Space>
          </Card>
        </Col>

        {/* Active Policies */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#e6f7ff' }}>
            <Statistic
              title={<Text strong>Active</Text>}
              value={activePolicies}
              prefix={<SafetyCertificateOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {totalPolicies > 0 ? ((activePolicies / totalPolicies) * 100).toFixed(1) : 0}% active rate
            </Text>
          </Card>
        </Col>

        {/* Expiring Soon */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff7e6' }}>
            <Statistic
              title={<Text strong>Expiring Soon</Text>}
              value={expiringSoon}
              prefix={<ClockCircleOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Within 30 days
            </Text>
          </Card>
        </Col>

        {/* Cancelled */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff1f0' }}>
            <Statistic
              title={<Text strong>Cancelled</Text>}
              value={cancelledPolicies}
              prefix={<SafetyCertificateOutlined style={{ color: '#ff4d4f' }} />}
              valueStyle={{ color: '#ff4d4f' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {totalPolicies > 0 ? ((cancelledPolicies / totalPolicies) * 100).toFixed(1) : 0}% cancellation rate
            </Text>
          </Card>
        </Col>

        {/* Total Premium Revenue */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#e6fffb' }}>
            <Statistic
              title={<Text strong>Total Premium Revenue</Text>}
              value={formatCurrencyFromCents(totalPremiumRevenue)}
              prefix={<DollarOutlined style={{ color: '#13c2c2' }} />}
              valueStyle={{ color: '#13c2c2', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Annual premiums
            </Text>
          </Card>
        </Col>

        {/* Average Premium */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Average Premium</Text>}
              value={formatCurrencyFromCents(avgPremium)}
              prefix={<DollarOutlined style={{ color: '#597ef7' }} />}
              valueStyle={{ color: '#597ef7', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Per policy
            </Text>
          </Card>
        </Col>

        {/* Top Coverage Type */}
        {topCoverage && (
          <Col xs={24} sm={12} lg={6}>
            <Card size="small" bordered={false} style={{ background: '#f9f0ff' }}>
              <Statistic
                title={<Text strong>Top Coverage</Text>}
                value={topCoverage[0]}
                valueStyle={{ fontSize: 20, color: '#722ed1' }}
              />
              <Text type="secondary" style={{ fontSize: 12 }}>
                {topCoverage[1]} policies ({totalPolicies > 0 ? ((topCoverage[1] / totalPolicies) * 100).toFixed(1) : 0}%)
              </Text>
            </Card>
          </Col>
        )}
      </Row>
    </div>
  );
};

export default PoliciesStats;
