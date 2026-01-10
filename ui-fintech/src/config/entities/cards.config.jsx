/**
 * Card Entity Configuration
 * Defines table columns, form fields, and validation for fintech cards
 */

import { Input, InputNumber, Select, Tag } from 'antd';
import { CreditCardOutlined, BankOutlined, DollarOutlined } from '@ant-design/icons';
import { formatTimestamp, formatCurrency } from '../../utils/formatters';

// Card type options
const CARD_TYPES = ['CREDIT', 'DEBIT', 'PREPAID'];

// Card status options
const CARD_STATUSES = ['ACTIVE', 'SUSPENDED', 'CLOSED', 'EXPIRED'];

// Status color mapping
const STATUS_COLORS = {
  ACTIVE: 'green',
  SUSPENDED: 'orange',
  CLOSED: 'red',
  EXPIRED: 'gray',
};

// Table configuration
export const cardTableConfig = {
  columns: [
    {
      title: 'Customer',
      dataIndex: ['data', 'customerName'],
      key: 'customerName',
      width: 180,
      ellipsis: true,
      render: (name) => name || '-',
    },
    {
      title: 'Card Number',
      dataIndex: ['data', 'cardNumber'],
      key: 'cardNumber',
      width: 150,
      ellipsis: true,
      render: (number) => number ? `****${number.slice(-4)}` : '-',
    },
    {
      title: 'Card Type',
      dataIndex: ['data', 'cardType'],
      key: 'cardType',
      width: 120,
      render: (type) => (
        <Tag color="blue" icon={<CreditCardOutlined />}>
          {type || 'CREDIT'}
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
          {status || 'ACTIVE'}
        </Tag>
      ),
    },
    {
      title: 'Credit Limit',
      dataIndex: ['data', 'creditLimit'],
      key: 'creditLimit',
      width: 130,
      align: 'right',
      render: (limit) => (limit !== undefined ? formatCurrency(limit * 100) : '-'),
    },
    {
      title: 'Current Balance',
      dataIndex: ['data', 'currentBalance'],
      key: 'currentBalance',
      width: 150,
      align: 'right',
      render: (balance) => (balance !== undefined ? formatCurrency(balance * 100) : '-'),
    },
    {
      title: 'Expiry Date',
      dataIndex: ['data', 'expiryDate'],
      key: 'expiryDate',
      width: 120,
      render: (date) => date || '-',
    },
    {
      title: 'Created',
      dataIndex: 'createdAt',
      key: 'createdAt',
      width: 120,
      render: (timestamp) => formatTimestamp(timestamp),
    },
  ],

  mobileFields: [
    {
      layout: 'row',
      items: [
        {
          label: 'Customer',
          getValue: (card) => card.data?.customerName || '-',
          flex: 1,
        },
        {
          label: 'Status',
          getValue: (card) => card.data?.status || 'ACTIVE',
        },
      ],
    },
    {
      layout: 'row',
      items: [
        {
          label: 'Card Number',
          getValue: (card) => card.data?.cardNumber ? `****${card.data.cardNumber.slice(-4)}` : '-',
          flex: 1,
        },
        {
          label: 'Type',
          getValue: (card) => card.data?.cardType || 'CREDIT',
        },
      ],
    },
    {
      layout: 'row',
      items: [
        {
          label: 'Credit Limit',
          getValue: (card) => card.data?.creditLimit ? formatCurrency(card.data.creditLimit * 100) : '-',
          flex: 1,
        },
        {
          label: 'Balance',
          getValue: (card) => card.data?.currentBalance ? formatCurrency(card.data.currentBalance * 100) : '-',
        },
      ],
    },
  ],
};

// Detail view configuration
export const cardDetailConfig = {
  sections: [
    {
      title: 'Card Information',
      icon: <CreditCardOutlined />,
      fields: [
        {
          label: 'Card ID',
          key: 'id',
          render: (item) => item.id || '-',
        },
        {
          label: 'Customer Name',
          key: 'customerName',
          render: (item) => item.data?.customerName || '-',
        },
        {
          label: 'Customer Email',
          key: 'customerEmail',
          render: (item) => item.data?.customerEmail || '-',
        },
        {
          label: 'Card Number',
          key: 'cardNumber',
          render: (item) => item.data?.cardNumber ? `****${item.data.cardNumber.slice(-4)}` : '-',
        },
        {
          label: 'Card Type',
          key: 'cardType',
          render: (item) => (
            <Tag color="blue" icon={<CreditCardOutlined />}>
              {item.data?.cardType || 'CREDIT'}
            </Tag>
          ),
        },
        {
          label: 'Status',
          key: 'status',
          render: (item) => (
            <Tag color={STATUS_COLORS[item.data?.status] || 'default'}>
              {item.data?.status || 'ACTIVE'}
            </Tag>
          ),
        },
      ],
    },
    {
      title: 'Financial Information',
      icon: <DollarOutlined />,
      fields: [
        {
          label: 'Credit Limit',
          key: 'creditLimit',
          render: (item) =>
            item.data?.creditLimit !== undefined
              ? formatCurrency(item.data.creditLimit * 100)
              : '-',
        },
        {
          label: 'Current Balance',
          key: 'currentBalance',
          render: (item) =>
            item.data?.currentBalance !== undefined
              ? formatCurrency(item.data.currentBalance * 100)
              : '-',
        },
        {
          label: 'Available Credit',
          key: 'availableCredit',
          render: (item) => {
            const limit = item.data?.creditLimit || 0;
            const balance = item.data?.currentBalance || 0;
            return formatCurrency((limit - balance) * 100);
          },
        },
        {
          label: 'Expiry Date',
          key: 'expiryDate',
          render: (item) => item.data?.expiryDate || '-',
        },
      ],
    },
    {
      title: 'Metadata',
      icon: <BankOutlined />,
      fields: [
        {
          label: 'Created At',
          key: 'createdAt',
          render: (item) => formatTimestamp(item.createdAt),
        },
        {
          label: 'Last Updated',
          key: 'updatedAt',
          render: (item) => formatTimestamp(item.updatedAt),
        },
      ],
    },
  ],
};

// Form configuration
export const cardFormConfig = {
  fields: [
    {
      name: 'customerName',
      label: 'Customer Name',
      rules: [{ required: true, message: 'Customer name is required' }],
      component: {
        type: Input,
        props: {
          placeholder: 'Enter customer name',
          prefix: <BankOutlined />,
        },
      },
    },
    {
      name: 'customerEmail',
      label: 'Customer Email',
      rules: [
        { required: true, message: 'Customer email is required' },
        { type: 'email', message: 'Please enter a valid email' },
      ],
      component: {
        type: Input,
        props: {
          placeholder: 'customer@example.com',
        },
      },
    },
    {
      name: 'cardNumber',
      label: 'Card Number',
      rules: [{ required: true, message: 'Card number is required' }],
      component: {
        type: Input,
        props: {
          placeholder: '4532XXXXXXXX1234',
          maxLength: 16,
        },
      },
    },
    {
      name: 'cardType',
      label: 'Card Type',
      rules: [{ required: true, message: 'Card type is required' }],
      component: {
        type: Select,
        props: {
          placeholder: 'Select card type',
          options: CARD_TYPES.map((type) => ({ label: type, value: type })),
        },
      },
    },
    {
      name: 'creditLimit',
      label: 'Credit Limit',
      rules: [{ required: true, message: 'Credit limit is required' }],
      component: {
        type: InputNumber,
        props: {
          placeholder: '5000',
          min: 0,
          step: 100,
          style: { width: '100%' },
          prefix: '$',
        },
      },
    },
    {
      name: 'expiryDate',
      label: 'Expiry Date (MM/YY)',
      rules: [{ required: true, message: 'Expiry date is required' }],
      component: {
        type: Input,
        props: {
          placeholder: '12/25',
          maxLength: 5,
        },
      },
    },
    {
      name: 'status',
      label: 'Status',
      rules: [{ required: true, message: 'Status is required' }],
      component: {
        type: Select,
        props: {
          placeholder: 'Select status',
          options: CARD_STATUSES.map((status) => ({ label: status, value: status })),
        },
      },
    },
  ],
};

// Export fields array for form component compatibility
export const cardFormFields = cardFormConfig.fields;
