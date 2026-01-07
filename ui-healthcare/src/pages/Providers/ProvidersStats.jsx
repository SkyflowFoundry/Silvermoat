/**
 * Providers Statistics Component
 * Mini-dashboard showing provider-specific metrics
 */

import { Row, Col, Card, Statistic, Spin, Typography } from 'antd';
import {
  TeamOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
} from '@ant-design/icons';
import { useProviders } from '../../hooks/queries/useProviders';

const { Text } = Typography;

const ProvidersStats = () => {
  const { data: providersData, isLoading } = useProviders();
  const providers = providersData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  const totalProviders = providers.length;
  const active = providers.filter(p => p.status === 'ACTIVE').length;
  const inactive = providers.filter(p => p.status === 'INACTIVE').length;

  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={12} lg={8}>
        <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
          <Statistic
            title={<Text strong>Total Providers</Text>}
            value={totalProviders}
            prefix={<TeamOutlined style={{ color: '#52c41a' }} />}
            valueStyle={{ color: '#52c41a' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={8}>
        <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
          <Statistic
            title={<Text strong>Active</Text>}
            value={active}
            prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
            valueStyle={{ color: '#52c41a' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={8}>
        <Card size="small" bordered={false} style={{ background: '#f5f5f5' }}>
          <Statistic
            title={<Text strong>Inactive</Text>}
            value={inactive}
            prefix={<ClockCircleOutlined style={{ color: '#8c8c8c' }} />}
            valueStyle={{ color: '#8c8c8c' }}
          />
        </Card>
      </Col>
    </Row>
  );
};

export default ProvidersStats;
