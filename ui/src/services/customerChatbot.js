/**
 * Customer Chatbot Service
 * API communication for the customer AI assistant
 */

import { getApiBaseUrl, ApiError } from './api';

/**
 * Send a message to the customer chatbot and get a response
 * @param {string} message - User message
 * @param {Array} conversationHistory - Previous conversation messages
 * @param {string} customerEmail - Customer email for data filtering
 * @returns {Promise<Object>} Response with assistant message and updated conversation
 */
export const sendCustomerChatMessage = async (message, conversationHistory = [], customerEmail) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}/customer-chat`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      history: conversationHistory,
      customerEmail,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(
      `Customer chat request failed: ${response.statusText}`,
      response.status,
      errorText
    );
  }

  const data = await response.json();
  return data;
};
