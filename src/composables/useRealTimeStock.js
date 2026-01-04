/**
 * Real-time Stock Data Composable
 * Connects to Python WebSocket backend for live stock updates
 */
import { ref, onMounted, onUnmounted, computed } from 'vue'

// WebSocket server URL - change in production
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/stocks'
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export function useRealTimeStock() {
  // State
  const stocks = ref([])
  const indices = ref([])
  const isConnected = ref(false)
  const isLoading = ref(true)
  const error = ref(null)
  const lastUpdate = ref(null)
  
  // WebSocket instance
  let ws = null
  let reconnectTimeout = null
  let reconnectAttempts = 0
  const MAX_RECONNECT_ATTEMPTS = 5
  const RECONNECT_DELAY = 3000
  
  // Connect to WebSocket
  const connect = () => {
    try {
      ws = new WebSocket(WS_URL)
      
      ws.onopen = () => {
        console.log('WebSocket connected')
        isConnected.value = true
        error.value = null
        reconnectAttempts = 0
      }
      
      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          handleMessage(message)
        } catch (e) {
          console.error('Error parsing WebSocket message:', e)
        }
      }
      
      ws.onerror = (e) => {
        console.error('WebSocket error:', e)
        error.value = 'Connection error'
      }
      
      ws.onclose = () => {
        console.log('WebSocket disconnected')
        isConnected.value = false
        attemptReconnect()
      }
    } catch (e) {
      console.error('Failed to connect:', e)
      error.value = 'Failed to connect'
      attemptReconnect()
    }
  }
  
  // Handle incoming messages
  const handleMessage = (message) => {
    switch (message.type) {
      case 'initial_data':
      case 'price_update':
        if (message.data.stocks) {
          stocks.value = message.data.stocks
        }
        if (message.data.indices) {
          indices.value = message.data.indices
        }
        lastUpdate.value = new Date(message.timestamp)
        isLoading.value = false
        break
        
      case 'heartbeat':
        // Send pong response
        if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'pong' }))
        }
        break
        
      case 'subscribed':
        console.log(`Subscribed to ${message.symbol}`)
        break
    }
  }
  
  // Attempt to reconnect
  const attemptReconnect = () => {
    if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
      error.value = 'Max reconnection attempts reached'
      return
    }
    
    reconnectAttempts++
    console.log(`Attempting to reconnect (${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})...`)
    
    reconnectTimeout = setTimeout(() => {
      connect()
    }, RECONNECT_DELAY)
  }
  
  // Disconnect
  const disconnect = () => {
    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout)
    }
    if (ws) {
      ws.close()
      ws = null
    }
  }
  
  // Subscribe to a specific symbol
  const subscribeToSymbol = (symbol) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'subscribe',
        symbol: symbol.toUpperCase(),
      }))
    }
  }
  
  // Unsubscribe from a symbol
  const unsubscribeFromSymbol = (symbol) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'unsubscribe',
        symbol: symbol.toUpperCase(),
      }))
    }
  }
  
  // Get stock by symbol
  const getStock = (symbol) => {
    return computed(() => 
      stocks.value.find(s => s.symbol === symbol.toUpperCase())
    )
  }
  
  // Filter stocks by sector
  const getStocksBySector = (sector) => {
    return computed(() => 
      stocks.value.filter(s => s.sector === sector.toUpperCase())
    )
  }
  
  // Lifecycle hooks
  onMounted(() => {
    connect()
  })
  
  onUnmounted(() => {
    disconnect()
  })
  
  return {
    // State
    stocks,
    indices,
    isConnected,
    isLoading,
    error,
    lastUpdate,
    
    // Methods
    connect,
    disconnect,
    subscribeToSymbol,
    unsubscribeFromSymbol,
    getStock,
    getStocksBySector,
  }
}

/**
 * Composable for single stock real-time updates
 */
export function useRealTimeSingleStock(symbol) {
  const stock = ref(null)
  const isConnected = ref(false)
  const isLoading = ref(true)
  const error = ref(null)
  
  let ws = null
  
  const connect = () => {
    const url = `ws://localhost:8000/ws/stock/${symbol.toUpperCase()}`
    
    try {
      ws = new WebSocket(url)
      
      ws.onopen = () => {
        isConnected.value = true
        error.value = null
      }
      
      ws.onmessage = (event) => {
        const message = JSON.parse(event.data)
        if (message.type === 'initial_data' || message.type === 'price_update') {
          stock.value = message.data
          isLoading.value = false
        }
      }
      
      ws.onerror = () => {
        error.value = 'Connection error'
      }
      
      ws.onclose = () => {
        isConnected.value = false
      }
    } catch (e) {
      error.value = 'Failed to connect'
    }
  }
  
  const disconnect = () => {
    if (ws) {
      ws.close()
      ws = null
    }
  }
  
  onMounted(() => connect())
  onUnmounted(() => disconnect())
  
  return {
    stock,
    isConnected,
    isLoading,
    error,
  }
}

/**
 * REST API functions for stock data
 */
export const stockApi = {
  // Get all stocks
  async getStocks(symbols = null, sector = null) {
    const params = new URLSearchParams()
    if (symbols) params.append('symbols', symbols.join(','))
    if (sector) params.append('sector', sector)
    
    const response = await fetch(`${API_URL}/stocks?${params}`)
    return response.json()
  },
  
  // Get single stock
  async getStock(symbol) {
    const response = await fetch(`${API_URL}/stock/${symbol}`)
    return response.json()
  },
  
  // Get stock history
  async getHistory(symbol, interval = '1d', period = null) {
    const params = new URLSearchParams({ interval })
    if (period) params.append('period', period)
    
    const response = await fetch(`${API_URL}/stock/${symbol}/history?${params}`)
    return response.json()
  },
  
  // Get market indices
  async getIndices() {
    const response = await fetch(`${API_URL}/indices`)
    return response.json()
  },
  
  // Get technical indicators
  async getIndicators(symbol, interval = '1d') {
    const response = await fetch(`${API_URL}/indicators/${symbol}?interval=${interval}`)
    return response.json()
  },
  
  // Get RSI
  async getRSI(symbol, interval = '1d') {
    const response = await fetch(`${API_URL}/indicators/${symbol}/rsi?interval=${interval}`)
    return response.json()
  },
  
  // Get MACD
  async getMACD(symbol, interval = '1d') {
    const response = await fetch(`${API_URL}/indicators/${symbol}/macd?interval=${interval}`)
    return response.json()
  },
  
  // Get ADX
  async getADX(symbol, interval = '1d') {
    const response = await fetch(`${API_URL}/indicators/${symbol}/adx?interval=${interval}`)
    return response.json()
  },
  
  // Get available sectors
  async getSectors() {
    const response = await fetch(`${API_URL}/sectors`)
    return response.json()
  },
  
  // Get available symbols
  async getSymbols() {
    const response = await fetch(`${API_URL}/symbols`)
    return response.json()
  },
}
