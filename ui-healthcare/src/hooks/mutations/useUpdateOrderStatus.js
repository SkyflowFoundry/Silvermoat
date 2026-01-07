/**
 * useUpdateOrderStatus Hook
 * React Query mutation hook for updating order status
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { updateOrderStatus } from '../../services/orders';

export const useUpdateOrderStatus = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ orderId, status }) => updateOrderStatus(orderId, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      message.success('Order status updated successfully');
    },
    onError: (error) => {
      message.error(error.message || 'Failed to update order status');
    },
  });
};

export default useUpdateOrderStatus;
