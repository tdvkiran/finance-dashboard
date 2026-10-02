import os
import contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from database import engine, Base, AsyncSessionLocal
from models import Category
from routers import upload_router, transactions_router, analytics_router, categories_router, users_router

# Default categories to seed
DEFAULT_CATEGORIES = [
    {"name": "Food & Dining", "icon": "🍔", "color": "#FF5733"},
    {"name": "Transport", "icon": "🚗", "color": "#3357FF"},
    {"name": "Shopping", "icon": "🛍️", "color": "#FF33A8"},
    {"name": "Entertainment", "icon": "🎬", "color": "#9D33FF"},
    {"name": "Utilities", "icon": "💡", "color": "#33FFF6"},
    {"name": "Health & Medical", "icon": "🏥", "color": "#FF3333"},
    {"name": "Finance & Investment", "icon": "📈", "color": "#33FF57"},
    {"name": "ATM & Cash", "icon": "💵", "color": "#808080"},
    {"name": "EMI & Loans", "icon": "🏦", "color": "#FF8C00"},
    {"name": "Salary & Income", "icon": "💰", "color": "#008000"},
    {"name": "Transfers", "icon": "🔄", "color": "#00CED1"},
    {"name": "Other", "icon": "📦", "color": "#A9A9A9"}
]

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Safe migration: add username column if it doesn't exist yet
    async with engine.begin() as conn:
        try:
            await conn.execute(
                text("ALTER TABLE transactions ADD COLUMN username TEXT DEFAULT 'default'")
            )
        except Exception:
            pass  # Column already exists — skip
        
    # Seed default categories
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Category))
        existing_categories = result.scalars().all()
        
        if not existing_categories:
            for cat_data in DEFAULT_CATEGORIES:
                session.add(Category(**cat_data))
            await session.commit()
            
    yield
    # Cleanup
    pass

app = FastAPI(title="Finance Dashboard API", lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(transactions_router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(categories_router, prefix="/api/categories", tags=["Categories"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Serve static files if they exist
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
