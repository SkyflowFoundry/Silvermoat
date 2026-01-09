/**
 * Customer Entity Configuration
 * Defines table columns, form fields, and validation for customers
 */

import { Input, Tag } from 'antd';
import { UserOutlined, MailOutlined, PhoneOutlined } from '@ant-design/icons';
import { formatTimestamp } from '../../utils/formatters';

// Status color mapping
const STATUS_COLORS = {
  ACTIVE: 'green',
  INACTIVE: 'gray',
  ARCHIVED: 'red',
};

// Table configuration
export const customerTableConfig = {
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
      title: 'Email',
      dataIndex: ['data', 'email'],
      key: 'email',
      width: 200,
      ellipsis: true,
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
      title: 'Date of Birth',
      dataIndex: ['data', 'dateOfBirth'],
      key: 'dateOfBirth',
      width: 120,
      render: (dob) => dob || '-',
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
export const customerMobileFields = [
  { label: 'Name', key: ['data', 'name'] },
  { label: 'Email', key: ['data', 'email'] },
  { label: 'Phone', key: ['data', 'phone'] },
  { label: 'Status', key: 'status' },
];

// Form fields configuration
export const customerFormFields = [
  {
    name: 'name',
    label: 'Customer Name',
    required: true,
    message: 'Please enter customer name',
    component: <Input prefix={<UserOutlined />} placeholder="John Doe" />,
  },
  {
    name: 'email',
    label: 'Email',
    required: true,
    message: 'Please enter email address',
    type: 'email',
    component: <Input prefix={<MailOutlined />} placeholder="customer@example.com" />,
  },
  {
    name: 'phone',
    label: 'Phone Number',
    required: false,
    component: <Input prefix={<PhoneOutlined />} placeholder="(555) 123-4567" />,
  },
  {
    name: 'dateOfBirth',
    label: 'Date of Birth',
    required: false,
    component: <Input placeholder="YYYY-MM-DD" />,
  },
  {
    name: 'address',
    label: 'Address',
    required: false,
    component: <Input.TextArea placeholder="123 Main St, City, State ZIP" rows={2} />,
  },
  {
    name: 'emergencyContact',
    label: 'Emergency Contact',
    required: false,
    component: <Input placeholder="Emergency contact name and phone" />,
  },
];
