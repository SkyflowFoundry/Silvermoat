/**
 * Inventory Statistics Component
 * Mini-dashboard showing inventory-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import { InboxOutlined, ShopOutlined, WarningOutlined, CheckCircleOutlined } from '@ant-design/icons';
import { useInventory } from '../../hooks/queries/useInventory';

const { Text } = Typography;

const InventoryStats = () => {
  const { data: inventoryData, isLoading } = useInventory();
  const inventory = inventoryData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalItems = inventory.length;
  const totalQuantity = inventory.reduce((sum, item) => sum + (item.data?.quantity || 0), 0);
  const outOfStock = inventory.filter(item => (item.data?.quantity || 0) === 0).length;
  const lowStock = inventory.filter(item => {
    const qty = item.data?.quantity || 0;
    const reorder = item.data?.reorderLevel || 0;
    return qty > 0 && qty < reorder;
  }).length;

  // Warehouse distribution
  const warehouses = {};
  inventory.forEach(item => {
    const warehouse = item.data?.warehouse || 'Unknown';
    warehouses[warehouse] = (warehouses[warehouse] || 0) + 1;
  });
  const topWarehouse = Object.entries(warehouses).sort((a, b) => b[1] - a[1])[0];
  const warehouseCount = Object.keys(warehouses).length;

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Items */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Total Items</Text>}
              value={totalItems}
              prefix={<InboxOutlined style={{ color: '#531dab' }} />}
              valueStyle={{ color: '#531dab' }}
            />
          </Card>
        </Col>

        {/* Total Quantity */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Total Quantity</Text>}
              value={totalQuantity}
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>

        {/* Out of Stock */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: outOfStock > 0 ? '#fff1f0' : '#f6ffed' }}>
            <Statistic
              title={<Text strong>Out of Stock</Text>}
              value={outOfStock}
              valueStyle={{ color: outOfStock > 0 ? '#ff4d4f' : '#52c41a' }}
              suffix={`/ ${totalItems}`}
            />
          </Card>
        </Col>

        {/* Low Stock Alert */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: lowStock > 0 ? '#fffbe6' : '#f6ffed' }}>
            <Statistic
              title={<Text strong>Low Stock</Text>}
              value={lowStock}
              prefix={lowStock > 0 ? <WarningOutlined style={{ color: '#faad14' }} /> : null}
              valueStyle={{ color: lowStock > 0 ? '#faad14' : '#52c41a' }}
              suffix={`/ ${totalItems}`}
            />
          </Card>
        </Col>
      </Row>

      {/* Warehouse Info */}
      {topWarehouse && (
        <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
          <Col xs={24}>
            <Card size="small" bordered={false}>
              <Space>
                <ShopOutlined style={{ fontSize: 20, color: '#531dab' }} />
                <div>
                  <Text type="secondary">Warehouses: {warehouseCount}</Text>
                  <div>
                    <Text strong style={{ fontSize: 16 }}>
                      Top: {topWarehouse[0]} ({topWarehouse[1]} items)
                    </Text>
                  </div>
                </div>
              </Space>
            </Card>
          </Col>
        </Row>
      )}
    </div>
  );
};

export default InventoryStats;
