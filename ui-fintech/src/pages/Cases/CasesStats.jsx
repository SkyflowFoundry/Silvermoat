/**
 * Cases Statistics Component
 * Mini-dashboard showing case-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import {
  CustomerServiceOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  WarningOutlined,
} from '@ant-design/icons';
import { useCases } from '../../hooks/queries/useCases';

const { Text } = Typography;

const CasesStats = () => {
  const { data: casesData, isLoading } = useCases();
  const cases = casesData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalCases = cases.length;
  const openCases = cases.filter(c => c.data?.status === 'OPEN').length;
  const inProgressCases = cases.filter(c => c.data?.status === 'IN_PROGRESS').length;
  const resolvedCases = cases.filter(c => c.data?.status === 'RESOLVED' || c.data?.status === 'CLOSED').length;
  const urgentCases = cases.filter(c => c.data?.priority === 'URGENT').length;
  const highCases = cases.filter(c => c.data?.priority === 'HIGH').length;

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Cases */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Total Cases</Text>}
              value={totalCases}
              prefix={<CustomerServiceOutlined style={{ color: '#531dab' }} />}
              valueStyle={{ color: '#531dab' }}
            />
          </Card>
        </Col>

        {/* Open Cases */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fffbe6' }}>
            <Statistic
              title={<Text strong>Open</Text>}
              value={openCases}
              prefix={<ClockCircleOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>

        {/* In Progress */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#e6f7ff' }}>
            <Statistic
              title={<Text strong>In Progress</Text>}
              value={inProgressCases}
              prefix={<ClockCircleOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>

        {/* Resolved */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Resolved</Text>}
              value={resolvedCases}
              prefix={<CheckCircleOutlined style={{ color: '#13c2c2' }} />}
              valueStyle={{ color: '#13c2c2' }}
              suffix={`/ ${totalCases}`}
            />
          </Card>
        </Col>
      </Row>

      {/* Priority Breakdown */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24}>
          <Card size="small" bordered={false}>
            <Space direction="horizontal" size="large" wrap>
              <div>
                <Text type="secondary">Urgent</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#ff4d4f' }}>
                    {urgentCases}
                  </Text>
                </div>
              </div>
              <div>
                <Text type="secondary">High Priority</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#faad14' }}>
                    {highCases}
                  </Text>
                </div>
              </div>
              {(urgentCases > 0 || highCases > 0) && (
                <div>
                  <Text type="secondary">Needs Attention</Text>
                  <div>
                    <WarningOutlined style={{ color: '#ff4d4f', marginRight: 8 }} />
                    <Text strong style={{ fontSize: 16, color: '#ff4d4f' }}>
                      {urgentCases + highCases}
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

export default CasesStats;
