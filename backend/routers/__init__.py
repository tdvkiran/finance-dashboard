from fastapi import APIRouter

from .upload import router as upload_router
from .transactions import router as transactions_router
from .analytics import router as analytics_router
from .categories import router as categories_router
from .users import router as users_router

__all__ = [
    "upload_router",
    "transactions_router",
    "analytics_router",
    "categories_router",
    "users_router",
]
