/**
 * Loan Entity Configuration
 * Defines table columns, form fields, and validation for loans
 */

import { Input, InputNumber, Select, Tag } from 'antd';
import { BankOutlined, UserOutlined } from '@ant-design/icons';
import { formatTimestamp } from '../../utils/formatters';

const { TextArea } = Input;

// Status color mapping
const STATUS_COLORS = {
  ACTIVE: 'green',
  FILLED: 'blue',
  EXPIRED: 'gray',
  CANCELLED: 'red',
};

// Table configuration
export const loanTableConfig = {
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
      title: 'Medication',
      dataIndex: ['data', 'medication'],
      key: 'medication',
      width: 200,
      ellipsis: true,
      render: (med) => med || '-',
    },
    {
      title: 'Dosage',
      dataIndex: ['data', 'dosage'],
      key: 'dosage',
      width: 150,
      render: (dosage) => dosage || '-',
    },
    {
      title: 'Frequency',
      dataIndex: ['data', 'frequency'],
      key: 'frequency',
      width: 150,
      render: (freq) => freq || '-',
    },
    {
      title: 'Prescriber',
      dataIndex: ['data', 'prescriber'],
      key: 'prescriber',
      width: 150,
      ellipsis: true,
      render: (prescriber) => prescriber || '-',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => (
        <Tag color={STATUS_COLORS[status] || 'default'}>
          {status || 'ACTIVE'}
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
  scroll: { x: 1200 },
};

// Mobile fields for responsive table
export const loanMobileFields = [
  { label: 'Customer', key: ['data', 'customerName'] },
  { label: 'Medication', key: ['data', 'medication'] },
  { label: 'Dosage', key: ['data', 'dosage'] },
  { label: 'Status', key: 'status' },
];

// Form fields configuration
export const loanFormFields = [
  {
    name: 'customerName',
    label: 'Customer Name',
    required: true,
    message: 'Please enter customer name',
    component: <Input prefix={<UserOutlined />} placeholder="John Doe" />,
  },
  {
    name: 'medication',
    label: 'Medication',
    required: true,
    message: 'Please enter medication name',
    component: <Input prefix={<BankOutlined />} placeholder="Medication name" />,
  },
  {
    name: 'dosage',
    label: 'Dosage',
    required: true,
    message: 'Please enter dosage',
    component: <Input placeholder="e.g., 500mg" />,
  },
  {
    name: 'frequency',
    label: 'Frequency',
    required: true,
    message: 'Please enter frequency',
    component: <Input placeholder="e.g., Twice daily" />,
  },
  {
    name: 'duration',
    label: 'Duration',
    required: false,
    component: <Input placeholder="e.g., 7 days" />,
  },
  {
    name: 'prescriber',
    label: 'Prescriber',
    required: false,
    component: <Input placeholder="Dr. Smith" />,
  },
  {
    name: 'instructions',
    label: 'Instructions',
    required: false,
    component: <TextArea placeholder="Special instructions" rows={3} />,
  },
  {
    name: 'refillsAllowed',
    label: 'Refills Allowed',
    required: false,
    component: <InputNumber min={0} placeholder="Number of refills" style={{ width: '100%' }} />,
  },
];
