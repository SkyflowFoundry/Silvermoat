/**
 * Case List Page
 * Main page for case management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, CustomerServiceOutlined } from '@ant-design/icons';
import { useCases } from '../../hooks/queries/useCases';
import CaseTable from './CaseTable';
import CasesStats from './CasesStats';
import CaseForm from './CaseForm';

const { Title } = Typography;

const CaseList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = useCases();
  const cases = data?.items || [];

  // Check if we're on the /new route
  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/cases/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/cases');
    }
  };

  const handleCaseCreated = () => {
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
          <CustomerServiceOutlined style={{ fontSize: 24, color: '#531dab' }} />
          <Title level={2} style={{ margin: 0 }}>
            Cases
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
            New Case
          </Button>
        </Space>
      </Space>

      {/* Statistics */}
      <Card style={{ marginBottom: 24 }}>
        <CasesStats />
      </Card>

      {/* Table */}
      <CaseTable cases={cases} loading={isLoading} />

      {/* Create Modal */}
      <Modal
        title="Create New Case"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={700}
        destroyOnClose
      >
        <CaseForm onSuccess={handleCaseCreated} />
      </Modal>
    </div>
  );
};

export default CaseList;
