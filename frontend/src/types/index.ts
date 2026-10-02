export interface Category {
  id: number;
  name: string;
  icon: string;
  color: string;
  budget_limit: number | null;
}

export interface Transaction {
  id: number;
  date: string;
  description: string;
  amount: number; // in paise
  type: 'debit' | 'credit';
  category: string;
  merchant: string;
  source_bank: string;
  account_id: number;
}

export interface MonthlySummary {
  month: string;
  total_income: number;
  total_expense: number;
  net_savings: number;
  savings_rate: number;
}

export interface CategoryBreakdown {
  category: string;
  amount: number;
  percentage: number;
  color: string;
  icon: string;
  transaction_count: number;
}

export interface CashFlowPoint {
  date: string;
  inflow: number;
  outflow: number;
  balance: number;
}

export interface UploadResult {
  transactions_parsed: number;
  date_range: { from: string; to: string };
  total_debits: number;
  total_credits: number;
  bank: string;
}