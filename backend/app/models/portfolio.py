"""
Portfolio database model for tracking user stock holdings.
"""
from sqlalchemy import Column, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date
import uuid

from ..core.database import Base


class Portfolio(Base):
    """Portfolio model for tracking user stock holdings."""
    
    __tablename__ = "portfolio"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    symbol = Column(String(50), nullable=False, index=True)
    shares = Column(Float, nullable=False)
    buying_date = Column(Date, nullable=False)
    buying_price = Column(Float, nullable=True)  # Optional: price at purchase
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to user
    # user = relationship("User", back_populates="portfolio")
    
    def __repr__(self):
        return f"<Portfolio {self.symbol} - {self.shares} shares>"
