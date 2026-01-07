/**
 * Inventory Detail Page
 * Displays detailed information about a specific inventory item
 */

import { Card, Descriptions, Button, Space, Typography, Spin, Alert } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { useInventoryItem } from '../../hooks/queries/useInventoryItem';
import { formatTimestamp } from '../../utils/formatters';
import dayjs from 'dayjs';

const { Title, Paragraph } = Typography;

const InventoryDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: item, isLoading, error } = useInventoryItem(id);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading inventory details..." />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error Loading Inventory Item"
        description={error.message || 'Failed to load inventory details'}
        type="error"
        showIcon
      />
    );
  }

  if (!item) {
    return (
      <Alert
        message="Inventory Item Not Found"
        description="The requested inventory item could not be found."
        type="warning"
        showIcon
      />
    );
  }

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/inventory')}
        >
          Back to Inventory
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Inventory Item Details
            </Title>
          </Space>
        }
      >
        <Descriptions
          bordered
          column={{ xs: 1, sm: 1, md: 2, lg: 2, xl: 2 }}
          size="middle"
        >
          <Descriptions.Item label="Item ID" span={2}>
            {item.id}
          </Descriptions.Item>
          <Descriptions.Item label="Product ID" span={2}>
            {item.data?.productId || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Warehouse">
            {item.data?.warehouse || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Quantity">
            <strong>{item.data?.quantity !== undefined ? item.data.quantity.toLocaleString() : '-'}</strong>
          </Descriptions.Item>
          <Descriptions.Item label="Reorder Level">
            {item.data?.reorderLevel !== undefined ? item.data.reorderLevel : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Last Restocked">
            {item.data?.lastRestocked
              ? dayjs(item.data.lastRestocked).format('MMM D, YYYY')
              : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(item.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Status">
            {item.status || 'ACTIVE'}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {/* Raw Data (for debugging) */}
      <Card title="Raw Data" style={{ marginTop: 24 }} size="small">
        <pre style={{ maxHeight: '400px', overflow: 'auto', fontSize: '12px' }}>
          {JSON.stringify(item, null, 2)}
        </pre>
      </Card>
    </div>
  );
};

export default InventoryDetail;
