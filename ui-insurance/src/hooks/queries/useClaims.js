import { useQuery } from '@tanstack/react-query';
import { listClaims } from '../../services/claims';

export const useClaims = (options = {}) => {
  return useQuery({
    queryKey: ['claims'],
    queryFn: listClaims,
    ...options,
  });
};
