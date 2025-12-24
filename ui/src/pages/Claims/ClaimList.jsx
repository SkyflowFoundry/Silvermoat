/**
 * Claim List Page
 * Main page for managing claims
 */

import { useState } from 'react';
import { Typography, Row, Col, Space, Button } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation } from 'react-router-dom';
import { useClaims } from '../../hooks/queries/useClaims';
import ClaimForm from './ClaimForm';
import ClaimTable from './ClaimTable';

const { Title } = Typography;

const ClaimList = () => {
  const location = useLocation();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch claims from API
  const { data, isLoading, refetch } = useClaims();
  const claims = data?.items || [];

  const [showForm, setShowForm] = useState(isNewRoute);

  const handleClaimCreated = () => {
    // Refetch to get the updated list
    refetch();
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
          Claims
        </Title>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={handleRefresh}>
            Refresh
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? 'Hide Form' : 'New Claim'}
          </Button>
        </Space>
      </Space>

      <Row gutter={[16, 16]}>
        {showForm && (
          <Col xs={24} md={24} lg={8}>
            <ClaimForm onSuccess={handleClaimCreated} />
          </Col>
        )}
        <Col xs={24} md={24} lg={showForm ? 16 : 24}>
          <ClaimTable claims={claims} loading={isLoading} />
        </Col>
      </Row>

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
    </div>
  );
};

export default ClaimList;
