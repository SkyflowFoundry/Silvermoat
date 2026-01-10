/**
 * Transaction Entity Configuration
 * Defines table columns, form fields, and validation for transactions
 */

import { Input, InputNumber, Select, Tag, DatePicker } from 'antd';
import { DollarOutlined, UserOutlined } from '@ant-design/icons';
import { formatTimestamp } from '../../utils/formatters';

const { TextArea } = Input;

// Status color mapping
const STATUS_COLORS = {
  COMPLETED: 'green',
  PENDING: 'blue',
  FAILED: 'red',
  PROCESSING: 'orange',
};

// Transaction type color mapping
const TYPE_COLORS = {
  DEPOSIT: 'cyan',
  WITHDRAWAL: 'orange',
  TRANSFER: 'blue',
  PAYMENT: 'purple',
};

// Table configuration
export const transactionTableConfig = {
  columns: [
    {
      title: 'Customer Name',
      dataIndex: ['data', 'customerName'],
      key: 'customerName',
      width: 180,
      ellipsis: true,
      render: (name) => name || '-',
    },
    {
      title: 'Amount',
      dataIndex: ['data', 'amount'],
      key: 'amount',
      width: 150,
      render: (amount) => amount ? `$${parseFloat(amount).toFixed(2)}` : '-',
    },
    {
      title: 'Type',
      dataIndex: ['data', 'type'],
      key: 'type',
      width: 120,
      render: (type) => (
        <Tag color={TYPE_COLORS[type] || 'default'}>
          {type || 'PAYMENT'}
        </Tag>
      ),
    },
    {
      title: 'Account ID',
      dataIndex: ['data', 'accountId'],
      key: 'accountId',
      width: 150,
      ellipsis: true,
      render: (accountId) => accountId || '-',
    },
    {
      title: 'Description',
      dataIndex: ['data', 'description'],
      key: 'description',
      width: 200,
      ellipsis: true,
      render: (desc) => desc || '-',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      render: (status) => (
        <Tag color={STATUS_COLORS[status] || 'default'}>
          {status || 'COMPLETED'}
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
  defaultSortField: 'createdAt',
  defaultSortOrder: 'descend',

  mobileFields: [
    {
      layout: 'row',
      items: [
        {
          label: 'Customer',
          getValue: (transaction) => transaction.data?.customerName || '-',
          flex: 1,
        },
        {
          label: '',
          getValue: (transaction) => (
            transaction.status === 'COMPLETED' ? 'Completed' :
            transaction.status === 'PENDING' ? 'Pending' :
            transaction.status === 'FAILED' ? 'Failed' : 'Processing'
          ),
        },
      ],
    },
    {
      layout: 'row',
      items: [
        {
          label: 'Amount',
          getValue: (transaction) => transaction.data?.amount ? `$${parseFloat(transaction.data.amount).toFixed(2)}` : '-',
          flex: 1,
        },
        {
          label: 'Type',
          getValue: (transaction) => transaction.data?.type || 'PAYMENT',
        },
      ],
    },
    {
      label: 'Description',
      getValue: (transaction) => transaction.data?.description || '-',
    },
  ],
};

// Form configuration
export const transactionFormConfig = {
  fields: [
    {
      name: 'customerName',
      label: 'Customer Name',
      required: true,
      component: Input,
      props: {
        prefix: <UserOutlined />,
        placeholder: 'Enter customer name',
      },
    },
    {
      name: 'customerEmail',
      label: 'Customer Email',
      required: true,
      component: Input,
      props: {
        type: 'email',
        placeholder: 'customer@example.com',
      },
      rules: [
        { type: 'email', message: 'Please enter a valid email' },
      ],
    },
    {
      name: 'amount',
      label: 'Amount',
      required: true,
      component: InputNumber,
      props: {
        prefix: <DollarOutlined />,
        placeholder: 'Enter amount',
        min: 0.01,
        step: 0.01,
        precision: 2,
        style: { width: '100%' },
      },
    },
    {
      name: 'type',
      label: 'Transaction Type',
      required: true,
      component: Select,
      props: {
        placeholder: 'Select type',
        options: [
          { label: 'Deposit', value: 'DEPOSIT' },
          { label: 'Withdrawal', value: 'WITHDRAWAL' },
          { label: 'Transfer', value: 'TRANSFER' },
          { label: 'Payment', value: 'PAYMENT' },
        ],
      },
    },
    {
      name: 'accountId',
      label: 'Account ID',
      component: Input,
      props: {
        placeholder: 'Optional account ID',
      },
    },
    {
      name: 'description',
      label: 'Description',
      component: TextArea,
      props: {
        placeholder: 'Transaction description',
        rows: 3,
      },
    },
  ],
};

// Entity metadata
export const transactionEntityConfig = {
  name: 'transaction',
  displayName: 'Transaction',
  pluralName: 'Transactions',
  icon: DollarOutlined,
  color: '#13c2c2',
  description: 'Financial transactions including deposits, withdrawals, and payments',
};
