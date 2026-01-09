/**
 * Accounts Statistics Component
 * Mini-dashboard showing account-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import {
  CalendarOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import { useAccounts } from '../../hooks/queries/useAccounts';

const { Text } = Typography;

const AccountsStats = () => {
  const { data: accountsData, isLoading } = useAccounts();
  const accounts = accountsData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalAccounts = accounts.length;
  const scheduled = accounts.filter(a => a.status === 'SCHEDULED').length;
  const completed = accounts.filter(a => a.status === 'COMPLETED').length;
  const cancelled = accounts.filter(a => a.status === 'CANCELLED').length;
  const noShow = accounts.filter(a => a.status === 'NO_SHOW').length;

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Accounts */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Total Accounts</Text>}
              value={totalAccounts}
              prefix={<CalendarOutlined style={{ color: '#13c2c2' }} />}
              valueStyle={{ color: '#13c2c2' }}
            />
          </Card>
        </Col>

        {/* Scheduled */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#e6f7ff' }}>
            <Statistic
              title={<Text strong>Scheduled</Text>}
              value={scheduled}
              prefix={<ClockCircleOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>

        {/* Completed */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Completed</Text>}
              value={completed}
              prefix={<CheckCircleOutlined style={{ color: '#13c2c2' }} />}
              valueStyle={{ color: '#13c2c2' }}
            />
          </Card>
        </Col>

        {/* Cancelled/No-Show */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff1f0' }}>
            <Statistic
              title={<Text strong>Cancelled/No-Show</Text>}
              value={cancelled + noShow}
              prefix={<CloseCircleOutlined style={{ color: '#ff4d4f' }} />}
              valueStyle={{ color: '#ff4d4f' }}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default AccountsStats;
