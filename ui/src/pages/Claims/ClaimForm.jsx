/**
 * Claim Form Component
 * Form for creating new claims
 */

import { Form, Input, Button, Card, DatePicker, Select, InputNumber, Space } from 'antd';
import { FileTextOutlined, UserOutlined, DollarOutlined, FileProtectOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { useCreateClaim } from '../../hooks/mutations/useCreateClaim';
import { CLAIM_STATUS_OPTIONS } from '../../config/constants';
import { generateClaimSampleData } from '../../utils/formSampleData';
import dayjs from 'dayjs';

const { TextArea } = Input;

const ClaimForm = ({ onSuccess }) => {
  const [form] = Form.useForm();
  const createClaimMutation = useCreateClaim();

  const handleSubmit = async (values) => {
    try {
      const formattedValues = {
        ...values,
        incidentDate: values.incidentDate?.format('YYYY-MM-DD'),
      };

      const result = await createClaimMutation.mutateAsync(formattedValues);
      form.resetFields();
      if (onSuccess) {
        onSuccess(result);
      }
    } catch (error) {
      console.error('Failed to create claim:', error);
    }
  };

  const handleFillSampleData = () => {
    const sampleData = generateClaimSampleData();
    form.setFieldsValue({
      ...sampleData,
      incidentDate: dayjs(sampleData.incidentDate),
    });
  };

  return (
    <Card title="Create New Claim" bordered={false}>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        autoComplete="off"
        initialValues={{
          status: 'PENDING',
        }}
      >
        <Form.Item
          name="claimNumber"
          label="Claim Number"
          rules={[
            { required: true, message: 'Please enter a claim number' },
            { min: 3, message: 'Claim number must be at least 3 characters' },
          ]}
        >
          <Input
            prefix={<FileTextOutlined />}
            placeholder="CLM-2024-001"
            size="large"
          />
        </Form.Item>

        <Form.Item
          name="claimantName"
          label="Claimant Name"
          rules={[
            { required: true, message: 'Please enter the claimant name' },
            { min: 2, message: 'Name must be at least 2 characters' },
          ]}
        >
          <Input
            prefix={<UserOutlined />}
            placeholder="Jane Smith"
            size="large"
          />
        </Form.Item>

        <Form.Item
          name="incidentDate"
          label="Incident Date"
          rules={[{ required: true, message: 'Please select the incident date' }]}
        >
          <DatePicker
            id="incidentDate"
            size="large"
            style={{ width: '100%' }}
            format="MM/DD/YYYY"
          />
        </Form.Item>

        <Form.Item
          name="description"
          label="Description"
          rules={[
            { required: true, message: 'Please provide a description' },
            { min: 10, message: 'Description must be at least 10 characters' },
          ]}
        >
          <TextArea
            rows={4}
            placeholder="Describe the incident and damages..."
          />
        </Form.Item>

        <Form.Item
          name="amount"
          label="Claim Amount"
          rules={[
            { required: true, message: 'Please enter the claim amount' },
            { type: 'number', min: 0, message: 'Amount must be positive' },
          ]}
        >
          <InputNumber
            prefix={<DollarOutlined />}
            placeholder="5000.00"
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
            options={CLAIM_STATUS_OPTIONS.map((opt) => ({
              label: opt.label,
              value: opt.value,
            }))}
          />
        </Form.Item>

        <Form.Item
          name="policyId"
          label="Related Policy ID (Optional)"
        >
          <Input
            prefix={<FileProtectOutlined />}
            placeholder="Enter policy ID if applicable"
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
              loading={createClaimMutation.isPending}
              size="large"
              block
            >
              {createClaimMutation.isPending ? 'Creating Claim...' : 'Create Claim'}
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default ClaimForm;
