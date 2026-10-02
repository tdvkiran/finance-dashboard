import { useQuery } from '@tanstack/react-query';
import { getMonthlySummary, getCategoryBreakdown } from '../api/client';

export function useMonthlySummary(month: string) {
  return useQuery({
    queryKey: ['summary', month],
    queryFn: () => getMonthlySummary(month),
  });
}

export function useCategoryBreakdown(month: string) {
  return useQuery({
    queryKey: ['categories', month],
    queryFn: () => getCategoryBreakdown(month),
  });
}
