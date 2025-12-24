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

export default {
  formatDate,
  formatTimestamp,
  formatCurrency,
  formatCurrencyFromCents,
  formatPhone,
  formatZip,
  truncate,
  formatRelativeTime,
};
