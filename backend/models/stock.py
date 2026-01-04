"""
Stock Data Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TimeInterval(str, Enum):
    ONE_MIN = "1m"
    FIVE_MIN = "5m"
    FIFTEEN_MIN = "15m"
    THIRTY_MIN = "30m"
    ONE_HOUR = "1h"
    FOUR_HOUR = "4h"
    ONE_DAY = "1d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"


class StockPrice(BaseModel):
    """Real-time stock price data"""
    symbol: str
    name: Optional[str] = None
    price: float
    change: float = 0.0
    change_percent: float = 0.0
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    prev_close: float = 0.0
    volume: int = 0
    sector: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class OHLCV(BaseModel):
    """OHLCV candlestick data"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class StockHistory(BaseModel):
    """Historical stock data"""
    symbol: str
    interval: str
    data: List[OHLCV]


class TechnicalIndicators(BaseModel):
    """Technical indicators for a stock"""
    symbol: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Trend Indicators
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    
    # Momentum Indicators
    rsi_14: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    stoch_k: Optional[float] = None
    stoch_d: Optional[float] = None
    
    # Volatility Indicators
    atr_14: Optional[float] = None
    bb_upper: Optional[float] = None
    bb_middle: Optional[float] = None
    bb_lower: Optional[float] = None
    
    # Trend Strength
    adx_14: Optional[float] = None
    plus_di: Optional[float] = None
    minus_di: Optional[float] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MarketIndex(BaseModel):
    """Market index data"""
    symbol: str
    name: str
    value: float
    change: float
    change_percent: float
    timestamp: datetime = Field(default_factory=datetime.now)


class StockQuote(BaseModel):
    """Detailed stock quote"""
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    open: float
    high: float
    low: float
    close: float
    prev_close: float
    volume: int
    avg_volume: Optional[int] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None


class WebSocketMessage(BaseModel):
    """WebSocket message format"""
    type: str  # 'price_update', 'indicator_update', 'index_update'
    data: Any
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PriceUpdate(BaseModel):
    """Price update for WebSocket"""
    stocks: List[StockPrice]
    indices: Optional[List[MarketIndex]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
