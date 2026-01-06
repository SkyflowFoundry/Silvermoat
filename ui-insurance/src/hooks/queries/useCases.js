import { useQuery } from '@tanstack/react-query';
import { listCases } from '../../services/cases';

export const useCases = (options = {}) => {
  return useQuery({
    queryKey: ['cases'],
    queryFn: listCases,
    ...options,
  });
};
