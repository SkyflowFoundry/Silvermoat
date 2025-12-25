/**
 * Payment List Page
 */

import { useState, useEffect } from 'react';
import { Typography, Space, Button, Modal } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation, useNavigate } from 'react-router-dom';
import { usePayments } from '../../hooks/queries/usePayments';
import PaymentForm from './PaymentForm';
import PaymentTable from './PaymentTable';
import PaymentsStats from './PaymentsStats';

const { Title } = Typography;

const PaymentList = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch payments from API
  const { data, isLoading, refetch } = usePayments();
  const payments = data?.items || [];

  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handlePaymentCreated = () => {
    refetch();
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/payments');
    }
  };

  const handleRefresh = () => {
    refetch();
  };

  const handleModalOpen = () => {
    setModalOpen(true);
    navigate('/payments/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/payments');
    }
  };

  return (
    <div>
      <Space
        style={{
          marginBottom: 24,
          width: '100%',
          justifyContent: 'space-between',
        }}
      >
        <Title level={2} style={{ margin: 0 }}>
          Payments
        </Title>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={handleRefresh}>
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

      {/* Mini Dashboard */}
      <div style={{ marginBottom: 24 }}>
        <PaymentsStats />
      </div>

      <PaymentTable payments={payments} loading={isLoading} />

      {!isLoading && payments.length === 0 && (
        <div
          style={{
            textAlign: 'center',
            padding: '50px',
            color: '#8c8c8c',
          }}
        >
          <p>No payments recorded yet. Click "New Payment" to record one.</p>
        </div>
      )}

      {/* New Payment Modal */}
      <Modal
        title="New Payment"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={800}
        destroyOnClose
      >
        <PaymentForm onSuccess={handlePaymentCreated} />
      </Modal>
    </div>
  );
};

export default PaymentList;
