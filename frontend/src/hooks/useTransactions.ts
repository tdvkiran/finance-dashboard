import { useQuery } from '@tanstack/react-query';
import { getTransactions } from '../api/client';

export function useTransactions(filters: any) {
  return useQuery({
    queryKey: ['transactions', filters],
    queryFn: () => getTransactions(filters),
  });
}
