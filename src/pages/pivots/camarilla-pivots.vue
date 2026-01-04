<script setup>
const lastRefreshTime = ref('2026-01-02 10:53:00')
const activeTab = ref('breakout')
const autoRefresh = ref(false)
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']
const selectedPage = ref(1)

// Bullish Groups (Left Column)
const bullishGroups = ref([
  {
    title: 'PRICES ABOVE PP',
    count: 20,
    showAll: false,
    stocks: [
      { symbol: 'ADANIPOWER', price: 478.25, change: 2.3, signals: [1,1,1] },
      { symbol: 'COALINDIA', price: 385.40, change: 2.8, signals: [1,1,1] },
      { symbol: 'AUROPHARMA', price: 1245.60, change: 1.8, signals: [1,1,1] },
      { symbol: 'BALKRISIND', price: 2485.30, change: 1.5, signals: [1,1,1] },
      { symbol: 'CANBK', price: 95.60, change: 2.1, signals: [1,1,1] },
      { symbol: 'COALINDIA', price: 385.40, change: 1.9, signals: [1,1,1] },
      { symbol: 'BAJFINANCE', price: 7125.40, change: 2.4, signals: [1,1,1] },
      { symbol: 'INDUSINDBK', price: 1485.30, change: 1.6, signals: [1,1,1] },
      { symbol: 'BANKBARODA', price: 245.80, change: 2.2, signals: [1,1,1] },
      { symbol: 'HDFCAMC', price: 3245.60, change: 1.3, signals: [1,1,1] },
      { symbol: 'BAJAJFINSV', price: 1685.40, change: 1.8, signals: [1,1,1] },
      { symbol: 'MPHASIS', price: 2485.30, change: 2.0, signals: [1,1,1] },
      { symbol: 'BERGEPAINT', price: 545.80, change: 1.7, signals: [1,1,1] },
      { symbol: 'INDHOTEL', price: 485.30, change: 2.5, signals: [1,1,1] },
      { symbol: 'FEDERALBNK', price: 165.40, change: 1.4, signals: [1,1,1] },
      { symbol: 'PVRINOX', price: 1485.60, change: 1.9, signals: [1,1,1] },
    ]
  },
  {
    title: 'PRICES ABOVE H3',
    count: 60,
    showAll: false,
    stocks: [
      { symbol: 'FORTIS', price: 485.30, change: 3.2, signals: [1,1,1] },
      { symbol: 'HINDPETRO', price: 385.60, change: 2.8, signals: [1,1,1] },
      { symbol: 'APOLLOHOSP', price: 5845.40, change: 2.5, signals: [1,1,1] },
      { symbol: 'DRREDDY', price: 5625.30, change: 2.1, signals: [1,1,1] },
      { symbol: 'IDFCFIRSTB', price: 85.60, change: 1.9, signals: [1,1,1] },
      { symbol: 'GRASIM', price: 2085.40, change: 2.3, signals: [1,1,1] },
      { symbol: 'WIPRO', price: 485.30, change: 1.8, signals: [1,1,1] },
      { symbol: 'PIIND', price: 3485.60, change: 2.6, signals: [1,1,1] },
      { symbol: 'HDFC', price: 2985.40, change: 3.1, signals: [1,1,1] },
      { symbol: 'CHAMBLFERT', price: 385.30, change: 2.2, signals: [1,1,1] },
      { symbol: 'HAVELLS', price: 1485.60, change: 1.7, signals: [1,1,1] },
      { symbol: 'DABUR', price: 585.40, change: 2.0, signals: [1,1,1] },
      { symbol: 'BIOCON', price: 345.20, change: 1.6, signals: [1,1,1] },
      { symbol: 'BHEL', price: 245.30, change: 2.4, signals: [0,0,0] },
      { symbol: 'CONCOR', price: 785.60, change: 1.8, signals: [0,0,0] },
      { symbol: 'MCDOWELL', price: 985.40, change: 1.5, signals: [0,0,0] },
    ]
  },
  {
    title: 'PRICES ABOVE H3',
    count: 60,
    showAll: false,
    stocks: [
      { symbol: 'JUBLFOOD', price: 485.30, change: 2.8, signals: [1,1,1] },
      { symbol: 'POLYCAB', price: 5485.60, change: 2.5, signals: [1,1,1] },
      { symbol: 'CROMPTON', price: 385.40, change: 2.1, signals: [1,1,1] },
      { symbol: 'MOTHERSON', price: 125.30, change: 1.9, signals: [1,1,1] },
      { symbol: 'BPCL', price: 385.60, change: 2.3, signals: [1,1,1] },
      { symbol: 'ADANIENT', price: 2485.40, change: 1.8, signals: [1,1,1] },
      { symbol: 'ULTRACEMCO', price: 8485.30, change: 2.6, signals: [0,0,0] },
      { symbol: 'BANDHANBNK', price: 225.60, change: 3.1, signals: [0,0,0] },
      { symbol: 'ATUL', price: 6485.40, change: 2.2, signals: [0,0,0] },
      { symbol: 'BRITANNIA', price: 5085.30, change: 1.7, signals: [0,0,0] },
      { symbol: 'GODREJCP', price: 1085.60, change: 2.0, signals: [0,0,0] },
      { symbol: 'ADANIPORTS', price: 885.40, change: 1.6, signals: [0,0,0] },
    ]
  },
  { title: 'OPEN ABOVE H3', count: 0, showAll: false, stocks: [] },
  { title: 'OPEN ABOVE H4', count: 0, showAll: false, stocks: [] },
  {
    title: 'H3+L3 REJECTION',
    count: 4,
    showAll: false,
    stocks: [
      { symbol: 'MFSL', price: 1085.30, change: 1.5, signals: [1,1,1] },
      { symbol: 'MPHASIS', price: 2485.60, change: 1.8, signals: [1,1,1] },
      { symbol: 'BIOCON', price: 345.40, change: 2.1, signals: [1,1,1] },
      { symbol: 'ADANIPORT', price: 885.30, change: 1.6, signals: [1,1,1] },
    ]
  },
  {
    title: 'H4+L4 REJECTION',
    count: 2,
    showAll: false,
    stocks: [
      { symbol: 'INDIAMART', price: 2485.30, change: 2.3, signals: [1,1,1] },
      { symbol: 'AMBUJACEM', price: 585.60, change: 1.9, signals: [1,1,1] },
    ]
  },
])

// Bearish Groups (Right Column)
const bearishGroups = ref([
  {
    title: 'PRICES BELOW L3',
    count: 1,
    showAll: false,
    stocks: [
      { symbol: 'BANDHANBNK', price: 225.30, change: -2.8, signals: [0,0,0] },
    ]
  },
  {
    title: 'PRICES BELOW L4',
    count: 7,
    showAll: false,
    stocks: [
      { symbol: 'NATIONALUM', price: 185.30, change: -3.2, signals: [0,0,0] },
      { symbol: 'POLICYBZR', price: 1485.60, change: -2.8, signals: [0,0,0] },
      { symbol: 'MOTHERSON', price: 125.40, change: -2.5, signals: [0,0,0] },
      { symbol: 'MCX', price: 3985.30, change: -2.1, signals: [0,0,0] },
      { symbol: 'HINDCOPPER', price: 285.60, change: -1.9, signals: [0,0,0] },
      { symbol: 'STAR', price: 485.40, change: -2.3, signals: [0,0,0] },
    ]
  },
  {
    title: 'PRICES BELOW L3',
    count: 11,
    showAll: false,
    stocks: [
      { symbol: 'ITC', price: 445.30, change: -2.1, signals: [0,0,0] },
      { symbol: 'APOLLOHOSP', price: 5845.60, change: -1.8, signals: [0,0,0] },
      { symbol: 'LATTPE', price: 185.40, change: -2.5, signals: [0,0,0] },
      { symbol: 'ADANIENT', price: 2485.30, change: -1.9, signals: [0,0,0] },
      { symbol: 'MOTHERSON', price: 125.60, change: -2.3, signals: [0,0,0] },
      { symbol: 'HINDCOPPER', price: 285.40, change: -1.6, signals: [0,0,0] },
    ]
  },
  {
    title: 'PRICES BELOW L3',
    count: 4,
    showAll: false,
    stocks: [
      { symbol: 'ADANIPOWER', price: 478.30, change: -2.8, signals: [0,0,0] },
      { symbol: 'CANBK', price: 95.60, change: -2.1, signals: [0,0,0] },
      { symbol: 'INDUSTOWER', price: 385.40, change: -1.9, signals: [0,0,0] },
      { symbol: 'AXISBANK', price: 1085.30, change: -2.3, signals: [0,0,0] },
    ]
  },
  { title: 'OPEN BELOW L3', count: 0, showAll: false, stocks: [] },
  { title: 'OPEN BELOW L4', count: 0, showAll: false, stocks: [] },
  { title: 'H3+L3 BREAKOUT', count: 0, showAll: false, stocks: [] },
  { title: 'H4+L4 BREAKOUT', count: 0, showAll: false, stocks: [] },
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
          <VChip color="primary" variant="flat" size="small">Camarilla Pivots</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-medium-emphasis">Camarilla Pivots</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">New signals appear every 5 minutes.</p>
        </div>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Camarilla pivots use H3, H4, L3, L4 levels for breakout/rejection signals</p>
            <p class="mb-1">2. Green stocks indicate bullish momentum above pivot levels</p>
            <p class="mb-0">3. Red stocks indicate bearish momentum below pivot levels</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Tabs -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center gap-2">
          <VBtn :color="activeTab === 'breakout' ? 'success' : 'default'" :variant="activeTab === 'breakout' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'breakout'">Breakout</VBtn>
          <VBtn :color="activeTab === 'levels' ? 'info' : 'default'" :variant="activeTab === 'levels' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'levels'">Levels</VBtn>
        </div>
      </VCardText>
    </VCard>

    <!-- Filters -->
    <VCard class="mb-4">
      <VCardTitle class="py-2">Camarilla Pivots Filter</VCardTitle>
      <VCardText>
        <div class="d-flex align-center justify-space-between flex-wrap gap-4">
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Auto Refresh</span>
            <VSwitch v-model="autoRefresh" hide-details density="compact" color="primary" />
          </div>
          <div class="d-flex align-center gap-4">
            <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 140px" />
            <div class="d-flex align-center gap-2">
              <VBtn color="success" variant="flat" size="x-small">Bullish</VBtn>
              <span class="text-caption">Page:</span>
              <VSelect v-model="selectedPage" :items="[1,2,3]" density="compact" hide-details style="width: 60px" />
              <span class="text-caption">for:</span>
              <VSelect :items="[10,20,50]" density="compact" hide-details style="width: 60px" model-value="10" />
            </div>
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Stock Filter -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center justify-end gap-2">
          <VBtn color="success" variant="flat" size="x-small">Bullish</VBtn>
          <span class="text-caption">Page:</span>
          <VSelect v-model="selectedPage" :items="[1,2,3]" density="compact" hide-details style="width: 60px" />
          <span class="text-caption">for:</span>
          <VSelect :items="[10,20,50]" density="compact" hide-details style="width: 60px" model-value="10" />
        </div>
      </VCardText>
    </VCard>

    <!-- Content Grid -->
    <VRow>
      <!-- Bullish Column (Left) -->
      <VCol cols="12" md="6">
        <template v-for="(group, idx) in bullishGroups" :key="'bull-'+idx">
          <VCard class="mb-4">
            <VCardTitle class="d-flex align-center justify-space-between py-2">
              <div class="d-flex align-center gap-2">
                <span class="text-body-1">{{ group.title }}</span>
                <VChip :color="group.count > 0 ? 'success' : 'default'" size="x-small" variant="flat">{{ group.count }}</VChip>
              </div>
              <span v-if="group.count > 0" class="text-caption text-medium-emphasis">View All</span>
            </VCardTitle>
            <VCardText v-if="group.stocks.length > 0">
              <div class="stock-grid">
                <div 
                  v-for="(stock, sIdx) in (group.showAll ? group.stocks : group.stocks.slice(0,16))" 
                  :key="sIdx" 
                  class="stock-card" 
                  :class="stock.signals[0] ? 'bullish' : 'bearish'"
                >
                  <div class="signals d-flex gap-1 mb-1">
                    <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                  </div>
                  <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                  <div class="price text-caption">{{ stock.price }}</div>
                  <div class="change text-caption">{{ stock.change > 0 ? '+' : '' }}{{ stock.change }}%</div>
                </div>
              </div>
              <div v-if="group.stocks.length > 16" class="text-center mt-2">
                <VBtn variant="text" size="x-small" @click="toggleShowAll(group)">
                  <VIcon :icon="group.showAll ? 'tabler-chevron-up' : 'tabler-chevron-down'" size="14" />
                </VBtn>
              </div>
            </VCardText>
          </VCard>
        </template>
      </VCol>

      <!-- Bearish Column (Right) -->
      <VCol cols="12" md="6">
        <template v-for="(group, idx) in bearishGroups" :key="'bear-'+idx">
          <VCard class="mb-4">
            <VCardTitle class="d-flex align-center justify-space-between py-2">
              <div class="d-flex align-center gap-2">
                <span class="text-body-1">{{ group.title }}</span>
                <VChip :color="group.count > 0 ? 'error' : 'default'" size="x-small" variant="flat">{{ group.count }}</VChip>
              </div>
              <span v-if="group.count > 0" class="text-caption text-medium-emphasis">View All</span>
            </VCardTitle>
            <VCardText v-if="group.stocks.length > 0">
              <div class="stock-grid">
                <div 
                  v-for="(stock, sIdx) in (group.showAll ? group.stocks : group.stocks.slice(0,16))" 
                  :key="sIdx" 
                  class="stock-card bearish"
                >
                  <div class="signals d-flex gap-1 mb-1">
                    <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot"></span>
                  </div>
                  <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                  <div class="price text-caption">{{ stock.price }}</div>
                  <div class="change text-caption">{{ stock.change }}%</div>
                </div>
              </div>
              <div v-if="group.stocks.length > 16" class="text-center mt-2">
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

.symbol { font-size: 9px; }
.price { font-size: 8px; opacity: 0.9; }
.change { font-size: 8px; opacity: 0.8; }

@media (max-width: 600px) {
  .stock-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
