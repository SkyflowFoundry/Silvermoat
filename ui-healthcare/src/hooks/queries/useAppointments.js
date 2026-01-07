/**
 * useAppointments Hook
 * React Query hook for fetching appointments list
 */

import { useQuery } from '@tanstack/react-query';
import { listAppointments } from '../../services/appointments';

export const useAppointments = (options = {}) => {
  return useQuery({
    queryKey: ['appointments'],
    queryFn: listAppointments,
    ...options,
  });
};

export default useAppointments;
