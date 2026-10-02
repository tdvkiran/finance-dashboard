from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Category(Base):
    """
    Category model for transaction categorization.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    icon = Column(String)
    color = Column(String)
    budget_limit = Column(Integer, nullable=True)  # Stored in paise/cents
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
