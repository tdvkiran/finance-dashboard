import React, { useState } from 'react';
import { Card, CardContent } from '../ui/card';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { formatINR } from '../../lib/utils';
import { Search, ArrowDownLeft, ArrowUpRight } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { getTransactions } from '../../api/client';
import { useStore } from '../../store/useStore';

function getDateRangeFromMonth(month: string): { start_date?: string; end_date?: string } {
  if (!month || month === 'all' || month === 'current') return {};
  return {
    start_date: `${month}-01T00:00:00Z`,
    end_date: `${month}-31T23:59:59Z`,
  };
}

export default function TransactionsPage() {
  const [search, setSearch] = useState('');
  const [selectedType, setSelectedType] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const { selectedMonth, selectedUser } = useStore();

  const dateRange = getDateRangeFromMonth(selectedMonth);
  const userFilter = selectedUser !== 'all' ? selectedUser : undefined;

  const { data, isLoading } = useQuery({
    queryKey: ['transactions', search, selectedType, selectedCategory, selectedMonth, selectedUser],
    queryFn: () => getTransactions({
      search: search || undefined,
      category: selectedCategory !== 'all' ? selectedCategory : undefined,
      limit: 200,
      username: userFilter,
      ...dateRange,
    }),
  });

  const transactions = data?.items || [];
  const filteredTransactions = transactions.filter(tx => {
    if (selectedType !== 'all' && tx.type !== selectedType) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-primary">Transactions</h1>
          <p className="text-sm text-secondary mt-1">
            {data?.total ? `${data.total} transactions` : 'View and manage your account statement records'}
            {selectedMonth && selectedMonth !== 'all' && selectedMonth !== 'current'
              ? ` in ${new Date(selectedMonth + '-01').toLocaleDateString('en-IN', { month: 'long', year: 'numeric' })}`
              : selectedMonth === 'all' ? ' (All Time)' : ''}
          </p>
        </div>
      </div>

      <Card>
        <div className="p-4 border-b border-border flex flex-col md:flex-row gap-4 items-stretch md:items-center justify-between">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-3 h-4 w-4 text-secondary" />
            <Input
              className="pl-9 bg-background/50"
              placeholder="Search by merchant, note, or details..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="flex gap-2 items-center">
            <div className="flex bg-border/40 p-1 rounded-lg">
              <button
                onClick={() => setSelectedType('all')}
                className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${selectedType === 'all' ? 'bg-primary/20 text-primary' : 'text-secondary hover:text-primary'}`}
              >
                All
              </button>
              <button
                onClick={() => setSelectedType('debit')}
                className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${selectedType === 'debit' ? 'bg-danger/20 text-danger' : 'text-secondary hover:text-danger'}`}
              >
                Debits
              </button>
              <button
                onClick={() => setSelectedType('credit')}
                className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${selectedType === 'credit' ? 'bg-success/20 text-success' : 'text-secondary hover:text-success'}`}
              >
                Credits
              </button>
            </div>
          </div>
        </div>

        <CardContent className="p-0">
          {isLoading ? (
            <div className="p-12 text-center text-secondary">Loading transactions...</div>
          ) : filteredTransactions.length === 0 ? (
            <div className="p-12 text-center text-secondary">
              No transactions found matching the filter criteria.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-secondary uppercase bg-border/30 border-b border-border">
                  <tr>
                    <th className="px-6 py-3">Date</th>
                    <th className="px-6 py-3">Merchant / Party</th>
                    <th className="px-6 py-3">Description</th>
                    <th className="px-6 py-3">Category</th>
                    <th className="px-6 py-3">Source</th>
                    <th className="px-6 py-3 text-right">Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTransactions.map((tx) => {
                    const txDate = tx.date ? new Date(tx.date).toLocaleDateString('en-IN', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric'
                    }) : '-';

                    return (
                      <tr key={tx.id} className="border-b border-border/40 hover:bg-border/10 transition-colors">
                        <td className="px-6 py-4 text-secondary whitespace-nowrap">{txDate}</td>
                        <td className="px-6 py-4 font-semibold text-primary">
                          <div className="flex items-center gap-2">
                            <span className={`p-1 rounded-full ${tx.type === 'credit' ? 'bg-success/10 text-success' : 'bg-danger/10 text-danger'}`}>
                              {tx.type === 'credit' ? <ArrowDownLeft className="w-3.5 h-3.5" /> : <ArrowUpRight className="w-3.5 h-3.5" />}
                            </span>
                            {tx.merchant || 'Unknown'}
                          </div>
                        </td>
                        <td className="px-6 py-4 text-secondary text-xs max-w-xs truncate" title={tx.description}>
                          {tx.description}
                        </td>
                        <td className="px-6 py-4">
                          <Badge variant="secondary" className="font-normal text-xs">
                            {tx.category || 'Other'}
                          </Badge>
                        </td>
                        <td className="px-6 py-4 text-xs text-secondary uppercase">
                          {tx.source_bank || '—'}
                        </td>
                        <td className={`px-6 py-4 text-right font-medium whitespace-nowrap ${tx.type === 'credit' ? 'text-success' : 'text-primary'}`}>
                          {tx.type === 'credit' ? '+' : '-'}{formatINR(tx.amount)}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}