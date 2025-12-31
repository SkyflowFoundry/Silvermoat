/**
 * Customer Login Page
 * Simple authentication using policy number + ZIP code
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, Card, Typography, message } from 'antd';
import { LockOutlined, SafetyOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { authenticateCustomer } from '../../services/customer';
import { getApiBase } from '../../App';

const { Title, Text } = Typography;

const CustomerLogin = () => {
  const [loading, setLoading] = useState(false);
  const [autoFillLoading, setAutoFillLoading] = useState(false);
  const [form] = Form.useForm();
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

  const handleAutoFill = async () => {
    setAutoFillLoading(true);
    try {
      // Fetch a valid policy from the backend
      const apiBase = getApiBase();
      const response = await fetch(`${apiBase}/policy`);

      if (!response.ok) {
        throw new Error('Failed to fetch policies');
      }

      const data = await response.json();

      if (data.length === 0) {
        message.warning('No policies found. Please seed demo data first.');
        return;
      }

      // Use the first policy
      const policy = data[0];
      form.setFieldsValue({
        policyNumber: policy.policyNumber,
        zip: policy.zip,
      });

      message.success('Demo credentials loaded!');
    } catch (error) {
      message.error('Failed to load demo credentials');
    } finally {
      setAutoFillLoading(false);
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

        <Button
          type="dashed"
          icon={<ThunderboltOutlined />}
          onClick={handleAutoFill}
          loading={autoFillLoading}
          block
          style={{ marginBottom: 24, borderColor: '#722ed1', color: '#722ed1' }}
        >
          Load Demo Credentials
        </Button>

        <Form
          name="customer_login"
          form={form}
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
