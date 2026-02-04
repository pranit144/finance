"""
Stock data service using Yahoo Finance.
Fetches real-time stock quotes and company information.
"""
import yfinance as yf
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)


class StockService:
    """Service for fetching stock data from Yahoo Finance."""
    
    # Popular stocks to display by default
    POPULAR_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    
    # Simple cache
    _cache = {}
    _cache_duration = timedelta(minutes=1)  # Cache for 1 minute
    
    @staticmethod
    def get_stock_quote(symbol: str) -> Optional[Dict]:
        """
        Get current stock quote for a symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Dictionary with stock data or None if error
        """
        # Check cache first
        cache_key = f"quote_{symbol}"
        if cache_key in StockService._cache:
            cached_data, cached_time = StockService._cache[cache_key]
            if datetime.now() - cached_time < StockService._cache_duration:
                logger.info(f"Using cached data for {symbol}")
                return cached_data
        
        try:
            logger.info(f"Fetching fresh data for {symbol}")
            stock = yf.Ticker(symbol)
            
            # Use fast_info for quicker response
            try:
                fast_info = stock.fast_info
                current_price = fast_info.get('lastPrice') or fast_info.get('regularMarketPrice')
                previous_close = fast_info.get('previousClose')
            except:
                # Fallback to regular info if fast_info fails
                info = stock.info
                current_price = info.get('currentPrice') or info.get('regularMarketPrice')
                previous_close = info.get('previousClose')
            
            if not current_price or not previous_close:
                logger.warning(f"Missing price data for {symbol}")
                return None
            
            # Calculate change
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100
            
            # Get company name (use fast method)
            try:
                name = stock.info.get('longName') or stock.info.get('shortName') or symbol
            except:
                name = symbol
            
            result = {
                "symbol": symbol.upper(),
                "name": name,
                "price": round(float(current_price), 2),
                "change": round(float(change), 2),
                "change_percent": round(float(change_percent), 2),
                "volume": int(fast_info.get('volume', 0)) if 'fast_info' in locals() else 0,
                "market_cap": None,
                "pe_ratio": None,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Cache the result
            StockService._cache[cache_key] = (result, datetime.now())
            
            return result
            
        except Exception as e:
            logger.error(f"Error fetching stock data for {symbol}: {e}")
            return None
    
    @staticmethod
    def get_popular_stocks() -> List[Dict]:
        """
        Get quotes for popular stocks (fetched in parallel for speed).
        
        Returns:
            List of stock quote dictionaries
        """
        logger.info("Fetching popular stocks in parallel...")
        stocks = []
        
        # Use ThreadPoolExecutor to fetch stocks in parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all tasks
            future_to_symbol = {
                executor.submit(StockService.get_stock_quote, symbol): symbol 
                for symbol in StockService.POPULAR_SYMBOLS
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    quote = future.result(timeout=10)  # 10 second timeout per stock
                    if quote:
                        stocks.append(quote)
                        logger.info(f"✅ Got quote for {symbol}")
                except Exception as e:
                    logger.error(f"❌ Failed to get quote for {symbol}: {e}")
        
        logger.info(f"Fetched {len(stocks)} stocks successfully")
        return stocks
    
    @staticmethod
    def search_stocks(query: str, limit: int = 10) -> List[Dict]:
        """
        Search for stocks by symbol or name.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching stocks
        """
        # For now, just try to get the quote for the query as a symbol
        # In production, you'd use a proper search API
        query = query.upper().strip()
        quote = StockService.get_stock_quote(query)
        
        if quote:
            return [quote]
        return []


# Create singleton instance
stock_service = StockService()

