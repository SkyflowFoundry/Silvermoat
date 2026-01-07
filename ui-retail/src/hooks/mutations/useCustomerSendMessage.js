/**
 * useCustomerSendMessage Hook
 * React Query mutation hook for sending customer chat messages
 */

import { useMutation } from '@tanstack/react-query';
import { sendCustomerChatMessage } from '../../services/customerChatbot';

export const useCustomerSendMessage = () => {
  return useMutation({
    mutationFn: ({ message, conversationHistory }) =>
      sendCustomerChatMessage(message, conversationHistory),
  });
};

export default useCustomerSendMessage;
