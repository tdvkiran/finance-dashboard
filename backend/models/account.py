from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Account(Base):
    """
    Account model representing a user's bank account.
    """
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    bank = Column(String, index=True)
    account_number_last4 = Column(String)
    balance = Column(Integer)  # Stored in paise/cents
    currency = Column(String, default="INR")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
