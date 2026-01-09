/**
 * useCards Hook
 * React Query hook for fetching cards list
 */

import { useQuery } from '@tanstack/react-query';
import { listCards } from '../../services/cards';

export const useCards = (options = {}) => {
  return useQuery({
    queryKey: ['cards'],
    queryFn: listCards,
    ...options,
  });
};

export default useCards;
