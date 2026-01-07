/**
 * useProviders Hook
 * React Query hook for fetching providers list
 */

import { useQuery } from '@tanstack/react-query';
import { listProviders } from '../../services/providers';

export const useProviders = (options = {}) => {
  return useQuery({
    queryKey: ['providers'],
    queryFn: listProviders,
    ...options,
  });
};

export default useProviders;
