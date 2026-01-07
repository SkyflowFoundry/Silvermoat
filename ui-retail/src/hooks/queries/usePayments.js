/**
 * usePayments Hook
 * React Query hook for fetching payments list
 */

import { useQuery } from '@tanstack/react-query';
import { listPayments } from '../../services/payments';

export const usePayments = (options = {}) => {
  return useQuery({
    queryKey: ['payments'],
    queryFn: listPayments,
    ...options,
  });
};

export default usePayments;
