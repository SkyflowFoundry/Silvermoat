/**
 * Chat Interface Component
 * Main chat component with conversation history and message handling
 */

import { useState, useRef, useEffect } from 'react';
import { Drawer, Space, Typography, Button, Empty, Divider } from 'antd';
import { DeleteOutlined, MessageOutlined } from '@ant-design/icons';
import ChatMessage from './ChatMessage';
import MessageInput from './MessageInput';
import TypingIndicator from './TypingIndicator';
import { useSendMessage } from '../../hooks/mutations/useSendMessage';

const { Title, Text } = Typography;

const ChatInterface = ({ open, onClose }) => {
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);
  const sendMessageMutation = useSendMessage();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, sendMessageMutation.isPending]);

  const handleSendMessage = async (text) => {
    // Add user message
    const userMessage = { text, isUser: true, timestamp: new Date() };
    setMessages((prev) => [...prev, userMessage]);

    try {
      // Send to API
      const response = await sendMessageMutation.mutateAsync({
        message: text,
        conversationHistory: messages.map((m) => ({
          role: m.isUser ? 'user' : 'assistant',
          content: m.text || m.content,
        })),
      });

      // Add assistant response
      const assistantMessage = {
        text: response.response || response.message || 'No response',
        isUser: false,
        timestamp: new Date(),
        toolCalls: response.toolCalls || [],
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      // Add error message
      const errorMessage = {
        text: `Error: ${error.message || 'Failed to send message'}`,
        isUser: false,
        timestamp: new Date(),
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const handleClearHistory = () => {
    setMessages([]);
  };

  return (
    <Drawer
      title={
        <Space>
          <MessageOutlined style={{ color: '#531dab' }} />
          <Title level={4} style={{ margin: 0 }}>
            AI Assistant
          </Title>
        </Space>
      }
      placement="right"
      onClose={onClose}
      open={open}
      width={500}
      extra={
        <Button
          size="small"
          icon={<DeleteOutlined />}
          onClick={handleClearHistory}
          disabled={messages.length === 0}
        >
          Clear
        </Button>
      }
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          height: '100%',
        }}
      >
        {/* Messages Area */}
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            marginBottom: 16,
            padding: '0 4px',
          }}
        >
          {messages.length === 0 ? (
            <Empty
              description={
                <Space direction="vertical" size="small">
                  <Text type="secondary">No messages yet</Text>
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    Ask me about products, orders, inventory, payments, or cases
                  </Text>
                </Space>
              }
              style={{ marginTop: 48 }}
            />
          ) : (
            <>
              {messages.map((msg, idx) => (
                <ChatMessage key={idx} message={msg} isUser={msg.isUser} />
              ))}
              {sendMessageMutation.isPending && (
                <div style={{ marginBottom: 12 }}>
                  <TypingIndicator />
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        <Divider style={{ margin: '16px 0' }} />

        {/* Input Area */}
        <MessageInput
          onSend={handleSendMessage}
          disabled={sendMessageMutation.isPending}
        />
      </div>
    </Drawer>
  );
};

export default ChatInterface;
