/**
 * Payment Entity Configuration
 * Table and form configuration for Payment entities
 */

import { Button, Input, DatePicker, Select, InputNumber } from 'antd';
import {
  EyeOutlined,
  DollarOutlined,
  FileProtectOutlined,
} from '@ant-design/icons';
import { formatTimestamp, formatCurrency } from '../../utils/formatters';
import StatusTag from '../../components/common/StatusTag';
import { PAYMENT_METHOD_OPTIONS, PAYMENT_STATUS_OPTIONS } from '../constants';
import { generatePaymentSampleData } from '../../utils/formSampleData';
import dayjs from 'dayjs';

// Table Configuration
export const paymentTableConfig = {
  entityName: 'payment',
  entityNamePlural: 'payments',
  basePath: '/payments',
  scrollX: 1000,

  columns: (navigate) => [
    {
      title: 'Payment ID',
      dataIndex: 'id',
      key: 'id',
      width: 280,
      render: (id) => (
        <Button
          type="link"
          onClick={() => navigate(`/payments/${id}`)}
          style={{ padding: 0 }}
        >
          {id.substring(0, 8)}...
        </Button>
      ),
      ellipsis: true,
    },
    {
      title: 'Payment Date',
      key: 'paymentDate',
      width: 130,
      render: () => '-', // Payment date not in seed data
    },
    {
      title: 'Amount',
      dataIndex: ['data', 'amount'],
      key: 'amount',
      width: 120,
      align: 'right',
      sorter: (a, b) => (a.data?.amount || 0) - (b.data?.amount || 0),
      render: (amount) => formatCurrency(amount),
    },
    {
      title: 'Method',
      dataIndex: ['data', 'paymentMethod'],
      key: 'paymentMethod',
      width: 130,
      filters: [
        { text: 'Credit Card', value: 'CREDIT_CARD' },
        { text: 'Bank Transfer', value: 'BANK_TRANSFER' },
        { text: 'Check', value: 'CHECK' },
      ],
      onFilter: (value, record) => record.data?.paymentMethod === value,
      render: (method) => method ? method.replace('_', ' ') : '-',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      filters: [
        { text: 'Pending', value: 'PENDING' },
        { text: 'Completed', value: 'COMPLETED' },
        { text: 'Failed', value: 'FAILED' },
      ],
      onFilter: (value, record) => record.status === value,
      render: (status) => <StatusTag type="payment" value={status} />,
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

  mobileFields: (payment, navigate) => [
    {
      type: 'header',
      label: 'Payment ID',
      value: payment.id.substring(0, 16) + '...',
      status: <StatusTag type="payment" value={payment.status} />,
    },
    {
      type: 'double',
      items: [
        {
          label: 'Payment Date',
          value: '-',
        },
        {
          label: 'Method',
          value: payment.data?.paymentMethod ? payment.data.paymentMethod.replace('_', ' ') : '-',
        },
      ],
    },
    {
      type: 'single',
      label: 'Amount',
      value: formatCurrency(payment.data?.amount),
    },
    {
      type: 'footer',
      action: {
        text: 'View Details',
        icon: <EyeOutlined />,
        onClick: (e) => {
          e.stopPropagation();
          navigate(`/payments/${payment.id}`);
        },
        block: true,
      },
    },
  ],
};

// Form Configuration
export const paymentFormConfig = {
  title: 'Record New Payment',
  submitButtonText: 'Record Payment',
  submitButtonLoadingText: 'Recording Payment...',
  initialValues: {
    status: 'COMPLETED',
    method: 'CARD',
  },
  onFillSampleData: () => {
    const sampleData = generatePaymentSampleData();
    return {
      ...sampleData,
      paymentDate: dayjs(sampleData.paymentDate),
    };
  },

  fields: [
    {
      name: 'paymentDate',
      label: 'Payment Date',
      component: <DatePicker size="large" style={{ width: '100%' }} format="MM/DD/YYYY" />,
      rules: [{ required: true, message: 'Please select the payment date' }],
      transform: (value) => value?.format('YYYY-MM-DD'),
    },
    {
      name: 'amount',
      label: 'Payment Amount',
      component: (
        <InputNumber
          prefix={<DollarOutlined />}
          placeholder="250.00"
          size="large"
          style={{ width: '100%' }}
          precision={2}
          min={0}
          step={10}
        />
      ),
      rules: [
        { required: true, message: 'Please enter the payment amount' },
        { type: 'number', min: 0, message: 'Amount must be positive' },
      ],
    },
    {
      name: 'method',
      label: 'Payment Method',
      component: (
        <Select
          size="large"
          placeholder="Select payment method"
          options={PAYMENT_METHOD_OPTIONS}
        />
      ),
      rules: [{ required: true, message: 'Please select a payment method' }],
    },
    {
      name: 'status',
      label: 'Status',
      component: (
        <Select
          size="large"
          placeholder="Select status"
          options={PAYMENT_STATUS_OPTIONS.map((opt) => ({
            label: opt.label,
            value: opt.value,
          }))}
        />
      ),
      rules: [{ required: true, message: 'Please select a status' }],
    },
    {
      name: 'policyId',
      label: 'Related Policy ID',
      component: (
        <Input
          prefix={<FileProtectOutlined />}
          placeholder="Enter policy ID"
          size="large"
        />
      ),
      rules: [{ required: true, message: 'Please enter the policy ID' }],
    },
  ],
};
