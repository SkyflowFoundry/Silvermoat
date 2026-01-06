/**
 * React Query hook for fetching a single payment
 */

import { useQuery } from '@tanstack/react-query';
import { getPayment } from '../../services/payments';

export const usePayment = (id, options = {}) => {
  return useQuery({
    queryKey: ['payments', id],
    queryFn: () => getPayment(id),
    enabled: !!id,
    ...options,
  });
};

export default usePayment;
