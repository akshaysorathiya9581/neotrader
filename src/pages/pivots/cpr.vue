<script setup>
const lastRefreshTime = ref('2026-01-02 18:04:03')
const activeTab = ref('heatmap')
const autoRefresh = ref(false)
const changeNow = ref(false)
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']
const selectedDate = ref('')

// Bullish sections (Left side - Green)
const bullishInsideCPR = ref({
  title: 'Inside CPR',
  count: 3,
  filter: 'All',
  stocks: [
    { symbol: 'BAJAJAUTO', trend: 'up', signals: [1,1,1] },
    { symbol: 'IOC', trend: 'up', signals: [0,1,0,1] },
    { symbol: 'INDIAETNO', trend: 'up', signals: [0,0,0] },
  ]
})

const bullishLevel1 = ref({ title: 'Level 1', count: 0, filter: 'All', stocks: [] })
const bullishLevel2 = ref({ title: 'Level 2', count: 0, filter: 'All', stocks: [] })

const bullishLevel3 = ref({
  title: 'Level 3',
  count: 20,
  stocks: [
    { symbol: 'MARICO', trend: 'up', signals: [0,1] },
    { symbol: 'PNBHOUSING', trend: 'up', signals: [0,1] },
    { symbol: 'BAJAJFINSV', trend: 'up', signals: [0,1] },
    { symbol: 'ASIANPAINT', trend: 'up', signals: [0,1] },
    { symbol: 'EICHERMOTOR', trend: 'up', signals: [0,1] },
    { symbol: 'RELIANCE', trend: 'up', signals: [0,1] },
    { symbol: 'ADANIPORTS', trend: 'up', signals: [0,1] },
    { symbol: 'GUPIL', trend: 'up', signals: [0,1] },
    { symbol: 'TECHM', trend: 'up', signals: [0,1] },
    { symbol: 'CORPBANK', trend: 'up', signals: [0,1] },
    { symbol: 'ACE', trend: 'up', signals: [0,1] },
    { symbol: 'TITAN', trend: 'up', signals: [0,1] },
    { symbol: 'CANARA', trend: 'down', signals: [0,1,0] },
    { symbol: 'CROMPTON', trend: 'down', signals: [0,1,0] },
    { symbol: 'SWARAJ', trend: 'down', signals: [0,1] },
    { symbol: 'HINDPETRO', trend: 'down', signals: [0,1] },
    { symbol: 'NTPC', trend: 'down', signals: [0,1] },
    { symbol: 'SHREERAM', trend: 'down', signals: [0,1] },
    { symbol: 'TATASTEEL', trend: 'down', signals: [0,1] },
    { symbol: 'JSWSTEEL', trend: 'down', signals: [0,1] },
  ]
})

// Bearish sections (Right side - Red)
const bearishInsideCPR = ref({
  title: 'Inside CPR',
  count: 5,
  filter: 'All',
  stocks: [
    { symbol: 'HAL', trend: 'down', signals: [1,1,1] },
    { symbol: 'LTM', trend: 'down', signals: [0,1,0,1] },
    { symbol: 'MARICO', trend: 'down', signals: [0,1,0,1] },
    { symbol: 'SUDARSHAN', trend: 'down', signals: [0,1,0,1] },
    { symbol: 'PAGEIND', trend: 'down', signals: [0,1,0] },
  ]
})

const bearishLevel1 = ref({ title: 'Level 1', count: 0, filter: 'All', stocks: [] })
const bearishLevel2 = ref({ title: 'Level 2', count: 0, filter: 'All', stocks: [] })

const bearishLevel3 = ref({
  title: 'Level 3',
  count: 20,
  stocks: [
    { symbol: 'HAL', trend: 'down', signals: [0,1] },
    { symbol: 'GNATIPORT', trend: 'down', signals: [0,1] },
    { symbol: 'LTIM', trend: 'down', signals: [0,1] },
    { symbol: 'AMARCO', trend: 'down', signals: [0,1] },
    { symbol: 'MYCHARITS', trend: 'down', signals: [0,1] },
    { symbol: 'MYTHOODHIN', trend: 'down', signals: [0,1] },
    { symbol: 'ADANIPAINT', trend: 'down', signals: [0,1] },
    { symbol: 'KOTAKBANK', trend: 'down', signals: [0,1] },
    { symbol: 'BHARTIGNI', trend: 'down', signals: [0,1] },
    { symbol: 'ADANIPOWER', trend: 'down', signals: [0,1] },
    { symbol: 'TRENT', trend: 'down', signals: [0,1] },
    { symbol: 'MOTHERSON', trend: 'down', signals: [0,1] },
    { symbol: 'HREOMOTOCO', trend: 'down', signals: [0,1,0] },
    { symbol: 'LPL', trend: 'down', signals: [0,1,0] },
    { symbol: 'DK', trend: 'down', signals: [0,1] },
    { symbol: 'AUBANK', trend: 'down', signals: [0,1] },
    { symbol: 'AFCAPITAL', trend: 'down', signals: [0,1] },
    { symbol: 'SHRIRAMFIN', trend: 'down', signals: [0,1] },
    { symbol: 'AXISBANK', trend: 'down', signals: [0,1] },
    { symbol: 'JAINRISLABS', trend: 'down', signals: [0,1] },
  ]
})
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Central Pivot Range (CPR)</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-medium-emphasis">Central Pivot Range (CPR)</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">New signals appear every 5 minutes except CPR gap.</p>
          <p class="text-caption text-medium-emphasis mb-0">CPR gap updates at end of day.</p>
          <p class="text-caption mb-0">
            <span class="text-success">NIFTY50:</span> NIFTY 23993.892 Based on Cash Data 
            <span class="text-error ms-2">NIFTY50:</span> NIFTY50 23003 Based on Cash Data
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
            <p class="mb-1">1. CPR (Central Pivot Range) identifies key support/resistance zones</p>
            <p class="mb-1">2. Green stocks are bullish (above CPR), Red stocks are bearish (below CPR)</p>
            <p class="mb-0">3. Inside CPR indicates consolidation, Level 1-3 indicate trend strength</p>
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
          <VBtn :color="activeTab === 'cprwide' ? 'warning' : 'default'" :variant="activeTab === 'cprwide' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'cprwide'">CPR Wide Narrow</VBtn>
        </div>
      </VCardText>
    </VCard>

    <!-- CPR Heatmap Section -->
    <VCard class="mb-4">
      <VCardTitle class="d-flex align-center justify-space-between py-2 flex-wrap gap-2">
        <span class="text-body-1">CPR Heatmap</span>
        <div class="d-flex align-center gap-2">
          <span class="text-caption">Change now</span>
          <VSwitch v-model="changeNow" hide-details density="compact" color="primary" />
          <span class="text-caption">Auto Refresh</span>
          <VSwitch v-model="autoRefresh" hide-details density="compact" />
          <VTextField placeholder="Date" density="compact" hide-details style="width: 100px" type="date" />
          <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 120px" />
        </div>
      </VCardTitle>
    </VCard>

    <!-- Content Grid -->
    <VRow>
      <!-- Bullish Column (Left - Green) -->
      <VCol cols="12" md="6">
        <!-- Inside CPR Bullish -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Inside CPR</span>
            <div class="d-flex align-center gap-2">
              <VBtn color="success" variant="flat" size="x-small">All</VBtn>
              <VBtn variant="outlined" size="x-small">Narrow Filter</VBtn>
              <span class="text-caption">{{ bullishInsideCPR.count }} / 5</span>
              <span class="text-caption text-info">Watchlist</span>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid">
              <div v-for="(stock, idx) in bullishInsideCPR.stocks" :key="idx" class="stock-card bullish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon :icon="stock.trend === 'up' ? 'tabler-trending-up' : 'tabler-trending-down'" size="12" />
                <div class="signals d-flex gap-1 mt-1 justify-center">
                  <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                </div>
              </div>
            </div>
          </VCardText>
        </VCard>

        <!-- Level 1 Bullish -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Level 1</span>
            <div class="d-flex align-center gap-2">
              <VBtn color="success" variant="flat" size="x-small">All</VBtn>
              <VBtn variant="outlined" size="x-small">Wide Filter</VBtn>
              <VBtn variant="outlined" size="x-small">Narrow Filter</VBtn>
              <VBtn variant="outlined" size="x-small">Curated</VBtn>
            </div>
          </VCardTitle>
        </VCard>

        <!-- Level 2 Bullish -->
        <VCard class="mb-4">
          <VCardTitle class="py-2">Level 2</VCardTitle>
        </VCard>

        <!-- Level 3 Bullish -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Level 3</span>
            <div class="d-flex align-center gap-2">
              <span class="text-caption">20 / 148</span>
              <span class="text-caption text-info">Watchlist</span>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid">
              <div v-for="(stock, idx) in bullishLevel3.stocks" :key="idx" class="stock-card" :class="stock.trend === 'up' ? 'bullish' : 'bearish-light'">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon :icon="stock.trend === 'up' ? 'tabler-trending-up' : 'tabler-trending-down'" size="12" />
                <div class="signals d-flex gap-1 mt-1 justify-center">
                  <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                </div>
              </div>
            </div>
            <div class="text-center mt-2">
              <VBtn variant="text" size="x-small">
                <VIcon icon="tabler-chevron-down" size="14" />
              </VBtn>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Bearish Column (Right - Red) -->
      <VCol cols="12" md="6">
        <!-- Inside CPR Bearish -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Inside CPR</span>
            <div class="d-flex align-center gap-2">
              <VBtn color="error" variant="flat" size="x-small">All</VBtn>
              <VBtn variant="outlined" size="x-small">Narrow Filter</VBtn>
              <span class="text-caption">{{ bearishInsideCPR.count }} / 5</span>
              <span class="text-caption text-info">Watchlist</span>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid">
              <div v-for="(stock, idx) in bearishInsideCPR.stocks" :key="idx" class="stock-card bearish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon icon="tabler-trending-down" size="12" />
                <div class="signals d-flex gap-1 mt-1 justify-center">
                  <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                </div>
              </div>
            </div>
          </VCardText>
        </VCard>

        <!-- Level 1 Bearish -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Level 1</span>
            <div class="d-flex align-center gap-2">
              <VBtn color="error" variant="flat" size="x-small">All</VBtn>
              <VBtn variant="outlined" size="x-small">Wide</VBtn>
              <VBtn variant="outlined" size="x-small">Narrow Fil</VBtn>
              <VBtn variant="outlined" size="x-small">Deleted</VBtn>
              <span class="text-caption">0 / 0</span>
            </div>
          </VCardTitle>
        </VCard>

        <!-- Level 2 Bearish -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Level 2</span>
            <span class="text-caption">0 / 0</span>
          </VCardTitle>
        </VCard>

        <!-- Level 3 Bearish -->
        <VCard class="mb-4">
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">Level 3</span>
            <div class="d-flex align-center gap-2">
              <span class="text-caption">20 / 49</span>
              <span class="text-caption text-info">Watchlist</span>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="stock-grid">
              <div v-for="(stock, idx) in bearishLevel3.stocks" :key="idx" class="stock-card bearish">
                <div class="symbol font-weight-bold">{{ stock.symbol }}</div>
                <VIcon icon="tabler-trending-down" size="12" />
                <div class="signals d-flex gap-1 mt-1 justify-center">
                  <span v-for="(s, i) in stock.signals" :key="i" class="signal-dot" :class="s ? 'active' : ''"></span>
                </div>
              </div>
            </div>
            <div class="text-center mt-2">
              <VBtn variant="text" size="x-small">
                <VIcon icon="tabler-chevron-down" size="14" />
              </VBtn>
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

.stock-card.bearish-light {
  background-color: rgba(var(--v-theme-error), 0.7);
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
