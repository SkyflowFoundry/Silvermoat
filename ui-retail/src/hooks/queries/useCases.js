/**
 * useCases Hook
 * React Query hook for fetching cases list
 */

import { useQuery } from '@tanstack/react-query';
import { listCases } from '../../services/cases';

export const useCases = (options = {}) => {
  return useQuery({
    queryKey: ['cases'],
    queryFn: listCases,
    ...options,
  });
};

export default useCases;
