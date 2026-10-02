import axios from 'axios';
import { Transaction, MonthlySummary, CategoryBreakdown, CashFlowPoint, UploadResult, Category } from '../types';

const api = axios.create({
  baseURL: '/api'
});

export const uploadFile = async (file: File, password?: string, sourceBank?: string, username?: string): Promise<UploadResult> => {
  const formData = new FormData();
  formData.append('file', file);
  if (password) formData.append('password', password);
  if (sourceBank) formData.append('source_bank', sourceBank);
  if (username) formData.append('username', username);
  const { data } = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return data;
};

export const getTransactions = async (filters: any): Promise<{items: Transaction[], total: number}> => {
  const { data } = await api.get('/transactions', { params: filters });
  return data;
};

export const getAvailableMonths = async (): Promise<string[]> => {
  const { data } = await api.get('/transactions/months');
  return data;
};

export const getUsers = async (): Promise<string[]> => {
  const { data } = await api.get('/users');
  return data;
};

export const getMonthlySummary = async (month: string, username?: string): Promise<MonthlySummary> => {
  const { data } = await api.get('/analytics/summary', { params: { month, username: username || undefined } });
  return data;
};

export const getCategoryBreakdown = async (month: string, username?: string): Promise<CategoryBreakdown[]> => {
  const { data } = await api.get('/analytics/categories', { params: { month, username: username || undefined } });
  return data;
};

export const getCashFlow = async (from: string, to: string, username?: string): Promise<CashFlowPoint[]> => {
  const { data } = await api.get('/analytics/cashflow', { params: { from_date: from || undefined, to_date: to || undefined, username: username || undefined } });
  return data;
};

export const getTopMerchants = async (month: string, username?: string): Promise<{merchant: string, amount: number, count: number}[]> => {
  const { data } = await api.get('/analytics/merchants', { params: { month, username: username || undefined } });
  return data;
};

export const getMonthlyTrend = async (months: number): Promise<MonthlySummary[]> => {
  const { data } = await api.get('/analytics/monthlytrend', { params: { months } });
  return data;
};

// Categories
export const getCategories = async (): Promise<Category[]> => {
  const { data } = await api.get('/categories');
  return data;
};

export const createCategory = async (payload: Omit<Category, 'id'>): Promise<Category> => {
  const { data } = await api.post('/categories', payload);
  return data;
};

export const updateCategory = async (id: number, payload: Partial<Omit<Category, 'id'>>): Promise<Category> => {
  const { data } = await api.put(`/categories/${id}`, payload);
  return data;
};

export const deleteCategory = async (id: number): Promise<void> => {
  await api.delete(`/categories/${id}`);
};