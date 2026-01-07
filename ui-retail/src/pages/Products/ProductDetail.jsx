/**
 * Product Detail Page
 * Displays detailed information about a specific product
 */

import { Card, Descriptions, Button, Space, Typography, Spin, Alert } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { useProduct } from '../../hooks/queries/useProduct';
import { formatTimestamp, formatCurrency } from '../../utils/formatters';

const { Title, Paragraph } = Typography;

const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: product, isLoading, error } = useProduct(id);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading product details..." />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error Loading Product"
        description={error.message || 'Failed to load product details'}
        type="error"
        showIcon
      />
    );
  }

  if (!product) {
    return (
      <Alert
        message="Product Not Found"
        description="The requested product could not be found."
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
          onClick={() => navigate('/products')}
        >
          Back to Products
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Product Details
            </Title>
          </Space>
        }
      >
        <Descriptions
          bordered
          column={{ xs: 1, sm: 1, md: 2, lg: 2, xl: 2 }}
          size="middle"
        >
          <Descriptions.Item label="Product ID" span={2}>
            {product.id}
          </Descriptions.Item>
          <Descriptions.Item label="Name" span={2}>
            <strong>{product.data?.name || '-'}</strong>
          </Descriptions.Item>
          <Descriptions.Item label="SKU">
            {product.data?.sku || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Category">
            {product.data?.category || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Price">
            {product.data?.price ? formatCurrency(product.data.price * 100) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Stock Level">
            {product.data?.stockLevel !== undefined ? product.data.stockLevel : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Description" span={2}>
            {product.data?.description ? (
              <Paragraph style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
                {product.data.description}
              </Paragraph>
            ) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(product.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Status">
            {product.status || 'ACTIVE'}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {/* Raw Data (for debugging) */}
      <Card title="Raw Data" style={{ marginTop: 24 }} size="small">
        <pre style={{ maxHeight: '400px', overflow: 'auto', fontSize: '12px' }}>
          {JSON.stringify(product, null, 2)}
        </pre>
      </Card>
    </div>
  );
};

export default ProductDetail;
