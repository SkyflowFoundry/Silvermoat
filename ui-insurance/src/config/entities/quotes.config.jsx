/**
 * Quote Entity Configuration
 * Defines table columns, form fields, and mobile layout for quotes
 */

import { Button, Input, Typography } from 'antd';
import { UserOutlined, EnvironmentOutlined } from '@ant-design/icons';
import { formatTimestamp } from '../../utils/formatters';
import { generateQuoteSampleData } from '../../utils/formSampleData';

const { Text } = Typography;

export const quoteTableConfig = {
  entityName: 'quote',
  entityNamePlural: 'quotes',
  basePath: '/quotes',
  scrollX: 800,

  columns: (navigate) => [
    {
      title: 'Quote ID',
      dataIndex: 'id',
      key: 'id',
      width: 280,
      render: (id) => (
        <Button
          type="link"
          onClick={() => navigate(`/quotes/${id}`)}
          style={{ padding: 0 }}
        >
          {id}
        </Button>
      ),
      ellipsis: true,
    },
    {
      title: 'Name',
      dataIndex: ['data', 'customerName'],
      key: 'customerName',
      sorter: (a, b) => (a.data?.customerName || '').localeCompare(b.data?.customerName || ''),
      render: (name) => name || '-',
    },
    {
      title: 'ZIP Code',
      key: 'zip',
      width: 120,
      render: (_, record) => {
        const address = record.data?.propertyAddress || '';
        const zipMatch = address.match(/\b\d{5}\b/);
        return zipMatch ? zipMatch[0] : '-';
      },
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
      label: 'Quote ID',
      getValue: (quote) => quote.id,
      render: (quote) => (
        <Text strong style={{ fontSize: 13 }} ellipsis>
          {quote.id}
        </Text>
      ),
    },
    {
      layout: 'row',
      items: [
        {
          label: 'Name',
          getValue: (quote) => quote.data?.customerName || '-',
          flex: 1,
        },
        {
          label: 'ZIP',
          getValue: (quote) => {
            const address = quote.data?.propertyAddress || '';
            const zipMatch = address.match(/\b\d{5}\b/);
            return zipMatch ? zipMatch[0] : '-';
          },
        },
      ],
    },
    {
      label: 'Created',
      getValue: (quote) => formatTimestamp(quote.createdAt),
      render: (quote) => (
        <Text style={{ fontSize: 13 }}>{formatTimestamp(quote.createdAt)}</Text>
      ),
    },
  ],
};

export const quoteFormConfig = {
  title: 'Create New Quote',
  submitButtonText: 'Create Quote',
  submitButtonLoadingText: 'Creating Quote...',
  onFillSampleData: generateQuoteSampleData,

  fields: [
    {
      name: 'name',
      label: 'Full Name',
      component: (
        <Input
          prefix={<UserOutlined />}
          placeholder="Jane Doe"
          size="large"
        />
      ),
      rules: [
        { required: true, message: 'Please enter the customer name' },
        { min: 2, message: 'Name must be at least 2 characters' },
        { max: 100, message: 'Name must not exceed 100 characters' },
      ],
    },
    {
      name: 'zip',
      label: 'ZIP Code',
      component: (
        <Input
          prefix={<EnvironmentOutlined />}
          placeholder="12345"
          maxLength={5}
          size="large"
        />
      ),
      rules: [
        { required: true, message: 'Please enter a ZIP code' },
        {
          pattern: /^\d{5}$/,
          message: 'ZIP code must be exactly 5 digits',
        },
      ],
    },
  ],
};
