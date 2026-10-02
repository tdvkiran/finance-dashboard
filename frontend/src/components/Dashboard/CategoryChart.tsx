import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { formatINR } from '../../lib/utils';
import { useQuery } from '@tanstack/react-query';
import { getCategoryBreakdown } from '../../api/client';
import { useStore } from '../../store/useStore';

const COLORS = [
  '#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6',
  '#ec4899', '#06b6d4', '#84cc16', '#14b8a6', '#6366f1', '#64748b'
];

export default function CategoryChart() {
  const { selectedMonth, selectedUser } = useStore();

  const { data, isLoading } = useQuery({
    queryKey: ['categories', selectedMonth, selectedUser],
    queryFn: () => getCategoryBreakdown(selectedMonth || 'current', selectedUser !== 'all' ? selectedUser : undefined),
  });

  const chartData = data && data.length > 0 ? data.map((d, index) => ({
    name: d.category,
    value: d.amount / 100,
    rawAmount: d.amount,
    percentage: d.percentage,
    color: COLORS[index % COLORS.length]
  })) : [];

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Spending by Category</CardTitle>
      </CardHeader>
      <CardContent className="h-[300px] flex flex-col items-center justify-center">
        {isLoading ? (
          <div className="text-secondary text-sm">Loading categories...</div>
        ) : chartData.length === 0 ? (
          <div className="text-secondary text-sm">No expenses recorded</div>
        ) : (
          <>
            <div className="h-[190px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={chartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={75}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
                    formatter={(value: any, name: string) => [
                      formatINR(Number(value) * 100),
                      name
                    ]}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex flex-wrap justify-center gap-2 mt-2 max-h-[90px] overflow-y-auto px-2">
              {chartData.slice(0, 6).map(d => (
                <div key={d.name} className="flex items-center gap-1.5 text-xs text-secondary">
                  <span className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: d.color }}></span>
                  <span className="truncate max-w-[100px]">{d.name}</span>
                  <span className="text-[10px] text-primary font-medium">({d.percentage}%)</span>
                </div>
              ))}
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}