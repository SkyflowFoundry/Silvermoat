/**
 * useInventoryItem Hook
 * React Query hook for fetching a single inventory item
 */

import { useQuery } from '@tanstack/react-query';
import { getInventoryItem } from '../../services/inventory';

export const useInventoryItem = (id, options = {}) => {
  return useQuery({
    queryKey: ['inventory', id],
    queryFn: () => getInventoryItem(id),
    enabled: !!id,
    ...options,
  });
};

export default useInventoryItem;
