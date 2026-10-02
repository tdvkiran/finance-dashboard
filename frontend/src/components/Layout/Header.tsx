import React, { useEffect } from 'react';
import MonthYearPicker from '../ui/MonthYearPicker';
import { Select } from '../ui/select';
import { User } from 'lucide-react';
import { useStore } from '../../store/useStore';
import { getAvailableMonths, getUsers } from '../../api/client';

export default function Header() {
  const {
    selectedMonth, setSelectedMonth, availableMonths, setAvailableMonths,
    selectedUser, setSelectedUser, availableUsers, setAvailableUsers,
  } = useStore();

  useEffect(() => {
    // Fetch available months
    getAvailableMonths()
      .then(months => {
        setAvailableMonths(months);
        if ((selectedMonth === 'current' || !selectedMonth) && months.length > 0) {
          setSelectedMonth(months[0]);
        }
      })
      .catch(() => {});

    // Fetch available users
    getUsers()
      .then(users => {
        setAvailableUsers(users);
      })
      .catch(() => {});
  }, []);

  return (
    <header className="h-16 bg-background border-b border-border flex items-center justify-between px-6 gap-3">
      <div className="md:hidden text-lg font-bold text-primary">FinDash</div>

      <div className="ml-auto flex items-center gap-3">
        {/* User selector — only show when there are multiple users */}
        {availableUsers.length > 0 && (
          <div className="flex items-center gap-2">
            <User className="w-3.5 h-3.5 text-secondary flex-shrink-0" />
            <Select
              value={selectedUser}
              onChange={e => setSelectedUser(e.target.value)}
              className="w-36 h-9 text-sm"
            >
              <option value="all">All Users</option>
              {availableUsers.map(u => (
                <option key={u} value={u}>{u}</option>
              ))}
            </Select>
          </div>
        )}

        {/* Month picker */}
        <MonthYearPicker
          value={selectedMonth}
          onChange={setSelectedMonth}
          availableMonths={availableMonths}
        />
      </div>
    </header>
  );
}