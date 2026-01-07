/**
 * Customer Chatbot Service
 * API calls for customer-facing AI assistant
 */

import { post } from './api';

/**
 * Send a message to the customer chatbot
 * @param {string} message - User message
 * @param {Array} conversationHistory - Previous messages
 * @returns {Promise<Object>} Chatbot response
 */
export const sendCustomerChatMessage = async (message, conversationHistory = []) => {
  return post('/customer-chat', {
    message,
    conversationHistory,
  });
};

export default {
  sendCustomerChatMessage,
};
