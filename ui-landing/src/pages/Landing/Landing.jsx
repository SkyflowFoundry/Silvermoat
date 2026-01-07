/**
 * Landing Page Component
 * Directory/portal for accessing Silvermoat verticals
 */

import { useState } from 'react';
import { Card, Button, Typography, Space, Row, Col } from 'antd';
import {
  SafetyOutlined,
  ShoppingOutlined,
  MedicineBoxOutlined,
  ArrowRightOutlined,
  CheckCircleOutlined,
  InfoCircleOutlined,
} from '@ant-design/icons';
import ArchitectureViewer from '../../components/common/ArchitectureViewer';

const { Title, Text, Paragraph } = Typography;

/**
 * Get vertical URLs from environment variables
 * Requires VITE_INSURANCE_URL and VITE_RETAIL_URL in production builds
 * Falls back to localhost for local development
 */
const getVerticalUrls = () => {
  const insuranceUrl = import.meta.env.VITE_INSURANCE_URL;
  const retailUrl = import.meta.env.VITE_RETAIL_URL;
  const healthcareUrl = import.meta.env.VITE_HEALTHCARE_URL;

  // In production builds, URLs must be explicitly provided
  if (import.meta.env.PROD && (!insuranceUrl || !retailUrl || !healthcareUrl)) {
    throw new Error(
      'VITE_INSURANCE_URL, VITE_RETAIL_URL, and VITE_HEALTHCARE_URL must be set for production builds. ' +
      'These should be passed during build via deploy-ui.sh script.'
    );
  }

  // Local development fallbacks (localhost)
  return {
    insurance: insuranceUrl || 'http://localhost:5173',
    retail: retailUrl || 'http://localhost:5174',
    healthcare: healthcareUrl || 'http://localhost:5175',
  };
};

const Landing = () => {
  const [architectureVisible, setArchitectureVisible] = useState(false);

  // Get vertical URLs dynamically (no hardcoded production URLs)
  const { insurance: insuranceUrl, retail: retailUrl, healthcare: healthcareUrl } = getVerticalUrls();

  const verticals = [
    {
      name: 'Insurance',
      icon: <SafetyOutlined style={{ fontSize: 56, color: '#003d82' }} />,
      description: 'Enterprise insurance management with policy lifecycle, claims processing, and AI-powered customer support.',
      url: insuranceUrl,
      color: '#003d82',
    },
    {
      name: 'Retail',
      icon: <ShoppingOutlined style={{ fontSize: 56, color: '#722ed1' }} />,
      description: 'Complete e-commerce platform with product management, order processing, and inventory tracking.',
      url: retailUrl,
      color: '#722ed1',
    },
    {
      name: 'Healthcare',
      icon: <MedicineBoxOutlined style={{ fontSize: 56, color: '#52c41a' }} />,
      description: 'Healthcare management platform with patient records, appointments, and care coordination.',
      url: healthcareUrl,
      color: '#52c41a',
    },
  ];

  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      }}
    >
      {/* Hero Section */}
      <div style={{
        padding: '80px 20px 60px',
        textAlign: 'center',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
      }}>
        <div style={{ maxWidth: 800, margin: '0 auto' }}>
          <img
            src="/silvermoat-logo.png"
            alt="Silvermoat"
            style={{
              width: 100,
              height: 100,
              marginBottom: 32,
              filter: 'drop-shadow(0 4px 12px rgba(0,0,0,0.2))',
            }}
          />
          <Title level={1} style={{
            color: 'white',
            marginBottom: 16,
            fontSize: 56,
            fontWeight: 700,
            lineHeight: 1.2,
          }}>
            Silvermoat Platform
          </Title>
        </div>
      </div>

      {/* Verticals Grid Section */}
      <div style={{ padding: '60px 20px', maxWidth: 1200, margin: '0 auto' }}>
        <Title level={2} style={{
          color: 'white',
          textAlign: 'center',
          marginBottom: 16,
          fontSize: 32,
        }}>
          Choose Your Vertical
        </Title>
        <Text style={{
          display: 'block',
          textAlign: 'center',
          color: 'rgba(255, 255, 255, 0.8)',
          fontSize: 16,
          marginBottom: 48,
        }}>
          Select a vertical to access customer and employee portals
        </Text>

        {/* Vertical Cards - Compact Grid */}
        <Row gutter={[24, 24]} justify="center">
          {verticals.map((vertical) => (
            <Col xs={24} sm={12} md={8} lg={8} key={vertical.name}>
              <Card
                hoverable
                style={{
                  height: '100%',
                  minHeight: 280,
                  borderRadius: 12,
                  border: 'none',
                  boxShadow: '0 4px 16px rgba(0,0,0,0.12)',
                  transition: 'all 0.3s ease',
                  cursor: 'pointer',
                }}
                bodyStyle={{
                  padding: 28,
                  display: 'flex',
                  flexDirection: 'column',
                  height: '100%',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-4px)';
                  e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.18)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.12)';
                }}
              >
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                  {/* Icon */}
                  <div style={{
                    textAlign: 'center',
                    marginBottom: 20,
                  }}>
                    {vertical.icon}
                  </div>

                  {/* Name */}
                  <Title level={3} style={{
                    margin: '0 0 12px 0',
                    textAlign: 'center',
                    color: vertical.color,
                    fontSize: 24,
                  }}>
                    {vertical.name}
                  </Title>

                  {/* Description */}
                  <Paragraph style={{
                    fontSize: 14,
                    color: '#595959',
                    marginBottom: 20,
                    textAlign: 'center',
                    lineHeight: 1.6,
                    flex: 1,
                  }}>
                    {vertical.description}
                  </Paragraph>

                  {/* Learn More Button */}
                  <Button
                    type="primary"
                    size="large"
                    block
                    icon={<ArrowRightOutlined />}
                    href={vertical.url}
                    style={{
                      height: 44,
                      fontSize: 15,
                      fontWeight: 600,
                      backgroundColor: vertical.color,
                      borderColor: vertical.color,
                    }}
                  >
                    Enter Portal
                  </Button>
                </div>
              </Card>
            </Col>
          ))}
        </Row>

        {/* Footer */}
        <div style={{ textAlign: 'center', marginTop: 64, paddingBottom: 40 }}>
          <Text style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: 14 }}>
            © 2025 Silvermoat. All rights reserved.
          </Text>
        </div>
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
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
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
