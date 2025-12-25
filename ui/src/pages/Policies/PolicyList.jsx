/**
 * Policy List Page
 * Main page for managing policies
 */

import { useState } from 'react';
import { Typography, Row, Col, Space, Button } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation } from 'react-router-dom';
import { usePolicies } from '../../hooks/queries/usePolicies';
import PolicyForm from './PolicyForm';
import PolicyTable from './PolicyTable';
import PoliciesStats from './PoliciesStats';

const { Title } = Typography;

const PolicyList = () => {
  const location = useLocation();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch policies from API
  const { data, isLoading, refetch } = usePolicies();
  const policies = data?.items || [];

  const [showForm, setShowForm] = useState(isNewRoute);

  const handlePolicyCreated = () => {
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
          Policies
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
            {showForm ? 'Hide Form' : 'New Policy'}
          </Button>
        </Space>
      </Space>

      {/* Mini Dashboard */}
      <div style={{ marginBottom: 24 }}>
        <PoliciesStats />
      </div>

      <Row gutter={[16, 16]}>
        {showForm && (
          <Col xs={24} md={24} lg={8}>
            <PolicyForm onSuccess={handlePolicyCreated} />
          </Col>
        )}
        <Col xs={24} md={24} lg={showForm ? 16 : 24}>
          <PolicyTable policies={policies} loading={isLoading} />
        </Col>
      </Row>

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
    </div>
  );
};

export default PolicyList;
