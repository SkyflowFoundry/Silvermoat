/**
 * React Query hook for fetching a single case
 */

import { useQuery } from '@tanstack/react-query';
import { getCase } from '../../services/cases';

export const useCase = (id, options = {}) => {
  return useQuery({
    queryKey: ['cases', id],
    queryFn: () => getCase(id),
    enabled: !!id,
    ...options,
  });
};

export default useCase;
