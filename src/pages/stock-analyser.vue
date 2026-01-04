<script setup>
definePage({ meta: { title: 'Stock Analyser' } })

const searchSymbol = ref('NIFTY')
const autoRefresh = ref(true)
const lastRefreshTime = ref('2026-01-02 15:32:50')

// Tabs
const activeTab = ref('intraday')
const tabs = [
  { value: 'intraday', label: 'Intraday', icon: 'tabler-clock' },
  { value: 'multiday', label: 'Multiday', icon: 'tabler-calendar' },
  { value: 'positional', label: 'Positional', icon: 'tabler-trending-up' },
  { value: 'consolidated', label: 'Consolidated View', icon: 'tabler-layout-grid' },
]

// Stats Data
const statsData = ref({
  dayChange: { value: 0.73, label: 'Day Change', sublabel: 'percentage %' },
  weeklyChange: { value: 0.8, label: 'Weekly Change', sublabel: 'percentage %' },
  monthlyChange: { value: 0.8, label: 'Monthly Change', sublabel: 'percentage %' },
  yearChange: { value: 0.8, label: 'Year To Date Change', sublabel: 'percentage %' },
})

// ICHIMOKU Data
const ichimokuData = ref({
  ts: 26296.375,
  ks: 26226.7,
  ssb: 26032.975,
  ssa: 26073.5625,
  cs: 26338.6,
})

// Scores Data
const scoresData = ref({
  candlestick: 33,
  ichimokuBull: 77,
  ichimokuBear: 0,
  camarillaPivot: 'No update in Watchlist',
})

// Active Signals
const activeSignals = ref([
  { type: 'BREAKOUT-1', value: 'NO SIGNAL', color: 'default' },
  { type: 'BREAKOUT-2', value: 'NO SIGNAL', color: 'default' },
  { type: 'BTST-1', value: 'LONG', color: 'success' },
  { type: 'MOMENTUM-1', value: 'LONG', color: 'success' },
  { type: 'SWING-1', value: 'LONG', color: 'success' },
  { type: 'MOMENTUM-2', value: 'NO SIGNAL', color: 'default' },
  { type: 'BREAKOUT-3', value: 'NO SIGNAL', color: 'default' },
  { type: 'REVERSAL-1', value: 'NO SIGNAL', color: 'default' },
  { type: 'REVERSAL-2', value: 'SHORT', color: 'error' },
  { type: 'REVERSAL-3', value: 'NO SIGNAL', color: 'default' },
])

// Camarilla Pivot Values
const pivotValues = ref([
  { type: 'Recent CS', value: 26338.6, color: 'error' },
  { type: 'H8', value: 28877.77, color: 'default' },
  { type: 'H5', value: 26559.14, color: 'default' },
  { type: 'H4', value: 26467.68, color: 'default' },
  { type: 'H3', value: 26396.64, color: 'default' },
  { type: 'PIVOT', value: 26284.3, color: 'default' },
  { type: 'L3', value: 26274.76, color: 'default' },
  { type: 'L4', value: 26213.82, color: 'default' },
  { type: 'L5', value: 26112.26, color: 'default' },
  { type: 'L8', value: 25903.83, color: 'default' },
])

// Technical Indicators
const technicalIndicators = ref([
  { type: 'ADX', value: 37.09, color: 'default' },
  { type: 'PDI', value: 26.72, color: 'success' },
  { type: 'MDI', value: 7.17, color: 'error' },
  { type: 'MACD', value: 64.19, color: 'default' },
  { type: 'BB_UP', value: 26377.19, color: 'success' },
  { type: 'BB_MID', value: 26339.01, color: 'default' },
  { type: 'BB_LOW', value: 26300.84, color: 'error' },
  { type: 'RSI', value: 73.1, color: 'default' },
  { type: 'SLOW_K', value: 64.22, color: 'default' },
  { type: 'SLOW_D', value: 58.35, color: 'default' },
  { type: 'ATR', value: 35.43, color: 'default' },
])

const handleSearch = () => {
  console.log('Searching for:', searchSymbol.value)
}
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-3">
          <h5 class="text-h5 font-weight-bold">Stock Analyser</h5>
          <div class="d-flex align-center gap-1 text-caption text-medium-emphasis">
            <VIcon icon="tabler-home" size="14" />
            <span>- Stock Analyser</span>
          </div>
        </div>
        <div class="text-right">
          <p class="text-caption mb-0 text-medium-emphasis">First Refresh will happen 30 Mins after the Market Open</p>
          <p class="text-caption mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
        </div>
      </VCardText>
    </VCard>

    <!-- Search Bar -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VTextField
            v-model="searchSymbol"
            placeholder="Enter Symbol"
            density="compact"
            hide-details
            style="width: 180px"
          />
          <VBtn color="success" size="small" @click="handleSearch">Go</VBtn>
        </div>
        
        <div class="d-flex align-center gap-2">
          <h5 class="text-h6">Showing Results For - <strong class="text-primary">{{ searchSymbol }}</strong></h5>
        </div>

        <div class="d-flex align-center gap-2">
          <VBtn variant="outlined" color="primary" size="small">
            <VIcon icon="tabler-chart-line" size="16" class="me-1" />
            See Chart
          </VBtn>
          <VBtn variant="outlined" size="small">
            <VIcon icon="tabler-chart-bar" size="16" />
          </VBtn>
          <VBtn color="warning" size="small">WATCHLIST</VBtn>
          <div class="d-flex align-center gap-1">
            <span class="text-caption">Auto Refresh</span>
            <VSwitch v-model="autoRefresh" hide-details density="compact" color="primary" />
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>
            <div class="d-flex align-center gap-2">
              <span>How To Use</span>
            </div>
          </VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Enter stock symbol in the search box and click Go</p>
            <p class="mb-1">2. View technical analysis across different timeframes</p>
            <p class="mb-1">3. Check Active Signals for trading opportunities</p>
            <p class="mb-0">4. Monitor Technical Indicators for market sentiment</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Tabs -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center gap-2 flex-wrap">
          <VChip
            v-for="tab in tabs"
            :key="tab.value"
            :color="activeTab === tab.value ? 'default' : 'default'"
            :variant="activeTab === tab.value ? 'elevated' : 'outlined'"
            size="small"
            @click="activeTab = tab.value"
          >
            <VIcon :icon="tab.icon" size="14" class="me-1" />
            {{ tab.label }}
          </VChip>
          <VBtn color="success" size="small">
            <VIcon icon="tabler-device-floppy" size="14" class="me-1" />
            Save
          </VBtn>
          <VSpacer />
          <VBtn variant="text" size="small" color="error">
            <VIcon icon="tabler-file-type-pdf" size="18" />
          </VBtn>
        </div>
      </VCardText>
    </VCard>

    <!-- Stats Row -->
    <VCard class="mb-4">
      <VCardText class="py-3">
        <VRow>
          <VCol v-for="(stat, key) in statsData" :key="key" cols="6" md="3">
            <div class="d-flex justify-space-between align-center">
              <div>
                <p class="text-success text-body-2 font-weight-medium mb-0">{{ stat.label }}</p>
                <p class="text-caption text-success mb-0">{{ stat.sublabel }}</p>
              </div>
              <span class="text-h6 font-weight-bold">{{ stat.value }}</span>
            </div>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- ICHIMOKU Row -->
    <VCard class="mb-4">
      <VCardText class="py-3">
        <VRow align="center">
          <VCol cols="12" md="2">
            <span class="text-h6 font-weight-bold">ICHIMOKU</span>
          </VCol>
          <VCol cols="6" md="2">
            <div class="d-flex align-center gap-2">
              <span class="text-body-2 font-weight-medium">TS</span>
              <span class="text-success font-weight-bold">{{ ichimokuData.ts }}</span>
            </div>
          </VCol>
          <VCol cols="6" md="2">
            <div class="d-flex align-center gap-2">
              <span class="text-body-2 font-weight-medium">KS</span>
              <span class="text-success font-weight-bold">{{ ichimokuData.ks }}</span>
            </div>
          </VCol>
          <VCol cols="6" md="2">
            <div class="d-flex align-center gap-2">
              <span class="text-body-2 font-weight-medium">SSB</span>
              <span class="text-success font-weight-bold">{{ ichimokuData.ssb }}</span>
            </div>
          </VCol>
          <VCol cols="6" md="2">
            <div class="d-flex align-center gap-2">
              <span class="text-body-2 font-weight-medium">SSA</span>
              <span class="text-success font-weight-bold">{{ ichimokuData.ssa }}</span>
            </div>
          </VCol>
          <VCol cols="6" md="2">
            <div class="d-flex align-center gap-2">
              <span class="text-body-2 font-weight-medium">CS</span>
              <span class="text-success font-weight-bold">{{ ichimokuData.cs }}</span>
            </div>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- Scores Row -->
    <VCard class="mb-4">
      <VCardText class="py-3">
        <VRow>
          <VCol cols="6" md="3">
            <div class="d-flex justify-space-between align-center">
              <span class="text-success text-body-2 font-weight-medium">Candlestick Score</span>
              <span class="text-h5 font-weight-bold">{{ scoresData.candlestick }}</span>
            </div>
          </VCol>
          <VCol cols="6" md="3">
            <div class="d-flex justify-space-between align-center">
              <span class="text-success text-body-2 font-weight-medium">Ichimoku Bull Score</span>
              <span class="text-h5 font-weight-bold">{{ scoresData.ichimokuBull }}</span>
            </div>
          </VCol>
          <VCol cols="6" md="3">
            <div class="d-flex justify-space-between align-center">
              <span class="text-success text-body-2 font-weight-medium">Ichimoku Bear Score</span>
              <span class="text-h5 font-weight-bold">{{ scoresData.ichimokuBear }}</span>
            </div>
          </VCol>
          <VCol cols="6" md="3">
            <div>
              <span class="text-success text-body-2 font-weight-medium">Camarilla Pivot Range</span>
              <p class="text-caption text-medium-emphasis mb-0">
                <VIcon icon="tabler-info-circle" size="12" />
                {{ scoresData.camarillaPivot }}
              </p>
            </div>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- Tables Row -->
    <VRow>
      <!-- Active Signals -->
      <VCol cols="12" md="4">
        <VCard>
          <VCardTitle class="text-body-1 font-weight-bold py-2">Active Signals</VCardTitle>
          <VCardText class="pa-0">
            <VTable density="compact">
              <thead>
                <tr>
                  <th class="text-left text-caption text-success">Type</th>
                  <th class="text-right text-caption">Value</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="signal in activeSignals" :key="signal.type">
                  <td class="text-error text-caption font-weight-medium">{{ signal.type }}</td>
                  <td class="text-right">
                    <span :class="[
                      'text-caption font-weight-medium',
                      signal.color === 'success' ? 'text-success' : 
                      signal.color === 'error' ? 'text-error' : 'text-medium-emphasis'
                    ]">{{ signal.value }}</span>
                  </td>
                </tr>
              </tbody>
            </VTable>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Camarilla Pivot Values -->
      <VCol cols="12" md="4">
        <VCard>
          <VCardTitle class="text-body-1 font-weight-bold py-2">Camarilla Pivot Values</VCardTitle>
          <VCardText class="pa-0">
            <VTable density="compact">
              <thead>
                <tr>
                  <th class="text-left text-caption text-success">Type</th>
                  <th class="text-right text-caption">Value</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="pivot in pivotValues" :key="pivot.type">
                  <td :class="[
                    'text-caption font-weight-medium',
                    pivot.color === 'error' ? 'text-error' : ''
                  ]">{{ pivot.type }}</td>
                  <td class="text-right">
                    <span :class="[
                      'text-caption',
                      pivot.color === 'error' ? 'text-error' : 'text-success'
                    ]">{{ pivot.value }}</span>
                  </td>
                </tr>
              </tbody>
            </VTable>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Technical Indicators -->
      <VCol cols="12" md="4">
        <VCard>
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1 font-weight-bold">Technical Indicators</span>
            <span class="text-caption text-primary font-italic">Technical Indicators Computed Indexes for the Screen Only</span>
          </VCardTitle>
          <VCardText class="pa-0">
            <VTable density="compact">
              <thead>
                <tr>
                  <th class="text-left text-caption text-success">Type</th>
                  <th class="text-right text-caption">Value</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="indicator in technicalIndicators" :key="indicator.type">
                  <td class="text-caption font-weight-medium">{{ indicator.type }}</td>
                  <td class="text-right">
                    <span :class="[
                      'text-caption',
                      indicator.color === 'success' ? 'text-success' : 
                      indicator.color === 'error' ? 'text-error' : ''
                    ]">{{ indicator.value }}</span>
                  </td>
                </tr>
              </tbody>
            </VTable>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>

    <!-- Footer -->
    <div class="text-center mt-4 text-caption text-medium-emphasis">
      Product of Neotrader research LLP | 2026 © Powered by <span class="text-primary">NeoTrader</span>
    </div>
  </div>
</template>

<style scoped>
.v-table {
  font-size: 12px;
}
</style>
