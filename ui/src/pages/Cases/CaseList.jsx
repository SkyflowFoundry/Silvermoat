/**
 * Case List Page
 * Main page for managing cases
 */

import { useState } from 'react';
import { Typography, Row, Col, Space, Button } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation } from 'react-router-dom';
import { useCases } from '../../hooks/queries/useCases';
import CaseForm from './CaseForm';
import CaseTable from './CaseTable';

const { Title } = Typography;

const CaseList = () => {
  const location = useLocation();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch cases from API
  const { data, isLoading, refetch } = useCases();
  const cases = data?.items || [];

  const [showForm, setShowForm] = useState(isNewRoute);

  const handleCaseCreated = () => {
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
          Cases
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
            {showForm ? 'Hide Form' : 'New Case'}
          </Button>
        </Space>
      </Space>

      <Row gutter={[16, 16]}>
        {showForm && (
          <Col xs={24} md={24} lg={8}>
            <CaseForm onSuccess={handleCaseCreated} />
          </Col>
        )}
        <Col xs={24} md={24} lg={showForm ? 16 : 24}>
          <CaseTable cases={cases} loading={isLoading} />
        </Col>
      </Row>

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
    </div>
  );
};

export default CaseList;
