from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel
from database import get_db
from models import Category

router = APIRouter()

class CategoryCreate(BaseModel):
    name: str
    icon: str
    color: str
    budget_limit: Optional[int] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    budget_limit: Optional[int] = None

@router.get("")
@router.get("/")
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()

@router.post("")
@router.post("/")
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    db_category = Category(**category.dict())
    db.add(db_category)
    try:
        await db.commit()
        await db.refresh(db_category)
        return db_category
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Category already exists or invalid data")

@router.put("/{cat_id}")
async def update_category(
    cat_id: int,
    cat_update: CategoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Category).where(Category.id == cat_id))
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    for key, value in cat_update.dict(exclude_unset=True).items():
        setattr(category, key, value)
        
    await db.commit()
    await db.refresh(category)
    return category

@router.delete("/{cat_id}")
async def delete_category(
    cat_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Category).where(Category.id == cat_id))
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.delete(category)
    await db.commit()
    return {"status": "deleted", "id": cat_id}
