/**
 * Order Entity Configuration
 * Defines table columns, form fields, and validation for orders
 */

import { Input, InputNumber, Select, Tag } from 'antd';
import { ShoppingCartOutlined, UserOutlined, MailOutlined, PhoneOutlined, EnvironmentOutlined } from '@ant-design/icons';
import { formatTimestamp, formatCurrency } from '../../utils/formatters';
import { ORDER_STATUSES } from '../constants';

const { TextArea } = Input;

// Status color mapping
const STATUS_COLORS = {
  PENDING: 'orange',
  PROCESSING: 'blue',
  SHIPPED: 'cyan',
  DELIVERED: 'green',
  CANCELLED: 'red',
};

// Table configuration
export const orderTableConfig = {
  columns: [
    {
      title: 'Customer Email',
      dataIndex: ['data', 'customerEmail'],
      key: 'customerEmail',
      width: 200,
      ellipsis: true,
    },
    {
      title: 'Customer Name',
      dataIndex: ['data', 'customerName'],
      key: 'customerName',
      width: 150,
      ellipsis: true,
      render: (name) => name || '-',
    },
    {
      title: 'Items',
      dataIndex: ['data', 'items'],
      key: 'items',
      width: 100,
      align: 'center',
      render: (items) => items?.length || 0,
    },
    {
      title: 'Total Amount',
      dataIndex: ['data', 'totalAmount'],
      key: 'totalAmount',
      width: 120,
      align: 'right',
      render: (amount) => (amount !== undefined ? formatCurrency(amount * 100) : '-'),
    },
    {
      title: 'Status',
      dataIndex: ['data', 'status'],
      key: 'status',
      width: 120,
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
      width: 150,
      render: (timestamp) => formatTimestamp(timestamp),
    },
  ],
  rowKey: 'id',
  scroll: { x: 1100 },
};

// Mobile fields for responsive table
export const orderMobileFields = [
  {
    label: 'Customer',
    key: 'customer',
    render: (item) => (
      <div>
        <div><strong>{item.data?.customerName || 'Unknown'}</strong></div>
        <div style={{ fontSize: 12, color: '#666' }}>{item.data?.customerEmail || '-'}</div>
      </div>
    ),
  },
  {
    label: 'Items',
    key: 'items',
    render: (item) => `${item.data?.items?.length || 0} items`,
  },
  {
    label: 'Total',
    key: 'totalAmount',
    render: (item) => {
      const amount = item.data?.totalAmount;
      return amount !== undefined ? formatCurrency(amount * 100) : '-';
    },
  },
  {
    label: 'Status',
    key: 'status',
    render: (item) => (
      <Tag color={STATUS_COLORS[item.data?.status] || 'default'}>
        {item.data?.status || 'PENDING'}
      </Tag>
    ),
  },
];

// Form configuration
export const orderFormConfig = {
  fields: [
    {
      name: 'customerEmail',
      label: 'Customer Email',
      component: <Input
        prefix={<MailOutlined />}
        placeholder="customer@example.com"
        type="email"
      />,
      rules: [
        { required: true, message: 'Please enter customer email' },
        { type: 'email', message: 'Please enter a valid email' },
      ],
      help: 'Customer will be created/updated automatically',
    },
    {
      name: 'customerName',
      label: 'Customer Name',
      component: <Input
        prefix={<UserOutlined />}
        placeholder="John Doe"
      />,
      rules: [
        { min: 2, max: 100, message: 'Name must be 2-100 characters' },
      ],
    },
    {
      name: 'customerPhone',
      label: 'Customer Phone',
      component: <Input
        prefix={<PhoneOutlined />}
        placeholder="(555) 123-4567"
      />,
      rules: [],
    },
    {
      name: 'shippingAddress',
      label: 'Shipping Address',
      component: <TextArea
        placeholder="123 Main St, City, State ZIP"
        rows={2}
      />,
      rules: [
        { min: 10, max: 500, message: 'Address must be 10-500 characters' },
      ],
    },
    {
      name: 'items',
      label: 'Order Items (JSON)',
      component: <TextArea
        placeholder={'[\n  {"productId": "prod-123", "quantity": 2, "price": 29.99}\n]'}
        rows={6}
      />,
      rules: [
        { required: true, message: 'Please enter order items' },
        {
          validator: (_, value) => {
            if (!value) return Promise.reject('Items are required');
            try {
              const items = JSON.parse(value);
              if (!Array.isArray(items)) {
                return Promise.reject('Items must be an array');
              }
              if (items.length === 0) {
                return Promise.reject('At least one item is required');
              }
              for (const item of items) {
                if (!item.productId || typeof item.quantity !== 'number' || typeof item.price !== 'number') {
                  return Promise.reject('Each item must have productId (string), quantity (number), and price (number)');
                }
              }
              return Promise.resolve();
            } catch (e) {
              return Promise.reject('Invalid JSON format');
            }
          },
        },
      ],
      help: 'Array of items: [{productId, quantity, price}, ...]',
      // Transform from JSON string to array
      transformer: (value) => {
        try {
          return JSON.parse(value);
        } catch {
          return [];
        }
      },
    },
    {
      name: 'status',
      label: 'Status',
      component: <Select placeholder="Select status">
        {Object.values(ORDER_STATUSES).map(status => (
          <Select.Option key={status} value={status}>
            {status}
          </Select.Option>
        ))}
      </Select>,
      rules: [],
      initialValue: 'PENDING',
    },
  ],
  layout: 'vertical',
  requiredMark: true,
};

export default {
  orderTableConfig,
  orderMobileFields,
  orderFormConfig,
};
