/**
 * Payment Form Component
 */

import { Form, Input, Button, Card, DatePicker, Select, InputNumber, Space } from 'antd';
import { DollarOutlined, CreditCardOutlined, FileProtectOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { useCreatePayment } from '../../hooks/mutations/useCreatePayment';
import { PAYMENT_METHOD_OPTIONS, PAYMENT_STATUS_OPTIONS } from '../../config/constants';
import { generatePaymentSampleData } from '../../utils/formSampleData';
import dayjs from 'dayjs';

const PaymentForm = ({ onSuccess }) => {
  const [form] = Form.useForm();
  const createPaymentMutation = useCreatePayment();

  const handleSubmit = async (values) => {
    try {
      const formattedValues = {
        ...values,
        paymentDate: values.paymentDate?.format('YYYY-MM-DD'),
      };

      const result = await createPaymentMutation.mutateAsync(formattedValues);
      form.resetFields();
      if (onSuccess) {
        onSuccess(result);
      }
    } catch (error) {
      console.error('Failed to create payment:', error);
    }
  };

  const handleFillSampleData = () => {
    const sampleData = generatePaymentSampleData();
    form.setFieldsValue({
      ...sampleData,
      paymentDate: dayjs(sampleData.paymentDate),
    });
  };

  return (
    <Card title="Record New Payment" bordered={false}>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        autoComplete="off"
        initialValues={{
          status: 'COMPLETED',
          method: 'CARD',
        }}
      >
        <Form.Item
          name="paymentDate"
          label="Payment Date"
          rules={[{ required: true, message: 'Please select the payment date' }]}
        >
          <DatePicker
            size="large"
            style={{ width: '100%' }}
            format="MM/DD/YYYY"
          />
        </Form.Item>

        <Form.Item
          name="amount"
          label="Payment Amount"
          rules={[
            { required: true, message: 'Please enter the payment amount' },
            { type: 'number', min: 0, message: 'Amount must be positive' },
          ]}
        >
          <InputNumber
            prefix={<DollarOutlined />}
            placeholder="250.00"
            size="large"
            style={{ width: '100%' }}
            precision={2}
            min={0}
            step={10}
          />
        </Form.Item>

        <Form.Item
          name="method"
          label="Payment Method"
          rules={[{ required: true, message: 'Please select a payment method' }]}
        >
          <Select
            size="large"
            placeholder="Select payment method"
            options={PAYMENT_METHOD_OPTIONS}
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
            options={PAYMENT_STATUS_OPTIONS.map((opt) => ({
              label: opt.label,
              value: opt.value,
            }))}
          />
        </Form.Item>

        <Form.Item
          name="policyId"
          label="Related Policy ID"
          rules={[{ required: true, message: 'Please enter the policy ID' }]}
        >
          <Input
            prefix={<FileProtectOutlined />}
            placeholder="Enter policy ID"
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
              loading={createPaymentMutation.isPending}
              size="large"
              block
            >
              {createPaymentMutation.isPending ? 'Recording Payment...' : 'Record Payment'}
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default PaymentForm;
