/**
 * Quote Form Component
 * Form for creating new quotes with validation
 */

import { Form, Input, Button, Card } from 'antd';
import { UserOutlined, EnvironmentOutlined } from '@ant-design/icons';
import { useCreateQuote } from '../../hooks/mutations/useCreateQuote';

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
          <Button
            type="primary"
            htmlType="submit"
            loading={createQuoteMutation.isPending}
            size="large"
            block
          >
            {createQuoteMutation.isPending ? 'Creating Quote...' : 'Create Quote'}
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default QuoteForm;
