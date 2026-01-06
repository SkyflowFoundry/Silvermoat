/**
 * Dashboard Statistics Cards
 * Displays entity counts and status breakdowns
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import {
  FileTextOutlined,
  SafetyCertificateOutlined,
  ExclamationCircleOutlined,
  DollarOutlined,
  CustomerServiceOutlined,
} from '@ant-design/icons';
import { useQuotes } from '../../hooks/queries/useQuotes';
import { usePolicies } from '../../hooks/queries/usePolicies';
import { useClaims } from '../../hooks/queries/useClaims';
import { usePayments } from '../../hooks/queries/usePayments';
import { useCases } from '../../hooks/queries/useCases';
import { formatCurrencyFromCents } from '../../utils/formatters';

const { Text } = Typography;

const DashboardStats = () => {
  // Fetch all entity data
  const { data: quotesData, isLoading: quotesLoading } = useQuotes();
  const { data: policiesData, isLoading: policiesLoading } = usePolicies();
  const { data: claimsData, isLoading: claimsLoading } = useClaims();
  const { data: paymentsData, isLoading: paymentsLoading } = usePayments();
  const { data: casesData, isLoading: casesLoading } = useCases();

  const isLoading = quotesLoading || policiesLoading || claimsLoading || paymentsLoading || casesLoading;

  // Calculate statistics from real data
  const quotes = quotesData?.items || [];
  const policies = policiesData?.items || [];
  const claims = claimsData?.items || [];
  const payments = paymentsData?.items || [];
  const cases = casesData?.items || [];

  // Calculate financial metrics
  const totalPremiums = policies.reduce((sum, p) => sum + (p.data?.premium || 0), 0);
  const totalClaimsPaid = claims
    .filter(c => c.status === 'APPROVED')
    .reduce((sum, c) => sum + (c.data?.amount || 0), 0);
  const avgClaimAmount = claims.length > 0
    ? claims.reduce((sum, c) => sum + (c.data?.estimatedAmount_cents || 0), 0) / claims.length
    : 0;
  const lossRatio = totalPremiums > 0 ? (totalClaimsPaid / totalPremiums) * 100 : 0;

  const stats = {
    quotes: {
      total: quotes.length,
    },
    policies: {
      total: policies.length,
      active: policies.filter(p => p.status === 'ACTIVE').length,
      expired: policies.filter(p => p.status === 'EXPIRED').length,
      cancelled: policies.filter(p => p.status === 'CANCELLED').length,
    },
    claims: {
      total: claims.length,
      pending: claims.filter(c => c.status === 'PENDING').length,
      review: claims.filter(c => c.status === 'REVIEW').length,
      approved: claims.filter(c => c.status === 'APPROVED').length,
      denied: claims.filter(c => c.status === 'DENIED').length,
    },
    payments: {
      total: payments.length,
      pending: payments.filter(p => p.status === 'PENDING').length,
      completed: payments.filter(p => p.status === 'COMPLETED').length,
      failed: payments.filter(p => p.status === 'FAILED').length,
    },
    cases: {
      total: cases.length,
      open: cases.filter(c => c.status === 'OPEN').length,
      inProgress: cases.filter(c => c.status === 'IN_PROGRESS').length,
      resolved: cases.filter(c => c.status === 'RESOLVED').length,
      closed: cases.filter(c => c.status === 'CLOSED').length,
    },
    financials: {
      totalPremiums,
      totalClaimsPaid,
      avgClaimAmount,
      lossRatio,
    },
  };

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading statistics..." />
      </div>
    );
  }

  return (
    <div>
      <Row gutter={[24, 24]}>
        {/* Quotes Card */}
        <Col xs={24} sm={12} lg={8} xl={8}>
          <Card
            bordered={false}
            style={{ background: '#f0f5ff', borderLeft: '4px solid #0052A3' }}
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Space>
                <FileTextOutlined style={{ fontSize: 24, color: '#0052A3' }} />
                <Text strong style={{ fontSize: 16 }}>
                  Quotes
                </Text>
              </Space>
              <Statistic
                value={stats.quotes.total}
                valueStyle={{ fontSize: 32 }}
              />
              <Text type="secondary" style={{ fontSize: 12 }}>
                Total quotes in system
              </Text>
            </Space>
          </Card>
        </Col>

        {/* Policies Card */}
        <Col xs={24} sm={12} lg={8} xl={8}>
          <Card
            bordered={false}
            style={{ background: '#f6ffed', borderLeft: '4px solid #52c41a' }}
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Space>
                <SafetyCertificateOutlined
                  style={{ fontSize: 24, color: '#52c41a' }}
                />
                <Text strong style={{ fontSize: 16 }}>
                  Policies
                </Text>
              </Space>
              <Statistic
                value={stats.policies.total}
                valueStyle={{ fontSize: 32 }}
              />
              <Space split="|" size="small">
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#52c41a' }}>●</span> {stats.policies.active} Active
                </Text>
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#d9d9d9' }}>●</span> {stats.policies.expired} Expired
                </Text>
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#ff4d4f' }}>●</span> {stats.policies.cancelled} Cancelled
                </Text>
              </Space>
            </Space>
          </Card>
        </Col>

        {/* Claims Card */}
        <Col xs={24} sm={12} lg={8} xl={8}>
          <Card
            bordered={false}
            style={{ background: '#fff7e6', borderLeft: '4px solid #faad14' }}
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Space>
                <ExclamationCircleOutlined
                  style={{ fontSize: 24, color: '#faad14' }}
                />
                <Text strong style={{ fontSize: 16 }}>
                  Claims
                </Text>
              </Space>
              <Statistic
                value={stats.claims.total}
                valueStyle={{ fontSize: 32 }}
              />
              <Space split="|" size="small">
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#d9d9d9' }}>●</span> {stats.claims.pending} Pending
                </Text>
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#0052A3' }}>●</span> {stats.claims.review} Review
                </Text>
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#52c41a' }}>●</span> {stats.claims.approved} Approved
                </Text>
              </Space>
            </Space>
          </Card>
        </Col>

        {/* Payments Card */}
        <Col xs={24} sm={12} lg={8} xl={8}>
          <Card
            bordered={false}
            style={{ background: '#e6fffb', borderLeft: '4px solid #13c2c2' }}
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Space>
                <DollarOutlined style={{ fontSize: 24, color: '#13c2c2' }} />
                <Text strong style={{ fontSize: 16 }}>
                  Payments
                </Text>
              </Space>
              <Statistic
                value={stats.payments.total}
                valueStyle={{ fontSize: 32 }}
              />
              <Space split="|" size="small">
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#faad14' }}>●</span> {stats.payments.pending} Pending
                </Text>
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#52c41a' }}>●</span> {stats.payments.completed} Completed
                </Text>
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#ff4d4f' }}>●</span> {stats.payments.failed} Failed
                </Text>
              </Space>
            </Space>
          </Card>
        </Col>

        {/* Cases Card */}
        <Col xs={24} sm={12} lg={8} xl={8}>
          <Card
            bordered={false}
            style={{ background: '#f9f0ff', borderLeft: '4px solid #722ed1' }}
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Space>
                <CustomerServiceOutlined
                  style={{ fontSize: 24, color: '#722ed1' }}
                />
                <Text strong style={{ fontSize: 16 }}>
                  Cases
                </Text>
              </Space>
              <Statistic
                value={stats.cases.total}
                valueStyle={{ fontSize: 32 }}
              />
              <Space split="|" size="small">
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#0052A3' }}>●</span> {stats.cases.open} Open
                </Text>
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#faad14' }}>●</span> {stats.cases.inProgress} In Progress
                </Text>
                <Text style={{ fontSize: 12 }}>
                  <span style={{ color: '#52c41a' }}>●</span> {stats.cases.resolved} Resolved
                </Text>
              </Space>
            </Space>
          </Card>
        </Col>

        {/* Total Premium Revenue */}
        <Col xs={24} sm={12} lg={8} xl={8}>
          <Card
            bordered={false}
            style={{ background: '#e6f7ff', borderLeft: '4px solid #003D7A' }}
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Space>
                <DollarOutlined style={{ fontSize: 24, color: '#003D7A' }} />
                <Text strong style={{ fontSize: 16 }}>
                  Premium Revenue
                </Text>
              </Space>
              <Statistic
                value={formatCurrencyFromCents(stats.financials.totalPremiums)}
                valueStyle={{ fontSize: 28 }}
              />
              <Text type="secondary" style={{ fontSize: 12 }}>
                Total annual premiums
              </Text>
            </Space>
          </Card>
        </Col>

        {/* Total Claims Paid */}
        <Col xs={24} sm={12} lg={8} xl={8}>
          <Card
            bordered={false}
            style={{ background: '#fff1f0', borderLeft: '4px solid #cf1322' }}
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Space>
                <ExclamationCircleOutlined style={{ fontSize: 24, color: '#cf1322' }} />
                <Text strong style={{ fontSize: 16 }}>
                  Claims Paid
                </Text>
              </Space>
              <Statistic
                value={formatCurrencyFromCents(stats.financials.totalClaimsPaid)}
                valueStyle={{ fontSize: 28 }}
              />
              <Text type="secondary" style={{ fontSize: 12 }}>
                Total approved claims
              </Text>
            </Space>
          </Card>
        </Col>

        {/* Loss Ratio */}
        <Col xs={24} sm={12} lg={8} xl={8}>
          <Card
            bordered={false}
            style={{
              background: stats.financials.lossRatio > 70 ? '#fff1f0' : '#f6ffed',
              borderLeft: stats.financials.lossRatio > 70 ? '4px solid #cf1322' : '4px solid #389e0d'
            }}
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Space>
                <DollarOutlined
                  style={{
                    fontSize: 24,
                    color: stats.financials.lossRatio > 70 ? '#cf1322' : '#389e0d'
                  }}
                />
                <Text strong style={{ fontSize: 16 }}>
                  Loss Ratio
                </Text>
              </Space>
              <Statistic
                value={stats.financials.lossRatio.toFixed(1)}
                suffix="%"
                valueStyle={{
                  fontSize: 32,
                  color: stats.financials.lossRatio > 70 ? '#cf1322' : '#389e0d'
                }}
              />
              <Text type="secondary" style={{ fontSize: 12 }}>
                Claims / Premiums
              </Text>
            </Space>
          </Card>
        </Col>

        {/* Average Claim Amount */}
        <Col xs={24} sm={12} lg={8} xl={8}>
          <Card
            bordered={false}
            style={{ background: '#fcffe6', borderLeft: '4px solid #d4b106' }}
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Space>
                <DollarOutlined style={{ fontSize: 24, color: '#d4b106' }} />
                <Text strong style={{ fontSize: 16 }}>
                  Avg Claim Amount
                </Text>
              </Space>
              <Statistic
                value={formatCurrencyFromCents(stats.financials.avgClaimAmount)}
                valueStyle={{ fontSize: 28 }}
              />
              <Text type="secondary" style={{ fontSize: 12 }}>
                Average estimated claim
              </Text>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default DashboardStats;
