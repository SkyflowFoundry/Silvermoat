/**
 * Customer Order Tracking
 * Allows customers to track orders by email
 */

import { useState } from 'react';
import { Card, Input, Button, Space, Typography, Table, Tag, Alert, Empty } from 'antd';
import { SearchOutlined, MailOutlined, ArrowLeftOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { getCustomerOrders } from '../../services/customers';
import { formatTimestamp, formatCurrency } from '../../utils/formatters';

const { Title, Text } = Typography;

const STATUS_COLORS = {
  PENDING: 'orange',
  PROCESSING: 'blue',
  SHIPPED: 'cyan',
  DELIVERED: 'green',
  CANCELLED: 'red',
};

const CustomerOrderTracking = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [orders, setOrders] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!email.trim()) {
      setError('Please enter your email address');
      return;
    }

    setLoading(true);
    setError(null);
    setOrders(null);

    try {
      const response = await getCustomerOrders(email.trim());
      setOrders(response.orders || []);
    } catch (err) {
      setError(err.message || 'Failed to fetch orders');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: 'Order ID',
      dataIndex: 'id',
      key: 'id',
      render: (id) => <Text code>{id.substring(0, 12)}...</Text>,
    },
    {
      title: 'Items',
      dataIndex: ['data', 'items'],
      key: 'items',
      render: (items) => items?.length || 0,
    },
    {
      title: 'Total',
      dataIndex: ['data', 'totalAmount'],
      key: 'totalAmount',
      render: (amount) => (amount !== undefined ? formatCurrency(amount * 100) : '-'),
    },
    {
      title: 'Status',
      dataIndex: ['data', 'status'],
      key: 'status',
      render: (status) => (
        <Tag color={STATUS_COLORS[status] || 'default'}>
          {status || 'PENDING'}
        </Tag>
      ),
    },
    {
      title: 'Created',
      dataIndex: 'createdAt',
      key: 'createdAt',
      render: (timestamp) => formatTimestamp(timestamp),
    },
  ];

  return (
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: '24px' }}>
      <Button
        icon={<ArrowLeftOutlined />}
        onClick={() => navigate('/customer/dashboard')}
        style={{ marginBottom: 16 }}
      >
        Back to Dashboard
      </Button>

      <Card>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <Title level={2}>Track Your Orders</Title>
            <Text type="secondary">
              Enter your email address to view your order history and track shipments
            </Text>
          </div>

          {/* Search Input */}
          <Space.Compact style={{ width: '100%' }}>
            <Input
              size="large"
              prefix={<MailOutlined />}
              placeholder="Enter your email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onPressEnter={handleSearch}
            />
            <Button
              type="primary"
              size="large"
              icon={<SearchOutlined />}
              loading={loading}
              onClick={handleSearch}
            >
              Search
            </Button>
          </Space.Compact>

          {/* Error */}
          {error && (
            <Alert
              message="Error"
              description={error}
              type="error"
              showIcon
              closable
              onClose={() => setError(null)}
            />
          )}

          {/* Results */}
          {orders !== null && (
            <>
              {orders.length === 0 ? (
                <Empty
                  description="No orders found for this email address"
                  style={{ marginTop: 24 }}
                />
              ) : (
                <>
                  <Alert
                    message={`Found ${orders.length} order${orders.length !== 1 ? 's' : ''}`}
                    type="success"
                    showIcon
                  />
                  <Table
                    dataSource={orders}
                    columns={columns}
                    rowKey="id"
                    pagination={false}
                    scroll={{ x: 800 }}
                  />
                </>
              )}
            </>
          )}
        </Space>
      </Card>
    </div>
  );
};

export default CustomerOrderTracking;
