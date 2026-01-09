/**
 * Card List Page
 * Main page for card management with creation modal
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Space, Button, Typography, Modal, Card } from 'antd';
import { PlusOutlined, ReloadOutlined, DollarOutlined } from '@ant-design/icons';
import { useCards } from '../../hooks/queries/useCards';
import CardTable from './CardTable';
import CardsStats from './CardsStats';
import CardForm from './CardForm';

const { Title } = Typography;

const CardList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [modalOpen, setModalOpen] = useState(false);

  const { data, isLoading, refetch } = useCards();
  const cards = data?.items || [];

  // Check if we're on the /new route
  const isNewRoute = location.pathname.endsWith('/new');

  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleModalOpen = () => {
    navigate('/cards/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/cards');
    }
  };

  const handleCardCreated = () => {
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
          <DollarOutlined style={{ fontSize: 24, color: '#531dab' }} />
          <Title level={2} style={{ margin: 0 }}>
            Cards
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
            New Card
          </Button>
        </Space>
      </Space>

      {/* Statistics */}
      <Card style={{ marginBottom: 24 }}>
        <CardsStats />
      </Card>

      {/* Table */}
      <CardTable cards={cards} loading={isLoading} />

      {/* Create Modal */}
      <Modal
        title="Create New Card"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={600}
        destroyOnClose
      >
        <CardForm onSuccess={handleCardCreated} />
      </Modal>
    </div>
  );
};

export default CardList;
