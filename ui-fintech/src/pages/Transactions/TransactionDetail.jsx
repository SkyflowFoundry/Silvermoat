/**
 * Transaction Detail Page
 * Displays and allows editing of a single transaction
 */

import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Spin, Alert, Space, Descriptions, Tag, Typography } from 'antd';
import { ArrowLeftOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useTransaction } from '../../hooks/queries/useTransaction';
import { deleteTransaction } from '../../services/transactions';
import { formatTimestamp } from '../../utils/formatters';

const { Title } = Typography;

const STATUS_COLORS = {
  ACTIVE: 'green',
  FILLED: 'blue',
  EXPIRED: 'gray',
  CANCELLED: 'red',
};

const TransactionDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: transaction, isLoading, error } = useTransaction(id);

  const handleBack = () => {
    navigate('/transactions');
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this transaction?')) {
      try {
        await deleteTransaction(id);
        navigate('/transactions');
      } catch (err) {
        console.error('Failed to delete transaction:', err);
        alert('Failed to delete transaction');
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

  if (error || !transaction) {
    return (
      <Alert
        message="Error"
        description="Failed to load transaction details"
        type="error"
        showIcon
      />
    );
  }

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={handleBack}>
          Back to Transactions
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Transaction Details
            </Title>
            <Tag color={STATUS_COLORS[transaction.status] || 'default'}>
              {transaction.status || 'ACTIVE'}
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
          <Descriptions.Item label="Transaction ID">{transaction.id}</Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={STATUS_COLORS[transaction.status] || 'default'}>
              {transaction.status || 'ACTIVE'}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Patient">
            {transaction.data?.patientName || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Prescriber">
            {transaction.data?.prescriber || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Medication">
            {transaction.data?.medication || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Dosage">
            {transaction.data?.dosage || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Frequency">
            {transaction.data?.frequency || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Duration">
            {transaction.data?.duration || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Refills Allowed">
            {transaction.data?.refillsAllowed ?? '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Instructions" span={2}>
            {transaction.data?.instructions || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(transaction.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Last Updated">
            {formatTimestamp(transaction.updatedAt)}
          </Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
};

export default TransactionDetail;
