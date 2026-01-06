/**
 * Quote List Page
 * Main page for managing quotes with form and table
 */

import { useState, useEffect } from 'react';
import { Typography, Space, Button, Modal } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation, useNavigate } from 'react-router-dom';
import { useQuotes } from '../../hooks/queries/useQuotes';
import QuoteForm from './QuoteForm';
import QuoteTable from './QuoteTable';
import QuotesStats from './QuotesStats';

const { Title } = Typography;

const QuoteList = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch quotes from API
  const { data, isLoading, refetch } = useQuotes();
  const quotes = data?.items || [];

  const [modalOpen, setModalOpen] = useState(false);

  // Open modal if /new route is accessed
  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleQuoteCreated = () => {
    // Refetch to get the updated list
    refetch();
    // Close modal after successful creation
    setModalOpen(false);
    // Navigate back to list route
    if (isNewRoute) {
      navigate('/quotes');
    }
  };

  const handleRefresh = () => {
    refetch();
  };

  const handleModalOpen = () => {
    setModalOpen(true);
    navigate('/quotes/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/quotes');
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
          Quotes
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
            New Quote
          </Button>
        </Space>
      </Space>

      {/* Mini Dashboard */}
      <div style={{ marginBottom: 24 }}>
        <QuotesStats />
      </div>

      <QuoteTable quotes={quotes} loading={isLoading} />

      {!isLoading && quotes.length === 0 && (
        <div
          style={{
            textAlign: 'center',
            padding: '50px',
            color: '#8c8c8c',
          }}
        >
          <p>No quotes created yet. Click "New Quote" to create one.</p>
        </div>
      )}

      {/* New Quote Modal */}
      <Modal
        title="New Quote"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={800}
        destroyOnClose
      >
        <QuoteForm onSuccess={handleQuoteCreated} />
      </Modal>
    </div>
  );
};

export default QuoteList;
