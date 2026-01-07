/**
 * Chat Message Component
 * Displays a single message in the conversation
 */

import { Card, Typography, Tag, Space } from 'antd';
import { UserOutlined, RobotOutlined } from '@ant-design/icons';

const { Paragraph, Text } = Typography;

const ChatMessage = ({ message, isUser }) => {
  const cardStyle = {
    marginBottom: 12,
    maxWidth: '80%',
    marginLeft: isUser ? 'auto' : 0,
    marginRight: isUser ? 0 : 'auto',
    background: isUser ? '#531dab' : '#f5f5f5',
    color: isUser ? '#fff' : '#000',
  };

  const headerStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    marginBottom: 8,
    color: isUser ? '#fff' : '#666',
    fontSize: 12,
  };

  // Parse tool responses if present
  const hasToolCalls = message.toolCalls && message.toolCalls.length > 0;

  return (
    <Card
      size="small"
      style={cardStyle}
      bodyStyle={{ padding: '12px' }}
      bordered={false}
    >
      <div style={headerStyle}>
        {isUser ? <UserOutlined /> : <RobotOutlined />}
        <Text style={{ color: isUser ? '#fff' : '#666', fontWeight: 500 }}>
          {isUser ? 'You' : 'AI Assistant'}
        </Text>
      </div>

      <Paragraph
        style={{
          margin: 0,
          color: isUser ? '#fff' : '#000',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
        }}
      >
        {message.text || message.content || message}
      </Paragraph>

      {/* Display tool calls if present */}
      {hasToolCalls && (
        <Space direction="vertical" style={{ marginTop: 8, width: '100%' }} size="small">
          {message.toolCalls.map((tool, idx) => (
            <Card
              key={idx}
              size="small"
              style={{ background: '#fff', border: '1px solid #d9d9d9' }}
            >
              <Space direction="vertical" size="small" style={{ width: '100%' }}>
                <Tag color="blue">{tool.name || 'Tool'}</Tag>
                {tool.result && (
                  <pre
                    style={{
                      margin: 0,
                      fontSize: 11,
                      maxHeight: 200,
                      overflow: 'auto',
                      background: '#fafafa',
                      padding: 8,
                      borderRadius: 4,
                    }}
                  >
                    {typeof tool.result === 'string'
                      ? tool.result
                      : JSON.stringify(tool.result, null, 2)}
                  </pre>
                )}
              </Space>
            </Card>
          ))}
        </Space>
      )}
    </Card>
  );
};

export default ChatMessage;
