/**
 * useSendMessage Hook
 * React Query mutation hook for sending chat messages
 */

import { useMutation } from '@tanstack/react-query';
import { sendChatMessage } from '../../services/chatbot';

export const useSendMessage = () => {
  return useMutation({
    mutationFn: ({ message, conversationHistory }) =>
      sendChatMessage(message, conversationHistory),
  });
};

export default useSendMessage;
