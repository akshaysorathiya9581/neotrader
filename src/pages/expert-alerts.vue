<script setup>
const lastRefreshTime = ref('2026-01-02 15:32:39')

// Bullish Summary stocks
const bullishSummary = ref([
  { symbol: 'BAJAJFINSV', count: 5 }, { symbol: 'HINDALCO', count: 4 }, { symbol: 'TORNTPHARM', count: 3 }, { symbol: 'LICHSGFIN', count: 3 }, { symbol: 'BRITANNIA', count: 3 },
  { symbol: 'GODREJPROP', count: 3 }, { symbol: 'AMBUJACEM', count: 3 }, { symbol: 'LTIM', count: 3 }, { symbol: 'BEL', count: 2 }, { symbol: 'COFORGE', count: 2 },
  { symbol: 'CONCOR', count: 2 }, { symbol: 'ESCORTS', count: 2 }, { symbol: 'GMRINFRA', count: 2 }, { symbol: 'HDFCBANK', count: 2 }, { symbol: 'HINDPETRO', count: 2 },
  { symbol: 'JSWSTEEL', count: 2 }, { symbol: 'M&MFIN', count: 2 }, { symbol: 'OFSS', count: 2 }, { symbol: 'PETRONET', count: 2 }, { symbol: 'SBIN', count: 2 },
  { symbol: 'SYNGENE', count: 2 }, { symbol: 'TATASTEEL', count: 2 }, { symbol: 'TECHM', count: 2 }, { symbol: 'WIPRO', count: 2 },
])

// Bearish Summary stocks
const bearishSummary = ref([
  { symbol: 'PIIND', count: 3 }, { symbol: 'IPCALAB', count: 3 }, { symbol: 'GRANULES', count: 2 }, { symbol: 'LAURUSLABS', count: 2 }, { symbol: 'BIOCON', count: 2 },
  { symbol: 'BANDHANBNK', count: 2 },
])

// Tab selection
const selectedTab = ref('30Min')
const tabs = ['30Min', '60Min', '1Day', '1Week']
const rightTab = ref('30Min')

// Left column alerts
const filteredBreakingAlert = ref([
  { symbol: 'LTIM', trend: 'up' }, { symbol: 'BEL', trend: 'up' }, { symbol: 'TORNTPHARM', trend: 'up' },
])
const priceAction = ref([
  { symbol: 'BAJAJFINSV', trend: 'up' }, { symbol: 'TORNTPHARM', trend: 'up' }, { symbol: 'AMBUJACEM', trend: 'up' }, { symbol: 'BRITANNIA', trend: 'up' },
  { symbol: 'HINDALCO', trend: 'up' }, { symbol: 'LICHSGFIN', trend: 'up' },
])
const adxRising = ref([
  { symbol: 'HDFCBANK', info: 'ADX UP, +DI -' }, { symbol: 'BRITANNIA', info: 'ADX DOWN, +DI -' }, { symbol: 'AMBUJACEM', info: 'ADX DOWN, +DI -' },
  { symbol: 'WIPRO', info: 'ADX UP, +DI -' }, { symbol: 'BAJAJFINSV', info: 'ADX UP, -DI +' },
])
const entropyXUYZ = ref([
  { symbol: 'LTIM', trend: 'up' }, { symbol: 'HINDALCO', trend: 'up' }, { symbol: 'ESCORTS', trend: 'up' },
])
const bbSqueeze = ref([
  { symbol: 'BAJAJFINSV', info: 'Squeeze', percent: '80%' }, { symbol: 'HINDALCO', info: 'Squeeze', percent: '75%' },
  { symbol: 'CONCOR', info: 'Breakout', percent: '100%' }, { symbol: 'GODREJPROP', info: 'Squeeze', percent: '60%' },
])
const emamacdBreakout = ref([
  { symbol: 'LICHSGFIN', trend: 'up' }, { symbol: 'ESCORTS', trend: 'up' },
])
const premiumBar = ref([
  { symbol: 'BAJAJFINSV', trend: 'up' },
])
const volumeSpike = ref([
  { symbol: 'LTIM', vol: '245K', change: '0.5%', value: '245%', pctChange: '145%' },
  { symbol: 'AMIL', vol: '345K', change: '0.3%', value: '200%', pctChange: '100%' },
  { symbol: 'OFSS', vol: '125K', change: '-0.5%', value: '150%', pctChange: '50%' },
  { symbol: 'BEL', vol: '845K', change: '1.2%', value: '300%', pctChange: '200%' },
])
const volumeChangeMon = ref([
  { symbol: 'BEL', trend: 'up' }, { symbol: 'HINDALCO', trend: 'up' }, { symbol: 'BRITANNIA', trend: 'up' }, { symbol: 'LICHSGFIN', trend: 'up' },
  { symbol: 'PETRONET', trend: 'up' }, { symbol: 'TATASTEEL', trend: 'up' },
])
const intdayChangeMon = ref([
  { symbol: 'BAJAJFINSV', trend: 'up' }, { symbol: 'WIPRO', trend: 'up' }, { symbol: 'SYNGENE', trend: 'up' },
])

// Right column alerts
const reversePoliceCandles = ref([
  { symbol: 'HINDALCO', trend: 'up' },
])
const breakoutAndMultiTimeframes = ref([
  { symbol: 'LICHSGFIN', trend: 'up' }, { symbol: 'HINDALCO', trend: 'up' }, { symbol: 'GODREJPROP', trend: 'up' },
])
const reverseAndMultiTimeframes = ref([
  { symbol: 'BAJAJFINSV', trend: 'up' }, { symbol: 'M&MFIN', trend: 'up' }, { symbol: 'ESCORTS', trend: 'up' },
])
const bbCatchMultiTimeframes = ref([
  { symbol: 'BAJAJFINSV', trend: 'up' }, { symbol: 'HINDALCO', trend: 'up' }, { symbol: 'SBIN', trend: 'up' }, { symbol: 'TECHM', trend: 'up' },
])
const priceAlert = ref([
  { symbol: 'HINDALCO', type: 'ABOVE', price: '654.5', target: '655' },
  { symbol: 'GODREJPROP', type: 'ABOVE', price: '2435', target: '2440' },
  { symbol: 'AMBUJACEM', type: 'ABOVE', price: '567.5', target: '568' },
  { symbol: 'BRITANNIA', type: 'BELOW', price: '4876', target: '4870' },
  { symbol: 'LTIM', type: 'ABOVE', price: '5234', target: '5240' },
  { symbol: 'WIPRO', type: 'ABOVE', price: '289.5', target: '290' },
  { symbol: 'ESCORTS', type: 'ABOVE', price: '3456', target: '3460' },
  { symbol: 'PETRONET', type: 'ABOVE', price: '234.5', target: '235' },
  { symbol: 'BAJAJFINSV', type: 'ABOVE', price: '1567', target: '1570' },
  { symbol: 'COFORGE', type: 'BELOW', price: '5678', target: '5670' },
  { symbol: 'SBIN', type: 'ABOVE', price: '765.4', target: '766' },
  { symbol: 'TATASTEEL', type: 'ABOVE', price: '134.5', target: '135' },
  { symbol: 'TECHM', type: 'ABOVE', price: '1234', target: '1235' },
  { symbol: 'HDFCBANK', type: 'ABOVE', price: '1678', target: '1680' },
  { symbol: 'JSWSTEEL', type: 'BELOW', price: '876.5', target: '875' },
  { symbol: 'CONCOR', type: 'ABOVE', price: '987.5', target: '988' },
])
const trendSeparation = ref([
  { symbol: 'LICHSGFIN', trend: 'up' }, { symbol: 'ESCORTS', trend: 'up' }, { symbol: 'GODREJPROP', trend: 'up' },
])
const marketLongShort = ref([
  { symbol: 'LICHSGFIN', trend: 'up' }, { symbol: 'HINDALCO', trend: 'up' }, { symbol: 'TORNTPHARM', trend: 'up' },
])
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Expert Alerts</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-primary text-caption">Expert Alerts</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">Expert curated alerts triggered by multi indicator confluence and multi timeframe correlation.</p>
          <p class="text-caption text-medium-emphasis mb-0">Watchlist ~ NIFTY 200 / Cash Market AllCap</p>
        </div>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Expert alerts are curated signals based on multiple indicator confluence</p>
            <p class="mb-1">2. Bullish Summary shows stocks with multiple bullish signals</p>
            <p class="mb-0">3. Use timeframe tabs to filter alerts by trading horizon</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Summary Cards -->
    <VRow class="mb-4">
      <!-- Bullish Summary -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Bullish Summary</span>
            <a href="#" class="text-caption text-info">View All</a>
          </VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="stock in bullishSummary" :key="stock.symbol" color="success" variant="flat" size="small" class="stock-chip-sm">
                {{ stock.symbol }} <span class="ms-1 font-weight-bold">{{ stock.count }}</span>
              </VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Bearish Summary -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Bearish Summary</span>
            <a href="#" class="text-caption text-info">View All</a>
          </VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="stock in bearishSummary" :key="stock.symbol" color="error" variant="flat" size="small" class="stock-chip-sm">
                {{ stock.symbol }} <span class="ms-1 font-weight-bold">{{ stock.count }}</span>
              </VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>

    <!-- Alerts Grid -->
    <VRow>
      <!-- Left Column -->
      <VCol cols="12" md="6">
        <!-- Timeframe Tabs -->
        <VCard class="mb-4">
          <VCardText class="py-2">
            <div class="d-flex align-center gap-2">
              <VBtn v-for="tab in tabs" :key="tab" :color="selectedTab === tab ? 'info' : 'default'" :variant="selectedTab === tab ? 'flat' : 'outlined'" size="small" @click="selectedTab = tab">{{ tab }}</VBtn>
            </div>
          </VCardText>
        </VCard>

        <!-- Filtered Breaking Alert -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Filtered Breaking Alert</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 3</span>
              <span class="text-caption text-error">Bearish: 0</span>
              <a href="#" class="text-caption text-info">View All</a>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in filteredBreakingAlert" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- Price Action -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Price Action</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 6</span>
              <span class="text-caption text-error">Bearish: 0</span>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in priceAction" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- ADX Rising -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">ADX Rising</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 4</span>
              <span class="text-caption text-error">Bearish: 1</span>
              <a href="#" class="text-caption text-info">View All</a>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in adxRising" :key="s.symbol" color="success" variant="flat" size="small">
                {{ s.symbol }} <span class="text-caption ms-1">{{ s.info }}</span>
              </VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- Entropy X UV Z -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Entropy X UV Z Timeframe</span>
            <span class="text-caption text-info">View All</span>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in entropyXUYZ" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- BB Squeeze -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Bollinger & Keltner Breakout</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 3</span>
              <span class="text-caption text-error">Bearish: 1</span>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in bbSqueeze" :key="s.symbol" color="success" variant="flat" size="small">
                {{ s.symbol }} <span class="text-caption ms-1">{{ s.info }}</span>
              </VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- EMA MACD Breakout -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">EMA/MACD Breakout Timeframe</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 2</span>
              <span class="text-caption text-error">Bearish: 0</span>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in emamacdBreakout" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- Premium Bar -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Premium Bar</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 1</span>
              <span class="text-caption text-error">Bearish: 0</span>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in premiumBar" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- Volume Spike -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Volume Spike</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 3</span>
              <span class="text-caption text-error">Bearish: 1</span>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in volumeSpike" :key="s.symbol" color="success" variant="flat" size="small">
                {{ s.symbol }} <span class="text-caption ms-1">{{ s.vol }}</span>
              </VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- Volume Change Mon -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Volume Change Mon</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 6</span>
              <span class="text-caption text-error">Bearish: 0</span>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in volumeChangeMon" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- Intraday Change Mon -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Intraday Change Mon</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 3</span>
              <span class="text-caption text-error">Bearish: 0</span>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in intdayChangeMon" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Right Column -->
      <VCol cols="12" md="6">
        <!-- Timeframe Tabs -->
        <VCard class="mb-4">
          <VCardText class="py-2">
            <div class="d-flex align-center gap-2">
              <VBtn v-for="tab in tabs" :key="tab" :color="rightTab === tab ? 'info' : 'default'" :variant="rightTab === tab ? 'flat' : 'outlined'" size="small" @click="rightTab = tab">{{ tab }}</VBtn>
            </div>
          </VCardText>
        </VCard>

        <!-- Reverse Police Candles -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Reverse Police Candles</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 1</span>
              <span class="text-caption text-error">Bearish: 0</span>
              <a href="#" class="text-caption text-info">View All</a>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in reversePoliceCandles" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- Breakout And Multi Timeframes -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Breakout And Multi Timeframes</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 3</span>
              <span class="text-caption text-error">Bearish: 0</span>
              <a href="#" class="text-caption text-info">View All</a>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in breakoutAndMultiTimeframes" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- Reverse And Multi Timeframes -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Reverse And Multi Timeframes</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 3</span>
              <span class="text-caption text-error">Bearish: 0</span>
              <a href="#" class="text-caption text-info">View All</a>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in reverseAndMultiTimeframes" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- BB Catch Multi Timeframes -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">BB Catch Multi Timeframes</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 4</span>
              <span class="text-caption text-error">Bearish: 0</span>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in bbCatchMultiTimeframes" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- Price Alert -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Price Alert</span>
            <a href="#" class="text-caption text-info">View All</a>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="(s, i) in priceAlert" :key="i" :color="s.type === 'ABOVE' ? 'success' : 'error'" variant="flat" size="small">
                {{ s.symbol }} <span class="text-caption ms-1">{{ s.type }}</span>
              </VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- Trend Separation -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Trend Separation</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 3</span>
              <span class="text-caption text-error">Bearish: 0</span>
              <a href="#" class="text-caption text-info">View All</a>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in trendSeparation" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>

        <!-- Market Long Short -->
        <VCard class="mb-3">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-2">Market Long/Short</span>
            <div class="d-flex gap-2">
              <span class="text-caption text-success">Bullish: 3</span>
              <span class="text-caption text-error">Bearish: 0</span>
              <a href="#" class="text-caption text-info">View All</a>
            </div>
          </VCardTitle>
          <VCardText class="pt-0">
            <div class="d-flex flex-wrap gap-1">
              <VChip v-for="s in marketLongShort" :key="s.symbol" color="success" variant="flat" size="small">{{ s.symbol }}</VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </div>
</template>

<style scoped>
.stock-chip-sm { font-size: 9px !important; padding: 2px 6px !important; }
</style>
