/**
 * useInventory Hook
 * React Query hook for fetching inventory list
 */

import { useQuery } from '@tanstack/react-query';
import { listInventory } from '../../services/inventory';

export const useInventory = (options = {}) => {
  return useQuery({
    queryKey: ['inventory'],
    queryFn: listInventory,
    ...options,
  });
};

export default useInventory;
