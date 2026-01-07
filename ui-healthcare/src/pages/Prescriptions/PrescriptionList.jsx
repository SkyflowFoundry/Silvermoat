/**
 * Prescription List Page
 * Main page for prescription management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, MedicineBoxOutlined } from '@ant-design/icons';
import { usePrescriptions } from '../../hooks/queries/usePrescriptions';
import PrescriptionTable from './PrescriptionTable';
import PrescriptionsStats from './PrescriptionsStats';
import PrescriptionForm from './PrescriptionForm';

const { Title } = Typography;

const PrescriptionList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = usePrescriptions();
  const prescriptions = data?.items || [];

  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/prescriptions/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/prescriptions');
    }
  };

  const handlePrescriptionCreated = () => {
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
          <MedicineBoxOutlined style={{ fontSize: 24, color: '#52c41a' }} />
          <Title level={2} style={{ margin: 0 }}>
            Prescriptions
          </Title>
        </Space>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={handleRefresh} loading={isLoading}>
            Refresh
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleModalOpen}>
            New Prescription
          </Button>
        </Space>
      </Space>

      <Card style={{ marginBottom: 24 }}>
        <PrescriptionsStats />
      </Card>

      <PrescriptionTable prescriptions={prescriptions} loading={isLoading} />

      <Modal
        title="Create New Prescription"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={700}
        destroyOnClose
      >
        <PrescriptionForm onSuccess={handlePrescriptionCreated} />
      </Modal>
    </div>
  );
};

export default PrescriptionList;
