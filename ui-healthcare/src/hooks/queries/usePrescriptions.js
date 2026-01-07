/**
 * usePrescriptions Hook
 * React Query hook for fetching prescriptions list
 */

import { useQuery } from '@tanstack/react-query';
import { listPrescriptions } from '../../services/prescriptions';

export const usePrescriptions = (options = {}) => {
  return useQuery({
    queryKey: ['prescriptions'],
    queryFn: listPrescriptions,
    ...options,
  });
};

export default usePrescriptions;
