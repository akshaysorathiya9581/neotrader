<script setup>
const lastRefreshTime = ref('2026-01-02 15:32:36')
const activeTab = ref('heatmap')
const trendFilter = ref(false)
const autoRefresh = ref(false)
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']
const selectedTimeframe = ref('30min')
const timeframes = ['5min', '15min', '30min', '1hour', '4hour', 'daily']

// High ATR stocks
const highATR = ref({
  title: 'HIGH ATR',
  count: 11,
  stocks: [
    { symbol: 'KOTAKBANK', value: 3.63, trend: 'up' },
    { symbol: 'SBIN', value: 2.87, trend: 'up' },
    { symbol: 'NTPC', value: 2.82, trend: 'up' },
    { symbol: 'BAJAJ-AUTO', value: 85.4, trend: 'up' },
    { symbol: 'COROMANDEL', value: 2.77, trend: 'up' },
    { symbol: 'BOSCHLTD', value: 299.69, trend: 'up' },
    { symbol: 'TATAPOWER', value: 2.35, trend: 'up' },
    { symbol: 'DABUR', value: 3.48, trend: 'up' },
    { symbol: 'TORNTPOWER', value: 9.01, trend: 'up' },
    { symbol: 'NHPC', value: 0.67, trend: 'up' },
    { symbol: 'IFL', value: 5.29, trend: 'up' },
  ]
})

// Low ATR stocks
const lowATR = ref({
  title: 'LOW ATR',
  count: 77,
  showAll: false,
  stocks: [
    { symbol: 'ADANIENT', value: 8.83, trend: 'down' },
    { symbol: 'IIL', value: 1.64, trend: 'down' },
    { symbol: 'HDFCLIFE', value: 2.26, trend: 'down' },
    { symbol: 'NIFTY', value: 5.48, trend: 'down' },
    { symbol: 'SUNPHARMA', value: 0.79, trend: 'down' },
    { symbol: 'SRIRAMFIN', value: 6.02, trend: 'down' },
    { symbol: 'ETERNAL', value: 1.18, trend: 'down' },
    { symbol: 'ASOFTECH', value: 5.68, trend: 'down' },
    { symbol: 'INDIGO', value: 16.07, trend: 'down' },
    { symbol: 'TCS', value: 8.76, trend: 'down' },
    { symbol: 'JSWSTEEL', value: 6.68, trend: 'down' },
    { symbol: 'ADANIPORTS', value: 4.21, trend: 'down' },
    { symbol: 'JKSONY', value: 0.67, trend: 'down' },
    { symbol: 'MAXHEALTH', value: 4.37, trend: 'down' },
    { symbol: 'ABB', value: 16.25, trend: 'down' },
    { symbol: 'BAJAJFINSV', value: 60.7, trend: 'down' },
    { symbol: 'MAZDOCK', value: 12.23, trend: 'down' },
    { symbol: 'LTIOACFIN', value: 3.88, trend: 'down' },
    { symbol: 'AMBUJACEM', value: 7.8, trend: 'down' },
    { symbol: 'HINDZINC', value: 2.36, trend: 'down' },
  ]
})

// Spike Up stocks
const spikeUp = ref({
  title: 'SPIKE UP',
  stocks: [
    { symbol: 'SBIN', value: '94.70%', trend: 'up' },
    { symbol: 'TATASTEEL', value: '84.26%', trend: 'up' },
    { symbol: 'ABB', value: '96.62%', trend: 'up' },
  ]
})

// Spike Down stocks
const spikeDown = ref({
  title: 'SPIKE DOWN',
  stocks: [
    { symbol: 'KOTAKBANK', value: '94.50%', trend: 'down' },
    { symbol: 'BEL', value: '81.8%', trend: 'down' },
  ]
})
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">ATR Trends</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-medium-emphasis">ATR Trends</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">New signals appear in every 30 minutes.</p>
          <p class="text-caption mb-0">
            <span class="text-warning">TOPGAINER:</span> NIFTY SRIYSYOO Based on Cash Data 
            <span class="text-error ms-2">TOPLOSER:</span> NIFTY50 SYRAGTY Based on Cash Data
          </p>
        </div>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. ATR (Average True Range) measures market volatility</p>
            <p class="mb-1">2. High ATR indicates high volatility stocks</p>
            <p class="mb-0">3. Spike Up/Down shows sudden volatility changes</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Tabs -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center gap-2 flex-wrap">
          <VBtn :color="activeTab === 'heatmap' ? 'success' : 'default'" :variant="activeTab === 'heatmap' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'heatmap'">Heatmap</VBtn>
          <VBtn :color="activeTab === 'levels' ? 'info' : 'default'" :variant="activeTab === 'levels' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'levels'">Levels</VBtn>
        </div>
      </VCardText>
    </VCard>

    <!-- Filters -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center justify-space-between flex-wrap gap-4">
          <div class="d-flex align-center gap-4">
            <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 140px" />
            <VSelect v-model="selectedTimeframe" :items="timeframes" density="compact" hide-details style="width: 100px" />
          </div>
          <div class="d-flex align-center gap-4">
            <div class="d-flex align-center gap-2">
              <span class="text-caption">Trend Filter</span>
              <VSwitch v-model="trendFilter" hide-details density="compact" color="primary" />
            </div>
            <div class="d-flex align-center gap-2">
              <span class="text-caption">Auto Refresh</span>
              <VSwitch v-model="autoRefresh" hide-details density="compact" />
            </div>
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Content Grid -->
    <VRow>
      <!-- Left Column -->
      <VCol cols="12" md="6">
        <!-- High ATR -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">HIGH ATR ({{ highATR.count }})</span>
            <span class="text-caption text-info">Watchlist</span>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid-wide">
              <div v-for="(stock, idx) in highATR.stocks" :key="idx" class="stock-chip">
                <span class="font-weight-bold">{{ stock.symbol }}</span>
                <span class="text-warning ms-1">: {{ stock.value }}</span>
                <VIcon icon="tabler-trending-up" size="10" class="ms-1" />
              </div>
            </div>
          </VCardText>
        </VCard>

        <!-- Spike Up -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">SPIKE UP</span>
            <span class="text-caption text-info">Watchlist</span>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid">
              <div v-for="(stock, idx) in spikeUp.stocks" :key="idx" class="stock-card bullish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <div class="value text-caption">{{ stock.value }}</div>
                <VIcon icon="tabler-trending-up" size="12" />
              </div>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Right Column -->
      <VCol cols="12" md="6">
        <!-- Low ATR -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">LOW ATR ({{ lowATR.count }})</span>
            <span class="text-caption text-info">Watchlist</span>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid-wide">
              <div v-for="(stock, idx) in (lowATR.showAll ? lowATR.stocks : lowATR.stocks.slice(0,20))" :key="idx" class="stock-chip">
                <span class="font-weight-bold">{{ stock.symbol }}</span>
                <span class="text-warning ms-1">: {{ stock.value }}</span>
                <VIcon icon="tabler-trending-down" size="10" class="ms-1" />
              </div>
            </div>
            <div v-if="lowATR.stocks.length > 20" class="text-center mt-2">
              <VBtn variant="text" size="x-small" @click="lowATR.showAll = !lowATR.showAll">
                <VIcon :icon="lowATR.showAll ? 'tabler-chevron-up' : 'tabler-chevron-down'" size="14" />
              </VBtn>
            </div>
          </VCardText>
        </VCard>

        <!-- Spike Down -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">SPIKE DOWN</span>
            <span class="text-caption text-info">Watchlist</span>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid">
              <div v-for="(stock, idx) in spikeDown.stocks" :key="idx" class="stock-card bearish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <div class="value text-caption">{{ stock.value }}</div>
                <VIcon icon="tabler-trending-down" size="12" />
              </div>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </div>
</template>

<style scoped>
.stock-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.stock-grid-wide {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.stock-chip {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  border: 1px solid rgba(var(--v-border-color), 0.2);
  border-radius: 4px;
  font-size: 10px;
  background-color: rgba(var(--v-theme-surface-variant), 0.3);
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

.symbol { font-size: 9px; }
.value { font-size: 8px; opacity: 0.9; }

@media (max-width: 600px) {
  .stock-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
