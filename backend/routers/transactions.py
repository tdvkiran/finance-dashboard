import io
import csv
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import Optional, List
from database import get_db
from models import Transaction
from pydantic import BaseModel

router = APIRouter()

class TransactionUpdate(BaseModel):
    category: Optional[str] = None
    description: Optional[str] = None

@router.get("")
@router.get("/")
async def get_transactions(
    db: AsyncSession = Depends(get_db),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    bank: Optional[str] = None,
    search: Optional[str] = None,
    min_amount: Optional[int] = None,
    max_amount: Optional[int] = None,
    username: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0
):
    from sqlalchemy import func
    base_query = select(Transaction)
    
    if start_date:
        base_query = base_query.where(Transaction.date >= start_date)
    if end_date:
        base_query = base_query.where(Transaction.date <= end_date)
    if category:
        base_query = base_query.where(Transaction.category == category)
    if bank:
        base_query = base_query.where(Transaction.source_bank == bank)
    if username:
        base_query = base_query.where(Transaction.username == username)
    if search:
        search_filter = f"%{search}%"
        base_query = base_query.where(or_(
            Transaction.description.ilike(search_filter),
            Transaction.merchant.ilike(search_filter)
        ))
    if min_amount is not None:
        base_query = base_query.where(Transaction.amount >= min_amount)
    if max_amount is not None:
        base_query = base_query.where(Transaction.amount <= max_amount)
        
    count_query = select(func.count()).select_from(base_query.subquery())
    total_res = await db.execute(count_query)
    total_count = total_res.scalar_one()

    query = base_query.order_by(Transaction.date.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    return {
        "items": items,
        "total": total_count
    }

@router.put("/{txn_id}")
async def update_transaction(
    txn_id: int,
    txn_update: TransactionUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Transaction).where(Transaction.id == txn_id))
    txn = result.scalar_one_or_none()
    
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    if txn_update.category:
        txn.category = txn_update.category
    if txn_update.description:
        txn.description = txn_update.description
        
    await db.commit()
    await db.refresh(txn)
    return txn

@router.delete("/{txn_id}")
async def delete_transaction(
    txn_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Transaction).where(Transaction.id == txn_id))
    txn = result.scalar_one_or_none()
    
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    await db.delete(txn)
    await db.commit()
    return {"status": "deleted"}

@router.get("/months")
async def get_available_months(db: AsyncSession = Depends(get_db)):
    """Return a sorted list of distinct YYYY-MM strings that have transactions."""
    from sqlalchemy import text
    result = await db.execute(
        text("SELECT DISTINCT substr(date, 1, 7) as month FROM transactions ORDER BY month DESC")
    )
    months = [row[0] for row in result.all() if row[0]]
    return months

@router.get("/export")
async def export_transactions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Transaction).order_by(Transaction.date.desc()))
    transactions = result.scalars().all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Description', 'Amount', 'Type', 'Category', 'Merchant', 'Source Bank'])
    
    for txn in transactions:
        writer.writerow([
            txn.date, txn.description, txn.amount / 100, txn.type, 
            txn.category, txn.merchant, txn.source_bank
        ])
        
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"}
    )
