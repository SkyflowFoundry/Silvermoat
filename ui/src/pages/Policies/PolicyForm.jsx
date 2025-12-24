/**
 * Policy Form Component
 * Form for creating new policies with validation
 */

import { Form, Input, Button, Card, DatePicker, Select, InputNumber } from 'antd';
import {
  UserOutlined,
  FileTextOutlined,
  DollarOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons';
import { useCreatePolicy } from '../../hooks/mutations/useCreatePolicy';
import { POLICY_STATUS_OPTIONS } from '../../config/constants';
import dayjs from 'dayjs';

const PolicyForm = ({ onSuccess }) => {
  const [form] = Form.useForm();
  const createPolicyMutation = useCreatePolicy();

  const handleSubmit = async (values) => {
    try {
      // Format dates to ISO strings
      const formattedValues = {
        ...values,
        effectiveDate: values.effectiveDate?.format('YYYY-MM-DD'),
        expirationDate: values.expirationDate?.format('YYYY-MM-DD'),
      };

      const result = await createPolicyMutation.mutateAsync(formattedValues);
      form.resetFields();
      if (onSuccess) {
        onSuccess(result);
      }
    } catch (error) {
      console.error('Failed to create policy:', error);
    }
  };

  return (
    <Card title="Create New Policy" bordered={false}>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        autoComplete="off"
        initialValues={{
          status: 'ACTIVE',
        }}
      >
        <Form.Item
          name="policyNumber"
          label="Policy Number"
          rules={[
            { required: true, message: 'Please enter a policy number' },
            { min: 3, message: 'Policy number must be at least 3 characters' },
          ]}
        >
          <Input
            prefix={<FileTextOutlined />}
            placeholder="POL-2024-001"
            size="large"
          />
        </Form.Item>

        <Form.Item
          name="holderName"
          label="Policy Holder Name"
          rules={[
            { required: true, message: 'Please enter the policy holder name' },
            { min: 2, message: 'Name must be at least 2 characters' },
          ]}
        >
          <Input
            prefix={<UserOutlined />}
            placeholder="John Smith"
            size="large"
          />
        </Form.Item>

        <Form.Item
          name="effectiveDate"
          label="Effective Date"
          rules={[{ required: true, message: 'Please select an effective date' }]}
        >
          <DatePicker
            size="large"
            style={{ width: '100%' }}
            format="MM/DD/YYYY"
          />
        </Form.Item>

        <Form.Item
          name="expirationDate"
          label="Expiration Date"
          rules={[
            { required: true, message: 'Please select an expiration date' },
            ({ getFieldValue }) => ({
              validator(_, value) {
                const effectiveDate = getFieldValue('effectiveDate');
                if (!value || !effectiveDate || value.isAfter(effectiveDate)) {
                  return Promise.resolve();
                }
                return Promise.reject(
                  new Error('Expiration date must be after effective date')
                );
              },
            }),
          ]}
        >
          <DatePicker
            size="large"
            style={{ width: '100%' }}
            format="MM/DD/YYYY"
          />
        </Form.Item>

        <Form.Item
          name="premium"
          label="Annual Premium"
          rules={[
            { required: true, message: 'Please enter the premium amount' },
            { type: 'number', min: 0, message: 'Premium must be a positive number' },
          ]}
        >
          <InputNumber
            prefix={<DollarOutlined />}
            placeholder="1250.00"
            size="large"
            style={{ width: '100%' }}
            precision={2}
            min={0}
            step={100}
          />
        </Form.Item>

        <Form.Item
          name="status"
          label="Status"
          rules={[{ required: true, message: 'Please select a status' }]}
        >
          <Select
            size="large"
            placeholder="Select status"
            options={POLICY_STATUS_OPTIONS.map((opt) => ({
              label: opt.label,
              value: opt.value,
            }))}
          />
        </Form.Item>

        <Form.Item
          name="quoteId"
          label="Related Quote ID (Optional)"
        >
          <Input
            placeholder="Enter quote ID if applicable"
            size="large"
          />
        </Form.Item>

        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            loading={createPolicyMutation.isPending}
            size="large"
            block
          >
            {createPolicyMutation.isPending ? 'Creating Policy...' : 'Create Policy'}
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default PolicyForm;
