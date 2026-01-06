/**
 * Claim List Page
 * Main page for managing claims
 */

import { useState, useEffect } from 'react';
import { Typography, Space, Button, Modal } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation, useNavigate } from 'react-router-dom';
import { useClaims } from '../../hooks/queries/useClaims';
import ClaimForm from './ClaimForm';
import ClaimTable from './ClaimTable';
import ClaimsStats from './ClaimsStats';

const { Title } = Typography;

const ClaimList = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch claims from API
  const { data, isLoading, refetch } = useClaims();
  const claims = data?.items || [];

  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleClaimCreated = () => {
    refetch();
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/claims');
    }
  };

  const handleRefresh = () => {
    refetch();
  };

  const handleModalOpen = () => {
    setModalOpen(true);
    navigate('/claims/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/claims');
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
          Claims
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
            New Claim
          </Button>
        </Space>
      </Space>

      {/* Mini Dashboard */}
      <div style={{ marginBottom: 24 }}>
        <ClaimsStats />
      </div>

      <ClaimTable claims={claims} loading={isLoading} />

      {!isLoading && claims.length === 0 && (
        <div
          style={{
            textAlign: 'center',
            padding: '50px',
            color: '#8c8c8c',
          }}
        >
          <p>No claims created yet. Click "New Claim" to create one.</p>
        </div>
      )}

      {/* New Claim Modal */}
      <Modal
        title="New Claim"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={800}
        destroyOnClose
      >
        <ClaimForm onSuccess={handleClaimCreated} />
      </Modal>
    </div>
  );
};

export default ClaimList;
