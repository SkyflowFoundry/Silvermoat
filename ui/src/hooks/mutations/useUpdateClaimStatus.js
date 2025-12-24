/**
 * React Query mutation hook for updating claim status
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { updateStatus } from '../../services/claims';

export const useUpdateClaimStatus = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, status }) => updateStatus(id, status),
    onSuccess: (response, variables) => {
      // Invalidate specific claim and claims list
      queryClient.invalidateQueries({ queryKey: ['claims', variables.id] });
      queryClient.invalidateQueries({ queryKey: ['claims'] });
      message.success('Claim status updated successfully');
    },
    onError: (error) => {
      message.error(`Failed to update claim status: ${error.message}`);
    },
  });
};

export default useUpdateClaimStatus;
