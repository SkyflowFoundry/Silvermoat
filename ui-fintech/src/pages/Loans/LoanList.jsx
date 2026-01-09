/**
 * Loan List Page
 * Main page for loan management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, BankOutlined } from '@ant-design/icons';
import { useLoans } from '../../hooks/queries/useLoans';
import LoanTable from './LoanTable';
import LoansStats from './LoansStats';
import LoanForm from './LoanForm';

const { Title } = Typography;

const LoanList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = useLoans();
  const loans = data?.items || [];

  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/loans/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/loans');
    }
  };

  const handleLoanCreated = () => {
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
          <BankOutlined style={{ fontSize: 24, color: '#13c2c2' }} />
          <Title level={2} style={{ margin: 0 }}>
            Loans
          </Title>
        </Space>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={handleRefresh} loading={isLoading}>
            Refresh
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleModalOpen}>
            New Loan
          </Button>
        </Space>
      </Space>

      <Card style={{ marginBottom: 24 }}>
        <LoansStats />
      </Card>

      <LoanTable loans={loans} loading={isLoading} />

      <Modal
        title="Create New Loan"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={700}
        destroyOnClose
      >
        <LoanForm onSuccess={handleLoanCreated} />
      </Modal>
    </div>
  );
};

export default LoanList;
