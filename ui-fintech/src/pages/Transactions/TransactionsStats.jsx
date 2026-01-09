/**
 * Transactions Statistics Component
 * Mini-dashboard showing transaction-specific metrics
 */

import { Row, Col, Card, Statistic, Spin, Typography } from 'antd';
import {
  MedicineBoxOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import { useTransactions } from '../../hooks/queries/useTransactions';

const { Text } = Typography;

const TransactionsStats = () => {
  const { data: transactionsData, isLoading } = useTransactions();
  const transactions = transactionsData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  const totalTransactions = transactions.length;
  const active = transactions.filter(p => p.status === 'ACTIVE').length;
  const filled = transactions.filter(p => p.status === 'FILLED').length;
  const expired = transactions.filter(p => p.status === 'EXPIRED').length;

  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={12} lg={6}>
        <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
          <Statistic
            title={<Text strong>Total Transactions</Text>}
            value={totalTransactions}
            prefix={<MedicineBoxOutlined style={{ color: '#52c41a' }} />}
            valueStyle={{ color: '#52c41a' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
          <Statistic
            title={<Text strong>Active</Text>}
            value={active}
            prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
            valueStyle={{ color: '#52c41a' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card size="small" bordered={false} style={{ background: '#e6f7ff' }}>
          <Statistic
            title={<Text strong>Filled</Text>}
            value={filled}
            prefix={<ClockCircleOutlined style={{ color: '#1890ff' }} />}
            valueStyle={{ color: '#1890ff' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card size="small" bordered={false} style={{ background: '#f5f5f5' }}>
          <Statistic
            title={<Text strong>Expired</Text>}
            value={expired}
            prefix={<CloseCircleOutlined style={{ color: '#8c8c8c' }} />}
            valueStyle={{ color: '#8c8c8c' }}
          />
        </Card>
      </Col>
    </Row>
  );
};

export default TransactionsStats;
