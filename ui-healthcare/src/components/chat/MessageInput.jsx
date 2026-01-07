/**
 * Message Input Component
 * Input field for typing and sending chat messages
 */

import { useState } from 'react';
import { Input, Button, Space } from 'antd';
import { SendOutlined } from '@ant-design/icons';

const { TextArea } = Input;

const MessageInput = ({ onSend, disabled = false }) => {
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
    <Space.Compact style={{ width: '100%' }}>
      <TextArea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Ask me anything about products, orders, inventory, payments, or cases..."
        autoSize={{ minRows: 1, maxRows: 4 }}
        disabled={disabled}
        style={{ resize: 'none' }}
      />
      <Button
        type="primary"
        icon={<SendOutlined />}
        onClick={handleSend}
        disabled={disabled || !message.trim()}
      >
        Send
      </Button>
    </Space.Compact>
  );
};

export default MessageInput;
