/**
 * Customer Form Component
 * Form for creating/editing customers with validation
 */

import { Form, Input, Button, Card, Space, Row, Col, DatePicker } from 'antd';
import { UserOutlined, MailOutlined, PhoneOutlined, EnvironmentOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { useCreateCustomer } from '../../hooks/mutations/useCreateCustomer';
import { generateCustomerSampleData } from '../../utils/formSampleData';

const CustomerForm = ({ onSuccess }) => {
  const [form] = Form.useForm();
  const createCustomerMutation = useCreateCustomer();

  const handleSubmit = async (values) => {
    try {
      // Format date for backend (ISO string)
      const formattedValues = {
        ...values,
        dateOfBirth: values.dateOfBirth ? values.dateOfBirth.format('YYYY-MM-DD') : undefined,
      };

      const result = await createCustomerMutation.mutateAsync(formattedValues);
      form.resetFields();
      if (onSuccess) {
        onSuccess(result);
      }
    } catch (error) {
      // Error is handled by the mutation hook
      console.error('Failed to create customer:', error);
    }
  };

  const handleFillSampleData = () => {
    const sampleData = generateCustomerSampleData();
    form.setFieldsValue(sampleData);
  };

  return (
    <Card title="Create New Customer" bordered={false}>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        autoComplete="off"
      >
        <Form.Item
          name="name"
          label="Full Name"
          rules={[
            { required: true, message: 'Please enter the customer name' },
            { min: 2, message: 'Name must be at least 2 characters' },
            { max: 255, message: 'Name must not exceed 255 characters' },
          ]}
        >
          <Input
            prefix={<UserOutlined />}
            placeholder="John Doe"
            size="large"
          />
        </Form.Item>

        <Form.Item
          name="email"
          label="Email"
          rules={[
            { required: true, message: 'Please enter an email address' },
            { type: 'email', message: 'Please enter a valid email address' },
            { max: 255, message: 'Email must not exceed 255 characters' },
          ]}
        >
          <Input
            prefix={<MailOutlined />}
            placeholder="john.doe@example.com"
            size="large"
          />
        </Form.Item>

        <Form.Item
          name="phone"
          label="Phone"
          rules={[
            { max: 50, message: 'Phone must not exceed 50 characters' },
          ]}
        >
          <Input
            prefix={<PhoneOutlined />}
            placeholder="555-123-4567"
            size="large"
          />
        </Form.Item>

        <Form.Item
          name="address"
          label="Address"
          rules={[
            { max: 500, message: 'Address must not exceed 500 characters' },
          ]}
        >
          <Input
            prefix={<EnvironmentOutlined />}
            placeholder="123 Main Street"
            size="large"
          />
        </Form.Item>

        <Row gutter={16}>
          <Col xs={24} sm={12} md={12}>
            <Form.Item
              name="city"
              label="City"
              rules={[
                { max: 100, message: 'City must not exceed 100 characters' },
              ]}
            >
              <Input placeholder="Austin" size="large" />
            </Form.Item>
          </Col>

          <Col xs={24} sm={6} md={6}>
            <Form.Item
              name="state"
              label="State"
              rules={[
                { max: 50, message: 'State must not exceed 50 characters' },
              ]}
            >
              <Input placeholder="TX" maxLength={2} size="large" />
            </Form.Item>
          </Col>

          <Col xs={24} sm={6} md={6}>
            <Form.Item
              name="zip"
              label="ZIP"
              rules={[
                { pattern: /^\d{5}$/, message: 'ZIP must be 5 digits' },
              ]}
            >
              <Input placeholder="78701" maxLength={5} size="large" />
            </Form.Item>
          </Col>
        </Row>

        <Form.Item
          name="dateOfBirth"
          label="Date of Birth"
        >
          <DatePicker
            size="large"
            style={{ width: '100%' }}
            format="MM/DD/YYYY"
            placeholder="Select date of birth"
          />
        </Form.Item>

        <Form.Item>
          <Space direction="vertical" style={{ width: '100%' }} size="middle">
            <Button
              type="default"
              icon={<ThunderboltOutlined />}
              onClick={handleFillSampleData}
              size="large"
              block
              data-testid="fill-sample-data-button"
            >
              Fill with Sample Data
            </Button>
            <Button
              type="primary"
              htmlType="submit"
              loading={createCustomerMutation.isPending}
              size="large"
              block
            >
              {createCustomerMutation.isPending ? 'Creating Customer...' : 'Create Customer'}
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default CustomerForm;
