/**
 * useCreateCase Hook
 * React Query mutation hook for creating cases
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createCase } from '../../services/cases';

export const useCreateCase = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createCase(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cases'] });
      message.success('Case created successfully');
    },
    onError: (error) => {
      message.error(error.message || 'Failed to create case');
    },
  });
};

export default useCreateCase;
