/**
 * Customer Detail Page
 * Displays detailed information about a specific customer
 */

import { Card, Descriptions, Button, Space, Typography, Spin, Alert } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { useCustomer } from '../../hooks/queries/useCustomer';

const { Title } = Typography;

const CustomerDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: customer, isLoading, error } = useCustomer(id);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading customer details..." />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error Loading Customer"
        description={error.message || 'Failed to load customer details'}
        type="error"
        showIcon
      />
    );
  }

  if (!customer) {
    return (
      <Alert
        message="Customer Not Found"
        description="The requested customer could not be found."
        type="warning"
        showIcon
      />
    );
  }

  return (
    <div>
      <Space style={{ marginBottom: 24 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/customers')}
        >
          Back to Customers
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Customer Details
            </Title>
          </Space>
        }
      >
        <Descriptions
          bordered
          column={{ xs: 1, sm: 1, md: 2, lg: 2, xl: 2 }}
          size="middle"
        >
          <Descriptions.Item label="Customer ID" span={2}>
            {customer.id}
          </Descriptions.Item>

          <Descriptions.Item label="Name">
            {customer.name || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Email">
            {customer.email || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Phone">
            {customer.phone || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Status">
            {customer.status || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Address" span={2}>
            {customer.address || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="City">
            {customer.city || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="State">
            {customer.state || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="ZIP Code">
            {customer.zip || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Date of Birth">
            {customer.date_of_birth ? new Date(customer.date_of_birth).toLocaleDateString() : '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Created At" span={2}>
            {customer.created_at ? new Date(customer.created_at).toLocaleString() : '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Last Updated" span={2}>
            {customer.updated_at ? new Date(customer.updated_at).toLocaleString() : '-'}
          </Descriptions.Item>
        </Descriptions>

        {/* Display raw data for debugging/demo purposes */}
        <Card
          type="inner"
          title="Raw Data"
          size="small"
          style={{ marginTop: 24 }}
        >
          <pre style={{ margin: 0, fontSize: 12 }}>
            {JSON.stringify(customer, null, 2)}
          </pre>
        </Card>
      </Card>
    </div>
  );
};

export default CustomerDetail;
