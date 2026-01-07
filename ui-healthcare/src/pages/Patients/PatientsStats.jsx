/**
 * Patients Statistics Component
 * Mini-dashboard showing patient-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import {
  UserOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  TeamOutlined,
} from '@ant-design/icons';
import { usePatients } from '../../hooks/queries/usePatients';

const { Text } = Typography;

const PatientsStats = () => {
  const { data: patientsData, isLoading } = usePatients();
  const patients = patientsData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalPatients = patients.length;
  const activePatients = patients.filter(p => p.status === 'ACTIVE').length;
  const inactivePatients = patients.filter(p => p.status === 'INACTIVE').length;
  const archivedPatients = patients.filter(p => p.status === 'ARCHIVED').length;

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Patients */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Total Patients</Text>}
              value={totalPatients}
              prefix={<TeamOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>

        {/* Active Patients */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Active</Text>}
              value={activePatients}
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
              suffix={`/ ${totalPatients}`}
            />
          </Card>
        </Col>

        {/* Inactive Patients */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f5f5f5' }}>
            <Statistic
              title={<Text strong>Inactive</Text>}
              value={inactivePatients}
              prefix={<ClockCircleOutlined style={{ color: '#8c8c8c' }} />}
              valueStyle={{ color: '#8c8c8c' }}
            />
          </Card>
        </Col>

        {/* Archived Patients */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fff1f0' }}>
            <Statistic
              title={<Text strong>Archived</Text>}
              value={archivedPatients}
              prefix={<UserOutlined style={{ color: '#ff4d4f' }} />}
              valueStyle={{ color: '#ff4d4f' }}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default PatientsStats;
