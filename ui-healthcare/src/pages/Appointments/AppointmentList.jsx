/**
 * Appointment List Page
 * Main page for appointment management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, CalendarOutlined } from '@ant-design/icons';
import { useAppointments } from '../../hooks/queries/useAppointments';
import AppointmentTable from './AppointmentTable';
import AppointmentsStats from './AppointmentsStats';
import AppointmentForm from './AppointmentForm';

const { Title } = Typography;

const AppointmentList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = useAppointments();
  const appointments = data?.items || [];

  // Check if we're on the /new route
  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/appointments/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/appointments');
    }
  };

  const handleAppointmentCreated = () => {
    handleModalClose();
    refetch();
  };

  const handleRefresh = () => {
    refetch();
  };

  return (
    <div>
      <Space
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 24,
        }}
      >
        <Space>
          <CalendarOutlined style={{ fontSize: 24, color: '#52c41a' }} />
          <Title level={2} style={{ margin: 0 }}>
            Appointments
          </Title>
        </Space>
        <Space>
          <Button
            icon={<ReloadOutlined />}
            onClick={handleRefresh}
            loading={isLoading}
          >
            Refresh
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleModalOpen}
          >
            New Appointment
          </Button>
        </Space>
      </Space>

      {/* Statistics */}
      <Card style={{ marginBottom: 24 }}>
        <AppointmentsStats />
      </Card>

      {/* Table */}
      <AppointmentTable appointments={appointments} loading={isLoading} />

      {/* Create Modal */}
      <Modal
        title="Create New Appointment"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={700}
        destroyOnClose
      >
        <AppointmentForm onSuccess={handleAppointmentCreated} />
      </Modal>
    </div>
  );
};

export default AppointmentList;
