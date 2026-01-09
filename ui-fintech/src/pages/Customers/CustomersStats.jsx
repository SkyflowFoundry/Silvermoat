/**
 * Customers Statistics Component
 * Mini-dashboard showing customer-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import {
  UserOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  TeamOutlined,
} from '@ant-design/icons';
import { useCustomers } from '../../hooks/queries/useCustomers';

const { Text } = Typography;

const CustomersStats = () => {
  const { data: customersData, isLoading } = useCustomers();
  const customers = customersData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalCustomers = customers.length;
  const activeCustomers = customers.filter(p => p.status === 'ACTIVE').length;
  const inactiveCustomers = customers.filter(p => p.status === 'INACTIVE').length;
  const archivedCustomers = customers.filter(p => p.status === 'ARCHIVED').length;

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Customers */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Total Customers</Text>}
              value={totalCustomers}
              prefix={<TeamOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>

        {/* Active Customers */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Active</Text>}
              value={activeCustomers}
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
              suffix={`/ ${totalCustomers}`}
            />
          </Card>
        </Col>

        {/* Inactive Customers */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f5f5f5' }}>
            <Statistic
              title={<Text strong>Inactive</Text>}
              value={inactiveCustomers}
              prefix={<ClockCircleOutlined style={{ color: '#8c8c8c' }} />}
              valueStyle={{ color: '#8c8c8c' }}
            />
          </Card>
        </Col>

        {/* Archived Customers */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff1f0' }}>
            <Statistic
              title={<Text strong>Archived</Text>}
              value={archivedCustomers}
              prefix={<UserOutlined style={{ color: '#ff4d4f' }} />}
              valueStyle={{ color: '#ff4d4f' }}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default CustomersStats;
