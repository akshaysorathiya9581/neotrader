<script setup>
const lastRefreshTime = ref('Fri 2026-01-02 18:30:35')
const activeTab = ref('heatmap')
const autoRefresh = ref(false)
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']

// ADX Heatmap - New Trend Bullish Box
const newTrendBullish = ref({
  title: 'New Trend Bullish Box',
  count: 8,
  stocks: [
    { symbol: 'ASTRAL', price: 1845.30, signals: [1,1] },
    { symbol: 'COFORGE', price: 5485.60, signals: [1,1] },
    { symbol: 'PERSISTENT', price: 4685.40, signals: [1,1] },
    { symbol: 'POLYCAB', price: 5485.30, signals: [1,1] },
    { symbol: 'ESCORTS', price: 3285.60, signals: [1,1] },
    { symbol: 'NAVINFLUOR', price: 3485.40, signals: [1,1] },
    { symbol: 'SBIN', price: 812.30, signals: [1,1] },
    { symbol: 'CROMPTON', price: 385.60, signals: [1,1] },
  ]
})

// New Trend Bearish - empty
const newTrendBearish = ref({
  title: 'New Trend and Bearish',
  stocks: []
})

// Power Trend Bullish Box Exhaustion
const powerTrendBullishEx = ref({
  title: 'Power Trend Bullish Box Exhaustion',
  count: 4,
  stocks: [
    { symbol: 'INDHOTEL', price: 485.30, signals: [1,1] },
    { symbol: 'NATIONALUM', price: 185.60, signals: [1,1] },
    { symbol: 'NHPC', price: 85.40, signals: [1,1] },
    { symbol: 'LODHA', price: 1285.30, signals: [1,1] },
  ]
})

// ADX Bullish - Level 1
const adxBullishLevel1 = ref({
  title: 'Level 1',
  count: 8,
  stocks: [
    { symbol: 'ADANIENT', price: 2485.30, change: 2.1, signals: [1,1,0,0] },
    { symbol: 'APOLLOHOSP', price: 5845.60, change: 1.8, signals: [0,1,0,0] },
    { symbol: 'BAJAJFINSV', price: 1685.40, change: 1.5, signals: [0,0,1,0] },
    { symbol: 'DRREDDY', price: 5625.30, change: 2.3, signals: [0,0,0,1] },
    { symbol: 'BHARTIARTL', price: 1678.90, change: 1.9, signals: [0,1,0,0] },
    { symbol: 'POWERGRID', price: 285.60, change: 2.6, signals: [0,0,1,0] },
    { symbol: 'HINDALCO', price: 625.30, change: 1.7, signals: [1,0,0,0] },
    { symbol: 'RELIANCE', price: 2485.40, change: 2.0, signals: [0,1,0,0] },
    { symbol: 'INDIAOIL', price: 145.60, change: 1.4, signals: [0,0,0,1] },
    { symbol: 'AXISBANK', price: 1085.30, change: 1.8, signals: [1,0,0,0] },
    { symbol: 'SBILIFE', price: 1485.60, change: 2.2, signals: [0,1,0,0] },
    { symbol: 'ADANIPORT', price: 885.40, change: 1.6, signals: [0,0,1,0] },
  ]
})

// ADX Bullish - Level 2
const adxBullishLevel2 = ref({
  title: 'Level 2',
  count: 1,
  stocks: [
    { symbol: 'ACC', price: 2485.30, change: 1.5, signals: [1,1] },
  ]
})

// ADX Bullish - Level 3
const adxBullishLevel3 = ref({ title: 'Level 3', count: 0, stocks: [] })

// ADX Bearish - Level 1
const adxBearishLevel1 = ref({
  title: 'Level 1',
  count: 3,
  stocks: [
    { symbol: 'ADANIENT', price: 2485.30, change: -2.1, signals: [1,1,0,0] },
    { symbol: 'PERSISTENT', price: 4685.40, change: -1.8, signals: [0,1,0,0] },
    { symbol: 'ADANIPOWER', price: 478.30, change: -1.5, signals: [0,0,1,0] },
  ]
})

// ADX Bearish - Level 2
const adxBearishLevel2 = ref({
  title: 'Level 2',
  count: 1,
  stocks: [
    { symbol: 'YESBANK', price: 24.50, change: -2.8, signals: [1,1] },
  ]
})

// ADX Bearish - Level 3
const adxBearishLevel3 = ref({ title: 'Level 3', count: 0, stocks: [] })

// DI+ High section
const diPlusHigh = ref({
  title: 'DI+ High',
  count: 16,
  stocks: [
    { symbol: 'AFFY', price: 485.30, signals: [1,0], change: 2.1 },
    { symbol: 'APOLLOHOSP', price: 5845.60, signals: [1,1], change: 1.8 },
    { symbol: 'APOLLOTYRE', price: 485.40, signals: [0,1], change: 1.5 },
    { symbol: 'BANKBARODA', price: 245.30, signals: [1,0], change: 2.3 },
    { symbol: 'CHAMBLFERT', price: 385.60, signals: [0,1], change: 1.9 },
    { symbol: 'COALINDIA', price: 385.40, signals: [1,0], change: 2.6 },
    { symbol: 'COFORGE', price: 5485.30, signals: [0,1], change: 1.7 },
    { symbol: 'CUMMINS', price: 2485.60, signals: [1,0], change: 2.0 },
    { symbol: 'EICHERMOT', price: 4285.40, signals: [0,1], change: 1.4 },
    { symbol: 'ESCORTS', price: 3285.30, signals: [1,0], change: 1.8 },
    { symbol: 'FEDERALBNK', price: 165.60, signals: [0,1], change: 2.2 },
    { symbol: 'GAIL', price: 185.40, signals: [1,0], change: 1.6 },
    { symbol: 'GRASIM', price: 2085.30, signals: [1,1], change: 2.4 },
    { symbol: 'HAL', price: 4485.60, signals: [0,1], change: 1.3 },
    { symbol: 'HDFCAMC', price: 3245.40, signals: [1,0], change: 1.9 },
    { symbol: 'RELIANCE', price: 2485.30, signals: [0,1], change: 2.1 },
  ]
})

// DI- results section  
const diMinusResults = ref({ title: 'DI- results', count: 0, stocks: [] })

// DI Neutral sections
const diNeutralStock1 = ref({
  title: 'Stock 1',
  count: 10,
  stocks: [
    { symbol: 'APOLLOHOSP', price: 5845.30, signals: [0,1,0,0,0] },
    { symbol: 'COROMANDEL', price: 1285.60, signals: [0,0,1,0,0] },
    { symbol: 'BAJAJFINSV', price: 1685.40, signals: [0,0,0,1,0] },
    { symbol: 'INFY', price: 1545.30, signals: [0,0,0,0,1] },
    { symbol: 'PERSISTENT', price: 4685.60, signals: [0,1,0,0,0] },
    { symbol: 'DRREDDY', price: 5625.40, signals: [0,0,1,0,0] },
    { symbol: 'EICHERMOT', price: 4285.30, signals: [0,0,0,1,0] },
    { symbol: 'AUBANK', price: 685.60, signals: [0,0,0,0,1] },
    { symbol: 'FEDERALBNK', price: 165.40, signals: [0,1,0,0,0] },
    { symbol: 'AMBUJACEM', price: 585.30, signals: [0,0,1,0,0] },
  ]
})

const diNeutralStock2 = ref({
  title: 'Stock 2',
  count: 10,
  stocks: [
    { symbol: 'APOLLOHOSP', price: 5845.30, signals: [0,1,0,0,0] },
    { symbol: 'ADANIENT', price: 2485.60, signals: [0,0,1,0,0] },
    { symbol: 'AMBUJACEM', price: 585.40, signals: [0,0,0,1,0] },
    { symbol: 'AUBANK', price: 685.30, signals: [0,0,0,0,1] },
    { symbol: 'BAJAJFINSV', price: 1685.60, signals: [0,1,0,0,0] },
    { symbol: 'BHARTIARTL', price: 1678.40, signals: [0,0,1,0,0] },
    { symbol: 'PERSISTENT', price: 4685.30, signals: [0,0,0,1,0] },
    { symbol: 'DRREDDY', price: 5625.60, signals: [0,0,0,0,1] },
    { symbol: 'ADANIPOWER', price: 478.40, signals: [0,1,0,0,0] },
    { symbol: 'TATAPOWER', price: 412.30, signals: [0,0,1,0,0] },
  ]
})

const diNeutralStock3 = ref({
  title: 'Stock 3',
  count: 2,
  stocks: [
    { symbol: 'ADANIPORT', price: 885.30, signals: [0,1,0,0,0] },
    { symbol: 'ASIANPAINT', price: 2985.60, signals: [0,0,1,0,0] },
  ]
})

const diNeutralStock4 = ref({
  title: 'Stock 4',
  count: 5,
  stocks: [
    { symbol: 'BEL', price: 285.30, signals: [0,1] },
    { symbol: 'BHARTIARTL', price: 1678.60, signals: [0,0] },
    { symbol: 'PERSISTENT', price: 4685.40, signals: [0,1] },
    { symbol: 'MOTHERSON', price: 125.30, signals: [0,0] },
    { symbol: 'BPCL', price: 385.60, signals: [0,1] },
  ]
})
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">ADX Trends</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-medium-emphasis">ADX Trends</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last refresh date time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">Data refresh every 5 minutes until market close</p>
          <p class="text-caption mb-0">
            <span class="text-success">NIFTY50:</span> 24122.2025 Based on Cash Data - <span class="text-primary">NIFTY 50 stocks data</span>
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
            <p class="mb-1">1. ADX (Average Directional Index) measures trend strength</p>
            <p class="mb-1">2. DI+ indicates bullish momentum, DI- indicates bearish momentum</p>
            <p class="mb-0">3. Higher ADX values indicate stronger trends</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Tabs -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center gap-2">
          <VBtn :color="activeTab === 'heatmap' ? 'success' : 'default'" :variant="activeTab === 'heatmap' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'heatmap'">Heatmap</VBtn>
          <VBtn :color="activeTab === 'levels' ? 'info' : 'default'" :variant="activeTab === 'levels' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'levels'">Levels</VBtn>
        </div>
      </VCardText>
    </VCard>

    <!-- ADX Heatmap Section -->
    <VCard class="mb-4">
      <VCardTitle class="d-flex align-center justify-space-between py-2 flex-wrap gap-2">
        <span class="text-body-1">ADX Heatmap</span>
        <div class="d-flex align-center gap-2">
          <span class="text-caption">Auto Refresh</span>
          <VSwitch v-model="autoRefresh" hide-details density="compact" color="primary" />
          <VTextField placeholder="Date" density="compact" hide-details style="width: 100px" type="date" />
          <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 120px" />
        </div>
      </VCardTitle>
    </VCard>

    <!-- Heatmap Content -->
    <VRow>
      <!-- Left Column - Bullish -->
      <VCol cols="12" md="6">
        <!-- New Trend Bullish Box -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">New Trend Bullish Box</span>
            <span class="text-caption">{{ newTrendBullish.count }} / Watchlist</span>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid">
              <div v-for="(stock, idx) in newTrendBullish.stocks" :key="idx" class="stock-card bullish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon icon="tabler-trending-up" size="12" />
                <div class="signals d-flex gap-1 mt-1 justify-center">
                  <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                </div>
              </div>
            </div>
          </VCardText>
        </VCard>

        <!-- Power Trend Bullish Box Exhaustion -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Power Trend Bullish Box Exhaustion</span>
            <span class="text-caption">{{ powerTrendBullishEx.count }} / Watchlist</span>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid">
              <div v-for="(stock, idx) in powerTrendBullishEx.stocks" :key="idx" class="stock-card bullish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon icon="tabler-trending-up" size="12" />
                <div class="signals d-flex gap-1 mt-1 justify-center">
                  <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                </div>
              </div>
            </div>
          </VCardText>
        </VCard>

        <!-- ADX BULLISH Section -->
        <VCard class="mb-4 border-success">
          <VCardTitle class="py-2 text-success">ADX BULLISH</VCardTitle>
          
          <!-- Level 1 -->
          <VCardText>
            <div class="d-flex align-center justify-space-between mb-2">
              <span class="text-body-2 font-weight-medium">Level 1</span>
              <span class="text-caption">{{ adxBullishLevel1.count }} / Watchlist</span>
            </div>
            <div class="stock-grid">
              <div v-for="(stock, idx) in adxBullishLevel1.stocks" :key="idx" class="stock-card bullish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon icon="tabler-trending-up" size="12" />
                <div class="signals d-flex gap-1 mt-1 justify-center">
                  <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                </div>
              </div>
            </div>
          </VCardText>

          <!-- Level 2 -->
          <VCardText class="pt-0">
            <div class="d-flex align-center justify-space-between mb-2">
              <span class="text-body-2 font-weight-medium">Level 2</span>
            </div>
            <div class="stock-grid">
              <div v-for="(stock, idx) in adxBullishLevel2.stocks" :key="idx" class="stock-card bullish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon icon="tabler-trending-up" size="12" />
              </div>
            </div>
          </VCardText>

          <!-- Level 3 -->
          <VCardText class="pt-0">
            <div class="d-flex align-center justify-space-between mb-2">
              <span class="text-body-2 font-weight-medium">Level 3</span>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Right Column - Bearish -->
      <VCol cols="12" md="6">
        <!-- New Trend and Bearish -->
        <VCard class="mb-4">
          <VCardTitle class="py-2">New Trend and Bearish</VCardTitle>
          <VCardText>
            <p class="text-primary text-caption">Power Trend Bearish Exhaustion</p>
          </VCardText>
        </VCard>

        <!-- ADX BEARISH Section -->
        <VCard class="mb-4 border-error">
          <VCardTitle class="py-2 text-error">ADX BEARISH</VCardTitle>
          
          <!-- Level 1 -->
          <VCardText>
            <div class="d-flex align-center justify-space-between mb-2">
              <span class="text-body-2 font-weight-medium">Level 1</span>
              <span class="text-caption">{{ adxBearishLevel1.count }} / Watchlist</span>
            </div>
            <div class="stock-grid">
              <div v-for="(stock, idx) in adxBearishLevel1.stocks" :key="idx" class="stock-card bearish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon icon="tabler-trending-down" size="12" />
                <div class="signals d-flex gap-1 mt-1 justify-center">
                  <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                </div>
              </div>
            </div>
          </VCardText>

          <!-- Level 2 -->
          <VCardText class="pt-0">
            <div class="d-flex align-center justify-space-between mb-2">
              <span class="text-body-2 font-weight-medium">Level 2</span>
              <span class="text-caption">{{ adxBearishLevel2.count }} / Watchlist</span>
            </div>
            <div class="stock-grid">
              <div v-for="(stock, idx) in adxBearishLevel2.stocks" :key="idx" class="stock-card bearish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon icon="tabler-trending-down" size="12" />
              </div>
            </div>
          </VCardText>

          <!-- Level 3 -->
          <VCardText class="pt-0">
            <div class="d-flex align-center justify-space-between mb-2">
              <span class="text-body-2 font-weight-medium">Level 3</span>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>

    <!-- DI+ High Section -->
    <VCard class="mb-4">
      <VCardTitle class="d-flex align-center justify-space-between py-2">
        <span class="text-body-1">DI+ High</span>
        <span class="text-caption">{{ diPlusHigh.count }}</span>
      </VCardTitle>
      <VCardText>
        <div class="stock-grid">
          <div v-for="(stock, idx) in diPlusHigh.stocks" :key="idx" class="stock-card bullish">
            <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
            <VIcon icon="tabler-trending-up" size="12" />
            <div class="signals d-flex gap-1 mt-1 justify-center">
              <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
            </div>
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- DI- results -->
    <VCard class="mb-4">
      <VCardTitle class="py-2">DI- results</VCardTitle>
    </VCard>

    <!-- DI Neutral Section -->
    <VCard class="mb-4">
      <VCardTitle class="py-2">DI Neutral</VCardTitle>
      <VCardText>
        <span class="text-caption">Watchlist</span>
      </VCardText>
    </VCard>

    <!-- Stock 1 -->
    <VCard class="mb-4">
      <VCardTitle class="d-flex align-center justify-space-between py-2">
        <span class="text-body-2">Stock 1</span>
        <span class="text-caption">20 / 164</span>
      </VCardTitle>
      <VCardText>
        <div class="stock-grid-wide">
          <div v-for="(stock, idx) in diNeutralStock1.stocks" :key="idx" class="stock-card-wide bullish">
            <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
            <VIcon icon="tabler-trending-up" size="12" />
            <div class="signals d-flex gap-1 mt-1 justify-center">
              <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
            </div>
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Stock 2 -->
    <VCard class="mb-4">
      <VCardTitle class="d-flex align-center justify-space-between py-2">
        <span class="text-body-2">Stock 2</span>
      </VCardTitle>
      <VCardText>
        <div class="stock-grid-wide">
          <div v-for="(stock, idx) in diNeutralStock2.stocks" :key="idx" class="stock-card-wide bullish">
            <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
            <VIcon icon="tabler-trending-up" size="12" />
            <div class="signals d-flex gap-1 mt-1 justify-center">
              <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
            </div>
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Stock 3 -->
    <VCard class="mb-4">
      <VCardTitle class="d-flex align-center justify-space-between py-2">
        <span class="text-body-2">Stock 3</span>
        <span class="text-caption">0 / 16</span>
      </VCardTitle>
      <VCardText>
        <div class="stock-grid-wide">
          <div v-for="(stock, idx) in diNeutralStock3.stocks" :key="idx" class="stock-card-wide bullish">
            <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
            <VIcon icon="tabler-trending-up" size="12" />
            <div class="signals d-flex gap-1 mt-1 justify-center">
              <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
            </div>
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Stock 4 -->
    <VCard class="mb-4">
      <VCardTitle class="d-flex align-center justify-space-between py-2">
        <span class="text-body-2">Stock 4</span>
        <span class="text-caption">0 / 5</span>
      </VCardTitle>
      <VCardText>
        <div class="stock-grid-wide">
          <div v-for="(stock, idx) in diNeutralStock4.stocks" :key="idx" class="stock-card-wide bullish">
            <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
            <VIcon icon="tabler-trending-up" size="12" />
            <div class="signals d-flex gap-1 mt-1 justify-center">
              <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
            </div>
          </div>
        </div>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.stock-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.stock-grid-wide {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 8px;
}

.stock-card, .stock-card-wide {
  padding: 8px;
  border-radius: 6px;
  text-align: center;
  font-size: 10px;
}

.stock-card.bullish, .stock-card-wide.bullish {
  background-color: rgb(var(--v-theme-success));
  color: white;
}

.stock-card.bearish, .stock-card-wide.bearish {
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

.symbol { font-size: 8px; }

.border-success { border-left: 3px solid rgb(var(--v-theme-success)) !important; }
.border-error { border-left: 3px solid rgb(var(--v-theme-error)) !important; }

@media (max-width: 960px) {
  .stock-grid { grid-template-columns: repeat(2, 1fr); }
  .stock-grid-wide { grid-template-columns: repeat(5, 1fr); }
}
</style>
