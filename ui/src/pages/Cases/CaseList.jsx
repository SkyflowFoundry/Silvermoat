/**
 * Case List Page
 * Main page for managing cases
 */

import { useState, useEffect } from 'react';
import { Typography, Space, Button, Modal } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation, useNavigate } from 'react-router-dom';
import { useCases } from '../../hooks/queries/useCases';
import CaseForm from './CaseForm';
import CaseTable from './CaseTable';
import CasesStats from './CasesStats';

const { Title } = Typography;

const CaseList = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch cases from API
  const { data, isLoading, refetch } = useCases();
  const cases = data?.items || [];

  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleCaseCreated = () => {
    refetch();
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/cases');
    }
  };

  const handleRefresh = () => {
    refetch();
  };

  const handleModalOpen = () => {
    setModalOpen(true);
    navigate('/cases/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/cases');
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
          Cases
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
            New Case
          </Button>
        </Space>
      </Space>

      {/* Mini Dashboard */}
      <div style={{ marginBottom: 24 }}>
        <CasesStats />
      </div>

      <CaseTable cases={cases} loading={isLoading} />

      {!isLoading && cases.length === 0 && (
        <div
          style={{
            textAlign: 'center',
            padding: '50px',
            color: '#8c8c8c',
          }}
        >
          <p>No cases created yet. Click "New Case" to create one.</p>
        </div>
      )}

      {/* New Case Modal */}
      <Modal
        title="New Case"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={800}
        destroyOnClose
      >
        <CaseForm onSuccess={handleCaseCreated} />
      </Modal>
    </div>
  );
};

export default CaseList;
