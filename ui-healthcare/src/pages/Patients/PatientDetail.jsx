/**
 * Patient Detail Page
 * Displays and allows editing of a single patient
 */

import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Spin, Alert, Space, Descriptions, Tag, Typography } from 'antd';
import { ArrowLeftOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { usePatient } from '../../hooks/queries/usePatient';
import { deletePatient } from '../../services/patients';
import { formatTimestamp } from '../../utils/formatters';

const { Title } = Typography;

const STATUS_COLORS = {
  ACTIVE: 'green',
  INACTIVE: 'gray',
  ARCHIVED: 'red',
};

const PatientDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: patient, isLoading, error } = usePatient(id);

  const handleBack = () => {
    navigate('/patients');
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this patient?')) {
      try {
        await deletePatient(id);
        navigate('/patients');
      } catch (err) {
        console.error('Failed to delete patient:', err);
        alert('Failed to delete patient');
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

  if (error || !patient) {
    return (
      <Alert
        message="Error"
        description="Failed to load patient details"
        type="error"
        showIcon
      />
    );
  }

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={handleBack}>
          Back to Patients
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Patient Details
            </Title>
            <Tag color={STATUS_COLORS[patient.status] || 'default'}>
              {patient.status || 'ACTIVE'}
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
          <Descriptions.Item label="Patient ID">{patient.id}</Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={STATUS_COLORS[patient.status] || 'default'}>
              {patient.status || 'ACTIVE'}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Name">{patient.data?.name || '-'}</Descriptions.Item>
          <Descriptions.Item label="Email">{patient.data?.email || '-'}</Descriptions.Item>
          <Descriptions.Item label="Phone">{patient.data?.phone || '-'}</Descriptions.Item>
          <Descriptions.Item label="Date of Birth">
            {patient.data?.dateOfBirth || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Address" span={2}>
            {patient.data?.address || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Emergency Contact" span={2}>
            {patient.data?.emergencyContact || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(patient.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Last Updated">
            {formatTimestamp(patient.updatedAt)}
          </Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
};

export default PatientDetail;
