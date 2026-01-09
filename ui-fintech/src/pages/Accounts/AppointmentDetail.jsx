/**
 * Account Detail Page
 * Displays and allows editing of a single account
 */

import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Spin, Alert, Space, Descriptions, Tag, Typography } from 'antd';
import { ArrowLeftOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useAccount } from '../../hooks/queries/useAccount';
import { deleteAccount } from '../../services/accounts';
import { formatTimestamp } from '../../utils/formatters';

const { Title } = Typography;

const STATUS_COLORS = {
  SCHEDULED: 'blue',
  CONFIRMED: 'cyan',
  COMPLETED: 'green',
  CANCELLED: 'red',
  NO_SHOW: 'orange',
};

const AccountDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: account, isLoading, error } = useAccount(id);

  const handleBack = () => {
    navigate('/accounts');
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this account?')) {
      try {
        await deleteAccount(id);
        navigate('/accounts');
      } catch (err) {
        console.error('Failed to delete account:', err);
        alert('Failed to delete account');
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

  if (error || !account) {
    return (
      <Alert
        message="Error"
        description="Failed to load account details"
        type="error"
        showIcon
      />
    );
  }

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={handleBack}>
          Back to Accounts
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Account Details
            </Title>
            <Tag color={STATUS_COLORS[account.status] || 'default'}>
              {account.status || 'SCHEDULED'}
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
          <Descriptions.Item label="Account ID">{account.id}</Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={STATUS_COLORS[account.status] || 'default'}>
              {account.status || 'SCHEDULED'}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Customer Name">
            {account.data?.customerName || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Customer Email">
            {account.data?.customerEmail || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Date & Time">
            {account.data?.date || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Provider">
            {account.data?.provider || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Type">
            {account.data?.type || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Reason" span={2}>
            {account.data?.reason || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Notes" span={2}>
            {account.data?.notes || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(account.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Last Updated">
            {formatTimestamp(account.updatedAt)}
          </Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
};

export default AccountDetail;
