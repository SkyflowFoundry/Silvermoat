/**
 * Customer Dashboard
 * Landing page for customer portal with navigation
 */

import { Card, Row, Col, Typography, Button, Space } from 'antd';
import {
  ShoppingOutlined,
  SearchOutlined,
  ShoppingCartOutlined,
  CustomerServiceOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const { Title, Paragraph } = Typography;

const CustomerDashboard = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <SearchOutlined style={{ fontSize: 48, color: '#531dab' }} />,
      title: 'Track Your Order',
      description: 'Check the status of your orders by entering your email address',
      action: 'Track Orders',
      path: '/customer/orders',
    },
    {
      icon: <ShoppingOutlined style={{ fontSize: 48, color: '#531dab' }} />,
      title: 'Browse Products',
      description: 'Explore our product catalog and find what you need',
      action: 'View Products',
      path: '/customer/products',
    },
    {
      icon: <CustomerServiceOutlined style={{ fontSize: 48, color: '#531dab' }} />,
      title: 'Get Help',
      description: 'Chat with our AI assistant for instant support',
      action: 'Chat Now',
      onClick: () => {
        // Scroll to bottom to reveal chat (or trigger chat drawer)
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
      },
    },
  ];

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '24px' }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: 48 }}>
        <ShoppingCartOutlined style={{ fontSize: 64, color: '#531dab', marginBottom: 16 }} />
        <Title level={1} style={{ margin: 0, color: '#531dab' }}>
          Welcome to Silvermoat Retail
        </Title>
        <Paragraph style={{ fontSize: 16, color: '#666', marginTop: 12 }}>
          Track your orders, browse products, and get instant support
        </Paragraph>
      </div>

      {/* Feature Cards */}
      <Row gutter={[24, 24]}>
        {features.map((feature, idx) => (
          <Col xs={24} md={8} key={idx}>
            <Card
              hoverable
              style={{
                height: '100%',
                textAlign: 'center',
                borderRadius: 8,
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              }}
            >
              <Space direction="vertical" size="large" style={{ width: '100%' }}>
                {feature.icon}
                <div>
                  <Title level={3} style={{ margin: 0 }}>
                    {feature.title}
                  </Title>
                  <Paragraph style={{ color: '#666', marginTop: 8 }}>
                    {feature.description}
                  </Paragraph>
                </div>
                <Button
                  type="primary"
                  size="large"
                  onClick={feature.onClick || (() => navigate(feature.path))}
                >
                  {feature.action}
                </Button>
              </Space>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default CustomerDashboard;
