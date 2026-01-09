/**
 * Employee Chatbot Service
 * API calls for employee AI assistant
 */

import { post } from './api';

/**
 * Send a message to the employee chatbot
 * @param {string} message - User message
 * @param {Array} conversationHistory - Previous messages
 * @returns {Promise<Object>} Chatbot response
 */
export const sendChatMessage = async (message, conversationHistory = []) => {
  return post('/chat', {
    message,
    conversationHistory,
  });
};

export default {
  sendChatMessage,
};
