/**
 * React Query hook for fetching all products
 */

import { useQuery } from '@tanstack/react-query';
import { listProducts } from '../../services/products';

export const useProducts = (options = {}) => {
  return useQuery({
    queryKey: ['products'],
    queryFn: listProducts,
    ...options,
  });
};

export default useProducts;
