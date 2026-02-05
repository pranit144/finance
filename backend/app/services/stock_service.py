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
    
    # Popular stocks to display by default (Limited to 4 as requested)
    POPULAR_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA"]
    
    # Simple cache
    _cache = {}
    _cache_duration = timedelta(seconds=30)  # Cache for 30 seconds
    
    @staticmethod
    def get_stock_quote(symbol: str, include_sparkline: bool = False) -> Optional[Dict]:
        """
        Get current stock quote for a symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            include_sparkline: Whether to include last 1 month price history
            
        Returns:
            Dictionary with stock data or None if error
        """
        # Check cache first
        cache_key = f"quote_{symbol}_{include_sparkline}"
        if cache_key in StockService._cache:
            cached_data, cached_time = StockService._cache[cache_key]
            if datetime.now() - cached_time < StockService._cache_duration:
                logger.info(f"Using cached data for {symbol}")
                return cached_data
        
        try:
            logger.info(f"Fetching fresh data for {symbol}")
            stock = yf.Ticker(symbol)
            
            current_price = None
            previous_close = None
            volume = 0
            market_cap = 0
            
            # Use fast_info for quicker response
            try:
                fast_info = stock.fast_info
                current_price = fast_info.get('lastPrice') or fast_info.get('regularMarketPrice')
                previous_close = fast_info.get('previousClose')
                volume = fast_info.get('lastVolume') or fast_info.get('volume') or 0
                market_cap = fast_info.get('marketCap') or 0
            except:
                pass
                
            # Fallback to regular info if fast_info failed or missing data
            if not current_price:
                try:
                    info = stock.info
                    current_price = info.get('currentPrice') or info.get('regularMarketPrice')
                    previous_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
                    volume = info.get('volume') or info.get('regularMarketVolume') or 0
                    market_cap = info.get('marketCap') or 0
                except:
                    pass
            
            if not current_price:
                logger.warning(f"Missing price data for {symbol}")
                return None
                
            # Use previous close as current if missing (fallback)
            if not previous_close:
                previous_close = current_price
            
            # Calculate change
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close else 0
            
            # Get company name
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
                "volume": int(volume),
                "market_cap": int(market_cap),
                "pe_ratio": stock.info.get('trailingPE'),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            if include_sparkline:
                try:
                    # Fetch 1 month history for sparkline
                    hist = stock.history(period="1mo")
                    if not hist.empty:
                        # Normalize data for sparkline (list of floats)
                        result['sparkline'] = [round(float(p), 2) for p in hist['Close'].tolist()]
                except Exception as e:
                    logger.error(f"Error fetching sparkline for {symbol}: {e}")
                    result['sparkline'] = []
            
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

    @staticmethod
    def get_historical_price(symbol: str, date_obj: datetime) -> Optional[float]:
        """
        Get historical low price for a stock on a specific date.
        If date is non-trading (weekend/holiday), finds next trading day.
        
        Args:
            symbol: Stock ticker symbol
            date_obj: Date to fetch price for
            
        Returns:
            Low price on that date or None
        """
        def fetch_history(ticker_symbol):
            try:
                stock = yf.Ticker(ticker_symbol)
                # Search up to 7 days ahead to handle weekends/holidays
                start_date = date_obj.strftime("%Y-%m-%d")
                end_date_obj = date_obj + timedelta(days=7)
                end_date = end_date_obj.strftime("%Y-%m-%d")
                
                # Fetch history
                return stock.history(start=start_date, end=end_date)
            except:
                return None

        try:
            # 1. Try exact symbol
            history = fetch_history(symbol)
            
            # 2. If empty, try with .NS suffix (common for NSE India)
            if (history is None or history.empty) and not symbol.endswith('.NS'):
                history = fetch_history(f"{symbol}.NS")
            
            if history is not None and not history.empty:
                # Return the Low price of the *first available* trading day
                # ensuring we get the price closest to the requested date
                return float(history['Low'].iloc[0])
            
            logger.warning(f"No history found for {symbol} starting {date_obj}")
            return None
        except Exception as e:
            logger.error(f"Error fetching historical price for {symbol}: {e}")
            return None


# Create singleton instance
stock_service = StockService()
