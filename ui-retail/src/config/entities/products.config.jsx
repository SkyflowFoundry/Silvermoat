/**
 * Product Entity Configuration
 * Defines table columns, form fields, and mobile layout for products
 */

import { Button, Input, InputNumber, Typography, Select } from 'antd';
import { ShoppingOutlined, BarcodeOutlined, DollarOutlined } from '@ant-design/icons';
import { formatTimestamp, formatCurrency } from '../../utils/formatters';
import { generateProductSampleData } from '../../utils/formSampleData';

const { Text } = Typography;
const { TextArea } = Input;

export const productTableConfig = {
  entityName: 'product',
  entityNamePlural: 'products',
  basePath: '/products',
  scrollX: 1000,

  columns: (navigate) => [
    {
      title: 'SKU',
      dataIndex: ['data', 'sku'],
      key: 'sku',
      width: 140,
      sorter: (a, b) => (a.data?.sku || '').localeCompare(b.data?.sku || ''),
      render: (sku, record) => (
        <Button
          type="link"
          onClick={() => navigate(`/products/${record.id}`)}
          style={{ padding: 0 }}
        >
          {sku || '-'}
        </Button>
      ),
    },
    {
      title: 'Name',
      dataIndex: ['data', 'name'],
      key: 'name',
      sorter: (a, b) => (a.data?.name || '').localeCompare(b.data?.name || ''),
      render: (name) => <Text strong>{name || '-'}</Text>,
    },
    {
      title: 'Category',
      dataIndex: ['data', 'category'],
      key: 'category',
      width: 150,
      sorter: (a, b) => (a.data?.category || '').localeCompare(b.data?.category || ''),
      render: (category) => category || '-',
    },
    {
      title: 'Price',
      dataIndex: ['data', 'price'],
      key: 'price',
      width: 120,
      sorter: (a, b) => (a.data?.price || 0) - (b.data?.price || 0),
      render: (price) => price ? formatCurrency(price * 100) : '-', // Convert to cents
    },
    {
      title: 'Stock Level',
      dataIndex: ['data', 'stockLevel'],
      key: 'stockLevel',
      width: 120,
      sorter: (a, b) => (a.data?.stockLevel || 0) - (b.data?.stockLevel || 0),
      render: (stockLevel) => stockLevel !== undefined ? stockLevel : '-',
    },
    {
      title: 'Created',
      dataIndex: 'createdAt',
      key: 'createdAt',
      width: 180,
      sorter: (a, b) => (a.createdAt || 0) - (b.createdAt || 0),
      render: (timestamp) => formatTimestamp(timestamp),
      defaultSortOrder: 'descend',
    },
  ],

  mobileFields: [
    {
      label: 'SKU',
      getValue: (product) => product.data?.sku || '-',
      render: (product) => (
        <Text strong style={{ fontSize: 13 }}>
          {product.data?.sku || '-'}
        </Text>
      ),
    },
    {
      label: 'Name',
      getValue: (product) => product.data?.name || '-',
      render: (product) => (
        <Text style={{ fontSize: 14 }}>{product.data?.name || '-'}</Text>
      ),
    },
    {
      layout: 'row',
      items: [
        {
          label: 'Price',
          getValue: (product) => product.data?.price ? formatCurrency(product.data.price * 100) : '-',
          flex: 1,
        },
        {
          label: 'Stock',
          getValue: (product) => product.data?.stockLevel !== undefined ? product.data.stockLevel : '-',
        },
      ],
    },
    {
      label: 'Category',
      getValue: (product) => product.data?.category || '-',
    },
  ],
};

export const productFormConfig = {
  title: 'Create New Product',
  submitButtonText: 'Create Product',
  submitButtonLoadingText: 'Creating Product...',
  onFillSampleData: generateProductSampleData,

  fields: [
    {
      name: 'name',
      label: 'Product Name',
      component: (
        <Input
          prefix={<ShoppingOutlined />}
          placeholder="Wireless Headphones"
          size="large"
        />
      ),
      rules: [
        { required: true, message: 'Please enter the product name' },
        { min: 2, message: 'Name must be at least 2 characters' },
        { max: 200, message: 'Name must not exceed 200 characters' },
      ],
    },
    {
      name: 'sku',
      label: 'SKU',
      component: (
        <Input
          prefix={<BarcodeOutlined />}
          placeholder="WH-1000XM4"
          size="large"
        />
      ),
      rules: [
        { required: true, message: 'Please enter a SKU' },
        { min: 2, message: 'SKU must be at least 2 characters' },
        { max: 50, message: 'SKU must not exceed 50 characters' },
      ],
    },
    {
      name: 'price',
      label: 'Price ($)',
      component: (
        <InputNumber
          prefix={<DollarOutlined />}
          placeholder="349.99"
          min={0}
          step={0.01}
          precision={2}
          style={{ width: '100%' }}
          size="large"
        />
      ),
      rules: [
        { required: true, message: 'Please enter a price' },
        { type: 'number', min: 0, message: 'Price must be positive' },
      ],
    },
    {
      name: 'category',
      label: 'Category',
      component: (
        <Select
          placeholder="Select a category"
          size="large"
          options={[
            { label: 'Electronics', value: 'Electronics' },
            { label: 'Clothing', value: 'Clothing' },
            { label: 'Home & Garden', value: 'Home & Garden' },
            { label: 'Sports & Outdoors', value: 'Sports & Outdoors' },
            { label: 'Books', value: 'Books' },
            { label: 'Toys & Games', value: 'Toys & Games' },
            { label: 'Other', value: 'Other' },
          ]}
        />
      ),
      rules: [],
    },
    {
      name: 'description',
      label: 'Description',
      component: (
        <TextArea
          placeholder="Product description..."
          rows={4}
          maxLength={1000}
          showCount
        />
      ),
      rules: [],
    },
    {
      name: 'stockLevel',
      label: 'Stock Level',
      component: (
        <InputNumber
          placeholder="100"
          min={0}
          step={1}
          style={{ width: '100%' }}
          size="large"
        />
      ),
      rules: [
        { type: 'number', min: 0, message: 'Stock level must be non-negative' },
      ],
    },
  ],
};
