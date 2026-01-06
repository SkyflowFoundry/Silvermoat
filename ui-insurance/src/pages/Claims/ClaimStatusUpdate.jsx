/**
 * Claim Status Update Modal
 * Modal for updating claim status
 */

import { Modal, Form, Select } from 'antd';
import { CLAIM_STATUS_OPTIONS } from '../../config/constants';
import { useUpdateClaimStatus } from '../../hooks/mutations/useUpdateClaimStatus';

const ClaimStatusUpdate = ({ open, onClose, claim }) => {
  const [form] = Form.useForm();
  const updateStatusMutation = useUpdateClaimStatus();

  const handleSubmit = async (values) => {
    try {
      await updateStatusMutation.mutateAsync({
        id: claim.id,
        status: values.status,
      });
      form.resetFields();
      onClose();
    } catch (error) {
      console.error('Failed to update status:', error);
    }
  };

  const handleCancel = () => {
    form.resetFields();
    onClose();
  };

  return (
    <Modal
      title="Update Claim Status"
      open={open}
      onOk={() => form.submit()}
      onCancel={handleCancel}
      confirmLoading={updateStatusMutation.isPending}
      okText="Update Status"
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        initialValues={{
          status: claim?.data?.status || 'REVIEW',
        }}
      >
        <Form.Item
          name="status"
          label="New Status"
          rules={[{ required: true, message: 'Please select a status' }]}
        >
          <Select
            size="large"
            placeholder="Select new status"
            options={CLAIM_STATUS_OPTIONS.map((opt) => ({
              label: opt.label,
              value: opt.value,
            }))}
          />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default ClaimStatusUpdate;
