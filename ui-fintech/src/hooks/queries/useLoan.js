/**
 * useLoan Hook
 * React Query hook for fetching a single loan by ID
 */

import { useQuery } from '@tanstack/react-query';
import { getLoan } from '../../services/loans';

export const useLoan = (id, options = {}) => {
  return useQuery({
    queryKey: ['loan', id],
    queryFn: () => getLoan(id),
    enabled: !!id,
    ...options,
  });
};

export default useLoan;
