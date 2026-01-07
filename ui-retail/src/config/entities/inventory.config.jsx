/**
 * Inventory Entity Configuration
 * Defines table columns, form fields, and validation for inventory items
 */

import { Input, InputNumber, DatePicker, Select, Tag } from 'antd';
import { InboxOutlined, ShopOutlined, NumberOutlined, CalendarOutlined } from '@ant-design/icons';
import { formatTimestamp } from '../../utils/formatters';
import dayjs from 'dayjs';

// Table configuration
export const inventoryTableConfig = {
  columns: [
    {
      title: 'Product ID',
      dataIndex: ['data', 'productId'],
      key: 'productId',
      width: 200,
      ellipsis: true,
    },
    {
      title: 'Warehouse',
      dataIndex: ['data', 'warehouse'],
      key: 'warehouse',
      width: 150,
      render: (warehouse) => (
        <Tag color="blue" icon={<ShopOutlined />}>
          {warehouse || '-'}
        </Tag>
      ),
    },
    {
      title: 'Quantity',
      dataIndex: ['data', 'quantity'],
      key: 'quantity',
      width: 120,
      align: 'right',
      render: (quantity) => {
        const qty = quantity || 0;
        const color = qty === 0 ? 'red' : qty < 50 ? 'orange' : 'green';
        return <Tag color={color}>{qty.toLocaleString()}</Tag>;
      },
    },
    {
      title: 'Reorder Level',
      dataIndex: ['data', 'reorderLevel'],
      key: 'reorderLevel',
      width: 130,
      align: 'right',
      render: (level) => level || '-',
    },
    {
      title: 'Last Restocked',
      dataIndex: ['data', 'lastRestocked'],
      key: 'lastRestocked',
      width: 150,
      render: (date) => (date ? dayjs(date).format('MMM D, YYYY') : '-'),
    },
    {
      title: 'Created',
      dataIndex: 'createdAt',
      key: 'createdAt',
      width: 150,
      render: (timestamp) => formatTimestamp(timestamp),
    },
  ],
  rowKey: 'id',
  scroll: { x: 1000 },
};

// Mobile fields for responsive table
export const inventoryMobileFields = [
  {
    label: 'Product ID',
    key: 'productId',
    render: (item) => item.data?.productId || '-',
  },
  {
    label: 'Warehouse',
    key: 'warehouse',
    render: (item) => (
      <Tag color="blue" icon={<ShopOutlined />}>
        {item.data?.warehouse || '-'}
      </Tag>
    ),
  },
  {
    label: 'Quantity',
    key: 'quantity',
    render: (item) => {
      const qty = item.data?.quantity || 0;
      const color = qty === 0 ? 'red' : qty < 50 ? 'orange' : 'green';
      return <Tag color={color}>{qty.toLocaleString()}</Tag>;
    },
  },
  {
    label: 'Reorder Level',
    key: 'reorderLevel',
    render: (item) => item.data?.reorderLevel || '-',
  },
  {
    label: 'Last Restocked',
    key: 'lastRestocked',
    render: (item) =>
      item.data?.lastRestocked
        ? dayjs(item.data.lastRestocked).format('MMM D, YYYY')
        : '-',
  },
];

// Form configuration
export const inventoryFormConfig = {
  fields: [
    {
      name: 'productId',
      label: 'Product',
      component: <Select
        showSearch
        placeholder="Select a product"
        optionFilterProp="label"
        filterSort={(optionA, optionB) =>
          (optionA?.label ?? '').toLowerCase().localeCompare((optionB?.label ?? '').toLowerCase())
        }
      />,
      rules: [
        { required: true, message: 'Please select a product' },
      ],
      // Options will be dynamically populated from useProducts hook
      getOptions: (products) =>
        products?.map(p => ({
          value: p.id,
          label: `${p.data?.name || 'Unknown'} (${p.data?.sku || p.id})`,
        })) || [],
    },
    {
      name: 'warehouse',
      label: 'Warehouse',
      component: <Input
        prefix={<ShopOutlined />}
        placeholder="e.g., NYC-01, LA-02, etc."
        maxLength={50}
      />,
      rules: [
        { required: true, message: 'Please enter the warehouse location' },
        { min: 2, max: 50, message: 'Warehouse must be 2-50 characters' },
      ],
    },
    {
      name: 'quantity',
      label: 'Quantity',
      component: <InputNumber
        prefix={<NumberOutlined />}
        placeholder="0"
        min={0}
        step={1}
        precision={0}
        style={{ width: '100%' }}
      />,
      rules: [
        { required: true, message: 'Please enter the quantity' },
        { type: 'number', min: 0, message: 'Quantity must be non-negative' },
      ],
    },
    {
      name: 'reorderLevel',
      label: 'Reorder Level',
      component: <InputNumber
        prefix={<NumberOutlined />}
        placeholder="e.g., 10"
        min={0}
        step={1}
        precision={0}
        style={{ width: '100%' }}
      />,
      rules: [
        { type: 'number', min: 0, message: 'Reorder level must be non-negative' },
      ],
      help: 'Minimum quantity before reordering',
    },
    {
      name: 'lastRestocked',
      label: 'Last Restocked',
      component: <DatePicker
        style={{ width: '100%' }}
        format="YYYY-MM-DD"
      />,
      rules: [],
      help: 'Date when inventory was last restocked',
      // Transform from DatePicker (dayjs) to ISO string
      transformer: (value) => value ? value.format('YYYY-MM-DD') : null,
    },
  ],
  layout: 'vertical',
  requiredMark: true,
};

export default {
  inventoryTableConfig,
  inventoryMobileFields,
  inventoryFormConfig,
};
