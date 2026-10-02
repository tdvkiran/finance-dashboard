import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { Input } from '../ui/input';
import { Button } from '../ui/button';
import { Category } from '../../types';
import { formatINR } from '../../lib/utils';

const COLOR_SWATCHES = [
  '#ef4444', '#f97316', '#f59e0b', '#22c55e', '#10b981',
  '#06b6d4', '#3b82f6', '#6366f1', '#8b5cf6', '#ec4899',
  '#64748b', '#0f172a',
];

interface CategoryModalProps {
  category?: Category | null;  // null = create mode
  onClose: () => void;
  onSave: (data: Omit<Category, 'id'>) => Promise<void>;
}

export default function CategoryModal({ category, onClose, onSave }: CategoryModalProps) {
  const [name, setName] = useState(category?.name || '');
  const [icon, setIcon] = useState(category?.icon || '📦');
  const [color, setColor] = useState(category?.color || '#3b82f6');
  const [budgetLimit, setBudgetLimit] = useState<string>(
    category?.budget_limit ? String(category.budget_limit / 100) : ''
  );
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const isEdit = !!category;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) { setError('Name is required'); return; }
    if (!icon.trim()) { setError('Icon is required'); return; }
    setError('');
    setSaving(true);
    try {
      await onSave({
        name: name.trim(),
        icon: icon.trim(),
        color,
        budget_limit: budgetLimit ? Math.round(parseFloat(budgetLimit) * 100) : null,
      });
      onClose();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to save category');
    } finally {
      setSaving(false);
    }
  };

  // Close on Escape
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="bg-card border border-border rounded-xl shadow-2xl w-full max-w-md mx-4">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-border">
          <h2 className="text-lg font-semibold text-primary">
            {isEdit ? 'Edit Category' : 'New Category'}
          </h2>
          <button onClick={onClose} className="p-1 hover:bg-border/40 rounded-md transition-colors">
            <X className="w-4 h-4 text-secondary" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          {/* Icon + Name row */}
          <div className="flex gap-3">
            <div className="space-y-1.5">
              <label className="text-xs text-secondary font-medium uppercase tracking-wide">Icon</label>
              <Input
                value={icon}
                onChange={e => setIcon(e.target.value)}
                className="w-16 text-center text-xl"
                maxLength={2}
              />
            </div>
            <div className="flex-1 space-y-1.5">
              <label className="text-xs text-secondary font-medium uppercase tracking-wide">Name</label>
              <Input
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="e.g. Food & Dining"
              />
            </div>
          </div>

          {/* Color swatches */}
          <div className="space-y-1.5">
            <label className="text-xs text-secondary font-medium uppercase tracking-wide">Color</label>
            <div className="flex flex-wrap gap-2">
              {COLOR_SWATCHES.map(c => (
                <button
                  key={c}
                  type="button"
                  onClick={() => setColor(c)}
                  className={`w-7 h-7 rounded-full transition-transform hover:scale-110 ${color === c ? 'ring-2 ring-offset-2 ring-offset-card ring-white scale-110' : ''}`}
                  style={{ backgroundColor: c }}
                />
              ))}
              {/* Custom hex input */}
              <input
                type="color"
                value={color}
                onChange={e => setColor(e.target.value)}
                className="w-7 h-7 rounded-full cursor-pointer border-0 p-0 bg-transparent"
                title="Custom color"
              />
            </div>
          </div>

          {/* Budget Limit */}
          <div className="space-y-1.5">
            <label className="text-xs text-secondary font-medium uppercase tracking-wide">
              Monthly Budget Limit (₹) <span className="normal-case text-secondary/60">— optional</span>
            </label>
            <Input
              type="number"
              min={0}
              step={100}
              value={budgetLimit}
              onChange={e => setBudgetLimit(e.target.value)}
              placeholder="e.g. 5000"
            />
          </div>

          {/* Preview */}
          <div className="flex items-center gap-3 p-3 rounded-lg border border-border/60 bg-background/50">
            <div
              className="w-10 h-10 rounded-lg flex items-center justify-center text-xl"
              style={{ backgroundColor: `${color}22` }}
            >
              {icon || '📦'}
            </div>
            <div>
              <p className="text-sm font-medium text-primary">{name || 'Category Name'}</p>
              {budgetLimit && (
                <p className="text-xs text-secondary">Budget: {formatINR(parseFloat(budgetLimit) * 100)}/mo</p>
              )}
            </div>
            <div className="ml-auto w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
          </div>

          {error && <p className="text-xs text-danger">{error}</p>}

          <div className="flex gap-3 pt-1">
            <Button type="button" variant="outline" onClick={onClose} className="flex-1">
              Cancel
            </Button>
            <Button type="submit" disabled={saving} className="flex-1">
              {saving ? 'Saving...' : isEdit ? 'Save Changes' : 'Create Category'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
