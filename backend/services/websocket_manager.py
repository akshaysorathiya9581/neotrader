"""
WebSocket Connection Manager
Manages real-time connections to clients
"""
from fastapi import WebSocket
from typing import List, Dict, Set
import asyncio
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        # All active connections
        self.active_connections: List[WebSocket] = []
        
        # Connections subscribed to specific symbols
        self.symbol_subscriptions: Dict[str, Set[WebSocket]] = {}
        
        # Connection metadata
        self.connection_info: Dict[WebSocket, Dict] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_info[websocket] = {
            'client_id': client_id,
            'connected_at': datetime.now(),
            'subscriptions': set(),
        }
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        # Remove from symbol subscriptions
        if websocket in self.connection_info:
            for symbol in self.connection_info[websocket].get('subscriptions', set()):
                if symbol in self.symbol_subscriptions:
                    self.symbol_subscriptions[symbol].discard(websocket)
            del self.connection_info[websocket]
        
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def subscribe_to_symbol(self, websocket: WebSocket, symbol: str):
        """Subscribe a connection to a specific symbol"""
        if symbol not in self.symbol_subscriptions:
            self.symbol_subscriptions[symbol] = set()
        
        self.symbol_subscriptions[symbol].add(websocket)
        
        if websocket in self.connection_info:
            self.connection_info[websocket]['subscriptions'].add(symbol)
        
        logger.debug(f"Client subscribed to {symbol}")
    
    async def unsubscribe_from_symbol(self, websocket: WebSocket, symbol: str):
        """Unsubscribe a connection from a symbol"""
        if symbol in self.symbol_subscriptions:
            self.symbol_subscriptions[symbol].discard(websocket)
        
        if websocket in self.connection_info:
            self.connection_info[websocket]['subscriptions'].discard(symbol)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific client"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients"""
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
    
    async def broadcast_to_symbol(self, symbol: str, message: dict):
        """Broadcast a message to all clients subscribed to a symbol"""
        if symbol not in self.symbol_subscriptions:
            return
        
        disconnected = []
        
        for connection in self.symbol_subscriptions[symbol]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
    
    async def send_heartbeat(self):
        """Send heartbeat to all connections"""
        heartbeat = {
            'type': 'heartbeat',
            'timestamp': datetime.now().isoformat(),
        }
        await self.broadcast(heartbeat)
    
    def get_connection_count(self) -> int:
        """Get the number of active connections"""
        return len(self.active_connections)
    
    def get_symbol_subscriber_count(self, symbol: str) -> int:
        """Get the number of subscribers for a symbol"""
        return len(self.symbol_subscriptions.get(symbol, set()))
    
    def get_stats(self) -> dict:
        """Get WebSocket manager statistics"""
        return {
            'total_connections': len(self.active_connections),
            'subscriptions': {
                symbol: len(subs) 
                for symbol, subs in self.symbol_subscriptions.items()
            },
        }


# Singleton instance
websocket_manager = WebSocketManager()
