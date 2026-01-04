"""
Stock Data Service - Fetches real-time data from Yahoo Finance
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor
from cachetools import TTLCache
import logging

from models.stock import StockPrice, OHLCV, StockHistory, MarketIndex, StockQuote
from config import settings, STOCK_SYMBOLS, SECTOR_MAP

logger = logging.getLogger(__name__)

# Thread pool for running yfinance in async context
executor = ThreadPoolExecutor(max_workers=10)

# Cache for stock data (TTL = 5 seconds for real-time feel)
price_cache = TTLCache(maxsize=200, ttl=5)
history_cache = TTLCache(maxsize=100, ttl=60)


class StockService:
    """Service for fetching stock data from Yahoo Finance"""
    
    def __init__(self):
        self.symbols = list(STOCK_SYMBOLS.keys())
        self.yf_symbols = list(STOCK_SYMBOLS.values())
    
    def _get_yf_symbol(self, symbol: str) -> str:
        """Convert display symbol to Yahoo Finance symbol"""
        return STOCK_SYMBOLS.get(symbol, f"{symbol}.NS")
    
    def _get_display_symbol(self, yf_symbol: str) -> str:
        """Convert Yahoo Finance symbol to display symbol"""
        for display, yf in STOCK_SYMBOLS.items():
            if yf == yf_symbol:
                return display
        return yf_symbol.replace(".NS", "").replace("^", "")
    
    def _fetch_stock_data_sync(self, symbols: List[str]) -> Dict[str, Any]:
        """Synchronously fetch stock data (runs in thread pool)"""
        try:
            # Convert to yfinance symbols
            yf_symbols = [self._get_yf_symbol(s) for s in symbols]
            
            # Fetch data for all symbols at once
            tickers = yf.Tickers(" ".join(yf_symbols))
            
            result = {}
            for symbol, yf_symbol in zip(symbols, yf_symbols):
                try:
                    ticker = tickers.tickers.get(yf_symbol)
                    if ticker:
                        info = ticker.info
                        fast_info = ticker.fast_info
                        
                        price = fast_info.get('lastPrice', info.get('regularMarketPrice', 0))
                        prev_close = fast_info.get('previousClose', info.get('previousClose', price))
                        change = price - prev_close if prev_close else 0
                        change_pct = (change / prev_close * 100) if prev_close else 0
                        
                        result[symbol] = {
                            'symbol': symbol,
                            'name': info.get('shortName', symbol),
                            'price': round(price, 2),
                            'change': round(change, 2),
                            'change_percent': round(change_pct, 2),
                            'open': round(fast_info.get('open', info.get('regularMarketOpen', 0)), 2),
                            'high': round(fast_info.get('dayHigh', info.get('regularMarketDayHigh', 0)), 2),
                            'low': round(fast_info.get('dayLow', info.get('regularMarketDayLow', 0)), 2),
                            'close': round(price, 2),
                            'prev_close': round(prev_close, 2),
                            'volume': int(fast_info.get('lastVolume', info.get('regularMarketVolume', 0))),
                            'sector': SECTOR_MAP.get(symbol, 'OTHER'),
                            'timestamp': datetime.now(),
                        }
                except Exception as e:
                    logger.warning(f"Error fetching {symbol}: {e}")
                    continue
            
            return result
        except Exception as e:
            logger.error(f"Error fetching stock data: {e}")
            return {}
    
    async def get_stock_prices(self, symbols: Optional[List[str]] = None) -> List[StockPrice]:
        """Get current prices for multiple stocks"""
        if symbols is None:
            symbols = self.symbols[:40]  # Default to first 40 stocks
        
        # Check cache first
        cache_key = ",".join(sorted(symbols))
        if cache_key in price_cache:
            return price_cache[cache_key]
        
        # Fetch data in thread pool
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(executor, self._fetch_stock_data_sync, symbols)
        
        # Convert to StockPrice models
        prices = [StockPrice(**v) for v in data.values()]
        
        # Cache the result
        price_cache[cache_key] = prices
        
        return prices
    
    async def get_stock_price(self, symbol: str) -> Optional[StockPrice]:
        """Get current price for a single stock"""
        prices = await self.get_stock_prices([symbol])
        return prices[0] if prices else None
    
    def _fetch_history_sync(self, symbol: str, interval: str, period: str) -> List[Dict]:
        """Synchronously fetch historical data"""
        try:
            yf_symbol = self._get_yf_symbol(symbol)
            ticker = yf.Ticker(yf_symbol)
            
            # Map interval to yfinance format
            interval_map = {
                '1m': '1m', '5m': '5m', '15m': '15m', '30m': '30m',
                '1h': '1h', '4h': '1h', '1d': '1d', '1D': '1d',
                '1wk': '1wk', '1W': '1wk', '1mo': '1mo'
            }
            yf_interval = interval_map.get(interval, '1d')
            
            # Determine period based on interval
            period_map = {
                '1m': '1d', '5m': '5d', '15m': '1mo', '30m': '1mo',
                '1h': '3mo', '4h': '3mo', '1d': '1y', '1D': '1y',
                '1wk': '2y', '1W': '2y', '1mo': '5y'
            }
            yf_period = period or period_map.get(interval, '1mo')
            
            df = ticker.history(period=yf_period, interval=yf_interval)
            
            if df.empty:
                return []
            
            data = []
            for idx, row in df.iterrows():
                data.append({
                    'timestamp': idx.to_pydatetime(),
                    'open': round(row['Open'], 2),
                    'high': round(row['High'], 2),
                    'low': round(row['Low'], 2),
                    'close': round(row['Close'], 2),
                    'volume': int(row['Volume']),
                })
            
            return data
        except Exception as e:
            logger.error(f"Error fetching history for {symbol}: {e}")
            return []
    
    async def get_stock_history(
        self, 
        symbol: str, 
        interval: str = "1d",
        period: str = None
    ) -> StockHistory:
        """Get historical OHLCV data for a stock"""
        cache_key = f"{symbol}_{interval}_{period}"
        if cache_key in history_cache:
            return history_cache[cache_key]
        
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(
            executor, 
            self._fetch_history_sync, 
            symbol, 
            interval, 
            period
        )
        
        ohlcv_data = [OHLCV(**d) for d in data]
        history = StockHistory(symbol=symbol, interval=interval, data=ohlcv_data)
        
        history_cache[cache_key] = history
        return history
    
    async def get_market_indices(self) -> List[MarketIndex]:
        """Get market indices (NIFTY, BANKNIFTY, etc.)"""
        indices_data = []
        
        index_symbols = {
            "^NSEI": "NIFTY 50",
            "^NSEBANK": "NIFTY BANK",
            "^CNXIT": "NIFTY IT",
        }
        
        loop = asyncio.get_event_loop()
        
        def fetch_indices():
            result = []
            for yf_symbol, name in index_symbols.items():
                try:
                    ticker = yf.Ticker(yf_symbol)
                    info = ticker.fast_info
                    
                    price = info.get('lastPrice', 0)
                    prev_close = info.get('previousClose', price)
                    change = price - prev_close
                    change_pct = (change / prev_close * 100) if prev_close else 0
                    
                    result.append({
                        'symbol': yf_symbol.replace("^", ""),
                        'name': name,
                        'value': round(price, 2),
                        'change': round(change, 2),
                        'change_percent': round(change_pct, 2),
                        'timestamp': datetime.now(),
                    })
                except Exception as e:
                    logger.warning(f"Error fetching index {yf_symbol}: {e}")
            return result
        
        data = await loop.run_in_executor(executor, fetch_indices)
        return [MarketIndex(**d) for d in data]
    
    async def get_stock_quote(self, symbol: str) -> Optional[StockQuote]:
        """Get detailed quote for a stock"""
        try:
            yf_symbol = self._get_yf_symbol(symbol)
            
            def fetch_quote():
                ticker = yf.Ticker(yf_symbol)
                info = ticker.info
                fast_info = ticker.fast_info
                
                price = fast_info.get('lastPrice', info.get('regularMarketPrice', 0))
                prev_close = fast_info.get('previousClose', info.get('previousClose', price))
                change = price - prev_close
                change_pct = (change / prev_close * 100) if prev_close else 0
                
                return {
                    'symbol': symbol,
                    'name': info.get('shortName', symbol),
                    'price': round(price, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_pct, 2),
                    'open': round(fast_info.get('open', 0), 2),
                    'high': round(fast_info.get('dayHigh', 0), 2),
                    'low': round(fast_info.get('dayLow', 0), 2),
                    'close': round(price, 2),
                    'prev_close': round(prev_close, 2),
                    'volume': int(fast_info.get('lastVolume', 0)),
                    'avg_volume': info.get('averageVolume'),
                    'market_cap': info.get('marketCap'),
                    'pe_ratio': info.get('trailingPE'),
                    'week_52_high': info.get('fiftyTwoWeekHigh'),
                    'week_52_low': info.get('fiftyTwoWeekLow'),
                    'sector': SECTOR_MAP.get(symbol, info.get('sector')),
                    'industry': info.get('industry'),
                }
            
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(executor, fetch_quote)
            return StockQuote(**data)
        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {e}")
            return None


# Singleton instance
stock_service = StockService()
