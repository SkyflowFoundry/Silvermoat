/**
 * Provider List Page
 * Main page for provider management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, TeamOutlined } from '@ant-design/icons';
import { useProviders } from '../../hooks/queries/useProviders';
import ProviderTable from './ProviderTable';
import ProvidersStats from './ProvidersStats';
import ProviderForm from './ProviderForm';

const { Title } = Typography;

const ProviderList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = useProviders();
  const providers = data?.items || [];

  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/providers/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/providers');
    }
  };

  const handleProviderCreated = () => {
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
          <TeamOutlined style={{ fontSize: 24, color: '#52c41a' }} />
          <Title level={2} style={{ margin: 0 }}>
            Providers
          </Title>
        </Space>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={handleRefresh} loading={isLoading}>
            Refresh
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleModalOpen}>
            New Provider
          </Button>
        </Space>
      </Space>

      <Card style={{ marginBottom: 24 }}>
        <ProvidersStats />
      </Card>

      <ProviderTable providers={providers} loading={isLoading} />

      <Modal
        title="Create New Provider"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={700}
        destroyOnClose
      >
        <ProviderForm onSuccess={handleProviderCreated} />
      </Modal>
    </div>
  );
};

export default ProviderList;
