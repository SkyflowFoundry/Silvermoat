/**
 * Products Statistics Component
 * Mini-dashboard showing product-specific metrics
 */

import { Row, Col, Card, Statistic, Space, Typography, Spin } from 'antd';
import { ShoppingOutlined, InboxOutlined, DollarOutlined, AppstoreOutlined } from '@ant-design/icons';
import { useProducts } from '../../hooks/queries/useProducts';
import { formatCurrency } from '../../utils/formatters';

const { Text } = Typography;

const ProductsStats = () => {
  const { data: productsData, isLoading } = useProducts();
  const products = productsData?.items || [];

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '24px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Calculate statistics
  const totalProducts = products.length;
  const totalStock = products.reduce((sum, p) => sum + (p.data?.stockLevel || 0), 0);
  const avgPrice = totalProducts > 0
    ? products.reduce((sum, p) => sum + (p.data?.price || 0), 0) / totalProducts
    : 0;
  const lowStockCount = products.filter(p => (p.data?.stockLevel || 0) < 10).length;

  // Category distribution
  const categories = {};
  products.forEach(p => {
    const category = p.data?.category || 'Uncategorized';
    categories[category] = (categories[category] || 0) + 1;
  });
  const topCategory = Object.entries(categories).sort((a, b) => b[1] - a[1])[0];

  return (
    <div>
      <Row gutter={[16, 16]}>
        {/* Total Products */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title={<Text strong>Total Products</Text>}
              value={totalProducts}
              prefix={<ShoppingOutlined style={{ color: '#531dab' }} />}
              valueStyle={{ color: '#531dab' }}
            />
          </Card>
        </Col>

        {/* Total Stock */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title={<Text strong>Total Stock</Text>}
              value={totalStock}
              prefix={<InboxOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>

        {/* Average Price */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: '#fffbe6' }}>
            <Statistic
              title={<Text strong>Avg Price</Text>}
              value={avgPrice}
              prefix={<DollarOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
              precision={2}
            />
          </Card>
        </Col>

        {/* Low Stock Alert */}
        <Col xs={24} sm={12} lg={6}>
          <Card size="small" bordered={false} style={{ background: lowStockCount > 0 ? '#fff1f0' : '#f6ffed' }}>
            <Statistic
              title={<Text strong>Low Stock ({lowStockCount > 0 ? 'Alert' : 'Good'})</Text>}
              value={lowStockCount}
              valueStyle={{ color: lowStockCount > 0 ? '#ff4d4f' : '#52c41a' }}
              suffix={`/ ${totalProducts}`}
            />
          </Card>
        </Col>
      </Row>

      {/* Top Category */}
      {topCategory && (
        <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
          <Col xs={24}>
            <Card size="small" bordered={false}>
              <Space>
                <AppstoreOutlined style={{ fontSize: 20, color: '#531dab' }} />
                <div>
                  <Text type="secondary">Top Category</Text>
                  <div>
                    <Text strong style={{ fontSize: 16 }}>
                      {topCategory[0]} ({topCategory[1]} products)
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

export default ProductsStats;
