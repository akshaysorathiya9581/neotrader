export default [
  // SuperAdmin Section (visible only to superadmin)
  {
    title: 'Admin Panel',
    icon: { icon: 'tabler-shield-check' },
    badgeContent: 'Admin',
    badgeClass: 'bg-error',
    children: [
      { title: 'Admin Dashboard', to: { path: '/admin' } },
      { title: 'Manage Plans', to: { path: '/admin/plans' } },
      { title: 'Manage Modules', to: { path: '/admin/modules' } },
    ],
    meta: { requiresAdmin: true },
  },
  // Subscription Plans (for normal users)
  {
    title: 'Subscription',
    icon: { icon: 'tabler-credit-card' },
    to: { path: '/subscription' },
  },
  {
    title: 'Dashboard',
    icon: { icon: 'tabler-chart-pie' },
    children: [
      { title: 'Dashboard', to: { path: '/dashboard' } },
      { title: 'Market View', to: { path: '/dashboard/market-view' } },
      { title: 'Intraday Stock Trends', to: { path: '/dashboard/intraday-stock-trends' } },
    ],
  },
  {
    title: 'Ready Made Trades',
    icon: { icon: 'tabler-bulb' },
    children: [
      { title: 'Options Trade', to: { path: '/trades/options-trade' } },
      { title: 'Intraday Trades', to: { path: '/trades/intraday-trades' } },
      { title: 'Multiday Play', to: { path: '/trades/multiday-play' } },
      { title: 'Positional Play', to: { path: '/trades/positional-play' } },
      { title: 'Investment', to: { path: '/trades/investment' } },
    ],
  },
  {
    title: 'Important Links',
    icon: { icon: 'tabler-tool' },
    children: [
      { title: 'Read CK Narayan\'s insights', href: 'https://cknarayan.com/insights/', target: '_blank' },
      { title: 'Join WhatsApp Channel', href: 'https://www.whatsapp.com/channel/0029VaDQPnE5K3zXJDC5Sv16', target: '_blank' },
      { title: 'Trade Alerts: Telegram Bot', href: 'https://t.me/+K85HU-yNmT9hYjFl', target: '_blank' },
      { title: 'Video Vault', href: 'https://neotrader.in/video-tutorials/', target: '_blank' },
      { title: 'Training Portal', href: 'https://training.neotrader.in/s/store', target: '_blank' },
      { title: 'Leave us a Review', href: 'https://g.page/r/CRicLAL9m8bnEAE/review', target: '_blank' },
      { title: 'Live Support Room', to: { path: '/live-support' } },
    ],
  },
  {
    title: 'Pivots View',
    icon: { icon: 'tabler-arrows-split-2' },
    children: [
      { title: 'Fibonacci Pivots', to: { path: '/pivots/fibonacci-pivots' } },
      { title: 'Camarilla Pivots', to: { path: '/pivots/camarilla-pivots' } },
      { title: 'CPR', to: { path: '/pivots/cpr' } },
    ],
  },
  {
    title: 'Technical Indicator View',
    icon: { icon: 'tabler-chart-line' },
    children: [
      { title: 'ADX Trends', to: { path: '/technical/adx-trends' } },
      { title: 'RSI Trends', to: { path: '/technical/rsi-trends' } },
      { title: 'ATR Trends', to: { path: '/technical/atr-trends' } },
      { title: 'Key Technical Indicators', to: { path: '/technical/key-indicators' } },
    ],
  },
  {
    title: 'Candlestick Dashboard',
    icon: { icon: 'tabler-chart-candle' },
    children: [
      { title: 'Candlestick Dashboard', to: { path: '/candlestick' } },
      { title: 'Heikin Ashi Dashboard', to: { path: '/candlestick/heikin-ashi' } },
    ],
  },
  {
    title: 'Ichimoku Dashboard',
    icon: { icon: 'tabler-chart-area-line' },
    children: [
      { title: 'Ichimoku Dashboard', to: { path: '/ichimoku' } },
    ],
  },
  {
    title: 'Expert Alerts',
    icon: { icon: 'tabler-alert-circle' },
    children: [
      { title: 'Expert Alerts', to: { path: '/expert-alerts' } },
    ],
  },
  {
    title: 'Query Window',
    icon: { icon: 'tabler-search' },
    children: [
      { title: 'Query Window', to: { path: '/query-window' } },
    ],
  },
  {
    title: 'My Markets',
    icon: { icon: 'tabler-briefcase' },
    children: [
      { title: 'My Watchlist', to: { path: '/my-markets/watchlist' } },
      { title: 'My Trades', to: { path: '/my-markets/my-trades' } },
      { title: 'Charts', to: { path: '/my-markets/charts' } },
    ],
  },
  {
    title: 'Stock Analyser',
    icon: { icon: 'tabler-chart-dots-3' },
    to: { path: '/stock-analyser' },
  },
]
