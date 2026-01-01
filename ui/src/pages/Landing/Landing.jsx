/**
 * Landing Page Component
 * Unified entry point for Customer and Employee portals
 */

import { useNavigate } from 'react-router-dom';
import { Card, Button, Typography, Space, Row, Col, Divider } from 'antd';
import {
  SafetyOutlined,
  DashboardOutlined,
  FileProtectOutlined,
  CheckCircleOutlined,
  BarChartOutlined,
  TeamOutlined,
  ClockCircleOutlined,
  SafetyCertificateOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

const Landing = () => {
  const navigate = useNavigate();

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '20px',
      }}
    >
      <div style={{ maxWidth: 1200, width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: 48 }}>
          <img
            src="/silvermoat-logo.png"
            alt="Silvermoat Insurance"
            style={{
              width: 120,
              height: 120,
              marginBottom: 24,
              filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.15))',
            }}
          />
          <Title level={1} style={{ color: 'white', marginBottom: 12, fontSize: 48, fontWeight: 700 }}>
            Silvermoat Insurance
          </Title>
          <Text style={{
            color: 'rgba(255, 255, 255, 0.95)',
            fontSize: 20,
            fontWeight: 500,
            letterSpacing: '0.5px'
          }}>
            Enterprise Insurance Management Platform
          </Text>
          <Paragraph style={{
            color: 'rgba(255, 255, 255, 0.85)',
            fontSize: 16,
            marginTop: 16,
            maxWidth: 600,
            margin: '16px auto 0'
          }}>
            Streamlined policy management and claims processing for modern insurance organizations
          </Paragraph>
        </div>

        <Row gutter={[32, 32]} style={{ width: '100%' }}>
          <Col xs={24} sm={24} md={12}>
            <Card
              hoverable
              style={{
                minHeight: 456,
                boxShadow: '0 10px 30px rgba(0,0,0,0.15)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: 12,
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.3s ease, box-shadow 0.3s ease',
              }}
              bodyStyle={{
                display: 'flex',
                flexDirection: 'column',
                height: '100%',
                padding: '38px 30px',
              }}
            >
              <div style={{ flex: 1 }}>
                <div style={{
                  background: 'linear-gradient(135deg, #1890ff 0%, #096dd9 100%)',
                  borderRadius: '50%',
                  width: 80,
                  height: 80,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 24px',
                  boxShadow: '0 4px 12px rgba(24, 144, 255, 0.3)',
                }}>
                  <SafetyOutlined style={{ fontSize: 40, color: 'white' }} />
                </div>

                <Title level={2} style={{ marginBottom: 12, marginTop: 0, fontSize: 28, textAlign: 'center' }}>
                  Customer Portal
                </Title>

                <Paragraph style={{ fontSize: 16, color: 'rgba(0,0,0,0.65)', marginBottom: 24, textAlign: 'center', lineHeight: '1.6' }}>
                  Secure self-service platform for policyholders to manage their insurance needs
                </Paragraph>

                <Divider style={{ margin: '20px 0' }} />

                <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <FileProtectOutlined style={{ fontSize: 20, color: '#1890ff', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>Policy Management</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>View coverage details and documentation</Text>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <CheckCircleOutlined style={{ fontSize: 20, color: '#1890ff', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>Claims Submission</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>File and track claims with ease</Text>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <ClockCircleOutlined style={{ fontSize: 20, color: '#1890ff', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>24/7 Access</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>Manage your account anytime, anywhere</Text>
                    </div>
                  </div>
                </Space>
              </div>

              <Button
                type="primary"
                size="large"
                block
                onClick={() => navigate('/customer/dashboard')}
                style={{
                  marginTop: 32,
                  height: 48,
                  fontSize: 16,
                  fontWeight: 600,
                  boxShadow: '0 4px 12px rgba(24, 144, 255, 0.3)',
                }}
              >
                Access Customer Portal →
              </Button>
            </Card>
          </Col>

          <Col xs={24} sm={24} md={12}>
            <Card
              hoverable
              style={{
                minHeight: 456,
                boxShadow: '0 10px 30px rgba(0,0,0,0.15)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: 12,
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.3s ease, box-shadow 0.3s ease',
              }}
              bodyStyle={{
                display: 'flex',
                flexDirection: 'column',
                height: '100%',
                padding: '38px 30px',
              }}
            >
              <div style={{ flex: 1 }}>
                <div style={{
                  background: 'linear-gradient(135deg, #722ed1 0%, #531dab 100%)',
                  borderRadius: '50%',
                  width: 80,
                  height: 80,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 24px',
                  boxShadow: '0 4px 12px rgba(114, 46, 209, 0.3)',
                }}>
                  <DashboardOutlined style={{ fontSize: 40, color: 'white' }} />
                </div>

                <Title level={2} style={{ marginBottom: 12, marginTop: 0, fontSize: 28, textAlign: 'center' }}>
                  Employee Portal
                </Title>

                <Paragraph style={{ fontSize: 16, color: 'rgba(0,0,0,0.65)', marginBottom: 24, textAlign: 'center', lineHeight: '1.6' }}>
                  Comprehensive operations hub for insurance professionals and administrators
                </Paragraph>

                <Divider style={{ margin: '20px 0' }} />

                <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <BarChartOutlined style={{ fontSize: 20, color: '#722ed1', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>Analytics Dashboard</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>Real-time metrics and reporting</Text>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <TeamOutlined style={{ fontSize: 20, color: '#722ed1', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>Case Management</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>Handle quotes, policies, and claims</Text>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <SafetyCertificateOutlined style={{ fontSize: 20, color: '#722ed1', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>Enterprise Security</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>Role-based access and audit trails</Text>
                    </div>
                  </div>
                </Space>
              </div>

              <Button
                type="primary"
                size="large"
                block
                onClick={() => navigate('/dashboard')}
                style={{
                  marginTop: 32,
                  height: 48,
                  fontSize: 16,
                  fontWeight: 600,
                  background: 'linear-gradient(135deg, #722ed1 0%, #531dab 100%)',
                  border: 'none',
                  boxShadow: '0 4px 12px rgba(114, 46, 209, 0.3)',
                }}
              >
                Access Employee Portal →
              </Button>
            </Card>
          </Col>
        </Row>
      </div>
    </div>
  );
};

export default Landing;
