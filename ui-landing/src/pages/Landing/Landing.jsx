/**
 * Landing Page Component
 * Directory/portal for accessing Silvermoat verticals
 */

import { Card, Button, Typography, Space, Row, Col } from 'antd';
import {
  SafetyOutlined,
  ShoppingOutlined,
  ArrowRightOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

/**
 * Get vertical URLs from environment variables
 * Requires VITE_INSURANCE_URL and VITE_RETAIL_URL in production builds
 * Falls back to localhost for local development
 */
const getVerticalUrls = () => {
  const insuranceUrl = import.meta.env.VITE_INSURANCE_URL;
  const retailUrl = import.meta.env.VITE_RETAIL_URL;

  // In production builds, URLs must be explicitly provided
  if (import.meta.env.PROD && (!insuranceUrl || !retailUrl)) {
    throw new Error(
      'VITE_INSURANCE_URL and VITE_RETAIL_URL must be set for production builds. ' +
      'These should be passed during build via deploy-ui.sh script.'
    );
  }

  // Local development fallbacks (localhost)
  return {
    insurance: insuranceUrl || 'http://localhost:5173',
    retail: retailUrl || 'http://localhost:5174',
  };
};

const Landing = () => {
  // Get vertical URLs dynamically (no hardcoded production URLs)
  const { insurance: insuranceUrl, retail: retailUrl } = getVerticalUrls();

  const verticals = [
    {
      name: 'Insurance',
      icon: <SafetyOutlined style={{ fontSize: 48, color: '#003d82' }} />,
      description: 'Comprehensive insurance management platform for policies, claims, and customer service.',
      features: [
        'Policy Management & Quoting',
        'Claims Processing & Tracking',
        'Customer Portal & Support',
        'AI-Powered Assistance',
      ],
      url: insuranceUrl,
      color: '#003d82',
    },
    {
      name: 'Retail',
      icon: <ShoppingOutlined style={{ fontSize: 48, color: '#722ed1' }} />,
      description: 'Complete e-commerce solution for product management, orders, and inventory tracking.',
      features: [
        'Product Catalog & Management',
        'Order Processing & Fulfillment',
        'Inventory Tracking',
        'Customer Service Platform',
      ],
      url: retailUrl,
      color: '#722ed1',
    },
  ];

  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '40px 20px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div style={{ maxWidth: 1200, width: '100%' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: 48 }}>
          <img
            src="/silvermoat-logo.png"
            alt="Silvermoat"
            style={{
              width: 120,
              height: 120,
              marginBottom: 24,
              filter: 'drop-shadow(0 4px 12px rgba(0,0,0,0.2))',
            }}
          />
          <Title level={1} style={{ color: 'white', marginBottom: 8 }}>
            Welcome to Silvermoat
          </Title>
          <Text style={{ fontSize: 18, color: 'rgba(255, 255, 255, 0.9)' }}>
            Multi-Vertical Platform - Choose your vertical below
          </Text>
        </div>

        {/* Vertical Cards */}
        <Row gutter={[32, 32]} justify="center">
          {verticals.map((vertical) => (
            <Col xs={24} sm={24} md={12} lg={10} key={vertical.name}>
              <Card
                hoverable
                style={{
                  height: '100%',
                  borderRadius: 16,
                  border: 'none',
                  boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
                }}
                bodyStyle={{ padding: 32 }}
              >
                <Space direction="vertical" size="large" style={{ width: '100%' }}>
                  {/* Icon */}
                  <div style={{ textAlign: 'center' }}>{vertical.icon}</div>

                  {/* Name */}
                  <Title level={2} style={{ margin: 0, textAlign: 'center', color: vertical.color }}>
                    {vertical.name}
                  </Title>

                  {/* Description */}
                  <Paragraph style={{ fontSize: 16, color: '#595959', marginBottom: 16 }}>
                    {vertical.description}
                  </Paragraph>

                  {/* Features */}
                  <Space direction="vertical" size="small" style={{ width: '100%' }}>
                    {vertical.features.map((feature, index) => (
                      <div key={index} style={{ display: 'flex', alignItems: 'flex-start' }}>
                        <CheckCircleOutlined
                          style={{ color: '#52c41a', marginRight: 8, marginTop: 4 }}
                        />
                        <Text style={{ fontSize: 14 }}>{feature}</Text>
                      </div>
                    ))}
                  </Space>

                  {/* Learn More Button */}
                  <Button
                    type="primary"
                    size="large"
                    block
                    icon={<ArrowRightOutlined />}
                    href={vertical.url}
                    style={{
                      marginTop: 16,
                      height: 48,
                      fontSize: 16,
                      backgroundColor: vertical.color,
                      borderColor: vertical.color,
                    }}
                  >
                    Learn More
                  </Button>
                </Space>
              </Card>
            </Col>
          ))}
        </Row>

        {/* Footer */}
        <div style={{ textAlign: 'center', marginTop: 48 }}>
          <Text style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: 14 }}>
            © 2025 Silvermoat. All rights reserved.
          </Text>
        </div>
      </div>
    </div>
  );
};

export default Landing;
