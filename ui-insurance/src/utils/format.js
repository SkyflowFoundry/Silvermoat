/**
 * Formatting Utilities
 * Common formatting functions for display
 */

/**
 * Format cents to currency string
 * @param {number} cents - Amount in cents
 * @returns {string} - Formatted currency (e.g., "$1,234.56")
 */
export const formatCurrency = (cents) => {
  if (cents === null || cents === undefined) return 'N/A';
  const dollars = cents / 100;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(dollars);
};

/**
 * Format date string
 * @param {string|number} date - Date string or timestamp
 * @returns {string} - Formatted date (e.g., "Jan 15, 2024")
 */
export const formatDate = (date) => {
  if (!date) return '';

  let dateObj;
  if (typeof date === 'number') {
    // Unix timestamp
    dateObj = new Date(date * 1000);
  } else if (typeof date === 'string') {
    // ISO date string
    dateObj = new Date(date);
  } else {
    return '';
  }

  if (isNaN(dateObj.getTime())) return '';

  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(dateObj);
};

/**
 * Format date with time
 * @param {string|number} date - Date string or timestamp
 * @returns {string} - Formatted date with time
 */
export const formatDateTime = (date) => {
  if (!date) return '';

  let dateObj;
  if (typeof date === 'number') {
    dateObj = new Date(date * 1000);
  } else if (typeof date === 'string') {
    dateObj = new Date(date);
  } else {
    return '';
  }

  if (isNaN(dateObj.getTime())) return '';

  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
  }).format(dateObj);
};

/**
 * Format phone number
 * @param {string} phone - Phone number string
 * @returns {string} - Formatted phone number
 */
export const formatPhone = (phone) => {
  if (!phone) return '';
  const cleaned = phone.replace(/\D/g, '');
  const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
  if (match) {
    return `(${match[1]}) ${match[2]}-${match[3]}`;
  }
  return phone;
};

/**
 * Truncate text to specified length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} - Truncated text with ellipsis if needed
 */
export const truncate = (text, maxLength = 50) => {
  if (!text || text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};
