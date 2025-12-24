/**
 * Utility functions for formatting data
 */

import dayjs from 'dayjs';
import { DATE_FORMAT, DATETIME_FORMAT, CURRENCY_SYMBOL } from '../config/constants';

/**
 * Format a date
 * @param {number|string|Date} date - Date to format
 * @param {string} format - Format string (defaults to MM/DD/YYYY)
 * @returns {string} Formatted date
 */
export const formatDate = (date, format = DATE_FORMAT) => {
  if (!date) return '-';
  return dayjs(date).format(format);
};

/**
 * Format a timestamp (seconds or milliseconds)
 * @param {number} timestamp - Unix timestamp
 * @param {string} format - Format string
 * @returns {string} Formatted date/time
 */
export const formatTimestamp = (timestamp, format = DATETIME_FORMAT) => {
  if (!timestamp) return '-';
  // Handle both seconds and milliseconds
  const ms = timestamp < 10000000000 ? timestamp * 1000 : timestamp;
  return dayjs(ms).format(format);
};

/**
 * Format currency
 * @param {number} amount - Amount in dollars
 * @param {boolean} showSymbol - Whether to show currency symbol
 * @returns {string} Formatted currency
 */
export const formatCurrency = (amount, showSymbol = true) => {
  if (amount === null || amount === undefined) return '-';
  const formatted = Number(amount).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  return showSymbol ? `${CURRENCY_SYMBOL}${formatted}` : formatted;
};

/**
 * Format currency from cents
 * @param {number} cents - Amount in cents
 * @param {boolean} showSymbol - Whether to show currency symbol
 * @returns {string} Formatted currency
 */
export const formatCurrencyFromCents = (cents, showSymbol = true) => {
  if (cents === null || cents === undefined) return '-';
  return formatCurrency(cents / 100, showSymbol);
};

/**
 * Format a phone number
 * @param {string} phone - Phone number
 * @returns {string} Formatted phone number
 */
export const formatPhone = (phone) => {
  if (!phone) return '-';
  const cleaned = phone.replace(/\D/g, '');
  if (cleaned.length === 10) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  }
  return phone;
};

/**
 * Format a ZIP code
 * @param {string} zip - ZIP code
 * @returns {string} Formatted ZIP code
 */
export const formatZip = (zip) => {
  if (!zip) return '-';
  const cleaned = zip.replace(/\D/g, '');
  if (cleaned.length === 5) {
    return cleaned;
  }
  if (cleaned.length === 9) {
    return `${cleaned.slice(0, 5)}-${cleaned.slice(5)}`;
  }
  return zip;
};

/**
 * Truncate text with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export const truncate = (text, maxLength = 50) => {
  if (!text) return '-';
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Get relative time (e.g., "2 hours ago")
 * @param {number|string|Date} date - Date to format
 * @returns {string} Relative time string
 */
export const formatRelativeTime = (date) => {
  if (!date) return '-';
  return dayjs(date).fromNow();
};

/**
 * Format coverage type
 * @param {string} type - Coverage type (AUTO, HOME, LIFE, HEALTH)
 * @returns {string} Formatted coverage type
 */
export const formatCoverageType = (type) => {
  if (!type) return '-';
  const types = {
    AUTO: 'Auto Insurance',
    HOME: 'Home Insurance',
    LIFE: 'Life Insurance',
    HEALTH: 'Health Insurance',
  };
  return types[type] || type;
};

/**
 * Format payment method
 * @param {string} method - Payment method
 * @returns {string} Formatted payment method
 */
export const formatPaymentMethod = (method) => {
  if (!method) return '-';
  const methods = {
    CREDIT_CARD: 'Credit Card',
    ACH: 'ACH Transfer',
    CHECK: 'Check',
    WIRE: 'Wire Transfer',
  };
  return methods[method] || method;
};

/**
 * Format payment type
 * @param {string} type - Payment type
 * @returns {string} Formatted payment type
 */
export const formatPaymentType = (type) => {
  if (!type) return '-';
  const types = {
    PREMIUM: 'Premium Payment',
    CLAIM: 'Claim Payment',
    REFUND: 'Refund',
  };
  return types[type] || type;
};

/**
 * Format priority level
 * @param {string} priority - Priority level
 * @returns {string} Formatted priority
 */
export const formatPriority = (priority) => {
  if (!priority) return '-';
  const priorities = {
    LOW: 'Low',
    MEDIUM: 'Medium',
    HIGH: 'High',
    URGENT: 'Urgent',
  };
  return priorities[priority] || priority;
};

/**
 * Format loss type
 * @param {string} type - Loss type
 * @returns {string} Formatted loss type
 */
export const formatLossType = (type) => {
  if (!type) return '-';
  return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
};

/**
 * Format payment schedule
 * @param {string} schedule - Payment schedule
 * @returns {string} Formatted schedule
 */
export const formatPaymentSchedule = (schedule) => {
  if (!schedule) return '-';
  const schedules = {
    MONTHLY: 'Monthly',
    QUARTERLY: 'Quarterly',
    ANNUAL: 'Annual',
  };
  return schedules[schedule] || schedule;
};

/**
 * Format status with color class
 * @param {string} status - Status value
 * @param {string} entityType - Entity type (quote, policy, claim, payment, case)
 * @returns {object} Object with label and color
 */
export const formatStatus = (status, entityType) => {
  if (!status) return { label: '-', color: 'default' };

  const statusMap = {
    quote: {
      PENDING: { label: 'Pending', color: 'blue' },
      ACCEPTED: { label: 'Accepted', color: 'green' },
      DECLINED: { label: 'Declined', color: 'red' },
      EXPIRED: { label: 'Expired', color: 'default' },
    },
    policy: {
      ACTIVE: { label: 'Active', color: 'green' },
      EXPIRED: { label: 'Expired', color: 'default' },
      CANCELLED: { label: 'Cancelled', color: 'red' },
      SUSPENDED: { label: 'Suspended', color: 'orange' },
    },
    claim: {
      INTAKE: { label: 'Intake', color: 'blue' },
      PENDING: { label: 'Pending', color: 'orange' },
      REVIEW: { label: 'Review', color: 'cyan' },
      APPROVED: { label: 'Approved', color: 'green' },
      DENIED: { label: 'Denied', color: 'red' },
      CLOSED: { label: 'Closed', color: 'default' },
    },
    payment: {
      PENDING: { label: 'Pending', color: 'orange' },
      COMPLETED: { label: 'Completed', color: 'green' },
      FAILED: { label: 'Failed', color: 'red' },
      REFUNDED: { label: 'Refunded', color: 'blue' },
    },
    case: {
      OPEN: { label: 'Open', color: 'blue' },
      IN_PROGRESS: { label: 'In Progress', color: 'cyan' },
      RESOLVED: { label: 'Resolved', color: 'green' },
      CLOSED: { label: 'Closed', color: 'default' },
    },
  };

  const map = statusMap[entityType] || {};
  return map[status] || { label: status, color: 'default' };
};

export default {
  formatDate,
  formatTimestamp,
  formatCurrency,
  formatCurrencyFromCents,
  formatPhone,
  formatZip,
  truncate,
  formatRelativeTime,
  formatCoverageType,
  formatPaymentMethod,
  formatPaymentType,
  formatPriority,
  formatLossType,
  formatPaymentSchedule,
  formatStatus,
};
