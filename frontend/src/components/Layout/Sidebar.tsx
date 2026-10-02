import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Receipt, Upload, Tag, TrendingUp } from 'lucide-react';
import { cn } from '../../lib/utils';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', to: '/' },
  { icon: Receipt, label: 'Transactions', to: '/transactions' },
  { icon: Upload, label: 'Upload', to: '/upload' },
  { icon: Tag, label: 'Categories', to: '/categories' },
  { icon: TrendingUp, label: 'Insights', to: '/insights' },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-background border-r border-border hidden md:flex flex-col">
      <div className="h-16 flex items-center px-6 border-b border-border">
        <h1 className="text-xl font-bold text-accent flex items-center gap-2">
          <TrendingUp className="w-6 h-6" /> FinDash
        </h1>
      </div>
      <nav className="flex-1 py-4">
        <ul className="space-y-1 px-3">
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) => cn(
                  "flex items-center gap-3 px-3 py-2 rounded-md transition-colors",
                  isActive ? "bg-accent/10 text-accent" : "text-secondary hover:text-primary hover:bg-border/50"
                )}
              >
                <item.icon className="w-5 h-5" />
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}