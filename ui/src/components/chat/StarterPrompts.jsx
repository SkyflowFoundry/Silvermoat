/**
 * Context-Aware Starter Prompts Component
 * Shows relevant prompts based on current route
 */

import { useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import PropTypes from 'prop-types';
import { Button, Space, Typography } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
import { useAppContext } from '../../contexts/AppContext';

const { Text } = Typography;

// Map routes to relevant starter prompts
const ROUTE_PROMPTS = {
  '/': [
    'Show recent quotes',
    'Claims overview',
    'Generate weekly report',
  ],
  '/quotes': [
    'Find quotes from last week',
    'Show high-value quotes',
    'Search quotes by customer name',
  ],
  '/policies': [
    'Search active policies',
    'Show expiring policies this month',
    'Find policies by coverage type',
  ],
  '/claims': [
    'Show pending claims',
    'File a new claim',
    'Recent claim status updates',
  ],
  '/payments': [
    'Recent payments',
    'Outstanding invoices',
    'Payment history for this month',
  ],
  '/cases': [
    'Show open cases',
    'Case summary',
    'High priority cases',
  ],
};

// Default prompts for unknown routes
const DEFAULT_PROMPTS = [
  'Search for active policies',
  'Show me pending claims',
  'Find quotes from last week',
];

const StarterPrompts = ({ onPromptClick }) => {
  const location = useLocation();
  const { isMobile } = useAppContext();

  // Get prompts for current route, or use defaults (memoized)
  const prompts = useMemo(
    () => ROUTE_PROMPTS[location.pathname] || DEFAULT_PROMPTS,
    [location.pathname]
  );

  return (
    <Space direction="vertical" size="small" style={{ width: '100%' }}>
      <Text type="secondary" style={{ fontSize: isMobile ? 11 : 12 }}>
        Try these:
      </Text>
      {prompts.map((prompt, idx) => (
        <Button
          key={idx}
          size={isMobile ? 'middle' : 'small'}
          icon={<QuestionCircleOutlined />}
          onClick={() => onPromptClick(prompt)}
          style={{ textAlign: 'left', width: '100%' }}
          data-testid={`starter-prompt-${idx}`}
        >
          {prompt}
        </Button>
      ))}
    </Space>
  );
};

StarterPrompts.propTypes = {
  onPromptClick: PropTypes.func.isRequired,
};

export default StarterPrompts;
