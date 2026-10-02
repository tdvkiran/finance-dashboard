import React, { useState, useRef, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Calendar } from 'lucide-react';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

interface MonthYearPickerProps {
  value: string; // 'YYYY-MM' | 'all' | 'current'
  onChange: (value: string) => void;
  availableMonths: string[]; // list of 'YYYY-MM' with data
}

function getLabel(value: string): string {
  if (!value || value === 'all') return 'All Time';
  if (value === 'current') return 'Latest Month';
  const [year, month] = value.split('-');
  return `${MONTHS[parseInt(month) - 1]} ${year}`;
}

export default function MonthYearPicker({ value, onChange, availableMonths }: MonthYearPickerProps) {
  const currentYear = new Date().getFullYear();

  // Initialise display year from current value or most recent available month
  const initYear = () => {
    if (value && value !== 'all' && value !== 'current') {
      return parseInt(value.split('-')[0]);
    }
    if (availableMonths.length > 0) {
      return parseInt(availableMonths[0].split('-')[0]);
    }
    return currentYear;
  };

  const [open, setOpen] = useState(false);
  const [displayYear, setDisplayYear] = useState<number>(initYear);
  const ref = useRef<HTMLDivElement>(null);

  // Sync displayYear when availableMonths arrives
  useEffect(() => {
    if (availableMonths.length > 0 && displayYear === currentYear && value === 'current') {
      setDisplayYear(parseInt(availableMonths[0].split('-')[0]));
    }
  }, [availableMonths]);

  // Close picker on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const selectedYear = value && value !== 'all' && value !== 'current'
    ? parseInt(value.split('-')[0]) : null;
  const selectedMonthIdx = value && value !== 'all' && value !== 'current'
    ? parseInt(value.split('-')[1]) - 1 : null;

  const isAvailable = (year: number, monthIdx: number) => {
    const key = `${year}-${String(monthIdx + 1).padStart(2, '0')}`;
    return availableMonths.includes(key);
  };

  const handleMonthSelect = (monthIdx: number) => {
    if (!isAvailable(displayYear, monthIdx)) return;
    onChange(`${displayYear}-${String(monthIdx + 1).padStart(2, '0')}`);
    setOpen(false);
  };

  return (
    <div className="relative" ref={ref}>
      {/* Trigger button */}
      <button
        onClick={() => setOpen(prev => !prev)}
        className="flex items-center gap-2 h-9 px-3 rounded-md border border-border bg-background text-sm text-primary hover:bg-border/30 transition-colors min-w-[140px] justify-between"
      >
        <div className="flex items-center gap-2">
          <Calendar className="w-3.5 h-3.5 text-secondary flex-shrink-0" />
          <span className="truncate">{getLabel(value)}</span>
        </div>
        <ChevronRight
          className={`w-3.5 h-3.5 text-secondary transition-transform flex-shrink-0 ${open ? 'rotate-90' : ''}`}
        />
      </button>

      {/* Popover panel */}
      {open && (
        <div className="absolute right-0 top-11 z-50 bg-card border border-border rounded-xl shadow-2xl p-4 w-60">
          {/* Year navigation */}
          <div className="flex items-center justify-between mb-3">
            <button
              onClick={() => setDisplayYear(y => y - 1)}
              className="p-1.5 hover:bg-border/40 rounded-md transition-colors text-secondary hover:text-primary"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="font-semibold text-sm text-primary">{displayYear}</span>
            <button
              onClick={() => setDisplayYear(y => y + 1)}
              className="p-1.5 hover:bg-border/40 rounded-md transition-colors text-secondary hover:text-primary"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          {/* Month grid — 4 columns × 3 rows */}
          <div className="grid grid-cols-4 gap-1 mb-3">
            {MONTHS.map((m, idx) => {
              const available = isAvailable(displayYear, idx);
              const isSelected = selectedYear === displayYear && selectedMonthIdx === idx;
              return (
                <button
                  key={m}
                  onClick={() => handleMonthSelect(idx)}
                  disabled={!available}
                  className={[
                    'py-1.5 text-xs rounded-md font-medium transition-colors',
                    isSelected
                      ? 'bg-accent text-white shadow-sm'
                      : available
                        ? 'hover:bg-border/50 text-primary'
                        : 'text-secondary/25 cursor-not-allowed',
                  ].join(' ')}
                >
                  {m}
                </button>
              );
            })}
          </div>

          {/* Divider */}
          <div className="border-t border-border/60 mb-3" />

          {/* All Time */}
          <button
            onClick={() => { onChange('all'); setOpen(false); }}
            className={[
              'w-full py-1.5 text-xs rounded-md font-medium transition-colors',
              value === 'all'
                ? 'bg-accent text-white'
                : 'hover:bg-border/40 text-secondary hover:text-primary',
            ].join(' ')}
          >
            All Time
          </button>
        </div>
      )}
    </div>
  );
}
