/**
 * Case Detail Page
 * Displays detailed information about a specific case
 */

import { Card, Descriptions, Button, Space, Typography, Spin, Alert, Tag } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { useCase } from '../../hooks/queries/useCase';
import { formatTimestamp } from '../../utils/formatters';

const { Title, Paragraph } = Typography;

const PRIORITY_COLORS = {
  LOW: 'green',
  MEDIUM: 'blue',
  HIGH: 'orange',
  URGENT: 'red',
};

const STATUS_COLORS = {
  OPEN: 'orange',
  IN_PROGRESS: 'blue',
  RESOLVED: 'green',
  CLOSED: 'default',
};

const CaseDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: caseItem, isLoading, error } = useCase(id);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="Loading case details..." />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error Loading Case"
        description={error.message || 'Failed to load case details'}
        type="error"
        showIcon
      />
    );
  }

  if (!caseItem) {
    return (
      <Alert
        message="Case Not Found"
        description="The requested case could not be found."
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
          onClick={() => navigate('/cases')}
        >
          Back to Cases
        </Button>
      </Space>

      <Card
        title={
          <Space>
            <Title level={3} style={{ margin: 0 }}>
              Case Details
            </Title>
          </Space>
        }
      >
        <Descriptions
          bordered
          column={{ xs: 1, sm: 1, md: 2, lg: 2, xl: 2 }}
          size="middle"
        >
          <Descriptions.Item label="Case ID" span={2}>
            {caseItem.id}
          </Descriptions.Item>
          <Descriptions.Item label="Subject" span={2}>
            <strong>{caseItem.data?.subject || '-'}</strong>
          </Descriptions.Item>
          <Descriptions.Item label="Description" span={2}>
            {caseItem.data?.description ? (
              <Paragraph style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
                {caseItem.data.description}
              </Paragraph>
            ) : '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Customer Email">
            {caseItem.data?.customerEmail || '-'}
          </Descriptions.Item>
          <Descriptions.Item label="Assignee">
            {caseItem.data?.assignee || 'Unassigned'}
          </Descriptions.Item>
          <Descriptions.Item label="Priority">
            <Tag color={PRIORITY_COLORS[caseItem.data?.priority] || 'default'}>
              {caseItem.data?.priority || 'MEDIUM'}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={STATUS_COLORS[caseItem.data?.status] || 'default'}>
              {caseItem.data?.status || 'OPEN'}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Created">
            {formatTimestamp(caseItem.createdAt)}
          </Descriptions.Item>
          <Descriptions.Item label="Record Status">
            {caseItem.status || 'ACTIVE'}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {/* Raw Data (for debugging) */}
      <Card title="Raw Data" style={{ marginTop: 24 }} size="small">
        <pre style={{ maxHeight: '400px', overflow: 'auto', fontSize: '12px' }}>
          {JSON.stringify(caseItem, null, 2)}
        </pre>
      </Card>
    </div>
  );
};

export default CaseDetail;
