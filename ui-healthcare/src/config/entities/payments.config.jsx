/**
 * Payment Entity Configuration
 * Defines table columns, form fields, and validation for payments
 */

import { Input, InputNumber, Select, Tag } from 'antd';
import { DollarOutlined, CreditCardOutlined, SafetyCertificateOutlined, NumberOutlined } from '@ant-design/icons';
import { formatTimestamp, formatCurrency } from '../../utils/formatters';

// Payment method options
const PAYMENT_METHODS = ['CREDIT_CARD', 'ACH', 'CHECK'];

// Payment status options
const PAYMENT_STATUSES = ['PENDING', 'COMPLETED', 'FAILED'];

// Status color mapping
const STATUS_COLORS = {
  PENDING: 'orange',
  COMPLETED: 'green',
  FAILED: 'red',
};

// Table configuration
export const paymentTableConfig = {
  columns: [
    {
      title: 'Order ID',
      dataIndex: ['data', 'orderId'],
      key: 'orderId',
      width: 200,
      ellipsis: true,
    },
    {
      title: 'Amount',
      dataIndex: ['data', 'amount'],
      key: 'amount',
      width: 120,
      align: 'right',
      render: (amount) => (amount !== undefined ? formatCurrency(amount * 100) : '-'),
    },
    {
      title: 'Method',
      dataIndex: ['data', 'method'],
      key: 'method',
      width: 130,
      render: (method) => (
        <Tag color="blue" icon={<CreditCardOutlined />}>
          {method || '-'}
        </Tag>
      ),
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
      title: 'Transaction ID',
      dataIndex: ['data', 'transactionId'],
      key: 'transactionId',
      width: 150,
      ellipsis: true,
      render: (txId) => txId || '-',
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
export const paymentMobileFields = [
  {
    label: 'Order ID',
    key: 'orderId',
    render: (item) => item.data?.orderId || '-',
  },
  {
    label: 'Amount',
    key: 'amount',
    render: (item) => {
      const amount = item.data?.amount;
      return amount !== undefined ? formatCurrency(amount * 100) : '-';
    },
  },
  {
    label: 'Method',
    key: 'method',
    render: (item) => (
      <Tag color="blue" icon={<CreditCardOutlined />}>
        {item.data?.method || '-'}
      </Tag>
    ),
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
  {
    label: 'Transaction ID',
    key: 'transactionId',
    render: (item) => item.data?.transactionId || '-',
  },
];

// Form configuration
export const paymentFormConfig = {
  fields: [
    {
      name: 'orderId',
      label: 'Order',
      component: <Select
        showSearch
        placeholder="Select an order"
        optionFilterProp="label"
        filterSort={(optionA, optionB) =>
          (optionA?.label ?? '').toLowerCase().localeCompare((optionB?.label ?? '').toLowerCase())
        }
      />,
      rules: [
        { required: true, message: 'Please select an order' },
      ],
      // Options will be dynamically populated from useOrders hook
      getOptions: (orders) =>
        orders?.map(o => ({
          value: o.id,
          label: `${o.id.substring(0, 12)}... (${o.data?.customerEmail || 'Unknown'})`,
        })) || [],
    },
    {
      name: 'amount',
      label: 'Amount',
      component: <InputNumber
        prefix={<DollarOutlined />}
        placeholder="0.00"
        min={0}
        step={0.01}
        precision={2}
        style={{ width: '100%' }}
      />,
      rules: [
        { required: true, message: 'Please enter the payment amount' },
        { type: 'number', min: 0.01, message: 'Amount must be greater than 0' },
      ],
    },
    {
      name: 'method',
      label: 'Payment Method',
      component: <Select placeholder="Select payment method">
        {PAYMENT_METHODS.map(method => (
          <Select.Option key={method} value={method}>
            {method}
          </Select.Option>
        ))}
      </Select>,
      rules: [
        { required: true, message: 'Please select a payment method' },
      ],
    },
    {
      name: 'transactionId',
      label: 'Transaction ID',
      component: <Input
        prefix={<NumberOutlined />}
        placeholder="TXN-123456"
      />,
      rules: [
        { min: 3, max: 100, message: 'Transaction ID must be 3-100 characters' },
      ],
      help: 'External transaction reference ID',
    },
    {
      name: 'notes',
      label: 'Notes',
      component: <Input.TextArea
        placeholder="Additional payment notes..."
        rows={3}
      />,
      rules: [
        { max: 500, message: 'Notes must not exceed 500 characters' },
      ],
    },
    {
      name: 'status',
      label: 'Status',
      component: <Select placeholder="Select status">
        {PAYMENT_STATUSES.map(status => (
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
  paymentTableConfig,
  paymentMobileFields,
  paymentFormConfig,
};
