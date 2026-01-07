/**
 * Provider Detail Page
 * Displays and allows editing of a single provider
 */

import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Spin, Alert, Space, Descriptions, Tag, Typography } from 'antd';
import { ArrowLeftOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useProvider } from '../../hooks/queries/useProvider';
import { deleteProvider } from '../../services/providers';
import { formatTimestamp } from '../../utils/formatters';

const { Title } = Typography;

const STATUS_COLORS = {
  ACTIVE: 'green',
  INACTIVE: 'gray',
  ARCHIVED: 'red',
};

const ProviderDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: provider, isLoading, error } = useProvider(id);

  const handleBack = () => {
    navigate('/providers');
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this provider?')) {
      try {
        await deleteProvider(id);
        navigate('/providers');
      } catch (err) {
        console.error('Failed to delete provider:', err);
        alert('Failed to delete provider');
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

  if (error || !provider) {
    return (
      <Alert
        message="Error"
        description="Failed to load provider details"
        type="error"
        showIcon
      />
    );
  }

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={handleBack}>
          Back to Providers
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Provider Details
            </Title>
            <Tag color={STATUS_COLORS[provider.status] || 'default'}>
              {provider.status || 'ACTIVE'}
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
          <Descriptions.Item label="Provider ID">{provider.id}</Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={STATUS_COLORS[provider.status] || 'default'}>
              {provider.status || 'ACTIVE'}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Name">{provider.data?.name || '-'}</Descriptions.Item>
          <Descriptions.Item label="Specialty">
            {provider.data?.specialty || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Email">{provider.data?.email || '-'}</Descriptions.Item>
          <Descriptions.Item label="Phone">{provider.data?.phone || '-'}</Descriptions.Item>
          <Descriptions.Item label="License Number">
            {provider.data?.licenseNumber || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Address" span={2}>
            {provider.data?.address || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Notes" span={2}>
            {provider.data?.notes || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(provider.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Last Updated">
            {formatTimestamp(provider.updatedAt)}
          </Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
};

export default ProviderDetail;
