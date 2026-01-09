/**
 * Landing Page Component
 * Unified entry point for Customer and Employee portals
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button, Typography, Space, Row, Col, Divider } from 'antd';
import {
  BankOutlined,
  DashboardOutlined,
  CalendarOutlined,
  FileTextOutlined,
  UserOutlined,
  BarChartOutlined,
  TeamOutlined,
  SafetyCertificateOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';
import ArchitectureViewer from '../../components/common/ArchitectureViewer';

const { Title, Text, Paragraph } = Typography;

const Landing = () => {
  const navigate = useNavigate();
  const [architectureVisible, setArchitectureVisible] = useState(false);

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #13c2c2 0%, #08979c 100%)',
        padding: '20px',
      }}
    >
      <div style={{ maxWidth: 1200, width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: 48 }}>
          <img
            src="/silvermoat-logo.png"
            alt="Silvermoat Fintech"
            style={{
              width: 120,
              height: 120,
              marginBottom: 24,
              filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.15))',
            }}
          />
          <Title level={1} style={{ color: 'white', marginBottom: 12, fontSize: 48, fontWeight: 700 }}>
            Silvermoat Fintech
          </Title>
          <Text style={{
            color: 'rgba(255, 255, 255, 0.95)',
            fontSize: 20,
            fontWeight: 500,
            letterSpacing: '0.5px'
          }}>
            Enterprise Fintech Management Platform
          </Text>
          <Paragraph style={{
            color: 'rgba(255, 255, 255, 0.85)',
            fontSize: 16,
            marginTop: 16,
            maxWidth: 600,
            margin: '16px auto 0'
          }}>
            Comprehensive fintech solution for customer records, accounts, and care coordination
            for modern fintech organizations
          </Paragraph>
        </div>

        <Row gutter={[16, 16]} justify="center">
          <Col xs={24} sm={24} md={12}>
            <Card
              hoverable
              onClick={() => navigate('/customer/dashboard')}
              style={{
                minHeight: 456,
                boxShadow: '0 10px 30px rgba(0,0,0,0.15)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: 12,
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.3s ease, box-shadow 0.3s ease',
                cursor: 'pointer',
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
                  <BankOutlined style={{ fontSize: 40, color: 'white' }} />
                </div>

                <Title level={2} style={{ marginBottom: 12, marginTop: 0, fontSize: 28, textAlign: 'center' }}>
                  Customer Portal
                </Title>

                <Paragraph style={{ fontSize: 16, color: 'rgba(0,0,0,0.65)', marginBottom: 24, textAlign: 'center', lineHeight: '1.6' }}>
                  Secure self-service platform for customers to manage accounts and view medical records
                </Paragraph>

                <Divider style={{ margin: '20px 0' }} />

                <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <CalendarOutlined style={{ fontSize: 20, color: '#1890ff', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>Account Scheduling</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>Book and manage accounts online</Text>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <FileTextOutlined style={{ fontSize: 20, color: '#1890ff', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>Medical Records</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>Access health records and test results</Text>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <BankOutlined style={{ fontSize: 20, color: '#1890ff', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>Loan Tracking</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>View and manage loans</Text>
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
              onClick={() => navigate('/dashboard')}
              style={{
                minHeight: 456,
                boxShadow: '0 10px 30px rgba(0,0,0,0.15)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: 12,
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.3s ease, box-shadow 0.3s ease',
                cursor: 'pointer',
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
                  background: 'linear-gradient(135deg, #13c2c2 0%, #08979c 100%)',
                  borderRadius: '50%',
                  width: 80,
                  height: 80,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 24px',
                  boxShadow: '0 4px 12px rgba(82, 196, 26, 0.3)',
                }}>
                  <DashboardOutlined style={{ fontSize: 40, color: 'white' }} />
                </div>

                <Title level={2} style={{ marginBottom: 12, marginTop: 0, fontSize: 28, textAlign: 'center' }}>
                  Staff Portal
                </Title>

                <Paragraph style={{ fontSize: 16, color: 'rgba(0,0,0,0.65)', marginBottom: 24, textAlign: 'center', lineHeight: '1.6' }}>
                  Comprehensive operations hub for fintech professionals and administrators
                </Paragraph>

                <Divider style={{ margin: '20px 0' }} />

                <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <UserOutlined style={{ fontSize: 20, color: '#13c2c2', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>Customer Management</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>Manage customer records and history</Text>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <CalendarOutlined style={{ fontSize: 20, color: '#13c2c2', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>Account Calendar</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>Schedule and manage accounts</Text>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                    <TeamOutlined style={{ fontSize: 20, color: '#13c2c2', marginTop: 2 }} />
                    <div>
                      <Text strong style={{ display: 'block', fontSize: 15 }}>Care Coordination</Text>
                      <Text type="secondary" style={{ fontSize: 14 }}>Collaborate across care teams</Text>
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
                  background: 'linear-gradient(135deg, #13c2c2 0%, #08979c 100%)',
                  border: 'none',
                  boxShadow: '0 4px 12px rgba(82, 196, 26, 0.3)',
                }}
              >
                Access Staff Portal →
              </Button>
            </Card>
          </Col>
        </Row>
      </div>

      {/* Floating Info Icon */}
      <div
        onClick={() => setArchitectureVisible(true)}
        style={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          width: 44,
          height: 44,
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #13c2c2 0%, #08979c 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
          transition: 'transform 0.2s ease, box-shadow 0.2s ease',
          zIndex: 1000,
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.1)';
          e.currentTarget.style.boxShadow = '0 6px 16px rgba(0, 0, 0, 0.4)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
          e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.3)';
        }}
      >
        <InfoCircleOutlined style={{ fontSize: 22, color: 'white' }} />
      </div>

      {/* Architecture Viewer Modal */}
      <ArchitectureViewer
        open={architectureVisible}
        onClose={() => setArchitectureVisible(false)}
      />
    </div>
  );
};

export default Landing;
