/**
 * Customer (Patient) Dashboard Page
 * Patient portal showing appointments, prescriptions, and medical records
 */

import { Card, Row, Col, Typography, Space, Button } from 'antd';
import { useNavigate } from 'react-router-dom';
import {
  CalendarOutlined,
  MedicineBoxOutlined,
  FileTextOutlined,
  UserOutlined,
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

const CustomerDashboard = () => {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', background: '#f5f5f5', padding: '24px' }}>
      <Card style={{ maxWidth: 1200, margin: '0 auto' }}>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <Title level={2}>
              <UserOutlined /> Patient Portal
            </Title>
            <Paragraph type="secondary">
              Welcome to Silvermoat Healthcare. Access your health information and manage appointments.
            </Paragraph>
          </div>

          <Row gutter={[16, 16]}>
            {/* Appointments Card */}
            <Col xs={24} md={8}>
              <Card
                hoverable
                style={{ height: '100%', cursor: 'pointer' }}
                onClick={() => navigate('/customer/appointments')}
              >
                <Space direction="vertical" align="center" style={{ width: '100%' }}>
                  <CalendarOutlined style={{ fontSize: 48, color: '#52c41a' }} />
                  <Title level={4}>My Appointments</Title>
                  <Text type="secondary">View and manage your appointments</Text>
                  <Button type="primary" icon={<CalendarOutlined />}>
                    View Appointments
                  </Button>
                </Space>
              </Card>
            </Col>

            {/* Medical Records Card */}
            <Col xs={24} md={8}>
              <Card
                hoverable
                style={{ height: '100%', cursor: 'pointer' }}
                onClick={() => navigate('/customer/records')}
              >
                <Space direction="vertical" align="center" style={{ width: '100%' }}>
                  <FileTextOutlined style={{ fontSize: 48, color: '#52c41a' }} />
                  <Title level={4}>Medical Records</Title>
                  <Text type="secondary">Access your medical history</Text>
                  <Button type="primary" icon={<FileTextOutlined />}>
                    View Records
                  </Button>
                </Space>
              </Card>
            </Col>

            {/* Prescriptions Card */}
            <Col xs={24} md={8}>
              <Card hoverable style={{ height: '100%' }}>
                <Space direction="vertical" align="center" style={{ width: '100%' }}>
                  <MedicineBoxOutlined style={{ fontSize: 48, color: '#52c41a' }} />
                  <Title level={4}>Prescriptions</Title>
                  <Text type="secondary">View your prescriptions</Text>
                  <Button type="primary" icon={<MedicineBoxOutlined />} disabled>
                    View Prescriptions
                  </Button>
                </Space>
              </Card>
            </Col>
          </Row>

          {/* Quick Links */}
          <Card title="Quick Links" size="small">
            <Space direction="vertical">
              <Button type="link" onClick={() => navigate('/customer/appointments')}>
                Schedule New Appointment
              </Button>
              <Button type="link" onClick={() => navigate('/customer/records')}>
                View Test Results
              </Button>
              <Button type="link" disabled>
                Message Your Provider
              </Button>
            </Space>
          </Card>
        </Space>
      </Card>
    </div>
  );
};

export default CustomerDashboard;
