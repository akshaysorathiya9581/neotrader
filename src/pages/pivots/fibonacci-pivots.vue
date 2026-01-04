<script setup>
const lastRefreshTime = ref('Fri 2026-01-02 16:16:10')
const activeTab = ref('bullish')
const autoRefresh = ref(false)
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']

// Bullish stock groups
const bullishGroups = ref([
  {
    title: 'Stocks To Look',
    count: 6,
    showAll: false,
    type: 'bullish',
    stocks: [
      { symbol: 'ADANIPOWER', price: 478.25, change: 2.3, signals: [1,1,1] },
      { symbol: 'AUROPHARMA', price: 1245.60, change: 1.8, signals: [1,1,1] },
      { symbol: 'BAJFINANCE', price: 7125.40, change: 1.5, signals: [1,1,1] },
      { symbol: 'BANKBARODA', price: 245.80, change: 2.1, signals: [1,1,1] },
      { symbol: 'BHEL', price: 245.30, change: 1.9, signals: [1,1,1] },
      { symbol: 'BIOCON', price: 345.20, change: 2.4, signals: [1,1,1] },
    ]
  },
  {
    title: 'R1+',
    count: 28,
    showAll: false,
    type: 'bullish',
    stocks: [
      { symbol: 'TATAPOWER', price: 412.50, change: 3.2, signals: [1,1,1] },
      { symbol: 'COALINDIA', price: 385.40, change: 2.8, signals: [1,1,1] },
      { symbol: 'HINDALCO', price: 625.30, change: 2.5, signals: [1,1,1] },
      { symbol: 'JINDALSTEL', price: 845.60, change: 2.1, signals: [1,1,1] },
      { symbol: 'TATASTEEL', price: 142.80, change: 1.9, signals: [1,1,1] },
      { symbol: 'VEDL', price: 445.20, change: 2.3, signals: [1,1,1] },
      { symbol: 'JSWSTEEL', price: 892.40, change: 1.8, signals: [1,1,1] },
      { symbol: 'NMDC', price: 215.60, change: 2.6, signals: [1,1,1] },
      { symbol: 'NATIONALUM', price: 185.30, change: 3.1, signals: [1,1,1] },
      { symbol: 'SAIL', price: 125.40, change: 2.2, signals: [1,1,1] },
      { symbol: 'MOIL', price: 385.20, change: 1.7, signals: [1,1,1] },
      { symbol: 'HINDZINC', price: 645.80, change: 2.0, signals: [1,1,1] },
    ]
  },
  {
    title: 'R1-R2',
    count: 12,
    showAll: false,
    type: 'bullish',
    stocks: [
      { symbol: 'RELIANCE', price: 2485.30, change: 1.5, signals: [1,1,1] },
      { symbol: 'TCS', price: 3845.60, change: 1.2, signals: [1,1,1] },
      { symbol: 'INFY', price: 1545.80, change: 1.8, signals: [1,1,1] },
      { symbol: 'HDFCBANK', price: 1685.40, change: 1.3, signals: [1,1,1] },
    ]
  },
  {
    title: 'R2-R3',
    count: 8,
    showAll: false,
    type: 'bullish',
    stocks: [
      { symbol: 'ICICIBANK', price: 1125.40, change: 2.1, signals: [1,1,1] },
      { symbol: 'SBIN', price: 812.30, change: 1.9, signals: [1,1,1] },
      { symbol: 'AXISBANK', price: 1085.60, change: 1.6, signals: [1,1,1] },
      { symbol: 'KOTAKBANK', price: 1845.20, change: 1.4, signals: [1,1,1] },
    ]
  },
  {
    title: 'R1-R2',
    count: 6,
    showAll: false,
    type: 'bullish',
    stocks: [
      { symbol: 'WIPRO', price: 485.30, change: 2.3, signals: [1,1,1] },
      { symbol: 'TECHM', price: 1285.60, change: 1.8, signals: [1,1,1] },
      { symbol: 'HCLTECH', price: 1425.40, change: 1.5, signals: [1,1,1] },
      { symbol: 'LTI', price: 5245.80, change: 1.2, signals: [1,1,1] },
    ]
  },
  {
    title: 'P-S',
    count: 4,
    showAll: false,
    type: 'bullish',
    stocks: [
      { symbol: 'SUNPHARMA', price: 1185.40, change: 1.6, signals: [1,1,1] },
      { symbol: 'DRREDDY', price: 5845.30, change: 1.3, signals: [1,1,1] },
      { symbol: 'CIPLA', price: 1425.60, change: 1.8, signals: [1,1,1] },
    ]
  },
])

// Bearish stock groups
const bearishGroups = ref([
  {
    title: 'Bullish To Bearish',
    count: 4,
    showAll: false,
    type: 'bearish',
    stocks: [
      { symbol: 'ADANIENT', price: 2485.30, change: -2.3, signals: [0,0,0] },
      { symbol: 'TITAN', price: 3245.60, change: -1.8, signals: [0,0,0] },
      { symbol: 'TRENT', price: 4125.40, change: -1.5, signals: [0,0,0] },
      { symbol: 'ZOMATO', price: 185.80, change: -2.1, signals: [0,0,0] },
    ]
  },
  {
    title: 'S1-',
    count: 2,
    showAll: false,
    type: 'bearish',
    stocks: [
      { symbol: 'PAYTM', price: 845.30, change: -3.2, signals: [0,0,0] },
      { symbol: 'NYKAA', price: 185.60, change: -2.8, signals: [0,0,0] },
    ]
  },
  {
    title: 'S1-S2',
    count: 6,
    showAll: false,
    type: 'bearish',
    stocks: [
      { symbol: 'POLICYBZR', price: 1485.30, change: -2.1, signals: [0,0,0] },
      { symbol: 'DELHIVERY', price: 385.60, change: -1.9, signals: [0,0,0] },
      { symbol: 'CARTRADE', price: 785.40, change: -2.4, signals: [0,0,0] },
    ]
  },
  {
    title: 'S2-S3',
    count: 4,
    showAll: false,
    type: 'bearish',
    stocks: [
      { symbol: 'IRCTC', price: 845.30, change: -1.8, signals: [0,0,0] },
      { symbol: 'INDIGO', price: 2485.60, change: -1.5, signals: [0,0,0] },
    ]
  },
  {
    title: 'S3+',
    count: 8,
    showAll: false,
    type: 'bearish',
    stocks: [
      { symbol: 'YESBANK', price: 24.50, change: -2.8, signals: [0,0,0] },
      { symbol: 'RBLBANK', price: 185.30, change: -2.3, signals: [0,0,0] },
      { symbol: 'BANDHANBNK', price: 225.60, change: -1.9, signals: [0,0,0] },
      { symbol: 'IDFC', price: 112.40, change: -2.1, signals: [0,0,0] },
    ]
  },
  {
    title: 'P-R',
    count: 4,
    showAll: false,
    type: 'bearish',
    stocks: [
      { symbol: 'PNB', price: 105.30, change: -1.6, signals: [0,0,0] },
      { symbol: 'CANBK', price: 95.60, change: -1.8, signals: [0,0,0] },
      { symbol: 'UNIONBANK', price: 125.40, change: -1.4, signals: [0,0,0] },
    ]
  },
])

const toggleShowAll = (group) => {
  group.showAll = !group.showAll
}
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Fibonacci Pivots</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-medium-emphasis">Fibonacci Pivots</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">Markets will refresh everyday at 6:00am</p>
        </div>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Use Fibonacci pivot levels to identify support/resistance zones</p>
            <p class="mb-1">2. Green stocks are bullish, Red stocks are bearish</p>
            <p class="mb-0">3. R1, R2, R3 are resistance levels; S1, S2, S3 are support levels</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Tabs -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center gap-2">
          <VBtn :color="activeTab === 'bullish' ? 'success' : 'default'" :variant="activeTab === 'bullish' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'bullish'">Bullish</VBtn>
          <VBtn :color="activeTab === 'bearish' ? 'error' : 'default'" :variant="activeTab === 'bearish' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'bearish'">Bearish</VBtn>
        </div>
      </VCardText>
    </VCard>

    <!-- Filters -->
    <VCard class="mb-4">
      <VCardTitle class="py-2">Fibonacci Pivots Filter</VCardTitle>
      <VCardText>
        <div class="d-flex align-center justify-space-between flex-wrap gap-4">
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Auto Refresh</span>
            <VSwitch v-model="autoRefresh" hide-details density="compact" color="primary" />
          </div>
          <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 140px" />
        </div>
      </VCardText>
    </VCard>

    <!-- Content Grid -->
    <VRow>
      <!-- Bullish Column -->
      <VCol cols="12" md="6">
        <template v-for="(group, idx) in bullishGroups" :key="'bull-'+idx">
          <VCard class="mb-4">
            <VCardTitle class="d-flex align-center justify-space-between py-2">
              <div class="d-flex align-center gap-2">
                <span class="text-body-1">{{ group.title }}</span>
                <VChip color="success" size="x-small" variant="flat">{{ group.count }}</VChip>
              </div>
              <span class="text-caption text-medium-emphasis">Stocks of</span>
            </VCardTitle>
            <VCardText>
              <div class="stock-grid">
                <div 
                  v-for="(stock, sIdx) in (group.showAll ? group.stocks : group.stocks.slice(0,8))" 
                  :key="sIdx" 
                  class="stock-card bullish"
                >
                  <div class="signals d-flex gap-1 mb-1">
                    <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                  </div>
                  <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                  <div class="price text-caption">{{ stock.price }}</div>
                  <div class="change text-caption">+{{ stock.change }}%</div>
                </div>
              </div>
              <div v-if="group.stocks.length > 8" class="text-center mt-2">
                <VBtn variant="text" size="x-small" @click="toggleShowAll(group)">
                  <VIcon :icon="group.showAll ? 'tabler-chevron-up' : 'tabler-chevron-down'" size="14" />
                </VBtn>
              </div>
            </VCardText>
          </VCard>
        </template>
      </VCol>

      <!-- Bearish Column -->
      <VCol cols="12" md="6">
        <template v-for="(group, idx) in bearishGroups" :key="'bear-'+idx">
          <VCard class="mb-4">
            <VCardTitle class="d-flex align-center justify-space-between py-2">
              <div class="d-flex align-center gap-2">
                <span class="text-body-1">{{ group.title }}</span>
                <VChip color="error" size="x-small" variant="flat">{{ group.count }}</VChip>
              </div>
              <span class="text-caption text-medium-emphasis">Stocks of</span>
            </VCardTitle>
            <VCardText>
              <div class="stock-grid">
                <div 
                  v-for="(stock, sIdx) in (group.showAll ? group.stocks : group.stocks.slice(0,8))" 
                  :key="sIdx" 
                  class="stock-card bearish"
                >
                  <div class="signals d-flex gap-1 mb-1">
                    <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot bearish-dot"></span>
                  </div>
                  <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                  <div class="price text-caption">{{ stock.price }}</div>
                  <div class="change text-caption">{{ stock.change }}%</div>
                </div>
              </div>
              <div v-if="group.stocks.length > 8" class="text-center mt-2">
                <VBtn variant="text" size="x-small" @click="toggleShowAll(group)">
                  <VIcon :icon="group.showAll ? 'tabler-chevron-up' : 'tabler-chevron-down'" size="14" />
                </VBtn>
              </div>
            </VCardText>
          </VCard>
        </template>
      </VCol>
    </VRow>
  </div>
</template>

<style scoped>
.stock-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.stock-card {
  padding: 8px;
  border-radius: 6px;
  text-align: center;
  font-size: 10px;
}

.stock-card.bullish {
  background-color: rgb(var(--v-theme-success));
  color: white;
}

.stock-card.bearish {
  background-color: rgb(var(--v-theme-error));
  color: white;
}

.signal-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: rgba(255,255,255,0.4);
}

.signal-dot.active {
  background-color: white;
}

.signal-dot.bearish-dot {
  background-color: rgba(255,255,255,0.6);
}

.symbol { font-size: 9px; }
.price { font-size: 8px; opacity: 0.9; }
.change { font-size: 8px; opacity: 0.8; }

@media (max-width: 600px) {
  .stock-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
