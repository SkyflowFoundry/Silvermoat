/**
 * React Query mutation hook for sending customer chat messages
 */

import { useMutation } from '@tanstack/react-query';
import { sendCustomerChatMessage } from '../../services/customerChatbot';

/**
 * Hook for sending messages to the customer chatbot
 * @returns {Object} React Query mutation object
 */
export const useCustomerSendMessage = () => {
  return useMutation({
    mutationFn: ({ message, history, customerEmail }) =>
      sendCustomerChatMessage(message, history, customerEmail),
  });
};
