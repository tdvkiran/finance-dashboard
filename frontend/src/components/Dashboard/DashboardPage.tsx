import React from 'react';
import SummaryCards from './SummaryCards';
import CashFlowChart from './CashFlowChart';
import CategoryChart from './CategoryChart';
import TopMerchants from './TopMerchants';

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-primary mb-6">Dashboard</h1>
      <SummaryCards />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <CashFlowChart />
        </div>
        <div>
          <CategoryChart />
        </div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TopMerchants />
      </div>
    </div>
  );
}