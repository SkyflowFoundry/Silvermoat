/**
 * Status Message Component
 * Shows collapsible operation logs (DynamoDB queries, tool execution, AI processing)
 */

import { useState } from 'react';
import { Space, Typography, Collapse } from 'antd';
import { LoadingOutlined, DownOutlined, RightOutlined } from '@ant-design/icons';

const { Text } = Typography;
const { Panel } = Collapse;

const StatusMessage = ({ statusMessages = [] }) => {
  const [collapsed, setCollapsed] = useState(false);

  if (!statusMessages || statusMessages.length === 0) {
    return null;
  }

  return (
    <div style={{ padding: '12px 16px' }}>
      <Space direction="vertical" size="small" style={{ width: '100%' }}>
        <div
          onClick={() => setCollapsed(!collapsed)}
          style={{
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}
        >
          {collapsed ? <RightOutlined style={{ fontSize: 10, color: '#8c8c8c' }} /> : <DownOutlined style={{ fontSize: 10, color: '#8c8c8c' }} />}
          <Text type="secondary" style={{ fontSize: 12 }}>
            Operation Log ({statusMessages.length} {statusMessages.length === 1 ? 'operation' : 'operations'})
          </Text>
        </div>
        {!collapsed && (
          <div
            style={{
              paddingLeft: '18px',
              maxHeight: '150px',
              overflowY: 'auto',
              backgroundColor: '#f5f5f5',
              borderRadius: '4px',
              padding: '8px 12px',
            }}
          >
            {statusMessages.map((status, idx) => (
              <div key={idx} style={{ marginBottom: idx < statusMessages.length - 1 ? '4px' : 0 }}>
                <Space size="small">
                  <LoadingOutlined style={{ color: '#1890ff', fontSize: 12 }} />
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    {status.message}
                  </Text>
                </Space>
              </div>
            ))}
          </div>
        )}
      </Space>
    </div>
  );
};

export default StatusMessage;
