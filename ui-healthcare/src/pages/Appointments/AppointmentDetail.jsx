/**
 * Appointment Detail Page
 * Displays and allows editing of a single appointment
 */

import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Spin, Alert, Space, Descriptions, Tag, Typography } from 'antd';
import { ArrowLeftOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useAppointment } from '../../hooks/queries/useAppointment';
import { deleteAppointment } from '../../services/appointments';
import { formatTimestamp } from '../../utils/formatters';

const { Title } = Typography;

const STATUS_COLORS = {
  SCHEDULED: 'blue',
  CONFIRMED: 'cyan',
  COMPLETED: 'green',
  CANCELLED: 'red',
  NO_SHOW: 'orange',
};

const AppointmentDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: appointment, isLoading, error } = useAppointment(id);

  const handleBack = () => {
    navigate('/appointments');
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this appointment?')) {
      try {
        await deleteAppointment(id);
        navigate('/appointments');
      } catch (err) {
        console.error('Failed to delete appointment:', err);
        alert('Failed to delete appointment');
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

  if (error || !appointment) {
    return (
      <Alert
        message="Error"
        description="Failed to load appointment details"
        type="error"
        showIcon
      />
    );
  }

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={handleBack}>
          Back to Appointments
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Appointment Details
            </Title>
            <Tag color={STATUS_COLORS[appointment.status] || 'default'}>
              {appointment.status || 'SCHEDULED'}
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
          <Descriptions.Item label="Appointment ID">{appointment.id}</Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={STATUS_COLORS[appointment.status] || 'default'}>
              {appointment.status || 'SCHEDULED'}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Patient Name">
            {appointment.data?.patientName || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Patient Email">
            {appointment.data?.patientEmail || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Date & Time">
            {appointment.data?.date || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Provider">
            {appointment.data?.provider || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Type">
            {appointment.data?.type || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Reason" span={2}>
            {appointment.data?.reason || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Notes" span={2}>
            {appointment.data?.notes || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(appointment.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Last Updated">
            {formatTimestamp(appointment.updatedAt)}
          </Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
};

export default AppointmentDetail;
