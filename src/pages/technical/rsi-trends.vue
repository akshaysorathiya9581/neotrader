<script setup>
const lastRefreshTime = ref('2026-01-02 15:25:54')
const activeTab = ref('heatmap')
const autoRefresh = ref(false)
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']
const selectedTimeframe = ref('30MIN')
const timeframes = ['5MIN', '15MIN', '30MIN', '1HOUR', '4HOUR', 'DAILY']

// Turn Up stocks (Bullish - empty)
const turnUp = ref({ title: 'Turn up', stocks: [] })

// Break out stocks (Bullish)
const breakOut = ref({
  title: 'Break out',
  stocks: [
    { symbol: 'INFY', trend: 'up', signals: [0,0,0,0,0] },
    { symbol: 'ULTRACEMCO', trend: 'up', signals: [0,0,0,0,0] },
    { symbol: 'SIEMENS', trend: 'up', signals: [0,0,0,0,0] },
    { symbol: 'JYOTICABS', trend: 'up', signals: [0,0,0,0,0] },
    { symbol: 'BIOCON', trend: 'up', signals: [0,0,0,0,0] },
    { symbol: 'COLPAL', trend: 'up', signals: [0,0,0,0,0] },
    { symbol: 'PRESTIGE', trend: 'up', signals: [0,0,0,0,0] },
    { symbol: 'HINDCOPPER', trend: 'up', signals: [0,0,0,0,0] },
    { symbol: 'ADANIENT', trend: 'up', signals: [0,0,0,0,0] },
  ]
})

// Turn down stocks (Bearish)
const turnDown = ref({
  title: 'Turn down',
  stocks: [
    { symbol: 'TRENT', trend: 'down', signals: [0,0,0,0,0] },
    { symbol: 'MARUTI', trend: 'down', signals: [0,0,0,0,0] },
    { symbol: 'JSWENERGY', trend: 'down', signals: [0,0,0,0,0] },
    { symbol: 'ASHOKLEY', trend: 'down', signals: [0,0,0,0,0] },
    { symbol: 'HEROMOTOCO', trend: 'down', signals: [0,0,0,0,0] },
    { symbol: 'DIXON', trend: 'down', signals: [0,0,0,0,0] },
  ]
})

// Break down stocks (Bearish)
const breakDown = ref({
  title: 'Break down',
  stocks: [
    { symbol: 'KOTAKBANK', trend: 'down', signals: [0,0,0,0,0] },
  ]
})
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">RSI Trends</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-medium-emphasis">RSI Trends</span>
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
            <p class="mb-1">1. RSI (Relative Strength Index) measures overbought/oversold conditions</p>
            <p class="mb-1">2. Turn up/Break out indicate bullish momentum</p>
            <p class="mb-0">3. Turn down/Break down indicate bearish momentum</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Tabs -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center gap-2 flex-wrap">
          <VBtn :color="activeTab === 'heatmap' ? 'success' : 'default'" :variant="activeTab === 'heatmap' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'heatmap'">Heatmap</VBtn>
          <VBtn :color="activeTab === 'support' ? 'info' : 'default'" :variant="activeTab === 'support' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'support'">RSI Support / Resistance</VBtn>
          <VBtn :color="activeTab === 'divergence' ? 'warning' : 'default'" :variant="activeTab === 'divergence' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'divergence'">Divergence</VBtn>
          <VBtn variant="outlined" size="small" @click="activeTab = 'levels'">Levels</VBtn>
          <VBtn variant="outlined" size="small" @click="activeTab = 'screener'">RSI Screener</VBtn>
          <VBtn variant="outlined" size="small" @click="activeTab = 'multi'">RSI Multi timeframe</VBtn>
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
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Auto Refresh</span>
            <VSwitch v-model="autoRefresh" hide-details density="compact" color="primary" />
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Content Grid -->
    <VRow>
      <!-- Left Column - Bullish -->
      <VCol cols="12" md="6">
        <!-- Turn up -->
        <VCard class="mb-4">
          <VCardTitle class="py-2">Turn up</VCardTitle>
          <VCardText v-if="turnUp.stocks.length === 0">
            <p class="text-caption text-medium-emphasis">No stocks in this category</p>
          </VCardText>
        </VCard>

        <!-- Break out -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Break out</span>
            <span class="text-caption text-info">Watchlist</span>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid">
              <div v-for="(stock, idx) in breakOut.stocks" :key="idx" class="stock-card bullish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon icon="tabler-trending-up" size="12" />
                <div class="signals d-flex gap-1 mt-1 justify-center">
                  <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                </div>
              </div>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Right Column - Bearish -->
      <VCol cols="12" md="6">
        <!-- Turn down -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Turn down</span>
            <span class="text-caption text-info">Watchlist</span>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid">
              <div v-for="(stock, idx) in turnDown.stocks" :key="idx" class="stock-card bearish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon icon="tabler-trending-down" size="12" />
                <div class="signals d-flex gap-1 mt-1 justify-center">
                  <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                </div>
              </div>
            </div>
          </VCardText>
        </VCard>

        <!-- Break down -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Break down</span>
            <span class="text-caption text-info">Watchlist</span>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid">
              <div v-for="(stock, idx) in breakDown.stocks" :key="idx" class="stock-card bearish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon icon="tabler-trending-down" size="12" />
                <div class="signals d-flex gap-1 mt-1 justify-center">
                  <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                </div>
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

@media (max-width: 600px) {
  .stock-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
