import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { formatINR } from '../../lib/utils';
import { useQuery } from '@tanstack/react-query';
import { getCashFlow } from '../../api/client';
import { useStore } from '../../store/useStore';

function getDateRangeFromMonth(month: string): { from: string; to: string } {
  if (!month || month === 'all' || month === 'current') {
    return { from: '', to: '' };
  }
  return {
    from: `${month}-01`,
    to: `${month}-31`,
  };
}

export default function CashFlowChart() {
  const { selectedMonth, selectedUser } = useStore();
  const { from, to } = getDateRangeFromMonth(selectedMonth);
  const user = selectedUser !== 'all' ? selectedUser : undefined;

  const { data, isLoading } = useQuery({
    queryKey: ['cashflow', selectedMonth, selectedUser],
    queryFn: () => getCashFlow(from, to, user),
  });

  const chartData = data && data.length > 0 ? data.map(d => {
    const formattedDate = new Date(d.date).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
    return {
      date: formattedDate,
      inflow: d.inflow / 100,
      outflow: d.outflow / 100,
      rawInflow: d.inflow,
      rawOutflow: d.outflow
    };
  }) : [];

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Cash Flow Trend</CardTitle>
      </CardHeader>
      <CardContent className="h-[300px]">
        {isLoading ? (
          <div className="h-full flex items-center justify-center text-secondary">Loading chart...</div>
        ) : chartData.length === 0 ? (
          <div className="h-full flex items-center justify-center text-secondary">No cashflow data available</div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorIn" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorOut" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v) => `₹${v >= 1000 ? `${(v/1000).toFixed(0)}k` : v}`} />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
                formatter={(value: any, name: string) => [
                  formatINR(Number(value) * 100),
                  name === 'inflow' ? 'Income / Inflow' : 'Expense / Outflow'
                ]}
              />
              <Area type="monotone" dataKey="inflow" stroke="#22c55e" fillOpacity={1} fill="url(#colorIn)" />
              <Area type="monotone" dataKey="outflow" stroke="#ef4444" fillOpacity={1} fill="url(#colorOut)" />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  );
}