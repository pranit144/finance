"""
Portfolio schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class PortfolioAdd(BaseModel):
    """Schema for adding a stock to portfolio."""
    symbol: str = Field(..., min_length=1, max_length=50, description="Stock symbol")
    shares: float = Field(..., gt=0, description="Number of shares")
    buying_date: date = Field(..., description="Date when stock was purchased")
    buying_price: Optional[float] = Field(None, gt=0, description="Price at purchase (optional)")


class PortfolioUpdate(BaseModel):
    """Schema for updating portfolio entry."""
    shares: Optional[float] = Field(None, gt=0)
    buying_date: Optional[date] = None
    buying_price: Optional[float] = Field(None, gt=0)


class PortfolioResponse(BaseModel):
    """Schema for portfolio response."""
    id: str
    user_id: str
    symbol: str
    shares: float
    buying_date: date
    buying_price: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NSEStock(BaseModel):
    """Schema for NSE stock symbol."""
    symbol: str
    name: str
    series: Optional[str] = None
