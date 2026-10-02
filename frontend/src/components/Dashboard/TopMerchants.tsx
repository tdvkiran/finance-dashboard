import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Progress } from '../ui/progress';
import { formatINR } from '../../lib/utils';
import { useQuery } from '@tanstack/react-query';
import { getTopMerchants } from '../../api/client';
import { useStore } from '../../store/useStore';

export default function TopMerchants() {
  const { selectedMonth, selectedUser } = useStore();

  const { data, isLoading } = useQuery({
    queryKey: ['topMerchants', selectedMonth, selectedUser],
    queryFn: () => getTopMerchants(selectedMonth || 'current', selectedUser !== 'all' ? selectedUser : undefined),
  });

  const merchants = data || [];
  const maxAmount = merchants[0]?.amount || 1;

  return (
    <Card className="col-span-full lg:col-span-2">
      <CardHeader>
        <CardTitle>Top Spends / Merchants</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {isLoading ? (
          <div className="text-secondary text-sm">Loading top merchants...</div>
        ) : merchants.length === 0 ? (
          <div className="text-secondary text-sm">No expenses recorded</div>
        ) : (
          merchants.slice(0, 5).map((merchant, i) => (
            <div key={i} className="space-y-2">
              <div className="flex justify-between items-center text-sm">
                <span className="font-medium text-primary flex items-center gap-2">
                  <div className="w-6 h-6 rounded bg-accent/20 text-accent flex items-center justify-center text-xs font-bold uppercase">
                    {merchant.merchant ? merchant.merchant[0] : 'M'}
                  </div>
                  <span className="truncate max-w-xs">{merchant.merchant}</span>
                  {merchant.count > 1 && (
                    <span className="text-[10px] text-secondary bg-border/40 px-1.5 py-0.5 rounded">
                      {merchant.count} txns
                    </span>
                  )}
                </span>
                <span className="text-secondary font-medium">{formatINR(merchant.amount)}</span>
              </div>
              <Progress value={(merchant.amount / maxAmount) * 100} className="h-1.5" />
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
}