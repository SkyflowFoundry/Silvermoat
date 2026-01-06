/**
 * React Query hook for fetching a single policy
 */

import { useQuery } from '@tanstack/react-query';
import { getPolicy } from '../../services/policies';

export const usePolicy = (id, options = {}) => {
  return useQuery({
    queryKey: ['policies', id],
    queryFn: () => getPolicy(id),
    enabled: !!id,
    ...options,
  });
};

export default usePolicy;
