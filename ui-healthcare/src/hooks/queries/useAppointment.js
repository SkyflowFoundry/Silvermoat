/**
 * useAppointment Hook
 * React Query hook for fetching a single appointment by ID
 */

import { useQuery } from '@tanstack/react-query';
import { getAppointment } from '../../services/appointments';

export const useAppointment = (id, options = {}) => {
  return useQuery({
    queryKey: ['appointment', id],
    queryFn: () => getAppointment(id),
    enabled: !!id,
    ...options,
  });
};

export default useAppointment;
