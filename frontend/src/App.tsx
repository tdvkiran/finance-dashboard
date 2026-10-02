import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AppLayout from './components/Layout/AppLayout';
import DashboardPage from './components/Dashboard/DashboardPage';
import UploadPage from './components/Upload/UploadPage';
import TransactionsPage from './components/Transactions/TransactionsPage';
import CategoriesPage from './components/Categories/CategoriesPage';

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path="transactions" element={<TransactionsPage />} />
            <Route path="upload" element={<UploadPage />} />
            <Route path="categories" element={<CategoriesPage />} />
            <Route path="insights" element={<div className="p-6">Insights (Coming Soon)</div>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}