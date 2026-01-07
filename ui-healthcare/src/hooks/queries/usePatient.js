/**
 * usePatient Hook
 * React Query hook for fetching a single patient by ID
 */

import { useQuery } from '@tanstack/react-query';
import { getPatient } from '../../services/patients';

export const usePatient = (id, options = {}) => {
  return useQuery({
    queryKey: ['patient', id],
    queryFn: () => getPatient(id),
    enabled: !!id,
    ...options,
  });
};

export default usePatient;
