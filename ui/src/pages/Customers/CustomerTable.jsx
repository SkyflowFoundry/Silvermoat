/**
 * Customer Table Component
 * Displays customers in a professional data table with sorting and actions
 * On mobile, displays as card list
 */

import { Table, Button, Space, Card, List, Typography, Popconfirm } from 'antd';
import { EyeOutlined, DeleteOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { formatTimestamp } from '../../utils/formatters';
import { DEFAULT_PAGE_SIZE } from '../../config/constants';
import { useAppContext } from '../../contexts/AppContext';
import { useDeleteCustomer } from '../../hooks/mutations/useDeleteCustomer';

const { Text } = Typography;

const CustomerTable = ({ customers = [], loading = false }) => {
  const navigate = useNavigate();
  const { isMobile } = useAppContext();
  const deleteCustomerMutation = useDeleteCustomer();

  const handleDelete = async (id) => {
    try {
      await deleteCustomerMutation.mutateAsync(id);
    } catch (error) {
      console.error('Failed to delete customer:', error);
    }
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      sorter: (a, b) => (a.name || '').localeCompare(b.name || ''),
      render: (name, record) => (
        <Button
          type="link"
          onClick={() => navigate(`/customers/${record.id}`)}
          style={{ padding: 0 }}
        >
          {name || '-'}
        </Button>
      ),
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
      sorter: (a, b) => (a.email || '').localeCompare(b.email || ''),
      render: (email) => email || '-',
    },
    {
      title: 'Phone',
      dataIndex: 'phone',
      key: 'phone',
      width: 140,
      render: (phone) => phone || '-',
    },
    {
      title: 'City',
      dataIndex: 'city',
      key: 'city',
      width: 120,
      render: (city) => city || '-',
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      sorter: (a, b) => new Date(a.created_at) - new Date(b.created_at),
      render: (timestamp) => timestamp ? new Date(timestamp).toLocaleString() : '-',
      defaultSortOrder: 'descend',
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 160,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small">
          <Button
            type="default"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => navigate(`/customers/${record.id}`)}
          >
            View
          </Button>
          <Popconfirm
            title="Delete customer"
            description="Are you sure you want to delete this customer?"
            onConfirm={() => handleDelete(record.id)}
            okText="Yes"
            cancelText="No"
          >
            <Button
              type="default"
              size="small"
              danger
              icon={<DeleteOutlined />}
              loading={deleteCustomerMutation.isPending}
            >
              Delete
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  // Mobile card view
  if (isMobile) {
    return (
      <List
        loading={loading}
        dataSource={customers}
        pagination={{
          pageSize: DEFAULT_PAGE_SIZE,
          showSizeChanger: false,
          size: 'small',
        }}
        renderItem={(customer) => (
          <Card
            size="small"
            style={{ marginBottom: 12 }}
            onClick={() => navigate(`/customers/${customer.id}`)}
            hoverable
          >
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>Name</Text>
                <div>
                  <Text strong style={{ fontSize: 14 }}>
                    {customer.name || '-'}
                  </Text>
                </div>
              </div>
              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>Email</Text>
                <div><Text style={{ fontSize: 13 }}>{customer.email || '-'}</Text></div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16 }}>
                <div style={{ flex: 1 }}>
                  <Text type="secondary" style={{ fontSize: 12 }}>Phone</Text>
                  <div><Text style={{ fontSize: 13 }}>{customer.phone || '-'}</Text></div>
                </div>
                <div>
                  <Text type="secondary" style={{ fontSize: 12 }}>City</Text>
                  <div><Text style={{ fontSize: 13 }}>{customer.city || '-'}</Text></div>
                </div>
              </div>
              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>Created</Text>
                <div><Text style={{ fontSize: 12 }}>
                  {customer.created_at ? new Date(customer.created_at).toLocaleString() : '-'}
                </Text></div>
              </div>
              <Space style={{ width: '100%' }}>
                <Button
                  type="primary"
                  size="small"
                  icon={<EyeOutlined />}
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/customers/${customer.id}`)}
                  }
                  style={{ flex: 1 }}
                >
                  View
                </Button>
                <Popconfirm
                  title="Delete customer?"
                  onConfirm={(e) => {
                    e.stopPropagation();
                    handleDelete(customer.id);
                  }}
                  okText="Yes"
                  cancelText="No"
                >
                  <Button
                    danger
                    size="small"
                    icon={<DeleteOutlined />}
                    onClick={(e) => e.stopPropagation()}
                  >
                    Delete
                  </Button>
                </Popconfirm>
              </Space>
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
      dataSource={customers}
      loading={loading}
      rowKey="id"
      pagination={{
        pageSize: DEFAULT_PAGE_SIZE,
        showSizeChanger: true,
        showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} customers`,
      }}
      scroll={{ x: 1000 }}
    />
  );
};

export default CustomerTable;
