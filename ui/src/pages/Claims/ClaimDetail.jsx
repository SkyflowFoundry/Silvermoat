/**
 * Claim Detail Page
 * Displays detailed claim information with status update and doc upload
 */

import { useState } from 'react';
import { Card, Descriptions, Button, Space, Typography, Spin, Alert } from 'antd';
import { ArrowLeftOutlined, EditOutlined, FileAddOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { useClaim } from '../../hooks/queries/useClaim';
import { formatTimestamp, formatDate, formatCurrency } from '../../utils/formatters';
import StatusTag from '../../components/common/StatusTag';
import ClaimStatusUpdate from './ClaimStatusUpdate';
import ClaimDocUpload from './ClaimDocUpload';

const { Title } = Typography;

const ClaimDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: claim, isLoading, error } = useClaim(id);
  const [statusModalOpen, setStatusModalOpen] = useState(false);
  const [docModalOpen, setDocModalOpen] = useState(false);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading claim details..." />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error Loading Claim"
        description={error.message || 'Failed to load claim details'}
        type="error"
        showIcon
      />
    );
  }

  if (!claim) {
    return (
      <Alert
        message="Claim Not Found"
        description="The requested claim could not be found."
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
          onClick={() => navigate('/claims')}
        >
          Back to Claims
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Claim Details
            </Title>
          </Space>
        }
        extra={
          <Space>
            <Button
              type="primary"
              icon={<EditOutlined />}
              onClick={() => setStatusModalOpen(true)}
            >
              Update Status
            </Button>
            <Button
              icon={<FileAddOutlined />}
              onClick={() => setDocModalOpen(true)}
            >
              Upload Document
            </Button>
          </Space>
        }
      >
        <Descriptions
          bordered
          column={{ xs: 1, sm: 1, md: 2, lg: 2, xl: 2 }}
          size="middle"
        >
          <Descriptions.Item label="Claim ID" span={2}>
            {claim.id}
          </Descriptions.Item>

          <Descriptions.Item label="Claim Number">
            {claim.data?.claimNumber || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Status">
            <StatusTag type="claim" value={claim.data?.status} />
          </Descriptions.Item>

          <Descriptions.Item label="Claimant Name">
            {claim.data?.claimantName || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Claim Amount">
            {formatCurrency(claim.data?.amount)}
          </Descriptions.Item>

          <Descriptions.Item label="Incident Date" span={2}>
            {formatDate(claim.data?.incidentDate)}
          </Descriptions.Item>

          <Descriptions.Item label="Description" span={2}>
            {claim.data?.description || '-'}
          </Descriptions.Item>

          {claim.data?.policyId && (
            <Descriptions.Item label="Related Policy ID" span={2}>
              <Button
                type="link"
                onClick={() => navigate(`/policies/${claim.data.policyId}`)}
                style={{ padding: 0 }}
              >
                {claim.data.policyId}
              </Button>
            </Descriptions.Item>
          )}

          <Descriptions.Item label="Created At" span={2}>
            {formatTimestamp(claim.createdAt)}
          </Descriptions.Item>
        </Descriptions>

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
            {JSON.stringify(claim, null, 2)}
          </pre>
        </Card>
      </Card>

      <ClaimStatusUpdate
        open={statusModalOpen}
        onClose={() => setStatusModalOpen(false)}
        claim={claim}
      />

      <ClaimDocUpload
        open={docModalOpen}
        onClose={() => setDocModalOpen(false)}
        claim={claim}
      />
    </div>
  );
};

export default ClaimDetail;
