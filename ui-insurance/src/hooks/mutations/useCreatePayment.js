/**
 * React Query mutation hook for creating a payment
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createPayment } from '../../services/payments';

export const useCreatePayment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createPayment(data),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['payments'] });
      message.success('Payment created successfully');
    },
    onError: (error) => {
      message.error(`Failed to create payment: ${error.message}`);
    },
  });
};

export default useCreatePayment;
