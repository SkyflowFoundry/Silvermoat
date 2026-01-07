/**
 * useProvider Hook
 * React Query hook for fetching a single provider by ID
 */

import { useQuery } from '@tanstack/react-query';
import { getProvider } from '../../services/providers';

export const useProvider = (id, options = {}) => {
  return useQuery({
    queryKey: ['provider', id],
    queryFn: () => getProvider(id),
    enabled: !!id,
    ...options,
  });
};

export default useProvider;
