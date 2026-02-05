"""
Stock API endpoints.
Provides real-time stock quotes and market data.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import csv
import os
from ..services.stock_service import stock_service
from ..core.security import get_current_user
from ..models.user import User
from ..schemas.portfolio import NSEStock

router = APIRouter(prefix="/stocks", tags=["Stocks"])


@router.get("/quote/{symbol}")
async def get_stock_quote(
    symbol: str,
    sparkline: bool = False,
    current_user: User = Depends(get_current_user)
):
    """
    Get current quote for a stock symbol.
    
    **Requires authentication.**
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, GOOGL)
        sparkline: Whether to include 1mo price history
        
    Returns:
        Stock quote with price, change, volume, etc.
    """
    quote = stock_service.get_stock_quote(symbol, include_sparkline=sparkline)
    
    if not quote:
        raise HTTPException(
            status_code=404,
            detail=f"Stock symbol '{symbol}' not found or data unavailable"
        )
    
    return quote


@router.get("/popular")
async def get_popular_stocks(
    current_user: User = Depends(get_current_user)
):
    """
    Get quotes for popular stocks (AAPL, GOOGL, MSFT, TSLA, AMZN).
    
    **Requires authentication.**
    
    Returns:
        List of stock quotes
    """
    stocks = stock_service.get_popular_stocks()
    
    return {
        "stocks": stocks,
        "count": len(stocks)
    }


@router.get("/search")
async def search_stocks(
    q: str,
    current_user: User = Depends(get_current_user)
):
    """
    Search for stocks by symbol or name.
    
    **Requires authentication.**
    
    Args:
        q: Search query (symbol or company name)
        
    Returns:
        List of matching stocks
    """
    if not q or len(q) < 1:
        raise HTTPException(
            status_code=400,
            detail="Search query must be at least 1 character"
        )
    
    results = stock_service.search_stocks(q)
    
    return {
        "results": results,
        "count": len(results),
        "query": q
    }


@router.get("/nse-symbols", response_model=List[NSEStock])
async def get_nse_symbols(
    q: str = None,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """
    Get NSE India stock symbols from CSV file.
    
    **Requires authentication.**
    
    Args:
        q: Optional search query to filter symbols
        limit: Maximum number of results (default: 100)
        
    Returns:
        List of NSE stock symbols with company names
    """
    # Path to CSV file
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "Ticker_List_NSE_India.csv")
    
    if not os.path.exists(csv_path):
        raise HTTPException(
            status_code=500,
            detail="NSE stock symbols file not found"
        )
    
    stocks = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                symbol = row.get('SYMBOL', '').strip()
                name = row.get('NAME OF COMPANY', '').strip()
                series = row.get(' SERIES', '').strip()
                
                if not symbol:
                    continue
                
                # Filter by search query if provided
                if q:
                    q_lower = q.lower()
                    if q_lower not in symbol.lower() and q_lower not in name.lower():
                        continue
                
                stocks.append(NSEStock(
                    symbol=symbol,
                    name=name,
                    series=series if series else None
                ))
                
                # Limit results
                if len(stocks) >= limit:
                    break
        
        return stocks
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading NSE symbols: {str(e)}"
        )
