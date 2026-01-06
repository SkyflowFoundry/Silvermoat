/**
 * Policy List Page
 * Main page for managing policies
 */

import { useState, useEffect } from 'react';
import { Typography, Space, Button, Modal } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation, useNavigate } from 'react-router-dom';
import { usePolicies } from '../../hooks/queries/usePolicies';
import PolicyForm from './PolicyForm';
import PolicyTable from './PolicyTable';
import PoliciesStats from './PoliciesStats';

const { Title } = Typography;

const PolicyList = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch policies from API
  const { data, isLoading, refetch } = usePolicies();
  const policies = data?.items || [];

  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handlePolicyCreated = () => {
    refetch();
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/policies');
    }
  };

  const handleRefresh = () => {
    refetch();
  };

  const handleModalOpen = () => {
    setModalOpen(true);
    navigate('/policies/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/policies');
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
          Policies
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
            New Policy
          </Button>
        </Space>
      </Space>

      {/* Mini Dashboard */}
      <div style={{ marginBottom: 24 }}>
        <PoliciesStats />
      </div>

      <PolicyTable policies={policies} loading={isLoading} />

      {!isLoading && policies.length === 0 && (
        <div
          style={{
            textAlign: 'center',
            padding: '50px',
            color: '#8c8c8c',
          }}
        >
          <p>No policies created yet. Click "New Policy" to create one.</p>
        </div>
      )}

      {/* New Policy Modal */}
      <Modal
        title="New Policy"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={800}
        destroyOnClose
      >
        <PolicyForm onSuccess={handlePolicyCreated} />
      </Modal>
    </div>
  );
};

export default PolicyList;
