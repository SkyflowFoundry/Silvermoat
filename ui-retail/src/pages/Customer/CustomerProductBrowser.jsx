/**
 * Customer Product Browser
 * Allows customers to browse the product catalog
 */

import { Card, Row, Col, Typography, Tag, Button, Empty, Spin, Input, Space } from 'antd';
import { ArrowLeftOutlined, SearchOutlined, ShoppingOutlined, DollarOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useProducts } from '../../hooks/queries/useProducts';
import { formatCurrency } from '../../utils/formatters';

const { Title, Text, Paragraph } = Typography;
const { Search } = Input;

const CustomerProductBrowser = () => {
  const navigate = useNavigate();
  const { data, isLoading } = useProducts();
  const products = data?.items || [];
  const [searchTerm, setSearchTerm] = useState('');

  // Filter products based on search
  const filteredProducts = products.filter((product) => {
    if (!searchTerm) return true;
    const term = searchTerm.toLowerCase();
    const name = (product.data?.name || '').toLowerCase();
    const category = (product.data?.category || '').toLowerCase();
    const sku = (product.data?.sku || '').toLowerCase();
    return name.includes(term) || category.includes(term) || sku.includes(term);
  });

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '24px' }}>
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
            <Title level={2}>
              <ShoppingOutlined /> Browse Products
            </Title>
            <Text type="secondary">
              Explore our product catalog ({products.length} products available)
            </Text>
          </div>

          {/* Search */}
          <Search
            placeholder="Search products by name, category, or SKU..."
            size="large"
            prefix={<SearchOutlined />}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            allowClear
          />

          {/* Loading */}
          {isLoading && (
            <div style={{ textAlign: 'center', padding: '48px' }}>
              <Spin size="large" tip="Loading products..." />
            </div>
          )}

          {/* Empty State */}
          {!isLoading && filteredProducts.length === 0 && (
            <Empty description="No products found" style={{ margin: '48px 0' }} />
          )}

          {/* Product Grid */}
          {!isLoading && filteredProducts.length > 0 && (
            <Row gutter={[16, 16]}>
              {filteredProducts.map((product) => (
                <Col xs={24} sm={12} md={8} lg={6} key={product.id}>
                  <Card
                    hoverable
                    style={{ height: '100%' }}
                    cover={
                      <div
                        style={{
                          height: 180,
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <ShoppingOutlined style={{ fontSize: 64, color: '#fff', opacity: 0.5 }} />
                      </div>
                    }
                  >
                    <Space direction="vertical" size="small" style={{ width: '100%' }}>
                      <Title level={5} ellipsis style={{ margin: 0 }}>
                        {product.data?.name || 'Unknown Product'}
                      </Title>
                      <Tag color="blue">{product.data?.category || 'Uncategorized'}</Tag>
                      <Paragraph
                        ellipsis={{ rows: 2 }}
                        type="secondary"
                        style={{ fontSize: 12, margin: '8px 0' }}
                      >
                        {product.data?.description || 'No description available'}
                      </Paragraph>
                      <Space style={{ width: '100%', justifyContent: 'space-between' }}>
                        <Text strong style={{ fontSize: 18, color: '#531dab' }}>
                          <DollarOutlined />
                          {product.data?.price
                            ? formatCurrency(product.data.price * 100)
                            : '-'}
                        </Text>
                        <Tag color={product.data?.stockLevel > 0 ? 'green' : 'red'}>
                          {product.data?.stockLevel > 0 ? 'In Stock' : 'Out of Stock'}
                        </Tag>
                      </Space>
                    </Space>
                  </Card>
                </Col>
              ))}
            </Row>
          )}
        </Space>
      </Card>
    </div>
  );
};

export default CustomerProductBrowser;
