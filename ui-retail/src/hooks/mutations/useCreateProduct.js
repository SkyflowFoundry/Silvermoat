/**
 * React Query mutation hook for creating a product
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import { createProduct } from '../../services/products';

export const useCreateProduct = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => createProduct(data),
    onSuccess: (response) => {
      // Invalidate and refetch products list
      queryClient.invalidateQueries({ queryKey: ['products'] });
      message.success('Product created successfully');
    },
    onError: (error) => {
      message.error(`Failed to create product: ${error.message}`);
    },
  });
};

export default useCreateProduct;
