/**
 * React Query mutation hook for creating a claim
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createClaim } from '../../services/claims';

export const useCreateClaim = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createClaim(data),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['claims'] });
      message.success('Claim created successfully');
    },
    onError: (error) => {
      message.error(`Failed to create claim: ${error.message}`);
    },
  });
};

export default useCreateClaim;
