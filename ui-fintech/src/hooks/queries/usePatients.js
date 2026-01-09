/**
 * useCustomers Hook
 * React Query hook for fetching customers list
 */

import { useQuery } from '@tanstack/react-query';
import { listCustomers } from '../../services/customers';

export const useCustomers = (options = {}) => {
  return useQuery({
    queryKey: ['customers'],
    queryFn: listCustomers,
    ...options,
  });
};

export default useCustomers;
