/**
 * Loan Detail Page
 * Displays and allows editing of a single loan
 */

import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Spin, Alert, Space, Descriptions, Tag, Typography } from 'antd';
import { ArrowLeftOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useLoan } from '../../hooks/queries/useLoan';
import { deleteLoan } from '../../services/loans';
import { formatTimestamp } from '../../utils/formatters';

const { Title } = Typography;

const STATUS_COLORS = {
  ACTIVE: 'green',
  FILLED: 'blue',
  EXPIRED: 'gray',
  CANCELLED: 'red',
};

const LoanDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: loan, isLoading, error } = useLoan(id);

  const handleBack = () => {
    navigate('/loans');
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this loan?')) {
      try {
        await deleteLoan(id);
        navigate('/loans');
      } catch (err) {
        console.error('Failed to delete loan:', err);
        alert('Failed to delete loan');
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

  if (error || !loan) {
    return (
      <Alert
        message="Error"
        description="Failed to load loan details"
        type="error"
        showIcon
      />
    );
  }

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={handleBack}>
          Back to Loans
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Loan Details
            </Title>
            <Tag color={STATUS_COLORS[loan.status] || 'default'}>
              {loan.status || 'ACTIVE'}
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
          <Descriptions.Item label="Loan ID">{loan.id}</Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={STATUS_COLORS[loan.status] || 'default'}>
              {loan.status || 'ACTIVE'}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Customer">
            {loan.data?.customerName || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Prescriber">
            {loan.data?.prescriber || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Medication">
            {loan.data?.medication || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Dosage">
            {loan.data?.dosage || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Frequency">
            {loan.data?.frequency || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Duration">
            {loan.data?.duration || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Refills Allowed">
            {loan.data?.refillsAllowed ?? '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Instructions" span={2}>
            {loan.data?.instructions || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(loan.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Last Updated">
            {formatTimestamp(loan.updatedAt)}
          </Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
};

export default LoanDetail;
