/**
 * React Query hook for fetching a single product
 */

import { useQuery } from '@tanstack/react-query';
import { getProduct } from '../../services/products';

export const useProduct = (id, options = {}) => {
  return useQuery({
    queryKey: ['products', id],
    queryFn: () => getProduct(id),
    enabled: !!id, // Only run query if ID is provided
    ...options,
  });
};

export default useProduct;
