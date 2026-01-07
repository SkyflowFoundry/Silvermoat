/**
 * Order Detail Page
 * Displays detailed information about a specific order with status update
 */

import { Card, Descriptions, Button, Space, Typography, Spin, Alert, Select, Table, Tag } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useOrder } from '../../hooks/queries/useOrder';
import { useUpdateOrderStatus } from '../../hooks/mutations/useUpdateOrderStatus';
import { formatTimestamp, formatCurrency } from '../../utils/formatters';
import { ORDER_STATUSES } from '../../config/constants';

const { Title, Paragraph } = Typography;

const OrderDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: order, isLoading, error } = useOrder(id);
  const updateStatusMutation = useUpdateOrderStatus();
  const [selectedStatus, setSelectedStatus] = useState(null);

  const handleStatusUpdate = () => {
    if (selectedStatus && id) {
      updateStatusMutation.mutate({ orderId: id, status: selectedStatus });
    }
  };

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading order details..." />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error Loading Order"
        description={error.message || 'Failed to load order details'}
        type="error"
        showIcon
      />
    );
  }

  if (!order) {
    return (
      <Alert
        message="Order Not Found"
        description="The requested order could not be found."
        type="warning"
        showIcon
      />
    );
  }

  const items = order.data?.items || [];
  const itemColumns = [
    {
      title: 'Product ID',
      dataIndex: 'productId',
      key: 'productId',
      ellipsis: true,
    },
    {
      title: 'Quantity',
      dataIndex: 'quantity',
      key: 'quantity',
      align: 'right',
    },
    {
      title: 'Price',
      dataIndex: 'price',
      key: 'price',
      align: 'right',
      render: (price) => (price !== undefined ? formatCurrency(price * 100) : '-'),
    },
    {
      title: 'Total',
      key: 'total',
      align: 'right',
      render: (_, record) => {
        const total = (record.price || 0) * (record.quantity || 0);
        return formatCurrency(total * 100);
      },
    },
  ];

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/orders')}
        >
          Back to Orders
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Order Details
            </Title>
          </Space>
        }
      >
        <Descriptions
          bordered
          column={{ xs: 1, sm: 1, md: 2, lg: 2, xl: 2 }}
          size="middle"
        >
          <Descriptions.Item label="Order ID" span={2}>
            {order.id}
          </Descriptions.Item>
          <Descriptions.Item label="Customer Email">
            {order.data?.customerEmail || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Customer Name">
            {order.data?.customerName || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Customer Phone">
            {order.data?.customerPhone || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={order.data?.status === 'DELIVERED' ? 'green' : 'blue'}>
              {order.data?.status || 'PENDING'}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Shipping Address" span={2}>
            {order.data?.shippingAddress ? (
              <Paragraph style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
                {order.data.shippingAddress}
              </Paragraph>
            ) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Total Amount">
            <strong>
              {order.data?.totalAmount !== undefined
                ? formatCurrency(order.data.totalAmount * 100)
                : '-'}
            </strong>
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(order.createdAt)}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {/* Order Items */}
      <Card title="Order Items" style={{ marginTop: 24 }} size="small">
        <Table
          dataSource={items}
          columns={itemColumns}
          rowKey={(record, index) => `${record.productId}-${index}`}
          pagination={false}
          size="small"
        />
      </Card>

      {/* Update Status */}
      <Card title="Update Order Status" style={{ marginTop: 24 }} size="small">
        <Space>
          <Select
            placeholder="Select new status"
            style={{ width: 200 }}
            value={selectedStatus}
            onChange={setSelectedStatus}
          >
            {Object.values(ORDER_STATUSES).map(status => (
              <Select.Option key={status} value={status}>
                {status}
              </Select.Option>
            ))}
          </Select>
          <Button
            type="primary"
            onClick={handleStatusUpdate}
            disabled={!selectedStatus}
            loading={updateStatusMutation.isPending}
          >
            Update Status
          </Button>
        </Space>
      </Card>

      {/* Raw Data (for debugging) */}
      <Card title="Raw Data" style={{ marginTop: 24 }} size="small">
        <pre style={{ maxHeight: '400px', overflow: 'auto', fontSize: '12px' }}>
          {JSON.stringify(order, null, 2)}
        </pre>
      </Card>
    </div>
  );
};

export default OrderDetail;
