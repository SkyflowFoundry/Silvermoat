/**
 * React Query mutation hook for creating a quote
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createQuote } from '../../services/quotes';

export const useCreateQuote = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createQuote(data),
    onSuccess: (response) => {
      // Invalidate and refetch quotes list
      queryClient.invalidateQueries({ queryKey: ['quotes'] });
      message.success('Quote created successfully');
    },
    onError: (error) => {
      message.error(`Failed to create quote: ${error.message}`);
    },
  });
};

export default useCreateQuote;
