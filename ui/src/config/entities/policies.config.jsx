/**
 * Policy Entity Configuration
 * Table and form configuration for Policy entities
 */

import { Button, Input, DatePicker, Select, InputNumber } from 'antd';
import {
  EyeOutlined,
  UserOutlined,
  FileTextOutlined,
  DollarOutlined,
} from '@ant-design/icons';
import { formatTimestamp, formatDate, formatCurrency } from '../../utils/formatters';
import StatusTag from '../../components/common/StatusTag';
import { POLICY_STATUS_OPTIONS } from '../constants';
import { generatePolicySampleData } from '../../utils/formSampleData';
import dayjs from 'dayjs';

// Table Configuration
export const policyTableConfig = {
  entityName: 'policy',
  entityNamePlural: 'policies',
  basePath: '/policies',
  scrollX: 1200,

  columns: (navigate) => [
    {
      title: 'Policy Number',
      dataIndex: ['data', 'policyNumber'],
      key: 'policyNumber',
      width: 150,
      sorter: (a, b) => (a.data?.policyNumber || '').localeCompare(b.data?.policyNumber || ''),
      render: (policyNumber, record) => (
        <Button
          type="link"
          onClick={() => navigate(`/policies/${record.id}`)}
          style={{ padding: 0 }}
        >
          {policyNumber || '-'}
        </Button>
      ),
    },
    {
      title: 'Holder Name',
      dataIndex: ['data', 'holderName'],
      key: 'holderName',
      sorter: (a, b) => (a.data?.holderName || '').localeCompare(b.data?.holderName || ''),
      render: (name) => name || '-',
    },
    {
      title: 'Effective Date',
      dataIndex: ['data', 'effectiveDate'],
      key: 'effectiveDate',
      width: 130,
      sorter: (a, b) => (a.data?.effectiveDate || '').localeCompare(b.data?.effectiveDate || ''),
      render: (date) => formatDate(date),
    },
    {
      title: 'Expiration Date',
      dataIndex: ['data', 'expirationDate'],
      key: 'expirationDate',
      width: 140,
      sorter: (a, b) => (a.data?.expirationDate || '').localeCompare(b.data?.expirationDate || ''),
      render: (date) => formatDate(date),
    },
    {
      title: 'Premium',
      dataIndex: ['data', 'premium'],
      key: 'premium',
      width: 120,
      align: 'right',
      sorter: (a, b) => (a.data?.premium || 0) - (b.data?.premium || 0),
      render: (premium) => formatCurrency(premium),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 110,
      filters: [
        { text: 'Active', value: 'ACTIVE' },
        { text: 'Expired', value: 'EXPIRED' },
        { text: 'Cancelled', value: 'CANCELLED' },
      ],
      onFilter: (value, record) => record.status === value,
      render: (status) => <StatusTag type="policy" value={status} />,
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

  mobileFields: (policy, navigate) => [
    {
      type: 'header',
      label: 'Policy Number',
      value: policy.data?.policyNumber || '-',
      status: <StatusTag type="policy" value={policy.data?.status} />,
    },
    {
      type: 'single',
      label: 'Holder Name',
      value: policy.data?.holderName || '-',
    },
    {
      type: 'double',
      items: [
        {
          label: 'Effective',
          value: formatDate(policy.data?.effectiveDate),
        },
        {
          label: 'Expires',
          value: formatDate(policy.data?.expirationDate),
        },
      ],
    },
    {
      type: 'footer',
      label: 'Premium',
      value: formatCurrency(policy.data?.premium),
      action: {
        text: 'View',
        icon: <EyeOutlined />,
        onClick: (e) => {
          e.stopPropagation();
          navigate(`/policies/${policy.id}`);
        },
      },
    },
  ],
};

// Form Configuration
export const policyFormConfig = {
  title: 'Create New Policy',
  submitButtonText: 'Create Policy',
  submitButtonLoadingText: 'Creating Policy...',
  initialValues: {
    status: 'ACTIVE',
  },
  onFillSampleData: () => {
    const sampleData = generatePolicySampleData();
    return {
      ...sampleData,
      effectiveDate: dayjs(sampleData.effectiveDate),
      expirationDate: dayjs(sampleData.expirationDate),
    };
  },

  fields: [
    {
      name: 'policyNumber',
      label: 'Policy Number',
      component: (
        <Input
          prefix={<FileTextOutlined />}
          placeholder="POL-2024-001"
          size="large"
        />
      ),
      rules: [
        { required: true, message: 'Please enter a policy number' },
        { min: 3, message: 'Policy number must be at least 3 characters' },
      ],
    },
    {
      name: 'holderName',
      label: 'Policy Holder Name',
      component: (
        <Input
          prefix={<UserOutlined />}
          placeholder="John Smith"
          size="large"
        />
      ),
      rules: [
        { required: true, message: 'Please enter the policy holder name' },
        { min: 2, message: 'Name must be at least 2 characters' },
      ],
    },
    {
      name: 'effectiveDate',
      label: 'Effective Date',
      component: <DatePicker size="large" style={{ width: '100%' }} format="MM/DD/YYYY" />,
      rules: [{ required: true, message: 'Please select an effective date' }],
      transform: (value) => value?.format('YYYY-MM-DD'),
    },
    {
      name: 'expirationDate',
      label: 'Expiration Date',
      component: <DatePicker size="large" style={{ width: '100%' }} format="MM/DD/YYYY" />,
      rules: [
        { required: true, message: 'Please select an expiration date' },
        ({ getFieldValue }) => ({
          validator(_, value) {
            const effectiveDate = getFieldValue('effectiveDate');
            if (!value || !effectiveDate || value.isAfter(effectiveDate)) {
              return Promise.resolve();
            }
            return Promise.reject(
              new Error('Expiration date must be after effective date')
            );
          },
        }),
      ],
      transform: (value) => value?.format('YYYY-MM-DD'),
    },
    {
      name: 'premium',
      label: 'Annual Premium',
      component: (
        <InputNumber
          prefix={<DollarOutlined />}
          placeholder="1250.00"
          size="large"
          style={{ width: '100%' }}
          precision={2}
          min={0}
          step={100}
        />
      ),
      rules: [
        { required: true, message: 'Please enter the premium amount' },
        { type: 'number', min: 0, message: 'Premium must be a positive number' },
      ],
    },
    {
      name: 'status',
      label: 'Status',
      component: (
        <Select
          size="large"
          placeholder="Select status"
          options={POLICY_STATUS_OPTIONS.map((opt) => ({
            label: opt.label,
            value: opt.value,
          }))}
        />
      ),
      rules: [{ required: true, message: 'Please select a status' }],
    },
    {
      name: 'quoteId',
      label: 'Related Quote ID (Optional)',
      component: (
        <Input
          placeholder="Enter quote ID if applicable"
          size="large"
        />
      ),
    },
  ],
};
