/**
 * Customer Claim Submission Form
 * Allows customers to submit new claims
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  Form,
  Input,
  Button,
  DatePicker,
  InputNumber,
  message,
  Typography,
  Space,
  Select,
} from 'antd';
import { ArrowLeftOutlined, FileTextOutlined } from '@ant-design/icons';
import { submitClaim } from '../../services/customer';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const LOSS_TYPES = [
  'AUTO_COLLISION',
  'AUTO_GLASS',
  'AUTO_THEFT',
  'PROPERTY_DAMAGE',
  'WATER_DAMAGE',
  'FIRE',
  'THEFT',
  'VANDALISM',
];

const CustomerClaimForm = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Get customer auth from session storage
  const auth = JSON.parse(sessionStorage.getItem('customerAuth') || '{}');

  if (!auth.authenticated) {
    navigate('/customer/login');
    return null;
  }

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const claimData = {
        policyNumber: auth.policyNumber,
        claimantName: auth.holderName,
        incidentDate: values.incidentDate.format('YYYY-MM-DD'),
        lossType: values.lossType,
        description: values.description,
        estimatedAmount_cents: Math.round((values.estimatedAmount || 0) * 100),
      };

      const response = await submitClaim(claimData);

      message.success('Claim submitted successfully!');
      navigate('/customer/dashboard');
    } catch (error) {
      message.error(error.message || 'Failed to submit claim');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '24px', background: '#f0f2f5', minHeight: '100vh' }}>
      <Card style={{ maxWidth: 800, margin: '0 auto' }}>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <Button
              type="text"
              icon={<ArrowLeftOutlined />}
              onClick={() => navigate('/customer/dashboard')}
              style={{ marginBottom: 16 }}
            >
              Back to Dashboard
            </Button>
            <Title level={3}>
              <FileTextOutlined /> Submit New Claim
            </Title>
            <Text type="secondary">
              Policy: {auth.policyNumber} • {auth.holderName}
            </Text>
          </div>

          <Form
            form={form}
            layout="vertical"
            onFinish={onFinish}
            initialValues={{
              claimantName: auth.holderName,
            }}
          >
            <Form.Item
              name="lossType"
              label="Type of Loss"
              rules={[{ required: true, message: 'Please select the type of loss' }]}
            >
              <Select
                size="large"
                placeholder="Select loss type"
              >
                {LOSS_TYPES.map(type => (
                  <Option key={type} value={type}>
                    {type.replace(/_/g, ' ')}
                  </Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item
              name="incidentDate"
              label="Incident Date"
              rules={[{ required: true, message: 'Please select the incident date' }]}
            >
              <DatePicker
                size="large"
                style={{ width: '100%' }}
                placeholder="Select date"
                disabledDate={(current) => current && current > new Date()}
              />
            </Form.Item>

            <Form.Item
              name="estimatedAmount"
              label="Estimated Damage Amount ($)"
              rules={[
                { required: true, message: 'Please enter estimated amount' },
                { type: 'number', min: 0, message: 'Amount must be positive' },
              ]}
            >
              <InputNumber
                size="large"
                style={{ width: '100%' }}
                placeholder="0.00"
                formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                parser={value => value.replace(/\$\s?|(,*)/g, '')}
                precision={2}
              />
            </Form.Item>

            <Form.Item
              name="description"
              label="Description of Incident"
              rules={[
                { required: true, message: 'Please provide a description' },
                { min: 20, message: 'Description must be at least 20 characters' },
              ]}
            >
              <TextArea
                rows={6}
                placeholder="Please describe what happened in detail, including location, time, and any other relevant information..."
                maxLength={2000}
                showCount
              />
            </Form.Item>

            <Form.Item style={{ marginBottom: 0 }}>
              <Space>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  size="large"
                >
                  Submit Claim
                </Button>
                <Button
                  size="large"
                  onClick={() => navigate('/customer/dashboard')}
                >
                  Cancel
                </Button>
              </Space>
            </Form.Item>
          </Form>

          <Card type="inner" style={{ background: '#f7f9fc', border: '1px solid #d9d9d9' }}>
            <Text strong>What happens next?</Text>
            <ul style={{ marginTop: 8, marginBottom: 0 }}>
              <li>Your claim will be reviewed by our team within 24-48 hours</li>
              <li>We may contact you for additional information</li>
              <li>You can track your claim status in your dashboard</li>
              <li>An adjuster will be assigned to your case</li>
            </ul>
          </Card>
        </Space>
      </Card>
    </div>
  );
};

export default CustomerClaimForm;
