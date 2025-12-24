/**
 * Case Table Component
 * On mobile, displays as card list
 */

import { Table, Button, Space, Card, List, Typography } from 'antd';
import { EyeOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { formatTimestamp } from '../../utils/formatters';
import { DEFAULT_PAGE_SIZE, CASE_PRIORITY_OPTIONS, CASE_STATUS_OPTIONS, ENTITY_LABELS } from '../../config/constants';
import StatusTag from '../../components/common/StatusTag';
import { useAppContext } from '../../contexts/AppContext';

const { Text } = Typography;

const CaseTable = ({ cases = [], loading = false }) => {
  const navigate = useNavigate();
  const { isMobile } = useAppContext();

  const columns = [
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
      dataIndex: ['data', 'status'],
      key: 'status',
      width: 120,
      filters: CASE_STATUS_OPTIONS.map((opt) => ({
        text: opt.label,
        value: opt.value,
      })),
      onFilter: (value, record) => record.data?.status === value,
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
            onClick={() => navigate(`/cases/${record.id}`)}
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
        dataSource={cases}
        pagination={{
          pageSize: DEFAULT_PAGE_SIZE,
          showSizeChanger: false,
          size: 'small',
        }}
        renderItem={(caseItem) => (
          <Card
            size="small"
            style={{ marginBottom: 12 }}
            onClick={() => navigate(`/cases/${caseItem.id}`)}
            hoverable
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>Title</Text>
                <div><Text strong style={{ fontSize: 14 }}>{caseItem.data?.title || '-'}</Text></div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8 }}>
                <StatusTag type="case-priority" value={caseItem.data?.priority} />
                <StatusTag type="case-status" value={caseItem.data?.status} />
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16 }}>
                <div style={{ flex: 1 }}>
                  <Text type="secondary" style={{ fontSize: 12 }}>Assignee</Text>
                  <div><Text style={{ fontSize: 13 }}>{caseItem.data?.assignee || 'Unassigned'}</Text></div>
                </div>
                <div>
                  <Text type="secondary" style={{ fontSize: 12 }}>Related</Text>
                  <div><Text style={{ fontSize: 13 }}>{ENTITY_LABELS[caseItem.data?.relatedEntityType] || '-'}</Text></div>
                </div>
              </div>
              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>Created</Text>
                <div><Text style={{ fontSize: 13 }}>{formatTimestamp(caseItem.createdAt)}</Text></div>
              </div>
              <Button
                type="primary"
                size="small"
                icon={<EyeOutlined />}
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/cases/${caseItem.id}`);
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
      dataSource={cases}
      loading={loading}
      rowKey="id"
      pagination={{
        pageSize: DEFAULT_PAGE_SIZE,
        showSizeChanger: true,
        showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} cases`,
        pageSizeOptions: ['10', '20', '50', '100'],
      }}
      scroll={{ x: 1000 }}
      size="middle"
      bordered
    />
  );
};

export default CaseTable;
