/**
 * Claim Table Component
 * Displays claims with status filtering and actions
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

const ClaimTable = ({ claims = [], loading = false }) => {
  const navigate = useNavigate();
  const { isMobile } = useAppContext();

  const columns = [
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
      dataIndex: ['data', 'status'],
      key: 'status',
      width: 110,
      filters: [
        { text: 'Pending', value: 'PENDING' },
        { text: 'Review', value: 'REVIEW' },
        { text: 'Approved', value: 'APPROVED' },
        { text: 'Denied', value: 'DENIED' },
      ],
      onFilter: (value, record) => record.data?.status === value,
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
            onClick={() => navigate(`/claims/${record.id}`)}
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
        dataSource={claims}
        pagination={{
          pageSize: DEFAULT_PAGE_SIZE,
          showSizeChanger: false,
          size: 'small',
        }}
        renderItem={(claim) => (
          <Card
            size="small"
            style={{ marginBottom: 12 }}
            onClick={() => navigate(`/claims/${claim.id}`)}
            hoverable
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ flex: 1 }}>
                  <Text type="secondary" style={{ fontSize: 12 }}>Claim Number</Text>
                  <div><Text strong style={{ fontSize: 14 }}>{claim.data?.claimNumber || '-'}</Text></div>
                </div>
                <StatusTag type="claim" value={claim.status} />
              </div>
              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>Claimant</Text>
                <div><Text style={{ fontSize: 14 }}>{claim.data?.claimantName || '-'}</Text></div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16 }}>
                <div style={{ flex: 1 }}>
                  <Text type="secondary" style={{ fontSize: 12 }}>Incident Date</Text>
                  <div><Text style={{ fontSize: 13 }}>{formatDate(claim.data?.incidentDate)}</Text></div>
                </div>
                <div>
                  <Text type="secondary" style={{ fontSize: 12 }}>Amount</Text>
                  <div><Text strong style={{ fontSize: 14 }}>{formatCurrency(claim.data?.amount)}</Text></div>
                </div>
              </div>
              <Button
                type="primary"
                size="small"
                icon={<EyeOutlined />}
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/claims/${claim.id}`);
                }}
                block
              >
                View Details
              </Button>
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
      dataSource={claims}
      loading={loading}
      rowKey="id"
      pagination={{
        pageSize: DEFAULT_PAGE_SIZE,
        showSizeChanger: true,
        showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} claims`,
        pageSizeOptions: ['10', '20', '50', '100'],
      }}
      scroll={{ x: 1100 }}
      size="middle"
      bordered
    />
  );
};

export default ClaimTable;
