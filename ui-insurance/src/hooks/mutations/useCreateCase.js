/**
 * React Query mutation hook for creating a case
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createCase } from '../../services/cases';

export const useCreateCase = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createCase(data),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['cases'] });
      message.success('Case created successfully');
    },
    onError: (error) => {
      message.error(`Failed to create case: ${error.message}`);
    },
  });
};

export default useCreateCase;
