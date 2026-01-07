/**
 * Inventory List Page
 * Main page for inventory management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, InboxOutlined } from '@ant-design/icons';
import { useInventory } from '../../hooks/queries/useInventory';
import InventoryTable from './InventoryTable';
import InventoryStats from './InventoryStats';
import InventoryForm from './InventoryForm';

const { Title } = Typography;

const InventoryList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = useInventory();
  const inventory = data?.items || [];

  // Check if we're on the /new route
  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/inventory/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/inventory');
    }
  };

  const handleInventoryCreated = () => {
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
          <InboxOutlined style={{ fontSize: 24, color: '#531dab' }} />
          <Title level={2} style={{ margin: 0 }}>
            Inventory
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
            New Inventory Item
          </Button>
        </Space>
      </Space>

      {/* Statistics */}
      <Card style={{ marginBottom: 24 }}>
        <InventoryStats />
      </Card>

      {/* Table */}
      <InventoryTable inventory={inventory} loading={isLoading} />

      {/* Create Modal */}
      <Modal
        title="Create New Inventory Item"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={600}
        destroyOnClose
      >
        <InventoryForm onSuccess={handleInventoryCreated} />
      </Modal>
    </div>
  );
};

export default InventoryList;
