from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db

router = APIRouter()

@router.get("")
@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    """Return all distinct usernames that have transactions."""
    result = await db.execute(
        text("SELECT DISTINCT username FROM transactions WHERE username IS NOT NULL ORDER BY username")
    )
    users = [row[0] for row in result.all() if row[0]]
    return users
