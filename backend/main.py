"""
NeoTrader Backend - FastAPI Server
Real-time stock data with WebSocket support
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
import logging
from datetime import datetime
from typing import List, Optional

from config import settings
from models import StockPrice, StockHistory, TechnicalIndicators, MarketIndex, PriceUpdate
from services.stock_service import stock_service
from services.websocket_manager import websocket_manager
from services.technical_indicators import indicator_service

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Background task for broadcasting prices
async def broadcast_prices():
    """Background task to broadcast real-time prices"""
    while True:
        try:
            if websocket_manager.get_connection_count() > 0:
                # Fetch latest prices
                prices = await stock_service.get_stock_prices()
                indices = await stock_service.get_market_indices()
                
                # Create update message
                update = {
                    'type': 'price_update',
                    'data': {
                        'stocks': [p.model_dump() for p in prices],
                        'indices': [i.model_dump() for i in indices],
                    },
                    'timestamp': datetime.now().isoformat(),
                }
                
                # Broadcast to all clients
                await websocket_manager.broadcast(update)
                logger.debug(f"Broadcasted prices to {websocket_manager.get_connection_count()} clients")
            
            await asyncio.sleep(settings.WS_UPDATE_INTERVAL)
        except Exception as e:
            logger.error(f"Error in broadcast task: {e}")
            await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting NeoTrader Backend...")
    
    # Start background broadcast task
    broadcast_task = asyncio.create_task(broadcast_prices())
    logger.info("Started price broadcast task")
    
    yield
    
    # Shutdown
    broadcast_task.cancel()
    logger.info("NeoTrader Backend stopped")


# Create FastAPI app
app = FastAPI(
    title="NeoTrader API",
    description="Real-time stock data API with WebSocket support",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# REST API Endpoints
# ============================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "NeoTrader API",
        "version": "1.0.0",
        "status": "running",
        "websocket": "/ws/stocks",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "connections": websocket_manager.get_connection_count(),
    }


@app.get("/api/stocks", response_model=List[StockPrice])
async def get_all_stocks(
    symbols: Optional[str] = Query(None, description="Comma-separated stock symbols"),
    sector: Optional[str] = Query(None, description="Filter by sector"),
):
    """Get current prices for all stocks or filtered stocks"""
    try:
        symbol_list = symbols.split(",") if symbols else None
        prices = await stock_service.get_stock_prices(symbol_list)
        
        # Filter by sector if provided
        if sector:
            prices = [p for p in prices if p.sector and p.sector.upper() == sector.upper()]
        
        return prices
    except Exception as e:
        logger.error(f"Error fetching stocks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stock/{symbol}", response_model=StockPrice)
async def get_stock(symbol: str):
    """Get current price for a single stock"""
    try:
        price = await stock_service.get_stock_price(symbol.upper())
        if not price:
            raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
        return price
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching stock {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stock/{symbol}/history", response_model=StockHistory)
async def get_stock_history(
    symbol: str,
    interval: str = Query("1d", description="Time interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk)"),
    period: Optional[str] = Query(None, description="Time period (1d, 5d, 1mo, 3mo, 1y)"),
):
    """Get historical OHLCV data for a stock"""
    try:
        history = await stock_service.get_stock_history(symbol.upper(), interval, period)
        return history
    except Exception as e:
        logger.error(f"Error fetching history for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stock/{symbol}/quote")
async def get_stock_quote(symbol: str):
    """Get detailed quote for a stock"""
    try:
        quote = await stock_service.get_stock_quote(symbol.upper())
        if not quote:
            raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
        return quote
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching quote for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/indices", response_model=List[MarketIndex])
async def get_market_indices():
    """Get market indices (NIFTY 50, NIFTY BANK, etc.)"""
    try:
        indices = await stock_service.get_market_indices()
        return indices
    except Exception as e:
        logger.error(f"Error fetching indices: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/indicators/{symbol}", response_model=TechnicalIndicators)
async def get_technical_indicators(
    symbol: str,
    interval: str = Query("1d", description="Time interval"),
):
    """Get technical indicators for a stock"""
    try:
        indicators = await indicator_service.get_indicators(symbol.upper(), interval)
        return indicators
    except Exception as e:
        logger.error(f"Error fetching indicators for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/indicators/{symbol}/rsi")
async def get_rsi(symbol: str, interval: str = "1d"):
    """Get RSI for a stock"""
    try:
        rsi = await indicator_service.get_rsi(symbol.upper(), interval=interval)
        return {"symbol": symbol, "rsi": rsi}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/indicators/{symbol}/macd")
async def get_macd(symbol: str, interval: str = "1d"):
    """Get MACD for a stock"""
    try:
        macd = await indicator_service.get_macd(symbol.upper(), interval)
        return {"symbol": symbol, **macd}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/indicators/{symbol}/adx")
async def get_adx(symbol: str, interval: str = "1d"):
    """Get ADX for a stock"""
    try:
        adx = await indicator_service.get_adx(symbol.upper(), interval)
        return {"symbol": symbol, **adx}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sectors")
async def get_sectors():
    """Get list of available sectors"""
    from config import SECTOR_MAP
    sectors = list(set(SECTOR_MAP.values()))
    return {"sectors": sorted(sectors)}


@app.get("/api/symbols")
async def get_symbols():
    """Get list of available stock symbols"""
    from config import STOCK_SYMBOLS
    return {"symbols": list(STOCK_SYMBOLS.keys())}


# ============================================
# WebSocket Endpoints
# ============================================

@app.websocket("/ws/stocks")
async def websocket_stocks(websocket: WebSocket):
    """
    WebSocket endpoint for real-time stock updates.
    Broadcasts price updates every 2 seconds to all connected clients.
    """
    await websocket_manager.connect(websocket)
    try:
        # Send initial data
        prices = await stock_service.get_stock_prices()
        indices = await stock_service.get_market_indices()
        
        await websocket.send_json({
            'type': 'initial_data',
            'data': {
                'stocks': [p.model_dump() for p in prices],
                'indices': [i.model_dump() for i in indices],
            },
            'timestamp': datetime.now().isoformat(),
        })
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for messages from client (for subscriptions, etc.)
                data = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=settings.WS_HEARTBEAT_INTERVAL
                )
                
                # Handle client messages
                if data.get('type') == 'subscribe':
                    symbol = data.get('symbol')
                    if symbol:
                        await websocket_manager.subscribe_to_symbol(websocket, symbol)
                        await websocket.send_json({
                            'type': 'subscribed',
                            'symbol': symbol,
                        })
                
                elif data.get('type') == 'unsubscribe':
                    symbol = data.get('symbol')
                    if symbol:
                        await websocket_manager.unsubscribe_from_symbol(websocket, symbol)
                
                elif data.get('type') == 'ping':
                    await websocket.send_json({'type': 'pong'})
                
            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_json({
                    'type': 'heartbeat',
                    'timestamp': datetime.now().isoformat(),
                })
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        websocket_manager.disconnect(websocket)


@app.websocket("/ws/stock/{symbol}")
async def websocket_single_stock(websocket: WebSocket, symbol: str):
    """
    WebSocket endpoint for a single stock's real-time updates.
    """
    await websocket_manager.connect(websocket)
    await websocket_manager.subscribe_to_symbol(websocket, symbol.upper())
    
    try:
        # Send initial data for this stock
        price = await stock_service.get_stock_price(symbol.upper())
        if price:
            await websocket.send_json({
                'type': 'initial_data',
                'data': price.model_dump(),
                'timestamp': datetime.now().isoformat(),
            })
        
        # Keep connection alive
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=settings.WS_HEARTBEAT_INTERVAL
                )
                
                if data.get('type') == 'ping':
                    await websocket.send_json({'type': 'pong'})
                    
            except asyncio.TimeoutError:
                # Fetch and send updated price
                price = await stock_service.get_stock_price(symbol.upper())
                if price:
                    await websocket.send_json({
                        'type': 'price_update',
                        'data': price.model_dump(),
                        'timestamp': datetime.now().isoformat(),
                    })
                    
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error for {symbol}: {e}")
        websocket_manager.disconnect(websocket)


# ============================================
# Run the server
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
