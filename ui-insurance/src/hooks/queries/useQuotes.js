import { useQuery } from '@tanstack/react-query';
import { listQuotes } from '../../services/quotes';

export const useQuotes = (options = {}) => {
  return useQuery({
    queryKey: ['quotes'],
    queryFn: listQuotes,
    ...options,
  });
};
