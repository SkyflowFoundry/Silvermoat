/**
 * Product List Page
 * Main page for managing products with form and table
 */

import { useState, useEffect } from 'react';
import { Typography, Space, Button, Modal } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useLocation, useNavigate } from 'react-router-dom';
import { useProducts } from '../../hooks/queries/useProducts';
import ProductForm from './ProductForm';
import ProductTable from './ProductTable';
import ProductsStats from './ProductsStats';

const { Title } = Typography;

const ProductList = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isNewRoute = location.pathname.includes('/new');

  // Fetch products from API
  const { data, isLoading, refetch } = useProducts();
  const products = data?.items || [];

  const [modalOpen, setModalOpen] = useState(false);

  // Open modal if /new route is accessed
  useEffect(() => {
    if (isNewRoute) {
      setModalOpen(true);
    }
  }, [isNewRoute]);

  const handleProductCreated = () => {
    // Refetch to get the updated list
    refetch();
    // Close modal after successful creation
    setModalOpen(false);
    // Navigate back to list route
    if (isNewRoute) {
      navigate('/products');
    }
  };

  const handleRefresh = () => {
    refetch();
  };

  const handleModalOpen = () => {
    setModalOpen(true);
    navigate('/products/new');
  };

  const handleModalClose = () => {
    setModalOpen(false);
    if (isNewRoute) {
      navigate('/products');
    }
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
          Products
        </Title>
        <Space>
          <Button
            icon={<ReloadOutlined />}
            onClick={handleRefresh}
          >
            Refresh
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleModalOpen}
          >
            New Product
          </Button>
        </Space>
      </Space>

      {/* Mini Dashboard */}
      <div style={{ marginBottom: 24 }}>
        <ProductsStats />
      </div>

      <ProductTable products={products} loading={isLoading} />

      {!isLoading && products.length === 0 && (
        <div
          style={{
            textAlign: 'center',
            padding: '50px',
            color: '#8c8c8c',
          }}
        >
          <p>No products created yet. Click "New Product" to create one.</p>
        </div>
      )}

      {/* New Product Modal */}
      <Modal
        title="New Product"
        open={modalOpen}
        onCancel={handleModalClose}
        footer={null}
        width={800}
        destroyOnClose
      >
        <ProductForm onSuccess={handleProductCreated} />
      </Modal>
    </div>
  );
};

export default ProductList;
