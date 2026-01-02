/**
 * Payment Table Component
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

const PaymentTable = ({ payments = [], loading = false }) => {
  const navigate = useNavigate();
  const { isMobile } = useAppContext();

  const columns = [
    {
      title: 'Payment ID',
      dataIndex: 'id',
      key: 'id',
      width: 280,
      render: (id) => (
        <Button
          type="link"
          onClick={() => navigate(`/payments/${id}`)}
          style={{ padding: 0 }}
        >
          {id.substring(0, 8)}...
        </Button>
      ),
      ellipsis: true,
    },
    {
      title: 'Payment Date',
      dataIndex: ['data', 'paymentDate'],
      key: 'paymentDate',
      width: 130,
      sorter: (a, b) => (a.data?.paymentDate || '').localeCompare(b.data?.paymentDate || ''),
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
      title: 'Method',
      dataIndex: ['data', 'method'],
      key: 'method',
      width: 100,
      filters: [
        { text: 'Card', value: 'CARD' },
        { text: 'ACH', value: 'ACH' },
        { text: 'Check', value: 'CHECK' },
      ],
      onFilter: (value, record) => record.data?.method === value,
      render: (method) => method || '-',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      filters: [
        { text: 'Pending', value: 'PENDING' },
        { text: 'Completed', value: 'COMPLETED' },
        { text: 'Failed', value: 'FAILED' },
      ],
      onFilter: (value, record) => record.status === value,
      render: (status) => <StatusTag type="payment" value={status} />,
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
            onClick={() => navigate(`/payments/${record.id}`)}
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
        dataSource={payments}
        pagination={{
          pageSize: DEFAULT_PAGE_SIZE,
          showSizeChanger: false,
          size: 'small',
        }}
        renderItem={(payment) => (
          <Card
            size="small"
            style={{ marginBottom: 12 }}
            onClick={() => navigate(`/payments/${payment.id}`)}
            hoverable
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ flex: 1 }}>
                  <Text type="secondary" style={{ fontSize: 12 }}>Payment ID</Text>
                  <div>
                    <Text strong style={{ fontSize: 13 }} ellipsis>
                      {payment.id.substring(0, 16)}...
                    </Text>
                  </div>
                </div>
                <StatusTag type="payment" value={payment.data?.status} />
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16 }}>
                <div style={{ flex: 1 }}>
                  <Text type="secondary" style={{ fontSize: 12 }}>Payment Date</Text>
                  <div><Text style={{ fontSize: 14 }}>{formatDate(payment.data?.paymentDate)}</Text></div>
                </div>
                <div>
                  <Text type="secondary" style={{ fontSize: 12 }}>Method</Text>
                  <div><Text style={{ fontSize: 14 }}>{payment.data?.method || '-'}</Text></div>
                </div>
              </div>
              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>Amount</Text>
                <div><Text strong style={{ fontSize: 16 }}>{formatCurrency(payment.data?.amount)}</Text></div>
              </div>
              <Button
                type="primary"
                size="small"
                icon={<EyeOutlined />}
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/payments/${payment.id}`);
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
      dataSource={payments}
      loading={loading}
      rowKey="id"
      pagination={{
        pageSize: DEFAULT_PAGE_SIZE,
        showSizeChanger: true,
        showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} payments`,
        pageSizeOptions: ['10', '20', '50', '100'],
      }}
      scroll={{ x: 1000 }}
      size="middle"
      bordered
    />
  );
};

export default PaymentTable;
