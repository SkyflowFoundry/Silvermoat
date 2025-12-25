/**
 * Payment List Page
 */

import { useState } from 'react';
import { Typography, Row, Col, Space, Button } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation } from 'react-router-dom';
import { usePayments } from '../../hooks/queries/usePayments';
import PaymentForm from './PaymentForm';
import PaymentTable from './PaymentTable';
import PaymentsStats from './PaymentsStats';

const { Title } = Typography;

const PaymentList = () => {
  const location = useLocation();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch payments from API
  const { data, isLoading, refetch } = usePayments();
  const payments = data?.items || [];

  const [showForm, setShowForm] = useState(isNewRoute);

  const handlePaymentCreated = () => {
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
          Payments
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
            {showForm ? 'Hide Form' : 'New Payment'}
          </Button>
        </Space>
      </Space>

      {/* Mini Dashboard */}
      <div style={{ marginBottom: 24 }}>
        <PaymentsStats />
      </div>

      <Row gutter={[16, 16]}>
        {showForm && (
          <Col xs={24} md={24} lg={8}>
            <PaymentForm onSuccess={handlePaymentCreated} />
          </Col>
        )}
        <Col xs={24} md={24} lg={showForm ? 16 : 24}>
          <PaymentTable payments={payments} loading={isLoading} />
        </Col>
      </Row>

      {!isLoading && payments.length === 0 && (
        <div
          style={{
            textAlign: 'center',
            padding: '50px',
            color: '#8c8c8c',
          }}
        >
          <p>No payments recorded yet. Click "New Payment" to record one.</p>
        </div>
      )}
    </div>
  );
};

export default PaymentList;
