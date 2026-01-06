/**
 * Typing Indicator Component
 * Shows when the assistant is processing a response
 */

import { Space, Typography } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

const { Text } = Typography;

const TypingIndicator = () => {
  return (
    <div style={{ padding: '12px 16px' }}>
      <Space>
        <LoadingOutlined style={{ color: '#0052A3' }} />
        <Text type="secondary" style={{ fontSize: 13 }}>
          Assistant is typing...
        </Text>
      </Space>
    </div>
  );
};

export default TypingIndicator;
