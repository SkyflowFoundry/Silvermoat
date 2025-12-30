/**
 * Customer List Page
 * Main page for managing customers with form and table
 */

import { useState, useEffect } from 'react';
import { Typography, Space, Button, Modal } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation, useNavigate } from 'react-router-dom';
import { useCustomers } from '../../hooks/queries/useCustomers';
import CustomerForm from './CustomerForm';
import CustomerTable from './CustomerTable';

const { Title } = Typography;

const CustomerList = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch customers from API
  const { data, isLoading, refetch } = useCustomers();
  const customers = data?.items || [];

  const [modalOpen, setModalOpen] = useState(false);

  // Open modal if /new route is accessed
  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleCustomerCreated = () => {
    // Refetch to get the updated list
    refetch();
    // Close modal after successful creation
    setModalOpen(false);
    // Navigate back to list route
    if (isNewRoute) {
      navigate('/customers');
    }
  };

  const handleRefresh = () => {
    refetch();
  };

  const handleModalOpen = () => {
    setModalOpen(true);
    navigate('/customers/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/customers');
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
          Customers
        </Title>
        <Space>
          <Button
            icon={<ReloadOutlined />}
            onClick={handleRefresh}
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

      <CustomerTable customers={customers} loading={isLoading} />

      {!isLoading && customers.length === 0 && (
        <div
          style={{
            textAlign: 'center',
            padding: '50px',
            color: '#8c8c8c',
          }}
        >
          <p>No customers created yet. Click "New Customer" to create one.</p>
        </div>
      )}

      {/* New Customer Modal */}
      <Modal
        title="New Customer"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={800}
        destroyOnClose
      >
        <CustomerForm onSuccess={handleCustomerCreated} />
      </Modal>
    </div>
  );
};

export default CustomerList;
