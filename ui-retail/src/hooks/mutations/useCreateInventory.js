/**
 * useCreateInventory Hook
 * React Query mutation hook for creating inventory items
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createInventoryItem } from '../../services/inventory';

export const useCreateInventory = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createInventoryItem(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['inventory'] });
      message.success('Inventory item created successfully');
    },
    onError: (error) => {
      message.error(error.message || 'Failed to create inventory item');
    },
  });
};

export default useCreateInventory;
