/**
 * React Query hook for fetching a single claim
 */

import { useQuery } from '@tanstack/react-query';
import { getClaim } from '../../services/claims';

export const useClaim = (id, options = {}) => {
  return useQuery({
    queryKey: ['claims', id],
    queryFn: () => getClaim(id),
    enabled: !!id,
    ...options,
  });
};

export default useClaim;
