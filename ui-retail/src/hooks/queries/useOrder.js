/**
 * useOrder Hook
 * React Query hook for fetching a single order
 */

import { useQuery } from '@tanstack/react-query';
import { getOrder } from '../../services/orders';

export const useOrder = (id, options = {}) => {
  return useQuery({
    queryKey: ['orders', id],
    queryFn: () => getOrder(id),
    enabled: !!id,
    ...options,
  });
};

export default useOrder;
