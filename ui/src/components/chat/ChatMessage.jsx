/**
 * Chat Message Component
 * Displays a single message from user or assistant
 */

import { Typography, Avatar, Grid } from 'antd';
import { UserOutlined, RobotOutlined } from '@ant-design/icons';
import { useAppContext } from '../../contexts/AppContext';
import StatusMessage from './StatusMessage';

const { Text, Paragraph } = Typography;
const { useBreakpoint } = Grid;

const ChatMessage = ({ role, content, timestamp, statusMessages }) => {
  const isUser = role === 'user';
  const { isMobile } = useAppContext();

  return (
    <div
      style={{
        display: 'flex',
        gap: isMobile ? 8 : 12,
        padding: isMobile ? '8px 12px' : '12px 16px',
        flexDirection: isUser ? 'row-reverse' : 'row',
      }}
    >
      <Avatar
        icon={isUser ? <UserOutlined /> : <RobotOutlined />}
        size={isMobile ? 'default' : 'large'}
        style={{
          backgroundColor: isUser ? '#003d82' : '#52c41a',
          flexShrink: 0,
        }}
      />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        <div
          style={{
            maxWidth: isMobile ? '85%' : '70%',
            padding: isMobile ? '10px 12px' : '12px 16px',
            borderRadius: 8,
            backgroundColor: isUser ? '#f0f5ff' : '#ffffff',
            border: isUser ? 'none' : '1px solid #f0f0f0',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.06)',
          }}
        >
          <Paragraph style={{ margin: 0, whiteSpace: 'pre-wrap', fontSize: isMobile ? 14 : 15 }}>
            {content}
          </Paragraph>
          {timestamp && (
            <Text type="secondary" style={{ fontSize: isMobile ? 10 : 11 }}>
              {new Date(timestamp).toLocaleTimeString()}
            </Text>
          )}
        </div>
        {!isUser && statusMessages && statusMessages.length > 0 && (
          <StatusMessage statusMessages={statusMessages} />
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
