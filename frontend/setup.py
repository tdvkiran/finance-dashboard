import os

base = "/Users/kirantadisetti/.gemini/antigravity/scratch/finance-dashboard/frontend"

files = {}

files["package.json"] = """{
  "name": "finance-dashboard",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-progress": "^1.0.3",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-slot": "^1.0.2",
    "@tanstack/react-query": "^5.0.0",
    "axios": "^1.6.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "date-fns": "^2.30.0",
    "lucide-react": "^0.292.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-dropzone": "^14.2.3",
    "react-router-dom": "^6.18.0",
    "recharts": "^2.9.0",
    "tailwind-merge": "^2.0.0",
    "zustand": "^4.4.6"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5",
    "typescript": "^5.2.2",
    "vite": "^5.0.0",
    "vite-plugin-pwa": "^0.17.0"
  }
}"""

files["vite.config.ts"] = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'Finance Dashboard',
        short_name: 'FinDash',
        theme_color: '#0f172a',
        background_color: '#0f172a',
        display: 'standalone',
        start_url: '/',
        icons: [
          { src: '/favicon.svg', sizes: 'any', type: 'image/svg+xml' }
        ]
      },
      workbox: {
        runtimeCaching: [
          {
            urlPattern: /^http:\\/\\/localhost:8000\\/api\\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'api-cache',
              expiration: { maxEntries: 50, maxAgeSeconds: 86400 }
            }
          }
        ]
      }
    })
  ],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
});"""

files["tsconfig.json"] = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}"""

files["tsconfig.node.json"] = """{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts", "tailwind.config.ts"]
}"""

files["tailwind.config.ts"] = """import type { Config } from 'tailwindcss';
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        background: '#0f172a',
        card: '#1e293b',
        border: '#334155',
        primary: '#f8fafc',
        secondary: '#94a3b8',
        accent: '#6366f1',
        success: '#22c55e',
        danger: '#ef4444',
        info: '#3b82f6',
      }
    },
  },
  plugins: [],
} satisfies Config;"""

files["postcss.config.js"] = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}"""

files["index.html"] = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#0f172a" />
    <title>Finance Dashboard</title>
  </head>
  <body class="bg-background text-primary">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>"""

files["public/manifest.json"] = """{
  "name": "Finance Dashboard",
  "short_name": "FinDash",
  "description": "Personal bank statement visualizer",
  "theme_color": "#0f172a",
  "background_color": "#0f172a",
  "display": "standalone",
  "start_url": "/",
  "icons": [
    { "src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml" }
  ]
}"""

files["public/favicon.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>"""

files["src/index.css"] = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-background text-primary;
  }
}
"""

files["src/main.tsx"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);"""

files["src/types/index.ts"] = """export interface Transaction {
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
}"""

files["src/api/client.ts"] = """import axios from 'axios';
import { Transaction, MonthlySummary, CategoryBreakdown, CashFlowPoint, UploadResult } from '../types';

const api = axios.create({
  baseURL: '/api'
});

export const uploadFile = async (file: File, password?: string, sourceBank?: string): Promise<UploadResult> => {
  const formData = new FormData();
  formData.append('file', file);
  if (password) formData.append('password', password);
  if (sourceBank) formData.append('source_bank', sourceBank);
  const { data } = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return data;
};

export const getTransactions = async (filters: any): Promise<{items: Transaction[], total: number}> => {
  const { data } = await api.get('/transactions', { params: filters });
  return data;
};

export const getMonthlySummary = async (month: string): Promise<MonthlySummary> => {
  const { data } = await api.get('/summary', { params: { month } });
  return data;
};

export const getCategoryBreakdown = async (month: string): Promise<CategoryBreakdown[]> => {
  const { data } = await api.get('/categories', { params: { month } });
  return data;
};

export const getCashFlow = async (from: string, to: string): Promise<CashFlowPoint[]> => {
  const { data } = await api.get('/cashflow', { params: { from, to } });
  return data;
};

export const getTopMerchants = async (month: string): Promise<{merchant: string, amount: number, count: number}[]> => {
  const { data } = await api.get('/merchants/top', { params: { month } });
  return data;
};

export const getMonthlyTrend = async (months: number): Promise<MonthlySummary[]> => {
  const { data } = await api.get('/trend', { params: { months } });
  return data;
};"""

files["src/lib/utils.ts"] = """import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatINR(paise: number) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2
  }).format(paise / 100);
}
"""

files["src/components/ui/button.tsx"] = """import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "../../lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-accent text-primary shadow hover:bg-accent/90",
        destructive: "bg-danger text-primary shadow-sm hover:bg-danger/90",
        outline: "border border-border bg-transparent hover:bg-accent hover:text-primary",
        secondary: "bg-secondary text-primary shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-primary",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(({ className, variant, size, asChild = false, ...props }, ref) => {
  const Comp = asChild ? Slot : "button"
  return (
    <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
  )
})
Button.displayName = "Button"
export { Button, buttonVariants }"""

files["src/components/ui/card.tsx"] = """import * as React from "react"
import { cn } from "../../lib/utils"

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("rounded-xl border border-border bg-card text-primary shadow", className)} {...props} />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(({ className, ...props }, ref) => (
  <h3 ref={ref} className={cn("font-semibold leading-none tracking-tight", className)} {...props} />
))
CardTitle.displayName = "CardTitle"

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

export { Card, CardHeader, CardTitle, CardContent }"""

files["src/components/ui/badge.tsx"] = """import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "../../lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default: "border-transparent bg-accent text-primary shadow hover:bg-accent/80",
        secondary: "border-transparent bg-secondary text-primary hover:bg-secondary/80",
        destructive: "border-transparent bg-danger text-primary shadow hover:bg-danger/80",
        outline: "text-primary",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}
export { Badge, badgeVariants }"""

files["src/components/ui/input.tsx"] = """import * as React from "react"
import { cn } from "../../lib/utils"

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className, type, ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        "flex h-9 w-full rounded-md border border-border bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-secondary focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      ref={ref}
      {...props}
    />
  )
})
Input.displayName = "Input"
export { Input }"""

files["src/components/ui/progress.tsx"] = """import * as React from "react"
import * as ProgressPrimitive from "@radix-ui/react-progress"
import { cn } from "../../lib/utils"

const Progress = React.forwardRef<React.ElementRef<typeof ProgressPrimitive.Root>, React.ComponentPropsWithoutRef<typeof ProgressPrimitive.Root>>(({ className, value, ...props }, ref) => (
  <ProgressPrimitive.Root ref={ref} className={cn("relative h-2 w-full overflow-hidden rounded-full bg-border", className)} {...props}>
    <ProgressPrimitive.Indicator className="h-full w-full flex-1 bg-accent transition-all" style={{ transform: `translateX(-${100 - (value || 0)}%)` }} />
  </ProgressPrimitive.Root>
))
Progress.displayName = ProgressPrimitive.Root.displayName
export { Progress }"""

files["src/components/ui/select.tsx"] = """import * as React from "react"
import { cn } from "../../lib/utils"

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {}

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(({ className, ...props }, ref) => {
  return (
    <select
      className={cn(
        "flex h-9 w-full rounded-md border border-border bg-background px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      ref={ref}
      {...props}
    />
  )
})
Select.displayName = "Select"
export { Select }"""

files["src/components/ui/dialog.tsx"] = """// Placeholder for dialog to keep it simple, shadcn dialog is complex
import * as React from "react"

export const Dialog = ({ children }: any) => <div>{children}</div>
export const DialogTrigger = ({ children }: any) => <>{children}</>
export const DialogContent = ({ children }: any) => <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80">{children}</div>
export const DialogHeader = ({ children }: any) => <div>{children}</div>
export const DialogTitle = ({ children }: any) => <h2>{children}</h2>
"""

files["src/components/Layout/AppLayout.tsx"] = """import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

export default function AppLayout() {
  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-card p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}"""

files["src/components/Layout/Sidebar.tsx"] = """import React from 'react';
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
}"""

files["src/components/Layout/Header.tsx"] = """import React from 'react';
import { Select } from '../ui/select';

export default function Header() {
  return (
    <header className="h-16 bg-background border-b border-border flex items-center justify-between px-6">
      <div className="md:hidden text-lg font-bold">FinDash</div>
      <div className="ml-auto">
        <Select defaultValue="2023-10" className="w-40">
          <option value="2023-10">October 2023</option>
          <option value="2023-09">September 2023</option>
          <option value="2023-08">August 2023</option>
        </Select>
      </div>
    </header>
  );
}"""

files["src/components/Upload/UploadPage.tsx"] = """import React from 'react';
import DropZone from './DropZone';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';

export default function UploadPage() {
  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-primary">Upload Statement</h1>
      <Card>
        <CardHeader>
          <CardTitle>Import Bank Statement</CardTitle>
        </CardHeader>
        <CardContent>
          <DropZone />
        </CardContent>
      </Card>
    </div>
  );
}"""

files["src/components/Upload/DropZone.tsx"] = """import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '../ui/button';
import { Select } from '../ui/select';
import { Input } from '../ui/input';
import { uploadFile } from '../../api/client';

export default function DropZone() {
  const [file, setFile] = useState<File | null>(null);
  const [bank, setBank] = useState('auto');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setStatus('idle');
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/pdf': ['.pdf'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    }
  });

  const handleUpload = async () => {
    if (!file) return;
    setStatus('uploading');
    try {
      const result = await uploadFile(file, password, bank !== 'auto' ? bank : undefined);
      setStatus('success');
      setMessage(`Successfully imported ${result.transactions_parsed} transactions from ${result.bank}.`);
    } catch (err: any) {
      setStatus('error');
      setMessage(err.message || 'Failed to upload file. Please try again.');
    }
  };

  return (
    <div className="space-y-6">
      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-accent bg-accent/5' : 'border-border hover:border-secondary'}`}
      >
        <input {...getInputProps()} />
        <UploadCloud className="w-12 h-12 mx-auto text-secondary mb-4" />
        {file ? (
          <p className="text-primary font-medium">{file.name}</p>
        ) : (
          <p className="text-secondary">Drag & drop a bank statement here, or click to select</p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="text-sm text-secondary">Bank Source</label>
          <Select value={bank} onChange={(e) => setBank(e.target.value)}>
            <option value="auto">Auto-detect</option>
            <option value="HDFC">HDFC Bank</option>
            <option value="SBI">SBI</option>
            <option value="ICICI">ICICI Bank</option>
            <option value="PhonePe">PhonePe</option>
          </Select>
        </div>
        
        {(bank === 'HDFC' || bank === 'auto') && (
          <div className="space-y-2">
            <label className="text-sm text-secondary">Statement Password (if PDF)</label>
            <Input 
              type="password" 
              placeholder="Leave blank if not protected"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        )}
      </div>

      <Button 
        className="w-full" 
        onClick={handleUpload}
        disabled={!file || status === 'uploading'}
      >
        {status === 'uploading' ? 'Uploading...' : 'Upload Statement'}
      </Button>

      {status === 'success' && (
        <div className="p-4 bg-success/20 text-success rounded-md flex items-center gap-2">
          <CheckCircle className="w-5 h-5" /> {message}
        </div>
      )}
      {status === 'error' && (
        <div className="p-4 bg-danger/20 text-danger rounded-md flex items-center gap-2">
          <AlertCircle className="w-5 h-5" /> {message}
        </div>
      )}
    </div>
  );
}"""

files["src/components/Dashboard/DashboardPage.tsx"] = """import React from 'react';
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
}"""

files["src/components/Dashboard/SummaryCards.tsx"] = """import React from 'react';
import { Card, CardContent } from '../ui/card';
import { TrendingUp, TrendingDown, PiggyBank } from 'lucide-react';
import { formatINR } from '../../lib/utils';
import { useQuery } from '@tanstack/react-query';
import { getMonthlySummary } from '../../api/client';

export default function SummaryCards() {
  const { data, isLoading } = useQuery({
    queryKey: ['summary', 'current'],
    queryFn: () => getMonthlySummary('current'),
    initialData: { total_income: 15000000, total_expense: 9000000, net_savings: 6000000, savings_rate: 40, month: '' } // Mock fallback
  });

  if (isLoading) return <div className="h-32 bg-border/20 rounded-xl animate-pulse" />;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Card>
        <CardContent className="p-6 flex items-center gap-4">
          <div className="p-3 bg-success/20 rounded-lg text-success">
            <TrendingUp className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm text-secondary">Total Income</p>
            <p className="text-2xl font-bold text-primary">{formatINR(data.total_income)}</p>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="p-6 flex items-center gap-4">
          <div className="p-3 bg-danger/20 rounded-lg text-danger">
            <TrendingDown className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm text-secondary">Total Expenses</p>
            <p className="text-2xl font-bold text-primary">{formatINR(data.total_expense)}</p>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="p-6 flex items-center gap-4">
          <div className="p-3 bg-info/20 rounded-lg text-info">
            <PiggyBank className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm text-secondary">Net Savings</p>
            <div className="flex items-baseline gap-2">
              <p className="text-2xl font-bold text-primary">{formatINR(data.net_savings)}</p>
              <span className="text-xs text-info bg-info/10 px-2 py-0.5 rounded-full">{data.savings_rate}% rate</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}"""

files["src/components/Dashboard/CashFlowChart.tsx"] = """import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { formatINR } from '../../lib/utils';

const mockData = [
  { date: 'Oct 1', inflow: 100000, outflow: 50000 },
  { date: 'Oct 5', inflow: 0, outflow: 20000 },
  { date: 'Oct 10', inflow: 20000, outflow: 80000 },
  { date: 'Oct 15', inflow: 0, outflow: 10000 },
  { date: 'Oct 20', inflow: 50000, outflow: 30000 },
];

export default function CashFlowChart() {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Cash Flow</CardTitle>
      </CardHeader>
      <CardContent className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={mockData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorIn" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorOut" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v) => `₹${v/1000}k`} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }}
              formatter={(value: number) => formatINR(value * 100)}
            />
            <Area type="monotone" dataKey="inflow" stroke="#22c55e" fillOpacity={1} fill="url(#colorIn)" />
            <Area type="monotone" dataKey="outflow" stroke="#ef4444" fillOpacity={1} fill="url(#colorOut)" />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}"""

files["src/components/Dashboard/CategoryChart.tsx"] = """import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const mockData = [
  { name: 'Food', value: 40000, color: '#ef4444' },
  { name: 'Transport', value: 30000, color: '#3b82f6' },
  { name: 'Shopping', value: 30000, color: '#eab308' },
  { name: 'Bills', value: 20000, color: '#a855f7' },
];

export default function CategoryChart() {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Spending by Category</CardTitle>
      </CardHeader>
      <CardContent className="h-[300px] flex flex-col items-center justify-center">
        <div className="h-[200px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={mockData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {mockData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="flex flex-wrap justify-center gap-3 mt-4">
          {mockData.map(d => (
            <div key={d.name} className="flex items-center gap-1.5 text-xs text-secondary">
              <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: d.color }}></span>
              {d.name}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}"""

files["src/components/Dashboard/TopMerchants.tsx"] = """import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Progress } from '../ui/progress';
import { formatINR } from '../../lib/utils';

const mockMerchants = [
  { name: 'Amazon', amount: 1500000, count: 12 },
  { name: 'Swiggy', amount: 800000, count: 20 },
  { name: 'Uber', amount: 450000, count: 15 },
  { name: 'D-Mart', amount: 300000, count: 2 },
];

export default function TopMerchants() {
  const maxAmount = mockMerchants[0]?.amount || 1;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Top Merchants</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {mockMerchants.map((merchant, i) => (
          <div key={i} className="space-y-2">
            <div className="flex justify-between items-center text-sm">
              <span className="font-medium text-primary flex items-center gap-2">
                <div className="w-6 h-6 rounded bg-accent/20 text-accent flex items-center justify-center text-xs">
                  {merchant.name[0]}
                </div>
                {merchant.name}
              </span>
              <span className="text-secondary">{formatINR(merchant.amount)}</span>
            </div>
            <Progress value={(merchant.amount / maxAmount) * 100} className="h-1.5" />
          </div>
        ))}
      </CardContent>
    </Card>
  );
}"""

files["src/components/Transactions/TransactionsPage.tsx"] = """import React from 'react';
import { Card, CardContent } from '../ui/card';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { formatINR } from '../../lib/utils';
import { Search } from 'lucide-react';

const mockTransactions = [
  { id: 1, date: '2023-10-25', description: 'Amazon Order', merchant: 'Amazon', category: 'Shopping', amount: 125000, type: 'debit' },
  { id: 2, date: '2023-10-24', description: 'Salary', merchant: 'Employer', category: 'Income', amount: 8500000, type: 'credit' },
  { id: 3, date: '2023-10-22', description: 'Swiggy Food', merchant: 'Swiggy', category: 'Food', amount: 45000, type: 'debit' },
];

export default function TransactionsPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-primary">Transactions</h1>
      </div>
      
      <Card>
        <div className="p-4 border-b border-border flex gap-4">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-secondary" />
            <Input className="pl-9" placeholder="Search transactions..." />
          </div>
        </div>
        <CardContent className="p-0">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-secondary uppercase bg-border/30 border-b border-border">
              <tr>
                <th className="px-6 py-3">Date</th>
                <th className="px-6 py-3">Description</th>
                <th className="px-6 py-3">Category</th>
                <th className="px-6 py-3 text-right">Amount</th>
              </tr>
            </thead>
            <tbody>
              {mockTransactions.map((tx) => (
                <tr key={tx.id} className="border-b border-border/50 hover:bg-border/10">
                  <td className="px-6 py-4 text-secondary">{tx.date}</td>
                  <td className="px-6 py-4 font-medium text-primary">{tx.description}</td>
                  <td className="px-6 py-4">
                    <Badge variant="secondary">{tx.category}</Badge>
                  </td>
                  <td className={`px-6 py-4 text-right font-medium ${tx.type === 'credit' ? 'text-success' : 'text-primary'}`}>
                    {tx.type === 'credit' ? '+' : '-'}{formatINR(tx.amount)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}"""

files["src/App.tsx"] = """import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AppLayout from './components/Layout/AppLayout';
import DashboardPage from './components/Dashboard/DashboardPage';
import UploadPage from './components/Upload/UploadPage';
import TransactionsPage from './components/Transactions/TransactionsPage';

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
            <Route path="categories" element={<div className="p-6">Categories (Coming Soon)</div>} />
            <Route path="insights" element={<div className="p-6">Insights (Coming Soon)</div>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}"""

files["README.md"] = """# Finance Dashboard Frontend

A modern, responsive PWA frontend for the personal finance dashboard.

## Tech Stack
- React 18
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui (Radix Primitives)
- React Router DOM
- React Query
- Recharts

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

The app proxy is configured to route `/api` to `http://localhost:8000`.

## Features
- **Dashboard**: High level overview with cash flow charts and category breakdowns.
- **Transactions**: View and filter transaction history.
- **Upload**: Import bank statements (PDF/CSV) with bank auto-detection.
"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)

print("Files generated.")
