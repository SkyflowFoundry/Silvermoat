/**
 * useCard Hook
 * React Query hook for fetching a single card
 */

import { useQuery } from '@tanstack/react-query';
import { getCard } from '../../services/cards';

export const useCard = (id, options = {}) => {
  return useQuery({
    queryKey: ['card', id],
    queryFn: () => getCard(id),
    enabled: !!id,
    ...options,
  });
};

export default useCard;
