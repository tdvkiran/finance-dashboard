# 💰 Finance Dashboard

A full-stack personal finance dashboard for importing, visualizing, and managing bank statements from multiple Indian banks and UPI apps. Built with a **FastAPI** backend and a **React + TypeScript** frontend.

---

## ✨ Features

### 📤 Statement Import (Upload)
- Drag & drop or click-to-select (PDF, CSV, XLS, XLSX)
- **Supported sources**: HDFC Bank, SBI, IDFC First, Central Bank of India, PhonePe, Google Pay, CRED
- Auto-detect bank/app from filename
- PDF password support for protected statements
- Assign statements to a named **user profile** (e.g. "Kiran", "Spouse")
- Automatic deduplication — skips transactions already in the database

### 💳 Transactions
- Table view with all imported transactions
- Filter by **month** (via global month picker), **type** (debit/credit), **category**, and **search**
- Filter by **user profile**
- Edit transaction category or description
- Delete transactions
- Export all transactions as CSV

### 📊 Dashboard
- **Summary Cards** — Total Income, Total Expenses, Net Savings + savings rate %
- **Cash Flow Trend** — Area chart of daily inflow vs. outflow
- **Spending by Category** — Donut chart with percentages
- **Top Merchants** — Top spenders with progress bars

All dashboard widgets react to the global **month** and **user** filters in the header.

### 🗂️ Categories
- Card grid showing all categories with icon, color, name, and spending
- **Budget limits** per category with a monthly progress bar (turns red if over budget)
- Create, Edit, and Delete categories via a modal form
  - Emoji icon picker
  - Color swatches + custom color input
  - Optional monthly budget limit (INR)

### 🗓️ Global Month Picker
- Popover panel in the header with **← Year →** navigation arrows
- 4×3 month grid — months without data are dimmed and non-selectable
- **"All Time"** option shows data across all months

### 👤 Multi-User Profiles
- Upload statements under a named profile
- **User selector** in the header (appears automatically when 2+ users exist)
- Dashboard charts, summary cards, and transactions list all filter by selected user
- **"All Users"** option shows combined data

---

## 🏗️ Architecture

```
finance-dashboard/
├── backend/                  # FastAPI + SQLAlchemy + SQLite
│   ├── main.py               # App entry point, CORS, lifespan, seeding
│   ├── database.py           # Async SQLite engine (~/.finance-dashboard/data.db)
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── transaction.py    # Transaction (date, amount, type, category, username…)
│   │   ├── category.py       # Category (name, icon, color, budget_limit)
│   │   └── account.py        # Account (bank account metadata)
│   ├── routers/              # FastAPI route handlers
│   │   ├── transactions.py   # CRUD + /months endpoint
│   │   ├── analytics.py      # Summary, categories, cashflow, merchants
│   │   ├── categories.py     # Category CRUD
│   │   ├── upload.py         # Statement ingestion pipeline
│   │   └── users.py          # GET /api/users — distinct user profiles
│   ├── parsers/              # Bank-specific PDF/CSV parsers
│   │   ├── base.py           # BaseParser + ParsedTransaction dataclass
│   │   ├── hdfc.py
│   │   ├── sbi.py
│   │   ├── idfc.py
│   │   ├── central_bank.py
│   │   ├── phonepe.py
│   │   ├── google_pay.py
│   │   └── cred.py
│   └── services/
│       └── categorization.py # Rule-based keyword auto-categorization
│
└── frontend/                 # React 18 + TypeScript + Vite
    └── src/
        ├── api/client.ts     # Axios API calls for all endpoints
        ├── store/useStore.ts # Zustand global state (selectedMonth, selectedUser)
        ├── types/index.ts    # TypeScript interfaces
        ├── components/
        │   ├── Layout/       # AppLayout, Header (month picker + user selector), Sidebar
        │   ├── Dashboard/    # SummaryCards, CashFlowChart, CategoryChart, TopMerchants
        │   ├── Transactions/ # TransactionsPage (table, filters)
        │   ├── Categories/   # CategoriesPage (grid), CategoryModal (create/edit)
        │   ├── Upload/       # UploadPage, DropZone
        │   └── ui/           # Reusable: Button, Card, Input, Select, Badge,
        │                     #           MonthYearPicker, Progress, Dialog
        └── hooks/
            ├── useTransactions.ts
            └── useAnalytics.ts
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+

### 1. Backend

```bash
cd backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API is available at `http://localhost:8000`.  
Interactive docs (Swagger UI): `http://localhost:8000/docs`

> The SQLite database is stored at `~/.finance-dashboard/data.db` and is created automatically on first run. Default categories are seeded on startup.

### 2. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app is available at `http://localhost:5173`.  
All `/api/*` requests are proxied to `http://localhost:8000`.

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload a bank statement |
| `GET` | `/api/transactions` | List transactions (filterable) |
| `GET` | `/api/transactions/months` | Distinct months with transaction data |
| `GET` | `/api/transactions/export` | Download all transactions as CSV |
| `PUT` | `/api/transactions/{id}` | Edit category / description |
| `DELETE` | `/api/transactions/{id}` | Delete a transaction |
| `GET` | `/api/analytics/summary` | Monthly income/expense/savings |
| `GET` | `/api/analytics/categories` | Spending breakdown by category |
| `GET` | `/api/analytics/cashflow` | Daily inflow/outflow timeline |
| `GET` | `/api/analytics/merchants` | Top merchants by spend |
| `GET` | `/api/categories` | List categories |
| `POST` | `/api/categories` | Create a category |
| `PUT` | `/api/categories/{id}` | Update a category |
| `DELETE` | `/api/categories/{id}` | Delete a category |
| `GET` | `/api/users` | Distinct user profiles |
| `GET` | `/health` | Health check |

**Common query parameters:**
- `month` — `YYYY-MM` or `all` (analytics endpoints)
- `username` — filter by user profile (all endpoints)
- `start_date` / `end_date` — ISO date strings (transactions)
- `search`, `category`, `bank` — additional transaction filters

---

## 🗂️ Auto-Categorization

Transactions are categorized automatically on import using keyword matching against the description and merchant name.

| Category | Example keywords |
|---|---|
| Food & Dining | zomato, swiggy, dominos, kfc, blinkit |
| Groceries | bigbasket, instamart, supermarket |
| Transport | uber, ola, rapido, irctc, petrol |
| Shopping | amazon, flipkart, myntra, nykaa |
| Entertainment | netflix, spotify, hotstar, pvr |
| Health & Medical | apollo, medplus, pharmacy, hospital |
| Finance & Investment | zerodha, groww, lic, insurance |
| Home & Utilities | airtel, jio, bescom, electricity |
| ATM & Cash | atm, cash withdrawal |
| EMI & Loans | emi, bajaj, loan |
| Transfers | transfer, sent to, received from |

Unrecognized merchants fall back to **"Other"**.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** — async REST API
- **SQLAlchemy** (async) — ORM
- **aiosqlite** — async SQLite driver
- **pdfplumber** — PDF text extraction
- **pydantic** — request/response validation

### Frontend
- **React 18** + **TypeScript**
- **Vite** — build tool + dev server with proxy
- **Tailwind CSS** — utility-first styling
- **Zustand** — global state (month/user filters)
- **TanStack Query** — server state & caching
- **Recharts** — charts (area, pie)
- **React Router DOM** — client-side routing
- **Lucide React** — icons
- **Vite PWA** — Progressive Web App support
