"""
Technical Indicators Service
Calculates various technical indicators for stocks
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import ta
from ta.trend import ADXIndicator, EMAIndicator, SMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import AverageTrueRange, BollingerBands

from models.stock import TechnicalIndicators
from services.stock_service import stock_service

logger = logging.getLogger(__name__)
executor = ThreadPoolExecutor(max_workers=5)


class TechnicalIndicatorService:
    """Service for calculating technical indicators"""
    
    def _calculate_indicators_sync(self, df: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """Calculate all technical indicators (synchronous)"""
        try:
            if df.empty or len(df) < 20:
                return {'symbol': symbol}
            
            close = df['close']
            high = df['high']
            low = df['low']
            
            result = {'symbol': symbol}
            
            # Simple Moving Averages
            if len(df) >= 20:
                sma_20 = SMAIndicator(close, window=20)
                result['sma_20'] = round(sma_20.sma_indicator().iloc[-1], 2)
            
            if len(df) >= 50:
                sma_50 = SMAIndicator(close, window=50)
                result['sma_50'] = round(sma_50.sma_indicator().iloc[-1], 2)
            
            if len(df) >= 200:
                sma_200 = SMAIndicator(close, window=200)
                result['sma_200'] = round(sma_200.sma_indicator().iloc[-1], 2)
            
            # Exponential Moving Averages
            ema_12 = EMAIndicator(close, window=12)
            ema_26 = EMAIndicator(close, window=26)
            result['ema_12'] = round(ema_12.ema_indicator().iloc[-1], 2)
            result['ema_26'] = round(ema_26.ema_indicator().iloc[-1], 2)
            
            # RSI
            rsi = RSIIndicator(close, window=14)
            result['rsi_14'] = round(rsi.rsi().iloc[-1], 2)
            
            # MACD
            macd = MACD(close, window_slow=26, window_fast=12, window_sign=9)
            result['macd'] = round(macd.macd().iloc[-1], 2)
            result['macd_signal'] = round(macd.macd_signal().iloc[-1], 2)
            result['macd_histogram'] = round(macd.macd_diff().iloc[-1], 2)
            
            # Stochastic
            stoch = StochasticOscillator(high, low, close, window=14, smooth_window=3)
            result['stoch_k'] = round(stoch.stoch().iloc[-1], 2)
            result['stoch_d'] = round(stoch.stoch_signal().iloc[-1], 2)
            
            # ATR
            atr = AverageTrueRange(high, low, close, window=14)
            result['atr_14'] = round(atr.average_true_range().iloc[-1], 2)
            
            # Bollinger Bands
            bb = BollingerBands(close, window=20, window_dev=2)
            result['bb_upper'] = round(bb.bollinger_hband().iloc[-1], 2)
            result['bb_middle'] = round(bb.bollinger_mavg().iloc[-1], 2)
            result['bb_lower'] = round(bb.bollinger_lband().iloc[-1], 2)
            
            # ADX
            adx = ADXIndicator(high, low, close, window=14)
            result['adx_14'] = round(adx.adx().iloc[-1], 2)
            result['plus_di'] = round(adx.adx_pos().iloc[-1], 2)
            result['minus_di'] = round(adx.adx_neg().iloc[-1], 2)
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating indicators for {symbol}: {e}")
            return {'symbol': symbol}
    
    async def get_indicators(self, symbol: str, interval: str = "1d") -> TechnicalIndicators:
        """Get technical indicators for a stock"""
        # Get historical data
        history = await stock_service.get_stock_history(symbol, interval)
        
        if not history.data:
            return TechnicalIndicators(symbol=symbol)
        
        # Convert to DataFrame
        df = pd.DataFrame([{
            'open': d.open,
            'high': d.high,
            'low': d.low,
            'close': d.close,
            'volume': d.volume,
        } for d in history.data])
        
        # Calculate indicators in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            self._calculate_indicators_sync,
            df,
            symbol
        )
        
        return TechnicalIndicators(**result)
    
    async def get_rsi(self, symbol: str, period: int = 14, interval: str = "1d") -> Optional[float]:
        """Get RSI for a stock"""
        indicators = await self.get_indicators(symbol, interval)
        return indicators.rsi_14
    
    async def get_macd(self, symbol: str, interval: str = "1d") -> Dict[str, float]:
        """Get MACD values for a stock"""
        indicators = await self.get_indicators(symbol, interval)
        return {
            'macd': indicators.macd,
            'signal': indicators.macd_signal,
            'histogram': indicators.macd_histogram,
        }
    
    async def get_adx(self, symbol: str, interval: str = "1d") -> Dict[str, float]:
        """Get ADX values for a stock"""
        indicators = await self.get_indicators(symbol, interval)
        return {
            'adx': indicators.adx_14,
            'plus_di': indicators.plus_di,
            'minus_di': indicators.minus_di,
        }
    
    async def get_bollinger_bands(self, symbol: str, interval: str = "1d") -> Dict[str, float]:
        """Get Bollinger Bands for a stock"""
        indicators = await self.get_indicators(symbol, interval)
        return {
            'upper': indicators.bb_upper,
            'middle': indicators.bb_middle,
            'lower': indicators.bb_lower,
        }
    
    async def get_bulk_indicators(
        self, 
        symbols: list, 
        interval: str = "1d"
    ) -> list[TechnicalIndicators]:
        """Get indicators for multiple stocks"""
        tasks = [self.get_indicators(symbol, interval) for symbol in symbols]
        return await asyncio.gather(*tasks)


# Singleton instance
indicator_service = TechnicalIndicatorService()
