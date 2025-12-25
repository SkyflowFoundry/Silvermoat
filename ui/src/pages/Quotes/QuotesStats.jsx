/**
 * Quotes Statistics Component
 * Mini-dashboard showing quote-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import { FileTextOutlined, DollarOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import { useQuotes } from '../../hooks/queries/useQuotes';
import { formatCurrencyFromCents } from '../../utils/formatters';

const { Text } = Typography;

const QuotesStats = () => {
  const { data: quotesData, isLoading } = useQuotes();
  const quotes = quotesData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalQuotes = quotes.length;
  const pendingQuotes = quotes.filter(q => q.data?.status === 'PENDING').length;
  const acceptedQuotes = quotes.filter(q => q.data?.status === 'ACCEPTED').length;
  const declinedQuotes = quotes.filter(q => q.data?.status === 'DECLINED').length;
  const expiredQuotes = quotes.filter(q => q.data?.status === 'EXPIRED').length;

  const conversionRate = totalQuotes > 0 ? (acceptedQuotes / totalQuotes) * 100 : 0;

  // Financial metrics
  const totalQuoteValue = quotes.reduce((sum, q) => sum + (q.data?.premium_cents || 0), 0);
  const avgQuoteValue = totalQuotes > 0 ? totalQuoteValue / totalQuotes : 0;
  const acceptedValue = quotes
    .filter(q => q.data?.status === 'ACCEPTED')
    .reduce((sum, q) => sum + (q.data?.premium_cents || 0), 0);

  // Coverage type distribution
  const coverageTypes = {};
  quotes.forEach(q => {
    const type = q.data?.coverageType || 'UNKNOWN';
    coverageTypes[type] = (coverageTypes[type] || 0) + 1;
  });
  const topCoverage = Object.entries(coverageTypes).sort((a, b) => b[1] - a[1])[0];

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Quotes */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Total Quotes</Text>}
              value={totalQuotes}
              prefix={<FileTextOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff' }}
            />
            <Space split="|" size="small" style={{ marginTop: 8 }}>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#faad14' }}>●</span> {pendingQuotes} Pending
              </Text>
              <Text style={{ fontSize: 12 }}>
                <span style={{ color: '#52c41a' }}>●</span> {acceptedQuotes} Accepted
              </Text>
            </Space>
          </Card>
        </Col>

        {/* Accepted Quotes */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Accepted</Text>}
              value={acceptedQuotes}
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {conversionRate.toFixed(1)}% conversion rate
            </Text>
          </Card>
        </Col>

        {/* Declined Quotes */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff1f0' }}>
            <Statistic
              title={<Text strong>Declined</Text>}
              value={declinedQuotes}
              prefix={<CloseCircleOutlined style={{ color: '#ff4d4f' }} />}
              valueStyle={{ color: '#ff4d4f' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {totalQuotes > 0 ? ((declinedQuotes / totalQuotes) * 100).toFixed(1) : 0}% decline rate
            </Text>
          </Card>
        </Col>

        {/* Expired Quotes */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff7e6' }}>
            <Statistic
              title={<Text strong>Expired</Text>}
              value={expiredQuotes}
              prefix={<FileTextOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Missed opportunities
            </Text>
          </Card>
        </Col>

        {/* Total Quote Value */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#e6f7ff' }}>
            <Statistic
              title={<Text strong>Total Quote Value</Text>}
              value={formatCurrencyFromCents(totalQuoteValue)}
              prefix={<DollarOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Potential revenue
            </Text>
          </Card>
        </Col>

        {/* Accepted Value */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Accepted Value</Text>}
              value={formatCurrencyFromCents(acceptedValue)}
              prefix={<DollarOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {totalQuoteValue > 0 ? ((acceptedValue / totalQuoteValue) * 100).toFixed(1) : 0}% of total
            </Text>
          </Card>
        </Col>

        {/* Average Quote */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#e6fffb' }}>
            <Statistic
              title={<Text strong>Average Quote</Text>}
              value={formatCurrencyFromCents(avgQuoteValue)}
              prefix={<DollarOutlined style={{ color: '#13c2c2' }} />}
              valueStyle={{ color: '#13c2c2', fontSize: 20 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Per quote
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
                {topCoverage[1]} quotes ({totalQuotes > 0 ? ((topCoverage[1] / totalQuotes) * 100).toFixed(1) : 0}%)
              </Text>
            </Card>
          </Col>
        )}
      </Row>
    </div>
  );
};

export default QuotesStats;
