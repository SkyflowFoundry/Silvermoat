/**
 * Customer Detail Page
 * Displays and allows editing of a single customer
 */

import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Spin, Alert, Space, Descriptions, Tag, Typography } from 'antd';
import { ArrowLeftOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useCustomer } from '../../hooks/queries/useCustomer';
import { deleteCustomer } from '../../services/customers';
import { formatTimestamp } from '../../utils/formatters';

const { Title } = Typography;

const STATUS_COLORS = {
  ACTIVE: 'green',
  INACTIVE: 'gray',
  ARCHIVED: 'red',
};

const CustomerDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: customer, isLoading, error } = useCustomer(id);

  const handleBack = () => {
    navigate('/customers');
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this customer?')) {
      try {
        await deleteCustomer(id);
        navigate('/customers');
      } catch (err) {
        console.error('Failed to delete customer:', err);
        alert('Failed to delete customer');
      }
    }
  };

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '48px' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (error || !customer) {
    return (
      <Alert
        message="Error"
        description="Failed to load customer details"
        type="error"
        showIcon
      />
    );
  }

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={handleBack}>
          Back to Customers
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Customer Details
            </Title>
            <Tag color={STATUS_COLORS[customer.status] || 'default'}>
              {customer.status || 'ACTIVE'}
            </Tag>
          </Space>
        }
        extra={
          <Space>
            <Button icon={<EditOutlined />} disabled>
              Edit
            </Button>
            <Button icon={<DeleteOutlined />} danger onClick={handleDelete}>
              Delete
            </Button>
          </Space>
        }
      >
        <Descriptions column={2} bordered>
          <Descriptions.Item label="Customer ID">{customer.id}</Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={STATUS_COLORS[customer.status] || 'default'}>
              {customer.status || 'ACTIVE'}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Name">{customer.data?.name || '-'}</Descriptions.Item>
          <Descriptions.Item label="Email">{customer.data?.email || '-'}</Descriptions.Item>
          <Descriptions.Item label="Phone">{customer.data?.phone || '-'}</Descriptions.Item>
          <Descriptions.Item label="Date of Birth">
            {customer.data?.dateOfBirth || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Address" span={2}>
            {customer.data?.address || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Emergency Contact" span={2}>
            {customer.data?.emergencyContact || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(customer.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Last Updated">
            {formatTimestamp(customer.updatedAt)}
          </Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
};

export default CustomerDetail;
