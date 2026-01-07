/**
 * usePrescription Hook
 * React Query hook for fetching a single prescription by ID
 */

import { useQuery } from '@tanstack/react-query';
import { getPrescription } from '../../services/prescriptions';

export const usePrescription = (id, options = {}) => {
  return useQuery({
    queryKey: ['prescription', id],
    queryFn: () => getPrescription(id),
    enabled: !!id,
    ...options,
  });
};

export default usePrescription;
