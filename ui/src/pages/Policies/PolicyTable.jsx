/**
 * Policy Table Component
 * Displays policies in a professional data table with sorting and actions
 * On mobile, displays as card list
 */

import { Table, Button, Space, Card, List, Typography } from 'antd';
import { EyeOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { formatTimestamp, formatDate, formatCurrency } from '../../utils/formatters';
import { DEFAULT_PAGE_SIZE } from '../../config/constants';
import StatusTag from '../../components/common/StatusTag';
import { useAppContext } from '../../contexts/AppContext';

const { Text } = Typography;

const PolicyTable = ({ policies = [], loading = false }) => {
  const navigate = useNavigate();
  const { isMobile } = useAppContext();

  const columns = [
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
    {
      title: 'Actions',
      key: 'actions',
      width: 120,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small">
          <Button
            type="default"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => navigate(`/policies/${record.id}`)}
          >
            View
          </Button>
        </Space>
      ),
    },
  ];

  // Mobile card view
  if (isMobile) {
    return (
      <List
        loading={loading}
        dataSource={policies}
        pagination={{
          pageSize: DEFAULT_PAGE_SIZE,
          showSizeChanger: false,
          size: 'small',
        }}
        renderItem={(policy) => (
          <Card
            size="small"
            style={{ marginBottom: 12 }}
            onClick={() => navigate(`/policies/${policy.id}`)}
            hoverable
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ flex: 1 }}>
                  <Text type="secondary" style={{ fontSize: 12 }}>Policy Number</Text>
                  <div><Text strong style={{ fontSize: 14 }}>{policy.data?.policyNumber || '-'}</Text></div>
                </div>
                <StatusTag type="policy" value={policy.data?.status} />
              </div>
              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>Holder Name</Text>
                <div><Text style={{ fontSize: 14 }}>{policy.data?.holderName || '-'}</Text></div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16 }}>
                <div style={{ flex: 1 }}>
                  <Text type="secondary" style={{ fontSize: 12 }}>Effective</Text>
                  <div><Text style={{ fontSize: 13 }}>{formatDate(policy.data?.effectiveDate)}</Text></div>
                </div>
                <div style={{ flex: 1 }}>
                  <Text type="secondary" style={{ fontSize: 12 }}>Expires</Text>
                  <div><Text style={{ fontSize: 13 }}>{formatDate(policy.data?.expirationDate)}</Text></div>
                </div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <Text type="secondary" style={{ fontSize: 12 }}>Premium</Text>
                  <div><Text strong style={{ fontSize: 15 }}>{formatCurrency(policy.data?.premium)}</Text></div>
                </div>
                <Button
                  type="primary"
                  size="small"
                  icon={<EyeOutlined />}
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/policies/${policy.id}`);
                  }}
                >
                  View
                </Button>
              </div>
            </Space>
          </Card>
        )}
      />
    );
  }

  // Desktop table view
  return (
    <Table
      columns={columns}
      dataSource={policies}
      loading={loading}
      rowKey="id"
      pagination={{
        pageSize: DEFAULT_PAGE_SIZE,
        showSizeChanger: true,
        showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} policies`,
        pageSizeOptions: ['10', '20', '50', '100'],
      }}
      scroll={{ x: 1200 }}
      size="middle"
      bordered
    />
  );
};

export default PolicyTable;
