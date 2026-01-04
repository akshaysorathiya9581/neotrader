<script setup>
const activeTab = ref('bullish')
const indexFilter = ref('NIFTY 500')
const timeframeFilter = ref('INTRADAY')

const indexOptions = ['NIFTY 500', 'NIFTY 50', 'NIFTY 100', 'NIFTY 200', 'BANK NIFTY']
const timeframeOptions = ['INTRADAY', 'DAILY', 'WEEKLY']

// Bullish Summary stocks
const bullishStocks = ref([
  { symbol: 'PRESTIGE', change: 3.2 },
  { symbol: 'COLPAL', change: 2.8 },
  { symbol: 'SIEMENS', change: 2.5 },
  { symbol: 'TATATECH', change: 2.3 },
  { symbol: 'PATANJALI', change: 2.1 },
  { symbol: 'ABB', change: 1.9 },
  { symbol: 'ICICIBANK', change: 1.7 },
  { symbol: 'TATACHEM', change: 1.5 },
])

// Bearish Summary stocks
const bearishStocks = ref([
  { symbol: 'HINDUNILVR', change: -2.1 },
  { symbol: 'TITAN', change: -1.8 },
])

// RSI Trends
const rsiTrends = ref({
  bullish: [
    { symbol: 'INFY', change: 2.1 },
    { symbol: 'ULTRACEMCO', change: 1.9 },
    { symbol: 'SHRIRAMFIN', change: 1.7 },
    { symbol: 'ZYDUSLIFE', change: 1.5 },
    { symbol: 'BIOCON', change: 1.3 },
    { symbol: 'COLPAL', change: 1.2 },
    { symbol: 'PRESTIGE', change: 1.1 },
    { symbol: 'INDUSTOWER', change: 1.0 },
    { symbol: 'ANGELONE', change: 0.9 },
  ],
  bearish: []
})

// Fibonacci Pivots
const fibonacciPivots = ref({
  bullish: [
    { symbol: 'JSWM', change: 2.3 },
    { symbol: 'CRISPOWER', change: 2.1 },
    { symbol: 'INDHOTEL', change: 1.9 },
    { symbol: 'PNB', change: 1.7 },
    { symbol: 'BHEL', change: 1.5 },
    { symbol: 'SYNGENE', change: 1.3 },
    { symbol: 'LICI', change: 1.2 },
    { symbol: 'MAHINPRA', change: 1.1 },
  ],
  bearish: []
})

// Camarilla Pivots
const camarillaPivots = ref({
  bullish: [
    { symbol: 'DLF', change: 2.5 },
    { symbol: 'ASHOKLEY', change: 2.2 },
    { symbol: 'PATANJALI', change: 1.9 },
  ],
  bearish: []
})

// ADX Trends
const adxTrends = ref({
  bullish: [
    { symbol: 'ICICIBANK', change: 2.8 },
    { symbol: 'ABB', change: 2.5 },
    { symbol: 'ASHOKIND', change: 2.3 },
    { symbol: 'VBIL', change: 2.1 },
    { symbol: 'KALYANKJIL', change: 1.9 },
    { symbol: 'TATACHEM', change: 1.7 },
    { symbol: 'CONCOR', change: 1.5 },
    { symbol: 'NATIONALUM', change: 1.4 },
    { symbol: 'PAYTM', change: 1.3 },
    { symbol: 'AUXTM', change: 1.2 },
    { symbol: 'YESBANK', change: 1.1 },
    { symbol: 'PATANJALI', change: 1.0 },
    { symbol: 'IREDA', change: 0.9 },
    { symbol: 'TATATECH', change: 0.8 },
    { symbol: 'HUDCO', change: 0.7 },
    { symbol: 'CAMS', change: 0.6 },
    { symbol: 'MAHINPRA', change: 0.5 },
    { symbol: 'COAL', change: 0.4 },
    { symbol: 'NMTRO', change: 0.3 },
    { symbol: 'NAVYMATRIX', change: 0.2 },
  ],
  bearish: []
})

// Ichimoku Trends
const ichimokuTrends = ref({
  bullish: [
    { symbol: 'APOLLOHOSP', change: 3.1 },
    { symbol: 'ICICIBANK', change: 2.8 },
    { symbol: 'ABB', change: 2.5 },
    { symbol: 'HAL', change: 2.3 },
    { symbol: 'SIEMENS', change: 2.1 },
    { symbol: 'GAWRIK', change: 1.9 },
    { symbol: 'INFY', change: 1.7 },
    { symbol: 'LUPIN', change: 1.5 },
    { symbol: 'COLPAL', change: 1.3 },
    { symbol: 'TATATECH', change: 1.2 },
    { symbol: 'PRESTIGE', change: 1.1 },
  ],
  bearish: []
})

// Scalping Trends
const scalpingTrends = ref({
  bullish: [
    { symbol: 'ABB', change: 2.1 },
    { symbol: 'TATACHEM', change: 1.8 },
  ],
  bearish: []
})

const refresh = () => {
  console.log('Refreshing data...')
}
</script>

<template>
  <div class="changed-now-page">
    <!-- Page Header -->
    <div class="d-flex justify-space-between align-center mb-4">
      <div>
        <h4 class="text-h4 font-weight-bold">Changed Now</h4>
        <VBreadcrumbs :items="[{ title: 'Home', to: '/' }, { title: 'Changed Now', disabled: true }]" class="pa-0" />
      </div>
      <div class="text-right">
        <div class="text-caption text-medium-emphasis">Using realtime data</div>
        <div class="text-caption text-medium-emphasis">To get precise refresh time of all services please refer HOW TO USE section below.</div>
      </div>
    </div>

    <!-- How To Use Section -->
    <VExpansionPanels class="mb-4">
      <VExpansionPanel title="How To Use" color="warning">
        <template #text>
          <p>This page shows real-time stock changes based on various technical indicators.</p>
          <ul>
            <li>Use the filters to select index and timeframe</li>
            <li>Click on any stock chip to view detailed analysis</li>
            <li>Green chips indicate bullish signals, red indicate bearish</li>
          </ul>
        </template>
      </VExpansionPanel>
    </VExpansionPanels>

    <!-- Summary Cards -->
    <VRow class="mb-4">
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="text-success">Bullish Summary</VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-2">
              <VChip
                v-for="stock in bullishStocks"
                :key="stock.symbol"
                color="success"
                variant="flat"
                size="small"
              >
                {{ stock.symbol }}
                <VIcon icon="tabler-chart-line" size="14" class="ms-1" />
              </VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="text-error">Bearish Summary</VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-2">
              <VChip
                v-for="stock in bearishStocks"
                :key="stock.symbol"
                color="error"
                variant="flat"
                size="small"
              >
                {{ stock.symbol }}
                <VIcon icon="tabler-chart-line" size="14" class="ms-1" />
              </VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>

    <!-- Filters -->
    <VCard class="mb-4">
      <VCardText>
        <VRow align="center">
          <VCol cols="12" md="2">
            <VBtnToggle v-model="activeTab" mandatory color="primary" density="compact">
              <VBtn value="bullish">Bullish</VBtn>
              <VBtn value="bearish">Bearish</VBtn>
            </VBtnToggle>
          </VCol>
          <VCol cols="12" md="3">
            <VSelect
              v-model="indexFilter"
              :items="indexOptions"
              label="Index"
              density="compact"
              hide-details
            />
          </VCol>
          <VCol cols="12" md="3">
            <VSelect
              v-model="timeframeFilter"
              :items="timeframeOptions"
              label="Timeframe"
              density="compact"
              hide-details
            />
          </VCol>
          <VCol cols="12" md="2">
            <VBtn color="primary" @click="refresh">Refresh</VBtn>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- Trend Cards -->
    <VRow>
      <!-- RSI Trends -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex justify-space-between align-center">
            <span>RSI Trends</span>
            <div>
              <VChip size="small" color="success" variant="text">Bullish {{ rsiTrends.bullish.length }}</VChip>
              <VChip size="small" color="error" variant="text">Bearish {{ rsiTrends.bearish.length }}</VChip>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-2">
              <VChip
                v-for="stock in rsiTrends.bullish"
                :key="stock.symbol"
                color="success"
                variant="flat"
                size="small"
              >
                {{ stock.symbol }}
                <VIcon icon="tabler-chart-line" size="14" class="ms-1" />
              </VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Fibonacci Pivots -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex justify-space-between align-center">
            <span>Fibonacci Pivots</span>
            <div>
              <VChip size="small" color="success" variant="text">Bullish {{ fibonacciPivots.bullish.length }}</VChip>
              <VChip size="small" color="error" variant="text">Bearish {{ fibonacciPivots.bearish.length }}</VChip>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-2">
              <VChip
                v-for="stock in fibonacciPivots.bullish"
                :key="stock.symbol"
                color="success"
                variant="flat"
                size="small"
              >
                {{ stock.symbol }}
                <VIcon icon="tabler-chart-line" size="14" class="ms-1" />
              </VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Camarilla Pivots -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex justify-space-between align-center">
            <span>Camarilla Pivots</span>
            <div>
              <VChip size="small" color="success" variant="text">Bullish {{ camarillaPivots.bullish.length }}</VChip>
              <VChip size="small" color="error" variant="text">Bearish {{ camarillaPivots.bearish.length }}</VChip>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-2">
              <VChip
                v-for="stock in camarillaPivots.bullish"
                :key="stock.symbol"
                color="success"
                variant="flat"
                size="small"
              >
                {{ stock.symbol }}
                <VIcon icon="tabler-chart-line" size="14" class="ms-1" />
              </VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- ADX Trends -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex justify-space-between align-center">
            <span>ADX Trends</span>
            <div>
              <VChip size="small" color="success" variant="text">Bullish {{ adxTrends.bullish.length }}</VChip>
              <VChip size="small" color="error" variant="text">Bearish {{ adxTrends.bearish.length }}</VChip>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-2">
              <VChip
                v-for="stock in adxTrends.bullish"
                :key="stock.symbol"
                color="success"
                variant="flat"
                size="small"
              >
                {{ stock.symbol }}
                <VIcon icon="tabler-chart-line" size="14" class="ms-1" />
              </VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Ichimoku Trends -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex justify-space-between align-center">
            <span>Ichimoku Trends</span>
            <div>
              <VChip size="small" color="success" variant="text">Bullish {{ ichimokuTrends.bullish.length }}</VChip>
              <VChip size="small" color="error" variant="text">Bearish {{ ichimokuTrends.bearish.length }}</VChip>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-2">
              <VChip
                v-for="stock in ichimokuTrends.bullish"
                :key="stock.symbol"
                color="success"
                variant="flat"
                size="small"
              >
                {{ stock.symbol }}
                <VIcon icon="tabler-chart-line" size="14" class="ms-1" />
              </VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Scalping Trends -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex justify-space-between align-center">
            <span>Scalping Trends</span>
            <div>
              <VChip size="small" color="success" variant="text">Bullish {{ scalpingTrends.bullish.length }}</VChip>
              <VChip size="small" color="error" variant="text">Bearish {{ scalpingTrends.bearish.length }}</VChip>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-2">
              <VChip
                v-for="stock in scalpingTrends.bullish"
                :key="stock.symbol"
                color="success"
                variant="flat"
                size="small"
              >
                {{ stock.symbol }}
                <VIcon icon="tabler-chart-line" size="14" class="ms-1" />
              </VChip>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </div>
</template>
