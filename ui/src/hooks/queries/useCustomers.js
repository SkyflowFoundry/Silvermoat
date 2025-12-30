import { useQuery } from '@tanstack/react-query';
import { listCustomers } from '../../services/customers';

export const useCustomers = (options = {}) => {
  return useQuery({
    queryKey: ['customers'],
    queryFn: listCustomers,
    ...options,
  });
};
