/**
 * usePatients Hook
 * React Query hook for fetching patients list
 */

import { useQuery } from '@tanstack/react-query';
import { listPatients } from '../../services/patients';

export const usePatients = (options = {}) => {
  return useQuery({
    queryKey: ['patients'],
    queryFn: listPatients,
    ...options,
  });
};

export default usePatients;
