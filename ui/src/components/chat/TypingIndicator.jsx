/**
 * Typing Indicator Component
 * Shows when the assistant is processing a response with real-time status messages
 */

import { Space, Typography } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import StatusMessage from './StatusMessage';

const { Text } = Typography;

const TypingIndicator = ({ statusMessages = [] }) => {
  return (
    <div style={{ padding: '12px 16px' }}>
      <Space direction="vertical" style={{ width: '100%' }}>
        <Space>
          <LoadingOutlined style={{ color: '#1890ff' }} />
          <Text type="secondary" style={{ fontSize: 13 }}>
            Assistant is typing...
          </Text>
        </Space>
        {statusMessages.length > 0 && <StatusMessage statusMessages={statusMessages} />}
      </Space>
    </div>
  );
};

export default TypingIndicator;
