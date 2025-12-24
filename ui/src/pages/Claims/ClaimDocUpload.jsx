/**
 * Claim Document Upload Modal
 * Modal for uploading documents to a claim
 */

import { Modal, Form, Input } from 'antd';
import { useUploadClaimDocument } from '../../hooks/mutations/useUploadClaimDocument';

const { TextArea } = Input;

const ClaimDocUpload = ({ open, onClose, claim }) => {
  const [form] = Form.useForm();
  const uploadDocMutation = useUploadClaimDocument();

  const handleSubmit = async (values) => {
    try {
      await uploadDocMutation.mutateAsync({
        id: claim.id,
        text: values.text,
      });
      form.resetFields();
      onClose();
    } catch (error) {
      console.error('Failed to upload document:', error);
    }
  };

  const handleCancel = () => {
    form.resetFields();
    onClose();
  };

  return (
    <Modal
      title="Upload Document"
      open={open}
      onOk={() => form.submit()}
      onCancel={handleCancel}
      confirmLoading={uploadDocMutation.isPending}
      okText="Upload"
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
      >
        <Form.Item
          name="text"
          label="Document Content"
          rules={[
            { required: true, message: 'Please enter document content' },
            { min: 10, message: 'Document must be at least 10 characters' },
          ]}
        >
          <TextArea
            rows={8}
            placeholder="Enter document text content..."
          />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default ClaimDocUpload;
