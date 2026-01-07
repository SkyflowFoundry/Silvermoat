/**
 * useCreatePayment Hook
 * React Query mutation hook for creating payments
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createPayment } from '../../services/payments';

export const useCreatePayment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createPayment(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['payments'] });
      message.success('Payment created successfully');
    },
    onError: (error) => {
      message.error(error.message || 'Failed to create payment');
    },
  });
};

export default useCreatePayment;
