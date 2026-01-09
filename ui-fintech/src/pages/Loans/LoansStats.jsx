/**
 * Loans Statistics Component
 * Mini-dashboard showing loan-specific metrics
 */

import { Row, Col, Card, Statistic, Spin, Typography } from 'antd';
import {
  BankOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import { useLoans } from '../../hooks/queries/useLoans';

const { Text } = Typography;

const LoansStats = () => {
  const { data: loansData, isLoading } = useLoans();
  const loans = loansData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  const totalLoans = loans.length;
  const active = loans.filter(p => p.status === 'ACTIVE').length;
  const filled = loans.filter(p => p.status === 'FILLED').length;
  const expired = loans.filter(p => p.status === 'EXPIRED').length;

  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={12} lg={6}>
        <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
          <Statistic
            title={<Text strong>Total Loans</Text>}
            value={totalLoans}
            prefix={<BankOutlined style={{ color: '#13c2c2' }} />}
            valueStyle={{ color: '#13c2c2' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
          <Statistic
            title={<Text strong>Active</Text>}
            value={active}
            prefix={<CheckCircleOutlined style={{ color: '#13c2c2' }} />}
            valueStyle={{ color: '#13c2c2' }}
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

export default LoansStats;
