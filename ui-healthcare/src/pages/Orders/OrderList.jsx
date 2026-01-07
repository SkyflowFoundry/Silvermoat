/**
 * Order List Page
 * Main page for order management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, ShoppingCartOutlined } from '@ant-design/icons';
import { useOrders } from '../../hooks/queries/useOrders';
import OrderTable from './OrderTable';
import OrdersStats from './OrdersStats';
import OrderForm from './OrderForm';

const { Title } = Typography;

const OrderList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = useOrders();
  const orders = data?.items || [];

  // Check if we're on the /new route
  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/orders/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/orders');
    }
  };

  const handleOrderCreated = () => {
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
          <ShoppingCartOutlined style={{ fontSize: 24, color: '#531dab' }} />
          <Title level={2} style={{ margin: 0 }}>
            Orders
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
            New Order
          </Button>
        </Space>
      </Space>

      {/* Statistics */}
      <Card style={{ marginBottom: 24 }}>
        <OrdersStats />
      </Card>

      {/* Table */}
      <OrderTable orders={orders} loading={isLoading} />

      {/* Create Modal */}
      <Modal
        title="Create New Order"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={700}
        destroyOnClose
      >
        <OrderForm onSuccess={handleOrderCreated} />
      </Modal>
    </div>
  );
};

export default OrderList;
