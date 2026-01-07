/**
 * useOrders Hook
 * React Query hook for fetching orders list
 */

import { useQuery } from '@tanstack/react-query';
import { listOrders } from '../../services/orders';

export const useOrders = (options = {}) => {
  return useQuery({
    queryKey: ['orders'],
    queryFn: listOrders,
    ...options,
  });
};

export default useOrders;
