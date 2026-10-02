import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Pencil, Trash2 } from 'lucide-react';
import { Card, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { formatINR } from '../../lib/utils';
import { getCategories, createCategory, updateCategory, deleteCategory, getCategoryBreakdown } from '../../api/client';
import { Category } from '../../types';
import CategoryModal from './CategoryModal';
import { useStore } from '../../store/useStore';

export default function CategoriesPage() {
  const queryClient = useQueryClient();
  const { selectedMonth } = useStore();
  const [modalOpen, setModalOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  // Fetch categories list
  const { data: categories, isLoading } = useQuery({
    queryKey: ['categories-list'],
    queryFn: getCategories,
  });

  // Fetch spending breakdown for the selected month (to show budget usage)
  const { data: spending } = useQuery({
    queryKey: ['categories-spending', selectedMonth],
    queryFn: () => getCategoryBreakdown(selectedMonth || 'current'),
  });

  const spendingMap = new Map(spending?.map(s => [s.category, s.amount]) || []);

  const createMutation = useMutation({
    mutationFn: createCategory,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['categories-list'] }),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: Partial<Omit<Category, 'id'>> }) =>
      updateCategory(id, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['categories-list'] }),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteCategory,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['categories-list'] }),
  });

  const handleSave = async (data: Omit<Category, 'id'>) => {
    if (editingCategory) {
      await updateMutation.mutateAsync({ id: editingCategory.id, payload: data });
    } else {
      await createMutation.mutateAsync(data);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete this category? Existing transactions will keep the category name.')) return;
    setDeletingId(id);
    try {
      await deleteMutation.mutateAsync(id);
    } finally {
      setDeletingId(null);
    }
  };

  const openCreate = () => { setEditingCategory(null); setModalOpen(true); };
  const openEdit = (cat: Category) => { setEditingCategory(cat); setModalOpen(true); };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-primary">Categories</h1>
          <p className="text-sm text-secondary mt-1">
            Manage spending categories, icons, colors and monthly budgets
          </p>
        </div>
        <Button onClick={openCreate} className="flex items-center gap-2">
          <Plus className="w-4 h-4" />
          New Category
        </Button>
      </div>

      {/* Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-32 bg-border/20 rounded-xl animate-pulse" />
          ))}
        </div>
      ) : !categories || categories.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center text-secondary">
            No categories found. Click <strong>New Category</strong> to get started.
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {categories.map(cat => {
            const spent = spendingMap.get(cat.name) || 0;
            const budget = cat.budget_limit || 0;
            const pct = budget > 0 ? Math.min(Math.round((spent / budget) * 100), 100) : 0;
            const overBudget = budget > 0 && spent > budget;

            return (
              <Card key={cat.id} className="relative group">
                <CardContent className="p-5">
                  {/* Action buttons — visible on hover */}
                  <div className="absolute top-3 right-3 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => openEdit(cat)}
                      className="p-1.5 rounded-md hover:bg-border/40 text-secondary hover:text-primary transition-colors"
                    >
                      <Pencil className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => handleDelete(cat.id)}
                      disabled={deletingId === cat.id}
                      className="p-1.5 rounded-md hover:bg-danger/10 text-secondary hover:text-danger transition-colors"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  {/* Icon + Name */}
                  <div className="flex items-center gap-3 mb-3">
                    <div
                      className="w-10 h-10 rounded-lg flex items-center justify-center text-xl flex-shrink-0"
                      style={{ backgroundColor: `${cat.color}22` }}
                    >
                      {cat.icon}
                    </div>
                    <div className="min-w-0">
                      <p className="font-semibold text-primary truncate">{cat.name}</p>
                      {spent > 0 ? (
                        <p className="text-xs text-secondary">{formatINR(spent)} spent</p>
                      ) : (
                        <p className="text-xs text-secondary/50">No spending this period</p>
                      )}
                    </div>
                    <div className="ml-auto flex-shrink-0 w-2.5 h-2.5 rounded-full" style={{ backgroundColor: cat.color }} />
                  </div>

                  {/* Budget progress */}
                  {budget > 0 ? (
                    <div className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span className={overBudget ? 'text-danger font-medium' : 'text-secondary'}>
                          {overBudget ? '⚠ Over budget' : `${pct}% used`}
                        </span>
                        <span className="text-secondary">{formatINR(budget)}/mo</span>
                      </div>
                      <Progress
                        value={pct}
                        className={`h-1.5 ${overBudget ? '[&>div]:bg-danger' : ''}`}
                      />
                    </div>
                  ) : (
                    <Badge variant="secondary" className="text-xs font-normal">No budget set</Badge>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      {/* Modal */}
      {modalOpen && (
        <CategoryModal
          category={editingCategory}
          onClose={() => setModalOpen(false)}
          onSave={handleSave}
        />
      )}
    </div>
  );
}
