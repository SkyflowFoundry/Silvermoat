/**
 * useAccounts Hook
 * React Query hook for fetching accounts list
 */

import { useQuery } from '@tanstack/react-query';
import { listAccounts } from '../../services/accounts';

export const useAccounts = (options = {}) => {
  return useQuery({
    queryKey: ['accounts'],
    queryFn: listAccounts,
    ...options,
  });
};

export default useAccounts;
