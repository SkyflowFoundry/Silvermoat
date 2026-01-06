import { useQuery } from '@tanstack/react-query';
import { listPolicies } from '../../services/policies';

export const usePolicies = (options = {}) => {
  return useQuery({
    queryKey: ['policies'],
    queryFn: listPolicies,
    ...options,
  });
};
