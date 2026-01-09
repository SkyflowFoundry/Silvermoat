/**
 * Account List Page
 * Main page for account management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, CalendarOutlined } from '@ant-design/icons';
import { useAccounts } from '../../hooks/queries/useAccounts';
import AccountTable from './AccountTable';
import AccountsStats from './AccountsStats';
import AccountForm from './AccountForm';

const { Title } = Typography;

const AccountList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = useAccounts();
  const accounts = data?.items || [];

  // Check if we're on the /new route
  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/accounts/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/accounts');
    }
  };

  const handleAccountCreated = () => {
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
          <CalendarOutlined style={{ fontSize: 24, color: '#13c2c2' }} />
          <Title level={2} style={{ margin: 0 }}>
            Accounts
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
            New Account
          </Button>
        </Space>
      </Space>

      {/* Statistics */}
      <Card style={{ marginBottom: 24 }}>
        <AccountsStats />
      </Card>

      {/* Table */}
      <AccountTable accounts={accounts} loading={isLoading} />

      {/* Create Modal */}
      <Modal
        title="Create New Account"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={700}
        destroyOnClose
      >
        <AccountForm onSuccess={handleAccountCreated} />
      </Modal>
    </div>
  );
};

export default AccountList;
