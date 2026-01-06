/**
 * Case Detail Page
 */

import { Card, Descriptions, Button, Space, Typography, Spin, Alert } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { useCase } from '../../hooks/queries/useCase';
import { formatTimestamp } from '../../utils/formatters';
import { ENTITY_LABELS } from '../../config/constants';
import StatusTag from '../../components/common/StatusTag';

const { Title } = Typography;

const CaseDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: caseData, isLoading, error } = useCase(id);

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

  if (!caseData) {
    return (
      <Alert
        message="Case Not Found"
        description="The requested case could not be found."
        type="warning"
        showIcon
      />
    );
  }

  const handleNavigateToRelatedEntity = () => {
    const entityType = caseData.data?.relatedEntityType;
    const entityId = caseData.data?.relatedEntityId;
    if (entityType && entityId) {
      navigate(`/${entityType}s/${entityId}`);
    }
  };

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
            {caseData.id}
          </Descriptions.Item>

          <Descriptions.Item label="Title" span={2}>
            {caseData.data?.title || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Description" span={2}>
            {caseData.data?.description || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Related Entity Type">
            {ENTITY_LABELS[caseData.data?.relatedEntityType] || '-'}
          </Descriptions.Item>

          <Descriptions.Item label="Related Entity ID">
            {caseData.data?.relatedEntityId ? (
              <Button
                type="link"
                onClick={handleNavigateToRelatedEntity}
                style={{ padding: 0 }}
              >
                {caseData.data.relatedEntityId}
              </Button>
            ) : (
              '-'
            )}
          </Descriptions.Item>

          <Descriptions.Item label="Assignee">
            {caseData.data?.assignee || 'Unassigned'}
          </Descriptions.Item>

          <Descriptions.Item label="Priority">
            <StatusTag type="case-priority" value={caseData.data?.priority} />
          </Descriptions.Item>

          <Descriptions.Item label="Status" span={2}>
            <StatusTag type="case-status" value={caseData.data?.status} />
          </Descriptions.Item>

          <Descriptions.Item label="Created At" span={2}>
            {formatTimestamp(caseData.createdAt)}
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
            {JSON.stringify(caseData, null, 2)}
          </pre>
        </Card>
      </Card>
    </div>
  );
};

export default CaseDetail;
