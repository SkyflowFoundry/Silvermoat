/**
 * React Query mutation hook for creating a customer
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createCustomer } from '../../services/customers';

export const useCreateCustomer = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createCustomer(data),
    onSuccess: (response) => {
      // Invalidate and refetch customers list
      queryClient.invalidateQueries({ queryKey: ['customers'] });
      message.success('Customer created successfully');
    },
    onError: (error) => {
      message.error(`Failed to create customer: ${error.message}`);
    },
  });
};

export default useCreateCustomer;
