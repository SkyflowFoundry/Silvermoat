/**
 * Customer List Page
 * Main page for customer management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, UserOutlined } from '@ant-design/icons';
import { useCustomers } from '../../hooks/queries/useCustomers';
import CustomerTable from './CustomerTable';
import CustomersStats from './CustomersStats';
import CustomerForm from './CustomerForm';

const { Title } = Typography;

const CustomerList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = useCustomers();
  const customers = data?.items || [];

  // Check if we're on the /new route
  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/customers/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/customers');
    }
  };

  const handleCustomerCreated = () => {
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
          <UserOutlined style={{ fontSize: 24, color: '#52c41a' }} />
          <Title level={2} style={{ margin: 0 }}>
            Customers
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
            New Customer
          </Button>
        </Space>
      </Space>

      {/* Statistics */}
      <Card style={{ marginBottom: 24 }}>
        <CustomersStats />
      </Card>

      {/* Table */}
      <CustomerTable customers={customers} loading={isLoading} />

      {/* Create Modal */}
      <Modal
        title="Create New Customer"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={700}
        destroyOnClose
      >
        <CustomerForm onSuccess={handleCustomerCreated} />
      </Modal>
    </div>
  );
};

export default CustomerList;
