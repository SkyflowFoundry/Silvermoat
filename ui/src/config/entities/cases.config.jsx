/**
 * Case Entity Configuration
 * Table and form configuration for Case entities
 */

import { Button, Input, Select } from 'antd';
import {
  EyeOutlined,
  FileProtectOutlined,
  UserOutlined,
} from '@ant-design/icons';
import { formatTimestamp } from '../../utils/formatters';
import StatusTag from '../../components/common/StatusTag';
import {
  CASE_PRIORITY_OPTIONS,
  CASE_STATUS_OPTIONS,
  RELATED_ENTITY_TYPES,
  ENTITY_LABELS,
} from '../constants';
import { generateCaseSampleData } from '../../utils/formSampleData';

const { TextArea } = Input;

// Table Configuration
export const caseTableConfig = {
  entityName: 'case',
  entityNamePlural: 'cases',
  basePath: '/cases',
  scrollX: 1000,

  columns: (navigate) => [
    {
      title: 'Case ID',
      dataIndex: 'id',
      key: 'id',
      width: 280,
      render: (id) => (
        <Button
          type="link"
          onClick={() => navigate(`/cases/${id}`)}
          style={{ padding: 0 }}
        >
          {id.substring(0, 8)}...
        </Button>
      ),
      ellipsis: true,
    },
    {
      title: 'Title',
      dataIndex: ['data', 'title'],
      key: 'title',
      width: 200,
      ellipsis: true,
      render: (title) => title || '-',
    },
    {
      title: 'Related Entity',
      dataIndex: ['data', 'relatedEntityType'],
      key: 'relatedEntityType',
      width: 120,
      filters: [
        { text: 'Quote', value: 'quote' },
        { text: 'Policy', value: 'policy' },
        { text: 'Claim', value: 'claim' },
      ],
      onFilter: (value, record) => record.data?.relatedEntityType === value,
      render: (type) => ENTITY_LABELS[type] || '-',
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
      title: 'Priority',
      dataIndex: ['data', 'priority'],
      key: 'priority',
      width: 120,
      filters: CASE_PRIORITY_OPTIONS.map((opt) => ({
        text: opt.label,
        value: opt.value,
      })),
      onFilter: (value, record) => record.data?.priority === value,
      render: (priority) => <StatusTag type="case-priority" value={priority} />,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      filters: CASE_STATUS_OPTIONS.map((opt) => ({
        text: opt.label,
        value: opt.value,
      })),
      onFilter: (value, record) => record.status === value,
      render: (status) => <StatusTag type="case-status" value={status} />,
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

  mobileFields: (caseItem, navigate) => [
    {
      type: 'single',
      label: 'Title',
      value: caseItem.data?.title || '-',
    },
    {
      type: 'status',
      items: [
        <StatusTag type="case-priority" value={caseItem.data?.priority} />,
        <StatusTag type="case-status" value={caseItem.data?.status} />,
      ],
    },
    {
      type: 'double',
      items: [
        {
          label: 'Assignee',
          value: caseItem.data?.assignee || 'Unassigned',
        },
        {
          label: 'Related',
          value: ENTITY_LABELS[caseItem.data?.relatedEntityType] || '-',
        },
      ],
    },
    {
      type: 'single',
      label: 'Created',
      value: formatTimestamp(caseItem.createdAt),
    },
    {
      type: 'footer',
      action: {
        text: 'View Details',
        icon: <EyeOutlined />,
        onClick: (e) => {
          e.stopPropagation();
          navigate(`/cases/${caseItem.id}`);
        },
        block: true,
      },
    },
  ],
};

// Form Configuration
export const caseFormConfig = {
  title: 'Create New Case',
  submitButtonText: 'Create Case',
  submitButtonLoadingText: 'Creating Case...',
  initialValues: {
    status: 'OPEN',
    priority: 'MEDIUM',
  },
  onFillSampleData: () => {
    return generateCaseSampleData();
  },

  fields: [
    {
      name: 'title',
      label: 'Case Title',
      component: (
        <Input
          placeholder="Brief description of the issue"
          size="large"
          maxLength={100}
          showCount
        />
      ),
      rules: [
        { required: true, message: 'Please enter a case title' },
        { max: 100, message: 'Title must be less than 100 characters' },
      ],
    },
    {
      name: 'description',
      label: 'Description',
      component: (
        <TextArea
          placeholder="Detailed description of the case"
          rows={4}
          maxLength={500}
          showCount
        />
      ),
      rules: [
        { required: true, message: 'Please enter a description' },
        { max: 500, message: 'Description must be less than 500 characters' },
      ],
    },
    {
      name: 'relatedEntityType',
      label: 'Related Entity Type',
      component: (
        <Select
          size="large"
          placeholder="Select entity type"
          options={RELATED_ENTITY_TYPES}
        />
      ),
      rules: [{ required: true, message: 'Please select an entity type' }],
    },
    {
      name: 'relatedEntityId',
      label: 'Related Entity ID',
      component: (
        <Input
          prefix={<FileProtectOutlined />}
          placeholder="Enter entity ID"
          size="large"
        />
      ),
      rules: [{ required: true, message: 'Please enter the entity ID' }],
    },
    {
      name: 'assignee',
      label: 'Assignee',
      component: (
        <Input
          prefix={<UserOutlined />}
          placeholder="Enter assignee name"
          size="large"
        />
      ),
      rules: [{ required: true, message: 'Please enter an assignee name' }],
    },
    {
      name: 'priority',
      label: 'Priority',
      component: (
        <Select
          size="large"
          placeholder="Select priority"
          options={CASE_PRIORITY_OPTIONS.map((opt) => ({
            label: opt.label,
            value: opt.value,
          }))}
        />
      ),
      rules: [{ required: true, message: 'Please select a priority' }],
    },
    {
      name: 'status',
      label: 'Status',
      component: (
        <Select
          size="large"
          placeholder="Select status"
          options={CASE_STATUS_OPTIONS.map((opt) => ({
            label: opt.label,
            value: opt.value,
          }))}
        />
      ),
      rules: [{ required: true, message: 'Please select a status' }],
    },
  ],
};
