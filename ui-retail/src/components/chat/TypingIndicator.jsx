/**
 * Typing Indicator Component
 * Shows animated dots when AI is responding
 */

import { Space } from 'antd';
import './TypingIndicator.css';

const TypingIndicator = () => {
  return (
    <div className="typing-indicator-wrapper">
      <Space className="typing-indicator">
        <span className="dot"></span>
        <span className="dot"></span>
        <span className="dot"></span>
      </Space>
    </div>
  );
};

export default TypingIndicator;
