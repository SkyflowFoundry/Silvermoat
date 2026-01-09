/**
 * Payment List Page
 * Main page for payment management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, DollarOutlined } from '@ant-design/icons';
import { usePayments } from '../../hooks/queries/usePayments';
import PaymentTable from './PaymentTable';
import PaymentsStats from './PaymentsStats';
import PaymentForm from './PaymentForm';

const { Title } = Typography;

const PaymentList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = usePayments();
  const payments = data?.items || [];

  // Check if we're on the /new route
  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/payments/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/payments');
    }
  };

  const handlePaymentCreated = () => {
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
          <DollarOutlined style={{ fontSize: 24, color: '#531dab' }} />
          <Title level={2} style={{ margin: 0 }}>
            Payments
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
            New Payment
          </Button>
        </Space>
      </Space>

      {/* Statistics */}
      <Card style={{ marginBottom: 24 }}>
        <PaymentsStats />
      </Card>

      {/* Table */}
      <PaymentTable payments={payments} loading={isLoading} />

      {/* Create Modal */}
      <Modal
        title="Create New Payment"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={600}
        destroyOnClose
      >
        <PaymentForm onSuccess={handlePaymentCreated} />
      </Modal>
    </div>
  );
};

export default PaymentList;
