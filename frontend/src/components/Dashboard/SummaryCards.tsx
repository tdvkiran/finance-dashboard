import React from 'react';
import { Card, CardContent } from '../ui/card';
import { TrendingUp, TrendingDown, PiggyBank } from 'lucide-react';
import { formatINR } from '../../lib/utils';
import { useQuery } from '@tanstack/react-query';
import { getMonthlySummary } from '../../api/client';
import { useStore } from '../../store/useStore';

export default function SummaryCards() {
  const { selectedMonth, selectedUser } = useStore();

  const { data, isLoading } = useQuery({
    queryKey: ['summary', selectedMonth, selectedUser],
    queryFn: () => getMonthlySummary(selectedMonth || 'current', selectedUser !== 'all' ? selectedUser : undefined),
  });

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="h-28 bg-border/20 rounded-xl animate-pulse" />
        <div className="h-28 bg-border/20 rounded-xl animate-pulse" />
        <div className="h-28 bg-border/20 rounded-xl animate-pulse" />
      </div>
    );
  }

  const income = data?.total_income || 0;
  const expense = data?.total_expense || 0;
  const savings = data?.net_savings || 0;
  const savingsRate = data?.savings_rate || 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Card>
        <CardContent className="p-6 flex items-center gap-4">
          <div className="p-3 bg-success/20 rounded-lg text-success">
            <TrendingUp className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm text-secondary">Total Income</p>
            <p className="text-2xl font-bold text-primary">{formatINR(income)}</p>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="p-6 flex items-center gap-4">
          <div className="p-3 bg-danger/20 rounded-lg text-danger">
            <TrendingDown className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm text-secondary">Total Expenses</p>
            <p className="text-2xl font-bold text-primary">{formatINR(expense)}</p>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="p-6 flex items-center gap-4">
          <div className="p-3 bg-info/20 rounded-lg text-info">
            <PiggyBank className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm text-secondary">Net Savings</p>
            <div className="flex items-baseline gap-2">
              <p className={`text-2xl font-bold ${savings >= 0 ? 'text-primary' : 'text-danger'}`}>
                {formatINR(savings)}
              </p>
              {income > 0 && (
                <span className="text-xs text-info bg-info/10 px-2 py-0.5 rounded-full">
                  {savingsRate}% rate
                </span>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}