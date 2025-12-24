/**
 * React Query mutation hook for creating a policy
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createPolicy } from '../../services/policies';

export const useCreatePolicy = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createPolicy(data),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['policies'] });
      message.success('Policy created successfully');
    },
    onError: (error) => {
      message.error(`Failed to create policy: ${error.message}`);
    },
  });
};

export default useCreatePolicy;
