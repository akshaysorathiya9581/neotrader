"""
NeoTrader Backend Configuration
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "NeoTrader Backend"
    DEBUG: bool = True
    API_VERSION: str = "v1"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # WebSocket Settings
    WS_UPDATE_INTERVAL: float = 2.0  # seconds
    WS_HEARTBEAT_INTERVAL: float = 30.0  # seconds
    
    # Stock Data Settings
    DEFAULT_STOCKS: List[str] = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
        "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
        "LT.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS", "TITAN.NS",
        "SUNPHARMA.NS", "BAJFINANCE.NS", "WIPRO.NS", "ULTRACEMCO.NS", "NESTLEIND.NS",
        "TATAMOTORS.NS", "TATASTEEL.NS", "POWERGRID.NS", "NTPC.NS", "JSWSTEEL.NS",
        "M&M.NS", "TECHM.NS", "HCLTECH.NS", "ADANIENT.NS", "COALINDIA.NS",
        "ONGC.NS", "BAJAJFINSV.NS", "GRASIM.NS", "CIPLA.NS", "DRREDDY.NS",
        "EICHERMOT.NS", "APOLLOHOSP.NS", "DIVISLAB.NS", "BPCL.NS", "BRITANNIA.NS",
    ]
    
    # Index symbols
    INDICES: List[str] = [
        "^NSEI",      # NIFTY 50
        "^NSEBANK",   # NIFTY BANK
        "^CNXIT",     # NIFTY IT
    ]
    
    # Cache Settings
    CACHE_TTL: int = 60  # seconds
    
    # Data Source Priority
    DATA_SOURCE: str = "yfinance"  # Options: yfinance, nse
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Stock symbol mapping (Display Name -> Yahoo Finance Symbol)
STOCK_SYMBOLS = {
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "INFY": "INFY.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "HINDUNILVR": "HINDUNILVR.NS",
    "ITC": "ITC.NS",
    "SBIN": "SBIN.NS",
    "BHARTIARTL": "BHARTIARTL.NS",
    "KOTAKBANK": "KOTAKBANK.NS",
    "LT": "LT.NS",
    "AXISBANK": "AXISBANK.NS",
    "ASIANPAINT": "ASIANPAINT.NS",
    "MARUTI": "MARUTI.NS",
    "TITAN": "TITAN.NS",
    "SUNPHARMA": "SUNPHARMA.NS",
    "BAJFINANCE": "BAJFINANCE.NS",
    "WIPRO": "WIPRO.NS",
    "ULTRACEMCO": "ULTRACEMCO.NS",
    "NESTLEIND": "NESTLEIND.NS",
    "TATAMOTORS": "TATAMOTORS.NS",
    "TATASTEEL": "TATASTEEL.NS",
    "POWERGRID": "POWERGRID.NS",
    "NTPC": "NTPC.NS",
    "JSWSTEEL": "JSWSTEEL.NS",
    "M&M": "M%26M.NS",
    "TECHM": "TECHM.NS",
    "HCLTECH": "HCLTECH.NS",
    "ADANIENT": "ADANIENT.NS",
    "COALINDIA": "COALINDIA.NS",
    "ONGC": "ONGC.NS",
    "BAJAJFINSV": "BAJAJFINSV.NS",
    "GRASIM": "GRASIM.NS",
    "CIPLA": "CIPLA.NS",
    "DRREDDY": "DRREDDY.NS",
    "EICHERMOT": "EICHERMOT.NS",
    "APOLLOHOSP": "APOLLOHOSP.NS",
    "DIVISLAB": "DIVISLAB.NS",
    "BPCL": "BPCL.NS",
    "BRITANNIA": "BRITANNIA.NS",
    "BEL": "BEL.NS",
    "HINDALCO": "HINDALCO.NS",
    "INDUSINDBK": "INDUSINDBK.NS",
    "HDFCLIFE": "HDFCLIFE.NS",
    "SBILIFE": "SBILIFE.NS",
    "NIFTY": "^NSEI",
    "NIFTYBANK": "^NSEBANK",
    "NIFTYIT": "^CNXIT",
}

# Sector mapping
SECTOR_MAP = {
    "RELIANCE": "ENERGY",
    "TCS": "IT",
    "HDFCBANK": "BANK",
    "INFY": "IT",
    "ICICIBANK": "BANK",
    "HINDUNILVR": "FMCG",
    "ITC": "FMCG",
    "SBIN": "BANK",
    "BHARTIARTL": "TELECOM",
    "KOTAKBANK": "BANK",
    "LT": "INDUSTRIAL MANUFACTURING",
    "AXISBANK": "BANK",
    "ASIANPAINT": "CONSUMER GOODS",
    "MARUTI": "AUTO",
    "TITAN": "CONSUMER GOODS",
    "SUNPHARMA": "PHARMA",
    "BAJFINANCE": "FINANCIAL SERVICES",
    "WIPRO": "IT",
    "ULTRACEMCO": "CEMENT",
    "NESTLEIND": "FMCG",
    "TATAMOTORS": "AUTO",
    "TATASTEEL": "METALS",
    "POWERGRID": "ENERGY",
    "NTPC": "ENERGY",
    "JSWSTEEL": "METALS",
    "M&M": "AUTO",
    "TECHM": "IT",
    "HCLTECH": "IT",
    "ADANIENT": "INFRASTRUCTURE",
    "COALINDIA": "METALS",
    "ONGC": "ENERGY",
    "BAJAJFINSV": "FINANCIAL SERVICES",
    "GRASIM": "CEMENT",
    "CIPLA": "PHARMA",
    "DRREDDY": "PHARMA",
    "EICHERMOT": "AUTO",
    "APOLLOHOSP": "HEALTHCARE",
    "DIVISLAB": "PHARMA",
    "BPCL": "ENERGY",
    "BRITANNIA": "FMCG",
    "BEL": "INDUSTRIAL MANUFACTURING",
    "HINDALCO": "METALS",
    "INDUSINDBK": "BANK",
    "HDFCLIFE": "FINANCIAL SERVICES",
}
