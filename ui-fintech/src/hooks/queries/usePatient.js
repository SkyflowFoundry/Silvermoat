/**
 * useCustomer Hook
 * React Query hook for fetching a single customer by ID
 */

import { useQuery } from '@tanstack/react-query';
import { getCustomer } from '../../services/customers';

export const useCustomer = (id, options = {}) => {
  return useQuery({
    queryKey: ['customer', id],
    queryFn: () => getCustomer(id),
    enabled: !!id,
    ...options,
  });
};

export default useCustomer;
