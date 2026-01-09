/**
 * useTransaction Hook
 * React Query hook for fetching a single transaction by ID
 */

import { useQuery } from '@tanstack/react-query';
import { getTransaction } from '../../services/transactions';

export const useTransaction = (id, options = {}) => {
  return useQuery({
    queryKey: ['transaction', id],
    queryFn: () => getTransaction(id),
    enabled: !!id,
    ...options,
  });
};

export default useTransaction;
