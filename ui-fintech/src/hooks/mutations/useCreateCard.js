/**
 * useCreateCard Hook
 * React Query mutation hook for creating cards
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createCard } from '../../services/cards';

export const useCreateCard = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createCard(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cards'] });
      message.success('Card created successfully');
    },
    onError: (error) => {
      message.error(error.message || 'Failed to create card');
    },
  });
};

export default useCreateCard;
