/**
 * Recent Activity Component
 * Displays a table of recently created entities across all types
 */

import { Table, Tag, Button } from 'antd';
import { EyeOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { formatTimestamp } from '../../utils/formatters';
import { ENTITY_LABELS } from '../../config/constants';

const RecentActivity = () => {
  const navigate = useNavigate();

  // Placeholder data - in a real app, this would come from API or aggregated from context
  const recentItems = [];

  const columns = [
    {
      title: 'Type',
      dataIndex: 'type',
      key: 'type',
      width: 100,
      render: (type) => {
        const colorMap = {
          quote: 'blue',
          policy: 'green',
          claim: 'orange',
          payment: 'cyan',
          case: 'purple',
        };
        return (
          <Tag color={colorMap[type]}>
            {ENTITY_LABELS[type] || type}
          </Tag>
        );
      },
    },
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 200,
      ellipsis: true,
      render: (id) => (
        <span style={{ fontFamily: 'monospace', fontSize: 12 }}>
          {id?.substring(0, 8)}...
        </span>
      ),
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
      render: (_, record) => {
        // Generate a description based on the entity type and data
        if (record.type === 'quote') {
          return `Quote for ${record.data?.name || 'N/A'}`;
        } else if (record.type === 'policy') {
          return `Policy #${record.data?.policyNumber || 'N/A'} - ${record.data?.holderName || 'N/A'}`;
        } else if (record.type === 'claim') {
          return `Claim #${record.data?.claimNumber || 'N/A'} - ${record.data?.claimantName || 'N/A'}`;
        } else if (record.type === 'payment') {
          return `Payment of $${record.data?.amount || '0'} via ${record.data?.method || 'N/A'}`;
        } else if (record.type === 'case') {
          return record.data?.title || 'N/A';
        }
        return '-';
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
    {
      title: 'Actions',
      key: 'actions',
      width: 100,
      fixed: 'right',
      render: (_, record) => (
        <Button
          type="link"
          size="small"
          icon={<EyeOutlined />}
          onClick={() => navigate(`/${record.type}s/${record.id}`)}
        >
          View
        </Button>
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={recentItems}
      rowKey={(record) => `${record.type}-${record.id}`}
      pagination={false}
      size="small"
      locale={{
        emptyText: 'No recent activity. Start by creating a quote, policy, claim, payment, or case.',
      }}
    />
  );
};

export default RecentActivity;
