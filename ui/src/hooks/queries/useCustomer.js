/**
 * React Query hook for fetching a single customer
 */

import { useQuery } from '@tanstack/react-query';
import { getCustomer } from '../../services/customers';

export const useCustomer = (id, options = {}) => {
  return useQuery({
    queryKey: ['customers', id],
    queryFn: () => getCustomer(id),
    enabled: !!id, // Only run query if ID is provided
    ...options,
  });
};

export default useCustomer;
