/**
 * Message Input Component
 * Text input with send button for chat messages
 */

import { useState } from 'react';
import { Input, Button, Space } from 'antd';
import { SendOutlined } from '@ant-design/icons';
import { useAppContext } from '../../contexts/AppContext';

const { TextArea } = Input;

const MessageInput = ({ onSend, disabled = false }) => {
  const { isMobile } = useAppContext();
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim()) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div
      style={{
        padding: isMobile ? 12 : 16,
        borderTop: '1px solid #f0f0f0',
        backgroundColor: '#ffffff',
      }}
    >
      <Space.Compact style={{ width: '100%' }}>
        <TextArea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={isMobile ? "Ask me anything..." : "Ask me anything about quotes, policies, claims..."}
          disabled={disabled}
          autoSize={{ minRows: 1, maxRows: isMobile ? 3 : 4 }}
          style={{ resize: 'none', fontSize: isMobile ? 14 : 15 }}
        />
        <Button
          type="primary"
          icon={<SendOutlined />}
          onClick={handleSend}
          disabled={disabled || !message.trim()}
          style={{ height: 'auto', minWidth: isMobile ? 48 : 'auto' }}
        >
          {!isMobile && 'Send'}
        </Button>
      </Space.Compact>
    </div>
  );
};

export default MessageInput;
