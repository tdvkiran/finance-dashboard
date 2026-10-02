import { create } from 'zustand';

interface StoreState {
  // Month filter
  selectedMonth: string; // 'YYYY-MM' | 'all' | 'current'
  setSelectedMonth: (month: string) => void;
  availableMonths: string[];
  setAvailableMonths: (months: string[]) => void;

  // User filter
  selectedUser: string; // specific username | 'all'
  setSelectedUser: (user: string) => void;
  availableUsers: string[];
  setAvailableUsers: (users: string[]) => void;
}

export const useStore = create<StoreState>((set) => ({
  selectedMonth: 'current',
  setSelectedMonth: (month) => set({ selectedMonth: month }),
  availableMonths: [],
  setAvailableMonths: (months) => set({ availableMonths: months }),

  selectedUser: 'all',
  setSelectedUser: (user) => set({ selectedUser: user }),
  availableUsers: [],
  setAvailableUsers: (users) => set({ availableUsers: users }),
}));
