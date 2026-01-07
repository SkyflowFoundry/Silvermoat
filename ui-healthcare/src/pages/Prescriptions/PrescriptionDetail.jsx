/**
 * Prescription Detail Page
 * Displays and allows editing of a single prescription
 */

import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Spin, Alert, Space, Descriptions, Tag, Typography } from 'antd';
import { ArrowLeftOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { usePrescription } from '../../hooks/queries/usePrescription';
import { deletePrescription } from '../../services/prescriptions';
import { formatTimestamp } from '../../utils/formatters';

const { Title } = Typography;

const STATUS_COLORS = {
  ACTIVE: 'green',
  FILLED: 'blue',
  EXPIRED: 'gray',
  CANCELLED: 'red',
};

const PrescriptionDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: prescription, isLoading, error } = usePrescription(id);

  const handleBack = () => {
    navigate('/prescriptions');
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this prescription?')) {
      try {
        await deletePrescription(id);
        navigate('/prescriptions');
      } catch (err) {
        console.error('Failed to delete prescription:', err);
        alert('Failed to delete prescription');
      }
    }
  };

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '48px' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (error || !prescription) {
    return (
      <Alert
        message="Error"
        description="Failed to load prescription details"
        type="error"
        showIcon
      />
    );
  }

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={handleBack}>
          Back to Prescriptions
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Prescription Details
            </Title>
            <Tag color={STATUS_COLORS[prescription.status] || 'default'}>
              {prescription.status || 'ACTIVE'}
            </Tag>
          </Space>
        }
        extra={
          <Space>
            <Button icon={<EditOutlined />} disabled>
              Edit
            </Button>
            <Button icon={<DeleteOutlined />} danger onClick={handleDelete}>
              Delete
            </Button>
          </Space>
        }
      >
        <Descriptions column={2} bordered>
          <Descriptions.Item label="Prescription ID">{prescription.id}</Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={STATUS_COLORS[prescription.status] || 'default'}>
              {prescription.status || 'ACTIVE'}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Patient">
            {prescription.data?.patientName || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Prescriber">
            {prescription.data?.prescriber || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Medication">
            {prescription.data?.medication || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Dosage">
            {prescription.data?.dosage || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Frequency">
            {prescription.data?.frequency || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Duration">
            {prescription.data?.duration || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Refills Allowed">
            {prescription.data?.refillsAllowed ?? '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Instructions" span={2}>
            {prescription.data?.instructions || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(prescription.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Last Updated">
            {formatTimestamp(prescription.updatedAt)}
          </Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
};

export default PrescriptionDetail;
