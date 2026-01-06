/**
 * Chatbot Service
 * API communication for the AI assistant
 */

import { getApiBaseUrl, ApiError } from './api';

/**
 * Send a message to the chatbot and get a response
 * @param {string} message - User message
 * @param {Array} conversationHistory - Previous conversation messages
 * @returns {Promise<Object>} Response with assistant message and updated conversation
 */
export const sendChatMessage = async (message, conversationHistory = []) => {
  const apiBase = getApiBaseUrl();
  const url = `${apiBase}/chat`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      history: conversationHistory,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(
      `Chat request failed: ${response.statusText}`,
      response.status,
      errorText
    );
  }

  const data = await response.json();
  return data;
};
