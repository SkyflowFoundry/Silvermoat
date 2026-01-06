/**
 * Claim Entity Configuration
 * Defines table columns, form fields, and mobile layout for claims
 */

import { Button, Input, DatePicker, Select, InputNumber, Typography } from 'antd';
import {
  FileTextOutlined,
  UserOutlined,
  DollarOutlined,
  FileProtectOutlined,
} from '@ant-design/icons';
import { formatTimestamp, formatDate, formatCurrency } from '../../utils/formatters';
import { CLAIM_STATUS_OPTIONS } from '../constants';
import StatusTag from '../../components/common/StatusTag';
import { generateClaimSampleData } from '../../utils/formSampleData';
import dayjs from 'dayjs';

const { TextArea } = Input;
const { Text } = Typography;

export const claimTableConfig = {
  entityName: 'claim',
  entityNamePlural: 'claims',
  basePath: '/claims',
  scrollX: 1100,

  columns: (navigate) => [
    {
      title: 'Claim Number',
      dataIndex: ['data', 'claimNumber'],
      key: 'claimNumber',
      width: 150,
      sorter: (a, b) => (a.data?.claimNumber || '').localeCompare(b.data?.claimNumber || ''),
      render: (claimNumber, record) => (
        <Button
          type="link"
          onClick={() => navigate(`/claims/${record.id}`)}
          style={{ padding: 0 }}
        >
          {claimNumber || '-'}
        </Button>
      ),
    },
    {
      title: 'Claimant',
      dataIndex: ['data', 'claimantName'],
      key: 'claimantName',
      sorter: (a, b) => (a.data?.claimantName || '').localeCompare(b.data?.claimantName || ''),
      render: (name) => name || '-',
    },
    {
      title: 'Incident Date',
      dataIndex: ['data', 'incidentDate'],
      key: 'incidentDate',
      width: 130,
      sorter: (a, b) => (a.data?.incidentDate || '').localeCompare(b.data?.incidentDate || ''),
      render: (date) => formatDate(date),
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
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 110,
      filters: [
        { text: 'Pending', value: 'PENDING' },
        { text: 'Review', value: 'REVIEW' },
        { text: 'Approved', value: 'APPROVED' },
        { text: 'Denied', value: 'DENIED' },
      ],
      onFilter: (value, record) => record.status === value,
      render: (status) => <StatusTag type="claim" value={status} />,
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

  mobileFields: [
    {
      layout: 'row',
      items: [
        {
          label: 'Claim Number',
          getValue: (claim) => claim.data?.claimNumber || '-',
          render: (claim) => (
            <Text strong style={{ fontSize: 14 }}>{claim.data?.claimNumber || '-'}</Text>
          ),
          flex: 1,
        },
        {
          label: '',
          getValue: () => '',
          render: (claim) => <StatusTag type="claim" value={claim.status} />,
        },
      ],
    },
    {
      label: 'Claimant',
      getValue: (claim) => claim.data?.claimantName || '-',
    },
    {
      layout: 'row',
      items: [
        {
          label: 'Incident Date',
          getValue: (claim) => formatDate(claim.data?.incidentDate),
          render: (claim) => (
            <Text style={{ fontSize: 13 }}>{formatDate(claim.data?.incidentDate)}</Text>
          ),
          flex: 1,
        },
        {
          label: 'Amount',
          getValue: (claim) => formatCurrency(claim.data?.amount),
          render: (claim) => (
            <Text strong style={{ fontSize: 14 }}>{formatCurrency(claim.data?.amount)}</Text>
          ),
        },
      ],
    },
  ],
};

export const claimFormConfig = {
  title: 'Create New Claim',
  submitButtonText: 'Create Claim',
  submitButtonLoadingText: 'Creating Claim...',
  initialValues: {
    status: 'PENDING',
  },
  onFillSampleData: () => {
    const sampleData = generateClaimSampleData();
    return {
      ...sampleData,
      incidentDate: dayjs(sampleData.incidentDate),
    };
  },

  fields: [
    {
      name: 'claimNumber',
      label: 'Claim Number',
      component: (
        <Input
          prefix={<FileTextOutlined />}
          placeholder="CLM-2024-001"
          size="large"
        />
      ),
      rules: [
        { required: true, message: 'Please enter a claim number' },
        { min: 3, message: 'Claim number must be at least 3 characters' },
      ],
    },
    {
      name: 'claimantName',
      label: 'Claimant Name',
      component: (
        <Input
          prefix={<UserOutlined />}
          placeholder="Jane Smith"
          size="large"
        />
      ),
      rules: [
        { required: true, message: 'Please enter the claimant name' },
        { min: 2, message: 'Name must be at least 2 characters' },
      ],
    },
    {
      name: 'incidentDate',
      label: 'Incident Date',
      component: <DatePicker id="incidentDate" size="large" style={{ width: '100%' }} format="MM/DD/YYYY" />,
      rules: [{ required: true, message: 'Please select the incident date' }],
      transform: (value) => value?.format('YYYY-MM-DD'),
    },
    {
      name: 'amount',
      label: 'Claim Amount',
      component: (
        <InputNumber
          id="amount"
          prefix={<DollarOutlined />}
          placeholder="5000.00"
          size="large"
          style={{ width: '100%' }}
          min={0}
          precision={2}
        />
      ),
      rules: [
        { required: true, message: 'Please enter the claim amount' },
        { type: 'number', min: 0, message: 'Amount must be positive' },
      ],
    },
    {
      name: 'description',
      label: 'Description',
      component: (
        <TextArea
          placeholder="Describe the incident..."
          rows={4}
        />
      ),
      rules: [
        { required: true, message: 'Please enter a description' },
        { min: 10, message: 'Description must be at least 10 characters' },
      ],
    },
    {
      name: 'status',
      label: 'Status',
      component: (
        <Select size="large" options={CLAIM_STATUS_OPTIONS} />
      ),
      rules: [{ required: true, message: 'Please select a status' }],
    },
  ],
};
