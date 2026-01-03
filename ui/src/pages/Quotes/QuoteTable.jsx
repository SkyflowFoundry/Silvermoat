/**
 * Quote Table Component
 * Displays quotes in a professional data table with sorting and actions
 * On mobile, displays as card list
 */

import { Table, Button, Space, Card, List, Typography } from 'antd';
import { EyeOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { formatTimestamp } from '../../utils/formatters';
import { DEFAULT_PAGE_SIZE } from '../../config/constants';
import { useAppContext } from '../../contexts/AppContext';

const { Text } = Typography;

const QuoteTable = ({ quotes = [], loading = false }) => {
  const navigate = useNavigate();
  const { isMobile } = useAppContext();

  const columns = [
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
        // Extract ZIP from propertyAddress (last 5 digits)
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
            onClick={() => navigate(`/quotes/${record.id}`)}
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
        dataSource={quotes}
        pagination={{
          pageSize: DEFAULT_PAGE_SIZE,
          showSizeChanger: false,
          size: 'small',
        }}
        renderItem={(quote) => (
          <Card
            size="small"
            style={{ marginBottom: 12 }}
            onClick={() => navigate(`/quotes/${quote.id}`)}
            hoverable
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>Quote ID</Text>
                <div>
                  <Text strong style={{ fontSize: 13 }} ellipsis>
                    {quote.id}
                  </Text>
                </div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16 }}>
                <div style={{ flex: 1 }}>
                  <Text type="secondary" style={{ fontSize: 12 }}>Name</Text>
                  <div><Text style={{ fontSize: 14 }}>{quote.data?.customerName || '-'}</Text></div>
                </div>
                <div>
                  <Text type="secondary" style={{ fontSize: 12 }}>ZIP</Text>
                  <div><Text style={{ fontSize: 14 }}>
                    {(() => {
                      const address = quote.data?.propertyAddress || '';
                      const zipMatch = address.match(/\b\d{5}\b/);
                      return zipMatch ? zipMatch[0] : '-';
                    })()}
                  </Text></div>
                </div>
              </div>
              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>Created</Text>
                <div><Text style={{ fontSize: 13 }}>{formatTimestamp(quote.createdAt)}</Text></div>
              </div>
              <Button
                type="primary"
                size="small"
                icon={<EyeOutlined />}
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/quotes/${quote.id}`);
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
      dataSource={quotes}
      loading={loading}
      rowKey="id"
      pagination={{
        pageSize: DEFAULT_PAGE_SIZE,
        showSizeChanger: true,
        showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} quotes`,
        pageSizeOptions: ['10', '20', '50', '100'],
      }}
      scroll={{ x: 800 }}
      size="middle"
      bordered
    />
  );
};

export default QuoteTable;
