/**
 * useAccount Hook
 * React Query hook for fetching a single account by ID
 */

import { useQuery } from '@tanstack/react-query';
import { getAccount } from '../../services/accounts';

export const useAccount = (id, options = {}) => {
  return useQuery({
    queryKey: ['account', id],
    queryFn: () => getAccount(id),
    enabled: !!id,
    ...options,
  });
};

export default useAccount;
