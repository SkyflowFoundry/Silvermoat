/**
 * Case Form Component
 */

import { Form, Input, Button, Card, Select } from 'antd';
import { FileProtectOutlined, UserOutlined } from '@ant-design/icons';
import { useCreateCase } from '../../hooks/mutations/useCreateCase';
import {
  CASE_PRIORITY_OPTIONS,
  CASE_STATUS_OPTIONS,
  RELATED_ENTITY_TYPES,
} from '../../config/constants';

const { TextArea } = Input;

const CaseForm = ({ onSuccess }) => {
  const [form] = Form.useForm();
  const createCaseMutation = useCreateCase();

  const handleSubmit = async (values) => {
    try {
      const result = await createCaseMutation.mutateAsync(values);
      form.resetFields();
      if (onSuccess) {
        onSuccess(result);
      }
    } catch (error) {
      console.error('Failed to create case:', error);
    }
  };

  return (
    <Card title="Create New Case" bordered={false}>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        autoComplete="off"
        initialValues={{
          status: 'OPEN',
          priority: 'MEDIUM',
        }}
      >
        <Form.Item
          name="title"
          label="Case Title"
          rules={[
            { required: true, message: 'Please enter a case title' },
            { max: 100, message: 'Title must be less than 100 characters' },
          ]}
        >
          <Input
            placeholder="Brief description of the issue"
            size="large"
            maxLength={100}
            showCount
          />
        </Form.Item>

        <Form.Item
          name="description"
          label="Description"
          rules={[
            { required: true, message: 'Please enter a description' },
            { max: 500, message: 'Description must be less than 500 characters' },
          ]}
        >
          <TextArea
            placeholder="Detailed description of the case"
            rows={4}
            maxLength={500}
            showCount
          />
        </Form.Item>

        <Form.Item
          name="relatedEntityType"
          label="Related Entity Type"
          rules={[{ required: true, message: 'Please select an entity type' }]}
        >
          <Select
            size="large"
            placeholder="Select entity type"
            options={RELATED_ENTITY_TYPES}
          />
        </Form.Item>

        <Form.Item
          name="relatedEntityId"
          label="Related Entity ID"
          rules={[{ required: true, message: 'Please enter the entity ID' }]}
        >
          <Input
            prefix={<FileProtectOutlined />}
            placeholder="Enter entity ID"
            size="large"
          />
        </Form.Item>

        <Form.Item
          name="assignee"
          label="Assignee"
          rules={[{ required: true, message: 'Please enter an assignee name' }]}
        >
          <Input
            prefix={<UserOutlined />}
            placeholder="Enter assignee name"
            size="large"
          />
        </Form.Item>

        <Form.Item
          name="priority"
          label="Priority"
          rules={[{ required: true, message: 'Please select a priority' }]}
        >
          <Select
            size="large"
            placeholder="Select priority"
            options={CASE_PRIORITY_OPTIONS.map((opt) => ({
              label: opt.label,
              value: opt.value,
            }))}
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
            options={CASE_STATUS_OPTIONS.map((opt) => ({
              label: opt.label,
              value: opt.value,
            }))}
          />
        </Form.Item>

        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            loading={createCaseMutation.isPending}
            size="large"
            block
          >
            {createCaseMutation.isPending ? 'Creating Case...' : 'Create Case'}
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default CaseForm;
