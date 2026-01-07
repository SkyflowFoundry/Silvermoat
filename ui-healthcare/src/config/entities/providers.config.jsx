/**
 * Provider Entity Configuration
 * Defines table columns, form fields, and validation for providers
 */

import { Input, Select, Tag } from 'antd';
import { UserOutlined, MailOutlined, PhoneOutlined } from '@ant-design/icons';
import { formatTimestamp } from '../../utils/formatters';

const { TextArea } = Input;

// Status color mapping
const STATUS_COLORS = {
  ACTIVE: 'green',
  INACTIVE: 'gray',
  ARCHIVED: 'red',
};

// Table configuration
export const providerTableConfig = {
  columns: [
    {
      title: 'Name',
      dataIndex: ['data', 'name'],
      key: 'name',
      width: 200,
      ellipsis: true,
      render: (name) => name || '-',
    },
    {
      title: 'Specialty',
      dataIndex: ['data', 'specialty'],
      key: 'specialty',
      width: 180,
      ellipsis: true,
      render: (specialty) => specialty || '-',
    },
    {
      title: 'Email',
      dataIndex: ['data', 'email'],
      key: 'email',
      width: 200,
      ellipsis: true,
      render: (email) => email || '-',
    },
    {
      title: 'Phone',
      dataIndex: ['data', 'phone'],
      key: 'phone',
      width: 150,
      ellipsis: true,
      render: (phone) => phone || '-',
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
  scroll: { x: 1000 },
};

// Mobile fields for responsive table
export const providerMobileFields = [
  { label: 'Name', key: ['data', 'name'] },
  { label: 'Specialty', key: ['data', 'specialty'] },
  { label: 'Email', key: ['data', 'email'] },
  { label: 'Status', key: 'status' },
];

// Form fields configuration
export const providerFormFields = [
  {
    name: 'name',
    label: 'Provider Name',
    required: true,
    message: 'Please enter provider name',
    component: <Input prefix={<UserOutlined />} placeholder="Dr. Jane Smith" />,
  },
  {
    name: 'specialty',
    label: 'Specialty',
    required: true,
    message: 'Please enter specialty',
    component: (
      <Select placeholder="Select specialty">
        <Select.Option value="CARDIOLOGY">Cardiology</Select.Option>
        <Select.Option value="DERMATOLOGY">Dermatology</Select.Option>
        <Select.Option value="FAMILY_MEDICINE">Family Medicine</Select.Option>
        <Select.Option value="NEUROLOGY">Neurology</Select.Option>
        <Select.Option value="ORTHOPEDICS">Orthopedics</Select.Option>
        <Select.Option value="PEDIATRICS">Pediatrics</Select.Option>
        <Select.Option value="PSYCHIATRY">Psychiatry</Select.Option>
        <Select.Option value="OTHER">Other</Select.Option>
      </Select>
    ),
  },
  {
    name: 'email',
    label: 'Email',
    required: false,
    type: 'email',
    component: <Input prefix={<MailOutlined />} placeholder="provider@example.com" />,
  },
  {
    name: 'phone',
    label: 'Phone Number',
    required: false,
    component: <Input prefix={<PhoneOutlined />} placeholder="(555) 123-4567" />,
  },
  {
    name: 'licenseNumber',
    label: 'License Number',
    required: false,
    component: <Input placeholder="Medical license number" />,
  },
  {
    name: 'address',
    label: 'Office Address',
    required: false,
    component: <TextArea placeholder="Office address" rows={2} />,
  },
  {
    name: 'notes',
    label: 'Notes',
    required: false,
    component: <TextArea placeholder="Additional notes" rows={2} />,
  },
];
