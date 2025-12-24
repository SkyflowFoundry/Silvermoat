/**
 * Policy Detail Page
 * Displays detailed information about a specific policy
 */

import { Card, Descriptions, Button, Space, Typography, Spin, Alert } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { usePolicy } from '../../hooks/queries/usePolicy';
import { formatTimestamp, formatDate, formatCurrency } from '../../utils/formatters';
import StatusTag from '../../components/common/StatusTag';

const { Title } = Typography;

const PolicyDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: policy, isLoading, error } = usePolicy(id);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading policy details..." />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error Loading Policy"
        description={error.message || 'Failed to load policy details'}
        type="error"
        showIcon
      />
    );
  }

  if (!policy) {
    return (
      <Alert
        message="Policy Not Found"
        description="The requested policy could not be found."
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
          onClick={() => navigate('/policies')}
        >
          Back to Policies
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Policy Details
            </Title>
          </Space>
        }
      >
        <Descriptions
          bordered
          column={{ xs: 1, sm: 1, md: 2, lg: 2, xl: 2 }}
          size="middle"
        >
          <Descriptions.Item label="Policy ID" span={2}>
            {policy.id}
          </Descriptions.Item>

          <Descriptions.Item label="Policy Number">
            {policy.data?.policyNumber || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Status">
            <StatusTag type="policy" value={policy.data?.status} />
          </Descriptions.Item>

          <Descriptions.Item label="Policy Holder">
            {policy.data?.holderName || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Annual Premium">
            {formatCurrency(policy.data?.premium)}
          </Descriptions.Item>

          <Descriptions.Item label="Effective Date">
            {formatDate(policy.data?.effectiveDate)}
          </Descriptions.Item>

          <Descriptions.Item label="Expiration Date">
            {formatDate(policy.data?.expirationDate)}
          </Descriptions.Item>

          {policy.data?.quoteId && (
            <Descriptions.Item label="Related Quote ID" span={2}>
              <Button
                type="link"
                onClick={() => navigate(`/quotes/${policy.data.quoteId}`)}
                style={{ padding: 0 }}
              >
                {policy.data.quoteId}
              </Button>
            </Descriptions.Item>
          )}

          <Descriptions.Item label="Created At" span={2}>
            {formatTimestamp(policy.createdAt)}
          </Descriptions.Item>
        </Descriptions>

        {/* Display raw data for debugging/demo purposes */}
        <Card
          type="inner"
          title="Raw Data"
          size="small"
          style={{ marginTop: 24 }}
        >
          <pre
            style={{
              background: '#f5f5f5',
              padding: 16,
              borderRadius: 4,
              overflow: 'auto',
              maxHeight: 400,
            }}
          >
            {JSON.stringify(policy, null, 2)}
          </pre>
        </Card>
      </Card>
    </div>
  );
};

export default PolicyDetail;
