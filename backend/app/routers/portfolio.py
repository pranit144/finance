"""
Portfolio API endpoints for managing user stock holdings.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..models.portfolio import Portfolio
from ..schemas.portfolio import PortfolioAdd, PortfolioUpdate, PortfolioResponse

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.post("/add", response_model=PortfolioResponse)
async def add_to_portfolio(
    portfolio_data: PortfolioAdd,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a stock to user's portfolio.
    
    **Requires authentication.**
    """
    # Check if stock already exists in portfolio
    existing = db.query(Portfolio).filter(
        Portfolio.user_id == current_user.id,
        Portfolio.symbol == portfolio_data.symbol.upper()
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Stock {portfolio_data.symbol} already exists in your portfolio"
        )
    
    # Create new portfolio entry
    portfolio_entry = Portfolio(
        user_id=current_user.id,
        symbol=portfolio_data.symbol.upper(),
        shares=portfolio_data.shares,
        buying_date=portfolio_data.buying_date,
        buying_price=portfolio_data.buying_price
    )
    
    db.add(portfolio_entry)
    db.commit()
    db.refresh(portfolio_entry)
    
    return portfolio_entry


@router.get("/", response_model=List[PortfolioResponse])
async def get_portfolio(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's complete portfolio.
    
    **Requires authentication.**
    """
    portfolio = db.query(Portfolio).filter(
        Portfolio.user_id == current_user.id
    ).order_by(Portfolio.created_at.desc()).all()
    
    return portfolio


@router.delete("/{portfolio_id}")
async def remove_from_portfolio(
    portfolio_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a stock from portfolio.
    
    **Requires authentication.**
    """
    portfolio_entry = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()
    
    if not portfolio_entry:
        raise HTTPException(
            status_code=404,
            detail="Portfolio entry not found"
        )
    
    db.delete(portfolio_entry)
    db.commit()
    
    return {"message": f"Removed {portfolio_entry.symbol} from portfolio"}


@router.put("/{portfolio_id}", response_model=PortfolioResponse)
async def update_portfolio_entry(
    portfolio_id: str,
    update_data: PortfolioUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a portfolio entry.
    
    **Requires authentication.**
    """
    portfolio_entry = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()
    
    if not portfolio_entry:
        raise HTTPException(
            status_code=404,
            detail="Portfolio entry not found"
        )
    
    # Update fields if provided
    if update_data.shares is not None:
        portfolio_entry.shares = update_data.shares
    if update_data.buying_date is not None:
        portfolio_entry.buying_date = update_data.buying_date
    if update_data.buying_price is not None:
        portfolio_entry.buying_price = update_data.buying_price
    
    db.commit()
    db.refresh(portfolio_entry)
    
    return portfolio_entry
