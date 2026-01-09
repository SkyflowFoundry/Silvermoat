/**
 * useTransactions Hook
 * React Query hook for fetching transactions list
 */

import { useQuery } from '@tanstack/react-query';
import { listTransactions } from '../../services/transactions';

export const useTransactions = (options = {}) => {
  return useQuery({
    queryKey: ['transactions'],
    queryFn: listTransactions,
    ...options,
  });
};

export default useTransactions;
