/**
 * useLoans Hook
 * React Query hook for fetching loans list
 */

import { useQuery } from '@tanstack/react-query';
import { listLoans } from '../../services/loans';

export const useLoans = (options = {}) => {
  return useQuery({
    queryKey: ['loans'],
    queryFn: listLoans,
    ...options,
  });
};

export default useLoans;
