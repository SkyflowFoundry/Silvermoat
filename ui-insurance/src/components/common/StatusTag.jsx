/**
 * Reusable Status Tag Component
 * Displays status badges with appropriate colors
 */

import { Tag } from 'antd';
import {
  POLICY_STATUS_OPTIONS,
  CLAIM_STATUS_OPTIONS,
  PAYMENT_STATUS_OPTIONS,
  CASE_PRIORITY_OPTIONS,
  CASE_STATUS_OPTIONS,
} from '../../config/constants';

/**
 * Get tag color for a given status value
 * @param {string} status - Status value
 * @param {Array} options - Status options array with color mappings
 * @returns {string} Tag color
 */
const getTagColor = (status, options) => {
  const option = options.find((opt) => opt.value === status);
  return option?.color || 'default';
};

/**
 * Get label for a given status value
 * @param {string} status - Status value
 * @param {Array} options - Status options array
 * @returns {string} Status label
 */
const getStatusLabel = (status, options) => {
  const option = options.find((opt) => opt.value === status);
  return option?.label || status;
};

const StatusTag = ({ type, value }) => {
  if (!value) return <Tag>-</Tag>;

  let options = [];
  switch (type) {
    case 'policy':
      options = POLICY_STATUS_OPTIONS;
      break;
    case 'claim':
      options = CLAIM_STATUS_OPTIONS;
      break;
    case 'payment':
      options = PAYMENT_STATUS_OPTIONS;
      break;
    case 'case-priority':
      options = CASE_PRIORITY_OPTIONS;
      break;
    case 'case-status':
      options = CASE_STATUS_OPTIONS;
      break;
    default:
      return <Tag>{value}</Tag>;
  }

  const color = getTagColor(value, options);
  const label = getStatusLabel(value, options);

  return <Tag color={color}>{label}</Tag>;
};

export default StatusTag;
