from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional, List
from database import get_db
from models import Transaction
from collections import defaultdict
from datetime import datetime, timedelta

router = APIRouter()

async def resolve_month(month: Optional[str], db: AsyncSession) -> Optional[str]:
    """Returns YYYY-MM string, or None when month='all' (no date filter)."""
    if month == 'all':
        return None
    if month and month != "current" and len(month) == 7 and month[4] == '-':
        return month
        
    # Find latest transaction date in DB
    query = select(Transaction.date).order_by(Transaction.date.desc()).limit(1)
    result = await db.execute(query)
    latest_date = result.scalar_one_or_none()
    
    if latest_date:
        return latest_date[:7] # e.g. 2026-09
        
    return datetime.utcnow().strftime("%Y-%m")

@router.get("/summary")
async def get_summary(
    month: Optional[str] = "current",
    username: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    actual_month = await resolve_month(month, db)
    
    query = select(Transaction)
    if actual_month:
        start_date = f"{actual_month}-01T00:00:00Z"
        end_date = f"{actual_month}-31T23:59:59Z"
        query = query.where(
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    if username:
        query = query.where(Transaction.username == username)
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    total_income = sum(t.amount for t in transactions if t.type == 'credit')
    total_expense = sum(t.amount for t in transactions if t.type == 'debit')
    net_savings = total_income - total_expense
    savings_rate = round((net_savings / total_income * 100), 1) if total_income > 0 else 0.0
    
    category_totals = defaultdict(int)
    for t in transactions:
        if t.type == 'debit':
            category_totals[t.category] += t.amount
            
    top_category = max(category_totals, key=category_totals.get) if category_totals else "None"
    
    return {
        "month": actual_month or "all",
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": net_savings,
        "savings_rate": savings_rate,
        "top_category": top_category
    }

@router.get("/categories")
async def get_category_breakdown(
    month: Optional[str] = "current",
    username: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    actual_month = await resolve_month(month, db)

    query = select(Transaction.category, func.sum(Transaction.amount).label('total'))\
        .where(Transaction.type == 'debit')
    if actual_month:
        start_date = f"{actual_month}-01T00:00:00Z"
        end_date = f"{actual_month}-31T23:59:59Z"
        query = query.where(
            Transaction.date >= start_date,
            Transaction.date <= end_date,
        )
    if username:
        query = query.where(Transaction.username == username)
    query = query.group_by(Transaction.category)
        
    result = await db.execute(query)
    breakdown = [{"category": row.category, "amount": row.total} for row in result.all()]
    
    total_expense = sum(item["amount"] for item in breakdown)
    for item in breakdown:
        item["percentage"] = round((item["amount"] / total_expense * 100), 1) if total_expense > 0 else 0
        
    return sorted(breakdown, key=lambda x: x["amount"], reverse=True)

@router.get("/cashflow")
async def get_cashflow(
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    username: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Transaction)
    if from_date:
        query = query.where(Transaction.date >= from_date)
    if to_date:
        query = query.where(Transaction.date <= to_date)
    if username:
        query = query.where(Transaction.username == username)
        
    query = query.order_by(Transaction.date.asc())
    
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    cashflow = defaultdict(lambda: {"inflow": 0, "outflow": 0})
    for t in transactions:
        date_key = t.date[:10] # YYYY-MM-DD
        if t.type == 'credit':
            cashflow[date_key]["inflow"] += t.amount
        else:
            cashflow[date_key]["outflow"] += t.amount
            
    return [{"date": k, **v} for k, v in sorted(cashflow.items())]

@router.get("/merchants")
async def get_top_merchants(
    month: Optional[str] = "current",
    limit: int = 10,
    username: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    actual_month = await resolve_month(month, db)
    
    query = select(
        Transaction.merchant,
        func.sum(Transaction.amount).label('total'),
        func.count(Transaction.id).label('count')
    ).where(Transaction.type == 'debit')
    
    if actual_month:
        start_date = f"{actual_month}-01T00:00:00Z"
        end_date = f"{actual_month}-31T23:59:59Z"
        query = query.where(
            Transaction.date >= start_date,
            Transaction.date <= end_date,
        )
    if username:
        query = query.where(Transaction.username == username)
    
    query = query.group_by(Transaction.merchant)\
        .order_by(func.sum(Transaction.amount).desc())\
        .limit(limit)
        
    result = await db.execute(query)
    return [{"merchant": row.merchant, "amount": row.total, "count": row.count} for row in result.all()]

@router.get("/monthlytrend")
async def get_monthly_trend(
    months: int = 6,
    db: AsyncSession = Depends(get_db)
):
    trend = []
    return trend

