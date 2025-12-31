/**
 * Customer Login Page
 * Simple authentication using policy number + ZIP code
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, Card, Typography, message } from 'antd';
import { LockOutlined, SafetyOutlined } from '@ant-design/icons';
import { authenticateCustomer } from '../../services/customer';

const { Title, Text } = Typography;

const CustomerLogin = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const response = await authenticateCustomer(values.policyNumber, values.zip);

      // Store authentication in session storage
      sessionStorage.setItem('customerAuth', JSON.stringify({
        policyNumber: response.policyNumber,
        policyId: response.policyId,
        holderName: response.holderName,
        authenticated: true,
      }));

      message.success(`Welcome back, ${response.holderName}!`);
      navigate('/customer/dashboard');
    } catch (error) {
      message.error(error.message || 'Invalid policy number or ZIP code');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px',
    }}>
      <Card
        style={{
          width: '100%',
          maxWidth: 400,
          boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: 24 }}>
          <SafetyOutlined style={{ fontSize: 48, color: '#1890ff', marginBottom: 16 }} />
          <Title level={2} style={{ marginBottom: 8 }}>Customer Portal</Title>
          <Text type="secondary">Access your insurance information</Text>
        </div>

        <Form
          name="customer_login"
          onFinish={onFinish}
          layout="vertical"
          size="large"
        >
          <Form.Item
            name="policyNumber"
            label="Policy Number"
            rules={[
              { required: true, message: 'Please enter your policy number' },
            ]}
          >
            <Input
              prefix={<LockOutlined />}
              placeholder="POL-2024-XXXXXX"
            />
          </Form.Item>

          <Form.Item
            name="zip"
            label="ZIP Code"
            rules={[
              { required: true, message: 'Please enter your ZIP code' },
              { pattern: /^\d{5}$/, message: 'ZIP code must be 5 digits' },
            ]}
          >
            <Input
              placeholder="12345"
              maxLength={5}
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
            >
              Sign In
            </Button>
          </Form.Item>

          <div style={{ textAlign: 'center', marginTop: 16 }}>
            <Text type="secondary" style={{ fontSize: 12 }}>
              Your policy number can be found on your policy documents.
              For assistance, contact customer service.
            </Text>
          </div>
        </Form>
      </Card>
    </div>
  );
};

export default CustomerLogin;
