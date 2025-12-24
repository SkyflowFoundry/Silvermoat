/**
 * Quote List Page
 * Main page for managing quotes with form and table
 */

import { useState } from 'react';
import { Typography, Row, Col, Space, Button } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation } from 'react-router-dom';
import { useQuotes } from '../../hooks/queries/useQuotes';
import QuoteForm from './QuoteForm';
import QuoteTable from './QuoteTable';

const { Title } = Typography;

const QuoteList = () => {
  const location = useLocation();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch quotes from API
  const { data, isLoading, refetch } = useQuotes();
  const quotes = data?.items || [];

  const [showForm, setShowForm] = useState(isNewRoute);

  const handleQuoteCreated = () => {
    // Refetch to get the updated list
    refetch();
    // Hide form after successful creation
    setShowForm(false);
  };

  const handleRefresh = () => {
    refetch();
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
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? 'Hide Form' : 'New Quote'}
          </Button>
        </Space>
      </Space>

      <Row gutter={[24, 24]}>
        {showForm && (
          <Col xs={24} lg={8}>
            <QuoteForm onSuccess={handleQuoteCreated} />
          </Col>
        )}
        <Col xs={24} lg={showForm ? 16 : 24}>
          <QuoteTable quotes={quotes} loading={isLoading} />
        </Col>
      </Row>

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
    </div>
  );
};

export default QuoteList;
