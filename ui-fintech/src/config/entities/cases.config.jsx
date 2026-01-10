/**
 * Case Entity Configuration
 * Defines table columns, form fields, and validation for support cases
 */

import { Input, Select, Tag } from 'antd';
import { CustomerServiceOutlined, UserOutlined, MailOutlined, FileTextOutlined } from '@ant-design/icons';
import { formatTimestamp } from '../../utils/formatters';

const { TextArea } = Input;

// Priority options
const PRIORITIES = ['LOW', 'MEDIUM', 'HIGH', 'URGENT'];

// Status options
const CASE_STATUSES = ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'];

// Priority color mapping
const PRIORITY_COLORS = {
  LOW: 'green',
  MEDIUM: 'blue',
  HIGH: 'orange',
  URGENT: 'red',
};

// Status color mapping
const STATUS_COLORS = {
  OPEN: 'orange',
  IN_PROGRESS: 'blue',
  RESOLVED: 'green',
  CLOSED: 'default',
};

// Table configuration
export const caseTableConfig = {
  columns: [
    {
      title: 'Subject',
      dataIndex: ['data', 'subject'],
      key: 'subject',
      width: 250,
      ellipsis: true,
      render: (subject) => <strong>{subject || '-'}</strong>,
    },
    {
      title: 'Customer Email',
      dataIndex: ['data', 'customerEmail'],
      key: 'customerEmail',
      width: 200,
      ellipsis: true,
    },
    {
      title: 'Priority',
      dataIndex: ['data', 'priority'],
      key: 'priority',
      width: 100,
      render: (priority) => (
        <Tag color={PRIORITY_COLORS[priority] || 'default'}>
          {priority || 'MEDIUM'}
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
          {status || 'OPEN'}
        </Tag>
      ),
    },
    {
      title: 'Assignee',
      dataIndex: ['data', 'assignee'],
      key: 'assignee',
      width: 150,
      ellipsis: true,
      render: (assignee) => assignee || 'Unassigned',
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

  mobileFields: [
    {
      layout: 'row',
      items: [
        {
          label: 'Subject',
          getValue: (caseItem) => caseItem.data?.subject || '-',
          flex: 1,
        },
        {
          label: 'Priority',
          getValue: (caseItem) => caseItem.data?.priority || 'MEDIUM',
        },
      ],
    },
    {
      label: 'Customer',
      getValue: (caseItem) => caseItem.data?.customerEmail || '-',
    },
    {
      label: 'Assigned To',
      getValue: (caseItem) => caseItem.data?.assignedTo || 'Unassigned',
    },
  ],
};

// Mobile fields for responsive table
export const caseMobileFields = [
  {
    label: 'Subject',
    key: 'subject',
    render: (item) => <strong>{item.data?.subject || '-'}</strong>,
  },
  {
    label: 'Customer',
    key: 'customerEmail',
    render: (item) => item.data?.customerEmail || '-',
  },
  {
    label: 'Priority',
    key: 'priority',
    render: (item) => (
      <Tag color={PRIORITY_COLORS[item.data?.priority] || 'default'}>
        {item.data?.priority || 'MEDIUM'}
      </Tag>
    ),
  },
  {
    label: 'Status',
    key: 'status',
    render: (item) => (
      <Tag color={STATUS_COLORS[item.data?.status] || 'default'}>
        {item.data?.status || 'OPEN'}
      </Tag>
    ),
  },
  {
    label: 'Assignee',
    key: 'assignee',
    render: (item) => item.data?.assignee || 'Unassigned',
  },
];

// Form configuration
export const caseFormConfig = {
  fields: [
    {
      name: 'subject',
      label: 'Subject',
      component: <Input
        prefix={<FileTextOutlined />}
        placeholder="Brief description of the issue"
        maxLength={200}
      />,
      rules: [
        { required: true, message: 'Please enter the case subject' },
        { min: 5, max: 200, message: 'Subject must be 5-200 characters' },
      ],
    },
    {
      name: 'description',
      label: 'Description',
      component: <TextArea
        placeholder="Detailed description of the issue..."
        rows={5}
      />,
      rules: [
        { required: true, message: 'Please enter a description' },
        { min: 10, max: 2000, message: 'Description must be 10-2000 characters' },
      ],
    },
    {
      name: 'customerEmail',
      label: 'Customer Email',
      component: <Input
        prefix={<MailOutlined />}
        placeholder="customer@example.com"
        type="email"
      />,
      rules: [
        { type: 'email', message: 'Please enter a valid email' },
      ],
      help: 'Email of the customer who reported this issue',
    },
    {
      name: 'priority',
      label: 'Priority',
      component: <Select placeholder="Select priority">
        {PRIORITIES.map(priority => (
          <Select.Option key={priority} value={priority}>
            {priority}
          </Select.Option>
        ))}
      </Select>,
      rules: [
        { required: true, message: 'Please select a priority' },
      ],
      initialValue: 'MEDIUM',
    },
    {
      name: 'status',
      label: 'Status',
      component: <Select placeholder="Select status">
        {CASE_STATUSES.map(status => (
          <Select.Option key={status} value={status}>
            {status}
          </Select.Option>
        ))}
      </Select>,
      rules: [],
      initialValue: 'OPEN',
    },
    {
      name: 'assignee',
      label: 'Assignee',
      component: <Input
        prefix={<UserOutlined />}
        placeholder="Team member name"
      />,
      rules: [
        { min: 2, max: 100, message: 'Assignee must be 2-100 characters' },
      ],
      help: 'Team member assigned to this case',
    },
  ],
  layout: 'vertical',
  requiredMark: true,
};

// Export fields array for form component compatibility
export const caseFormFields = caseFormConfig.fields;

export default {
  caseTableConfig,
  caseMobileFields,
  caseFormConfig,
};
