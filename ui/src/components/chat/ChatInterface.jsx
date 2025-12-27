/**
 * Chat Interface Component
 * Main chat UI with message list and input
 */

import { useState, useRef, useEffect } from 'react';
import { Typography, Empty, Space, Button } from 'antd';
import { CloseOutlined } from '@ant-design/icons';
import ChatMessage from './ChatMessage';
import MessageInput from './MessageInput';
import TypingIndicator from './TypingIndicator';
import StarterPrompts from './StarterPrompts';
import { useSendMessage } from '../../hooks/mutations/useSendMessage';
import { useAppContext } from '../../contexts/AppContext';

const { Title, Text } = Typography;

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [conversationHistory, setConversationHistory] = useState([]);
  const messagesEndRef = useRef(null);
  const { mutate: sendMessage, isPending } = useSendMessage();
  const { isMobile, closeChatDrawer } = useAppContext();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = (text) => {
    // Add user message to UI
    const userMessage = {
      role: 'user',
      content: text,
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMessage]);

    // Send to backend
    sendMessage(
      {
        message: text,
        history: conversationHistory,
      },
      {
        onSuccess: (data) => {
          // Add assistant response to UI
          const assistantMessage = {
            role: 'assistant',
            content: data.response,
            timestamp: Date.now(),
          };
          setMessages((prev) => [...prev, assistantMessage]);

          // Update conversation history for context
          setConversationHistory(data.conversation || []);
        },
        onError: (error) => {
          // Show error message
          const errorMessage = {
            role: 'assistant',
            content: `Sorry, I encountered an error: ${error.message}`,
            timestamp: Date.now(),
          };
          setMessages((prev) => [...prev, errorMessage]);
        },
      }
    );
  };

  const handleStarterPrompt = (prompt) => {
    handleSend(prompt);
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: isMobile ? '12px 16px' : '16px 20px',
          borderBottom: '1px solid #f0f0f0',
          backgroundColor: '#fafafa',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
        }}
      >
        <div style={{ flex: 1 }}>
          <Title level={isMobile ? 5 : 4} style={{ margin: 0 }}>
            Chat Assistant
          </Title>
          <Text type="secondary" style={{ fontSize: isMobile ? 11 : 12 }}>
            Ask me about quotes, policies, claims, and more
          </Text>
        </div>
        <Button
          type="text"
          icon={<CloseOutlined />}
          onClick={closeChatDrawer}
          style={{
            fontSize: isMobile ? 16 : 18,
            color: '#8c8c8c',
          }}
          aria-label="Close chat"
        />
      </div>

      {/* Messages */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          backgroundColor: '#fafafa',
          padding: '16px 0',
        }}
      >
        {messages.length === 0 ? (
          <Empty
            image={Empty.PRESENTED_IMAGE_SIMPLE}
            description={
              <Space direction="vertical" size="large" style={{ marginTop: isMobile ? 20 : 40, padding: isMobile ? '0 12px' : 0 }}>
                <div>
                  <Text type="secondary" style={{ fontSize: isMobile ? 13 : 14 }}>
                    I can help you with:
                  </Text>
                  <ul style={{ textAlign: 'left', marginTop: 8, fontSize: isMobile ? 13 : 14 }}>
                    <li>Searching quotes, policies, claims, payments, cases</li>
                    <li>Getting details about specific records</li>
                    <li>Generating summaries and reports</li>
                    <li>Helping fill out forms</li>
                  </ul>
                </div>
                <StarterPrompts onPromptClick={handleStarterPrompt} />
              </Space>
            }
          />
        ) : (
          <>
            {messages.map((msg, idx) => (
              <ChatMessage
                key={idx}
                role={msg.role}
                content={msg.content}
                timestamp={msg.timestamp}
              />
            ))}
            {isPending && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input */}
      <MessageInput onSend={handleSend} disabled={isPending} />
    </div>
  );
};

export default ChatInterface;
