/**
 * Customer Claim Submission Form
 * Allows customers to submit new claims
 */

import { useState, useEffect } from 'react';
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
  Spin,
} from 'antd';
import { ArrowLeftOutlined, FileTextOutlined } from '@ant-design/icons';
import { submitClaim, getAvailableCustomers, getCustomerPolicies } from '../../services/customer';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const CLAIM_TYPES = [
  'water_damage',
  'fire',
  'theft',
  'liability',
];

const CustomerClaimForm = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [customers, setCustomers] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [policies, setPolicies] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    try {
      const customerList = await getAvailableCustomers();
      setCustomers(customerList);
      if (customerList.length > 0) {
        const defaultCustomer = customerList[0];
        setSelectedCustomer(defaultCustomer);
        await loadPolicies(defaultCustomer.email);
      }
    } catch (error) {
      message.error('Failed to load customers');
      console.error(error);
    } finally {
      setInitialLoading(false);
    }
  };

  const loadPolicies = async (email) => {
    try {
      const { policies: customerPolicies } = await getCustomerPolicies(email);
      setPolicies(customerPolicies);
    } catch (error) {
      message.error('Failed to load policies');
      console.error(error);
    }
  };

  const handleCustomerChange = async (email) => {
    const customer = customers.find(c => c.email === email);
    setSelectedCustomer(customer);
    await loadPolicies(email);
    form.resetFields(['policyId']);
  };

  if (initialLoading) {
    return (
      <div style={{ padding: '16px', background: '#f0f2f5', minHeight: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Spin size="large" />
      </div>
    );
  }

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const claimData = {
        policyId: values.policyId,
        claim_type: values.claim_type,
        date_of_loss: values.date_of_loss.format('YYYY-MM-DD'),
        description: values.description,
        claim_amount: Math.round(values.claim_amount || 0),
      };

      await submitClaim(claimData);

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
    <div style={{ padding: '16px', background: '#f0f2f5', minHeight: '100vh' }}>
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
            {selectedCustomer && (
              <Text type="secondary">
                Filing as: {selectedCustomer.name} ({selectedCustomer.email})
              </Text>
            )}
          </div>

          <Form
            form={form}
            layout="vertical"
            onFinish={onFinish}
          >
            <Form.Item
              label="Customer"
              style={{ marginBottom: 16 }}
            >
              <Select
                value={selectedCustomer?.email}
                onChange={handleCustomerChange}
                size="large"
              >
                {customers.map(customer => (
                  <Option key={customer.email} value={customer.email}>
                    {customer.name} ({customer.email})
                  </Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item
              name="policyId"
              label="Policy"
              rules={[{ required: true, message: 'Please select a policy' }]}
            >
              <Select
                size="large"
                placeholder="Select policy"
                disabled={!policies.length}
              >
                {policies.map(policy => (
                  <Option key={policy.id} value={policy.id}>
                    {policy.id.substring(0, 8)}... - {policy.data?.property_address || 'No address'}
                  </Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item
              name="claim_type"
              label="Type of Claim"
              rules={[{ required: true, message: 'Please select the claim type' }]}
            >
              <Select
                size="large"
                placeholder="Select claim type"
              >
                {CLAIM_TYPES.map(type => (
                  <Option key={type} value={type}>
                    {type.replace(/_/g, ' ').toUpperCase()}
                  </Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item
              name="date_of_loss"
              label="Date of Loss"
              rules={[{ required: true, message: 'Please select the date of loss' }]}
            >
              <DatePicker
                size="large"
                style={{ width: '100%' }}
                placeholder="Select date"
                disabledDate={(current) => current && current > new Date()}
              />
            </Form.Item>

            <Form.Item
              name="claim_amount"
              label="Claim Amount ($)"
              rules={[
                { required: true, message: 'Please enter claim amount' },
                { type: 'number', min: 0, message: 'Amount must be positive' },
              ]}
            >
              <InputNumber
                size="large"
                style={{ width: '100%' }}
                placeholder="0"
                formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                parser={value => value.replace(/\$\s?|(,*)/g, '')}
                precision={0}
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
