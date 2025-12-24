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

  const stats = {
    quotes: {
      total: quotes.length,
    },
    policies: {
      total: policies.length,
      active: policies.filter(p => p.data?.status === 'ACTIVE').length,
      expired: policies.filter(p => p.data?.status === 'EXPIRED').length,
      cancelled: policies.filter(p => p.data?.status === 'CANCELLED').length,
    },
    claims: {
      total: claims.length,
      pending: claims.filter(c => c.data?.status === 'PENDING').length,
      review: claims.filter(c => c.data?.status === 'REVIEW').length,
      approved: claims.filter(c => c.data?.status === 'APPROVED').length,
      denied: claims.filter(c => c.data?.status === 'DENIED').length,
    },
    payments: {
      total: payments.length,
      pending: payments.filter(p => p.data?.status === 'PENDING').length,
      completed: payments.filter(p => p.data?.status === 'COMPLETED').length,
      failed: payments.filter(p => p.data?.status === 'FAILED').length,
    },
    cases: {
      total: cases.length,
      open: cases.filter(c => c.data?.status === 'OPEN').length,
      inProgress: cases.filter(c => c.data?.status === 'IN_PROGRESS').length,
      resolved: cases.filter(c => c.data?.status === 'RESOLVED').length,
      closed: cases.filter(c => c.data?.status === 'CLOSED').length,
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
            style={{ background: '#f0f5ff', borderLeft: '4px solid #1890ff' }}
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <Space>
                <FileTextOutlined style={{ fontSize: 24, color: '#1890ff' }} />
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
                  <span style={{ color: '#1890ff' }}>●</span> {stats.claims.review} Review
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
                  <span style={{ color: '#1890ff' }}>●</span> {stats.cases.open} Open
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
      </Row>
    </div>
  );
};

export default DashboardStats;
