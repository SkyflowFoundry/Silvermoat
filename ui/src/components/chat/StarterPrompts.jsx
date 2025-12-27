/**
 * Starter Prompts Component
 * Context-aware prompts that change based on current route
 */

import { useLocation } from 'react-router-dom';
import { Button, Space, Typography } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';

const { Text } = Typography;

/**
 * Route-specific prompt mappings
 * Each route has tailored prompts relevant to that page
 */
const ROUTE_PROMPTS = {
  '/': [
    'Show recent quotes',
    'Claims overview',
    'Generate weekly report',
  ],
  '/quotes': [
    'Find quotes from last week',
    'Show high-value quotes',
    'Search quotes by customer',
  ],
  '/policies': [
    'Search active policies',
    'Expiring policies this month',
    'Policy renewal summary',
  ],
  '/claims': [
    'Show pending claims',
    'File a new claim',
    'Recent claim updates',
  ],
  '/payments': [
    'Recent payments',
    'Outstanding invoices',
    'Payment history summary',
  ],
  '/cases': [
    'Show open cases',
    'Case summary',
    'Urgent cases needing attention',
  ],
};

/**
 * Default prompts when route doesn't have specific ones
 */
const DEFAULT_PROMPTS = [
  'Search for active policies',
  'Show me pending claims',
  'Find quotes from last week',
];

/**
 * Get prompts for current route
 * Matches base path (e.g., /quotes/123 → /quotes)
 */
const getPromptsForRoute = (pathname) => {
  // Exact match first
  if (ROUTE_PROMPTS[pathname]) {
    return ROUTE_PROMPTS[pathname];
  }

  // Match base path (e.g., /quotes/123 → /quotes)
  const basePath = '/' + pathname.split('/')[1];
  if (ROUTE_PROMPTS[basePath]) {
    return ROUTE_PROMPTS[basePath];
  }

  // Default fallback
  return DEFAULT_PROMPTS;
};

/**
 * StarterPrompts Component
 * Displays context-aware starter prompts based on current route
 */
const StarterPrompts = ({ onPromptClick, isMobile = false }) => {
  const location = useLocation();
  const prompts = getPromptsForRoute(location.pathname);

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
        >
          {prompt}
        </Button>
      ))}
    </Space>
  );
};

export default StarterPrompts;
