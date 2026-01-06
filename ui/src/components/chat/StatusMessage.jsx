/**
 * Status Message Component
 * Displays operation log (status messages) during streaming chat responses
 */

import { Space, Typography, Collapse } from 'antd';
import { ClockCircleOutlined } from '@ant-design/icons';

const { Text } = Typography;
const { Panel } = Collapse;

const StatusMessage = ({ statusMessages = [] }) => {
  if (statusMessages.length === 0) return null;

  return (
    <Collapse
      ghost
      defaultActiveKey={['operations']}
      size="small"
      style={{
        marginTop: 8,
        backgroundColor: '#f5f5f5',
        borderRadius: 4,
        padding: '4px 8px',
      }}
    >
      <Panel
        header={
          <Text type="secondary" style={{ fontSize: 12 }}>
            Operation Log ({statusMessages.length} {statusMessages.length === 1 ? 'operation' : 'operations'})
          </Text>
        }
        key="operations"
      >
        <Space direction="vertical" size="small" style={{ width: '100%' }}>
          {statusMessages.map((status, idx) => (
            <div
              key={idx}
              style={{
                padding: '4px 8px',
                backgroundColor: '#fff',
                borderRadius: 4,
                borderLeft: '2px solid #1890ff',
              }}
            >
              <Space size="small">
                <ClockCircleOutlined style={{ fontSize: 11, color: '#8c8c8c' }} />
                <Text style={{ fontSize: 11, color: '#595959' }}>
                  {status.operation}:
                </Text>
                <Text style={{ fontSize: 11, color: '#262626' }}>
                  {status.message}
                </Text>
              </Space>
              {status.metadata && Object.keys(status.metadata).length > 0 && (
                <div style={{ marginTop: 4, marginLeft: 20 }}>
                  {Object.entries(status.metadata).map(([key, value]) => (
                    <Text key={key} style={{ fontSize: 10, color: '#8c8c8c', marginRight: 8 }}>
                      {key}: {typeof value === 'object' ? JSON.stringify(value) : value}
                    </Text>
                  ))}
                </div>
              )}
            </div>
          ))}
        </Space>
      </Panel>
    </Collapse>
  );
};

export default StatusMessage;
