/**
 * React Query hook for fetching a single quote
 */

import { useQuery } from '@tanstack/react-query';
import { getQuote } from '../../services/quotes';

export const useQuote = (id, options = {}) => {
  return useQuery({
    queryKey: ['quotes', id],
    queryFn: () => getQuote(id),
    enabled: !!id, // Only run query if ID is provided
    ...options,
  });
};

export default useQuote;
