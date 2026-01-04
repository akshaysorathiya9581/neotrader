import { defineStore } from 'pinia'

export const useSubscriptionStore = defineStore('subscription', {
  state: () => ({
    // Current user info - This should be loaded from API/database after login
    currentUser: {
      id: null,
      name: '',
      email: '',
      role: 'user', // 'superadmin' or 'user'
      planId: null, // Current subscription plan
      isAuthenticated: false,
    },
    
    // Loading state
    isLoading: false,
    
    // Available subscription plans
    plans: [
      {
        id: 1,
        name: 'Basic',
        price: 999,
        duration: 'month',
        description: 'Essential trading tools for beginners',
        features: ['Dashboard Access', 'Stock Query Window', 'Basic Charts'],
        moduleIds: [1, 2, 3],
        color: 'info',
        popular: false,
      },
      {
        id: 2,
        name: 'Professional',
        price: 2499,
        duration: 'month',
        description: 'Advanced tools for active traders',
        features: ['All Basic Features', 'Technical Indicators', 'Pivot Analysis', 'Candlestick Patterns', 'Real-time Charts'],
        moduleIds: [1, 2, 3, 4, 5, 6, 7],
        color: 'success',
        popular: true,
      },
      {
        id: 3,
        name: 'Enterprise',
        price: 4999,
        duration: 'month',
        description: 'Complete suite for professional traders',
        features: ['All Professional Features', 'Expert Alerts', 'Ichimoku Dashboard', 'Options Trading', 'Priority Support'],
        moduleIds: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        color: 'warning',
        popular: false,
      },
    ],
    
    // Available modules
    modules: [
      { id: 1, name: 'Dashboard', path: '/dashboard', icon: 'tabler-layout-dashboard', category: 'core' },
      { id: 2, name: 'Stock Query', path: '/query-window', icon: 'tabler-search', category: 'core' },
      { id: 3, name: 'Real-time Charts', path: '/my-markets/charts', icon: 'tabler-chart-line', category: 'core' },
      { id: 4, name: 'ADX Trends', path: '/technical/adx-trends', icon: 'tabler-trending-up', category: 'technical' },
      { id: 5, name: 'RSI Trends', path: '/technical/rsi-trends', icon: 'tabler-chart-dots', category: 'technical' },
      { id: 6, name: 'ATR Trends', path: '/technical/atr-trends', icon: 'tabler-activity', category: 'technical' },
      { id: 7, name: 'Key Indicators', path: '/technical/key-indicators', icon: 'tabler-gauge', category: 'technical' },
      { id: 8, name: 'Fibonacci Pivots', path: '/pivots/fibonacci-pivots', icon: 'tabler-spiral', category: 'pivots' },
      { id: 9, name: 'Camarilla Pivots', path: '/pivots/camarilla-pivots', icon: 'tabler-arrows-split', category: 'pivots' },
      { id: 10, name: 'CPR Analysis', path: '/pivots/cpr', icon: 'tabler-chart-bar', category: 'pivots' },
      { id: 11, name: 'Candlestick Patterns', path: '/candlestick', icon: 'tabler-chart-candle', category: 'candlestick' },
      { id: 12, name: 'Heikin Ashi', path: '/candlestick/heikin-ashi', icon: 'tabler-chart-candle-filled', category: 'candlestick' },
      { id: 13, name: 'Expert Alerts', path: '/expert-alerts', icon: 'tabler-bell-ringing', category: 'alerts' },
      { id: 14, name: 'Ichimoku Dashboard', path: '/ichimoku', icon: 'tabler-cloud', category: 'advanced' },
      { id: 15, name: 'Options Trade', path: '/trades/options-trade', icon: 'tabler-replace', category: 'trades' },
      { id: 16, name: 'Intraday Trades', path: '/trades/intraday-trades', icon: 'tabler-clock', category: 'trades' },
    ],
  }),
  
  getters: {
    isSuperAdmin: (state) => state.currentUser.role === 'superadmin',
    
    currentPlan: (state) => state.plans.find(p => p.id === state.currentUser.planId),
    
    accessibleModuleIds: (state) => {
      if (state.currentUser.role === 'superadmin') {
        return state.modules.map(m => m.id)
      }
      const plan = state.plans.find(p => p.id === state.currentUser.planId)
      return plan?.moduleIds || []
    },
    
    accessibleModules: (state) => {
      const accessibleIds = state.currentUser.role === 'superadmin' 
        ? state.modules.map(m => m.id)
        : (state.plans.find(p => p.id === state.currentUser.planId)?.moduleIds || [])
      return state.modules.filter(m => accessibleIds.includes(m.id))
    },
    
    modulesByCategory: (state) => {
      const categories = {}
      state.modules.forEach(m => {
        if (!categories[m.category]) categories[m.category] = []
        categories[m.category].push(m)
      })
      return categories
    },
  },
  
  actions: {
    // SuperAdmin actions
    addPlan(plan) {
      const maxId = Math.max(...this.plans.map(p => p.id), 0)
      this.plans.push({ ...plan, id: maxId + 1 })
    },
    
    updatePlan(planId, updates) {
      const index = this.plans.findIndex(p => p.id === planId)
      if (index !== -1) {
        this.plans[index] = { ...this.plans[index], ...updates }
      }
    },
    
    deletePlan(planId) {
      this.plans = this.plans.filter(p => p.id !== planId)
    },
    
    addModule(module) {
      const maxId = Math.max(...this.modules.map(m => m.id), 0)
      this.modules.push({ ...module, id: maxId + 1 })
    },
    
    updateModule(moduleId, updates) {
      const index = this.modules.findIndex(m => m.id === moduleId)
      if (index !== -1) {
        this.modules[index] = { ...this.modules[index], ...updates }
      }
    },
    
    deleteModule(moduleId) {
      this.modules = this.modules.filter(m => m.id !== moduleId)
      // Also remove from plans
      this.plans.forEach(p => {
        p.moduleIds = p.moduleIds.filter(id => id !== moduleId)
      })
    },
    
    // User actions
    setUserRole(role) {
      this.currentUser.role = role
    },
    
    subscribeToPlan(planId) {
      this.currentUser.planId = planId
    },
    
    hasAccessToModule(moduleId) {
      if (this.currentUser.role === 'superadmin') return true
      return this.accessibleModuleIds.includes(moduleId)
    },
    
    hasAccessToPath(path) {
      if (this.currentUser.role === 'superadmin') return true
      const module = this.modules.find(m => path.startsWith(m.path))
      if (!module) return true // Allow access to non-module pages
      return this.accessibleModuleIds.includes(module.id)
    },
    
    // ============================================
    // API METHODS - Connect to your backend
    // ============================================
    
    // Fetch current user from API after login
    async fetchCurrentUser() {
      this.isLoading = true
      try {
        // TODO: Replace with your actual API endpoint
        const response = await fetch('/api/user/profile', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
            'Content-Type': 'application/json',
          },
        })
        
        if (response.ok) {
          const userData = await response.json()
          // Expected response format from your users table:
          // {
          //   id: 1,
          //   name: "John Doe",
          //   email: "john@example.com",
          //   role: "superadmin" or "user",
          //   plan_id: 2
          // }
          this.currentUser = {
            id: userData.id,
            name: userData.name,
            email: userData.email,
            role: userData.role, // 'superadmin' or 'user' from database
            planId: userData.plan_id,
            isAuthenticated: true,
          }
        }
      } catch (error) {
        console.error('Failed to fetch user:', error)
      } finally {
        this.isLoading = false
      }
    },
    
    // Login and get user role from database
    async login(email, password) {
      this.isLoading = true
      try {
        // TODO: Replace with your actual login API
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        })
        
        if (response.ok) {
          const data = await response.json()
          // Store token
          localStorage.setItem('accessToken', data.token)
          
          // Set user data including role from database
          this.currentUser = {
            id: data.user.id,
            name: data.user.name,
            email: data.user.email,
            role: data.user.role, // This comes from your users table
            planId: data.user.plan_id,
            isAuthenticated: true,
          }
          return { success: true }
        } else {
          return { success: false, error: 'Invalid credentials' }
        }
      } catch (error) {
        return { success: false, error: error.message }
      } finally {
        this.isLoading = false
      }
    },
    
    // Logout
    logout() {
      localStorage.removeItem('accessToken')
      this.currentUser = {
        id: null,
        name: '',
        email: '',
        role: 'user',
        planId: null,
        isAuthenticated: false,
      }
    },
    
    // For demo/testing - remove in production
    setUserRole(role) {
      this.currentUser.role = role
    },
  },
})
