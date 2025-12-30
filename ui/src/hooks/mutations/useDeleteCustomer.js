/**
 * React Query mutation hook for deleting a customer
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { deleteCustomer } from '../../services/customers';

export const useDeleteCustomer = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id) => deleteCustomer(id),
    onSuccess: (response, variables) => {
      // Invalidate and refetch customers list
      queryClient.invalidateQueries({ queryKey: ['customers'] });
      // Also invalidate the specific customer query
      queryClient.invalidateQueries({ queryKey: ['customers', variables] });
      message.success('Customer deleted successfully');
    },
    onError: (error) => {
      message.error(`Failed to delete customer: ${error.message}`);
    },
  });
};

export default useDeleteCustomer;
