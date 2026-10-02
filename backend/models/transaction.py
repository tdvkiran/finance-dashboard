from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Transaction(Base):
    """
    Transaction model representing a single financial transaction.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True) # ISO String
    description = Column(String)
    amount = Column(Integer) # Stored in paise/cents
    type = Column(String) # 'debit' or 'credit'
    category = Column(String, index=True)
    merchant = Column(String, index=True)
    source_bank = Column(String)
    username = Column(String, index=True, default="default")
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    raw_text = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
