/**
 * useCreateOrder Hook
 * React Query mutation hook for creating orders
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createOrder } from '../../services/orders';

export const useCreateOrder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createOrder(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      message.success('Order created successfully');
    },
    onError: (error) => {
      message.error(error.message || 'Failed to create order');
    },
  });
};

export default useCreateOrder;
