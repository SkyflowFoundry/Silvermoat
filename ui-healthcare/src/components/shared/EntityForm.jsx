/**
 * Generic Entity Form Component
 * Reusable form component for creating entities with validation
 */

import { Form, Button, Card, Space } from 'antd';
import { ThunderboltOutlined } from '@ant-design/icons';

const EntityForm = ({
  title = 'Create New Item',
  fields = [],
  onSubmit,
  onSuccess,
  onFillSampleData,
  createMutation,
  initialValues = {},
  submitButtonText = 'Create',
  submitButtonLoadingText = 'Creating...',
}) => {
  const [form] = Form.useForm();

  const handleSubmit = async (values) => {
    try {
      let formattedValues = { ...values };

      // Apply field transformers if defined
      fields.forEach(field => {
        if (field.name && field.transform && values[field.name] !== undefined) {
          formattedValues[field.name] = field.transform(values[field.name]);
        }
      });

      // Call custom onSubmit if provided, otherwise use mutation
      const result = onSubmit
        ? await onSubmit(formattedValues)
        : await createMutation.mutateAsync(formattedValues);

      form.resetFields();
      if (onSuccess) {
        onSuccess(result);
      }
    } catch (error) {
      console.error('Failed to submit form:', error);
    }
  };

  const handleFillSampleData = () => {
    if (onFillSampleData) {
      const sampleData = onFillSampleData();
      form.setFieldsValue(sampleData);
    }
  };

  return (
    <Card title={title} bordered={false}>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        autoComplete="off"
        initialValues={initialValues}
      >
        {fields.map((field) => (
          <Form.Item
            key={field.name}
            name={field.name}
            label={field.label}
            rules={field.rules || []}
            {...field.formItemProps}
          >
            {field.component}
          </Form.Item>
        ))}

        <Form.Item>
          <Space direction="vertical" style={{ width: '100%' }} size="middle">
            {onFillSampleData && (
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
            )}
            <Button
              type="primary"
              htmlType="submit"
              loading={createMutation?.isPending}
              size="large"
              block
            >
              {createMutation?.isPending ? submitButtonLoadingText : submitButtonText}
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default EntityForm;
