/**
 * Quote Form Component
 * Form for creating new quotes with validation
 */

import { Form, Input, Button, Card, Space } from 'antd';
import { UserOutlined, EnvironmentOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { useCreateQuote } from '../../hooks/mutations/useCreateQuote';
import { generateQuoteSampleData } from '../../utils/formSampleData';

const QuoteForm = ({ onSuccess }) => {
  const [form] = Form.useForm();
  const createQuoteMutation = useCreateQuote();

  const handleSubmit = async (values) => {
    try {
      const result = await createQuoteMutation.mutateAsync(values);
      form.resetFields();
      if (onSuccess) {
        onSuccess(result);
      }
    } catch (error) {
      // Error is handled by the mutation hook
      console.error('Failed to create quote:', error);
    }
  };

  const handleFillSampleData = () => {
    const sampleData = generateQuoteSampleData();
    form.setFieldsValue(sampleData);
  };

  return (
    <Card title="Create New Quote" bordered={false}>
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
            { max: 100, message: 'Name must not exceed 100 characters' },
          ]}
        >
          <Input
            prefix={<UserOutlined />}
            placeholder="Jane Doe"
            size="large"
          />
        </Form.Item>

        <Form.Item
          name="zip"
          label="ZIP Code"
          rules={[
            { required: true, message: 'Please enter a ZIP code' },
            {
              pattern: /^\d{5}$/,
              message: 'ZIP code must be exactly 5 digits',
            },
          ]}
        >
          <Input
            prefix={<EnvironmentOutlined />}
            placeholder="12345"
            maxLength={5}
            size="large"
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
              loading={createQuoteMutation.isPending}
              size="large"
              block
            >
              {createQuoteMutation.isPending ? 'Creating Quote...' : 'Create Quote'}
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default QuoteForm;
