/**
 * React Query mutation hook for sending chat messages
 */

import { useMutation } from '@tanstack/react-query';
import { sendChatMessage } from '../../services/chatbot';

/**
 * Hook for sending messages to the chatbot
 * @returns {Object} React Query mutation object
 */
export const useSendMessage = () => {
  return useMutation({
    mutationFn: ({ message, history }) => sendChatMessage(message, history),
  });
};
