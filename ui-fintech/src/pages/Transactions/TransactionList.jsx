/**
 * Transaction List Page
 * Main page for transaction management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, MedicineBoxOutlined } from '@ant-design/icons';
import { useTransactions } from '../../hooks/queries/useTransactions';
import TransactionTable from './TransactionTable';
import TransactionsStats from './TransactionsStats';
import TransactionForm from './TransactionForm';

const { Title } = Typography;

const TransactionList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = useTransactions();
  const transactions = data?.items || [];

  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/transactions/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/transactions');
    }
  };

  const handleTransactionCreated = () => {
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
            Transactions
          </Title>
        </Space>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={handleRefresh} loading={isLoading}>
            Refresh
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleModalOpen}>
            New Transaction
          </Button>
        </Space>
      </Space>

      <Card style={{ marginBottom: 24 }}>
        <TransactionsStats />
      </Card>

      <TransactionTable transactions={transactions} loading={isLoading} />

      <Modal
        title="Create New Transaction"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={700}
        destroyOnClose
      >
        <TransactionForm onSuccess={handleTransactionCreated} />
      </Modal>
    </div>
  );
};

export default TransactionList;
