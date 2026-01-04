<script setup>
const lastRefreshTime = ref('2026-01-02 15:32:36')
const activeTab = ref('timeframe')
const autoRefresh = ref(false)
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']
const selectedTimeframe = ref('30Min')
const timeframes = ['5Min', '15Min', '30Min', '1Hour', '4Hour', 'Daily']
const searchQuery = ref('')

// Active indicators
const activeIndicators = ref({
  ama: true,
  adx: true,
  sma: true,
  macd: true,
  bb: true,
  rsi: true,
  stoch: true
})

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(20)
const totalItems = ref(215)

// Table data
const indicatorsData = ref([
  { id: 1, symbol: 'HDFCBANK', timeframe: '30Min', recentValue: 1091, adx: 32.88, atr: 2.0, pdi: 20.30, ndi: 0.72, macd: 2.91, bb_up: 1003.8, bb_mid: 956.44, bb_low: 908.07, rsi: 58.52, slowK: 43.72, slowD: 30.52, sk: 38 },
  { id: 2, symbol: 'HINDALCO', timeframe: '30Min', recentValue: 592.3, adx: 91.58, atr: 3.36, pdi: 41.29, ndi: 4.76, macd: 5.64, bb_up: 935.17, bb_mid: 900.9, bb_low: 584.03, rsi: 85.22, slowK: 91.54, slowD: 93.2, sk: 82 },
  { id: 3, symbol: 'HINDUNILVR', timeframe: '30Min', recentValue: 2349.5, adx: 43.33, atr: 7.73, pdi: 36.01, ndi: 11.77, macd: 10.43, bb_up: 2164.48, bb_mid: 2203.73, bb_low: 2309.82, rsi: 65.58, slowK: 33.8, slowD: 30.77, sk: 62 },
  { id: 4, symbol: 'INFY', timeframe: '30Min', recentValue: 1042.0, adx: 21.85, atr: 4.82, pdi: 22.57, ndi: 15.07, macd: 2.62, bb_up: 1644.25, bb_mid: 1638.72, bb_low: 1028.3, rsi: 60.78, slowK: 53.01, slowD: 18.39, sk: 61 },
  { id: 5, symbol: 'ITC', timeframe: '30Min', recentValue: 550.15, adx: 91.88, atr: 2.36, pdi: 10.87, ndi: 44.38, macd: -8.99, bb_up: 871.01, bb_mid: 855.32, bb_low: 189.62, rsi: 17.41, slowK: 61.41, slowD: 52.39, sk: 60 },
  { id: 6, symbol: 'KOTAKBANK', timeframe: '30Min', recentValue: 3186.0, adx: 43.14, atr: 8.5, pdi: 11.35, ndi: 31.96, macd: 3.51, bb_up: 2032.26, bb_mid: 2203.05, bb_low: 3158.45, rsi: 31.58, slowK: 17.71, slowD: 16.51, sk: 50 },
  { id: 7, symbol: 'TRENT', timeframe: '30Min', recentValue: 4403.9, adx: 55.01, atr: 20.94, pdi: 34.77, ndi: 14.87, macd: 38.22, bb_up: 4473.00, bb_mid: 4594.62, bb_low: 42.89, rsi: 69.16, slowK: 21.06, slowD: 40.3, sk: 62 },
])

const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Key Technical Indicators</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-medium-emphasis">Key Technical Indicators</span>
          <span class="text-primary text-caption ms-2">Generate Report</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">New signals appear in every 30 minutes.</p>
          <p class="text-caption text-medium-emphasis mb-0">TODAYOPEN DATAUSED</p>
        </div>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. View key technical indicators for all stocks in one place</p>
            <p class="mb-1">2. Toggle indicators (ADX, ATR, MACD, RSI, Stochastic) to show/hide columns</p>
            <p class="mb-0">3. Use timeframe and symbol view tabs to filter data</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Tabs -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center gap-2">
          <VBtn :color="activeTab === 'timeframe' ? 'info' : 'default'" :variant="activeTab === 'timeframe' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'timeframe'">Timeframe View</VBtn>
          <VBtn :color="activeTab === 'symbol' ? 'info' : 'default'" :variant="activeTab === 'symbol' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'symbol'">Symbol View</VBtn>
        </div>
      </VCardText>
    </VCard>

    <!-- Filters and Indicators -->
    <VCard class="mb-4">
      <VCardText>
        <VRow align="center">
          <VCol cols="12" md="4">
            <div class="d-flex gap-2">
              <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 140px" />
              <VSelect v-model="selectedTimeframe" :items="timeframes" density="compact" hide-details style="width: 100px" />
            </div>
          </VCol>
          <VCol cols="12" md="8">
            <div class="d-flex align-center justify-end gap-2 flex-wrap">
              <span class="text-caption me-2">AMA</span>
              <VSwitch v-model="activeIndicators.ama" hide-details density="compact" color="info" />
              <span class="text-caption ms-2 me-2">ADX</span>
              <VSwitch v-model="activeIndicators.adx" hide-details density="compact" color="info" />
              <span class="text-caption ms-2 me-2">S+M+B</span>
              <VSwitch v-model="activeIndicators.sma" hide-details density="compact" color="info" />
              <span class="text-caption ms-2 me-2">MACD</span>
              <VSwitch v-model="activeIndicators.macd" hide-details density="compact" color="info" />
              <span class="text-caption ms-2 me-2">BB</span>
              <VSwitch v-model="activeIndicators.bb" hide-details density="compact" color="info" />
              <span class="text-caption ms-2 me-2">RSI</span>
              <VSwitch v-model="activeIndicators.rsi" hide-details density="compact" color="info" />
              <span class="text-caption ms-2 me-2">STOCH</span>
              <VSwitch v-model="activeIndicators.stoch" hide-details density="compact" color="info" />
              <span class="text-caption ms-4">Auto Refresh</span>
              <VSwitch v-model="autoRefresh" hide-details density="compact" />
            </div>
          </VCol>
        </VRow>
        <VRow class="mt-2">
          <VCol cols="12" md="4">
            <VTextField v-model="searchQuery" placeholder="Search" density="compact" hide-details prepend-inner-icon="tabler-search" />
          </VCol>
          <VCol cols="12" md="8">
            <div class="d-flex justify-end gap-2">
              <VBtn color="primary" variant="outlined" size="small">Trading View Charts</VBtn>
              <VBtn color="info" variant="outlined" size="small">Watchlist</VBtn>
            </div>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- Data Table -->
    <VCard>
      <div class="table-responsive">
        <VTable density="compact" class="indicators-table">
          <thead>
            <tr>
              <th><VCheckbox hide-details density="compact" /></th>
              <th>SYMBOL</th>
              <th>TIMEFRAME</th>
              <th>RECENT VALUE</th>
              <th v-if="activeIndicators.adx">ADX</th>
              <th v-if="activeIndicators.ama">ATR</th>
              <th v-if="activeIndicators.adx">PDI</th>
              <th v-if="activeIndicators.adx">NDI</th>
              <th v-if="activeIndicators.macd">MACD</th>
              <th v-if="activeIndicators.bb">BB_UP</th>
              <th v-if="activeIndicators.bb">BB_MID</th>
              <th v-if="activeIndicators.bb">BB_LOW</th>
              <th v-if="activeIndicators.rsi">RSI</th>
              <th v-if="activeIndicators.stoch">SLOWK</th>
              <th v-if="activeIndicators.stoch">SLOWD</th>
              <th>SK</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in indicatorsData" :key="item.id">
              <td><VCheckbox hide-details density="compact" /></td>
              <td><a href="#" class="text-warning font-weight-medium">{{ item.symbol }}</a></td>
              <td>{{ item.timeframe }}</td>
              <td><VChip color="info" size="x-small" variant="flat">{{ item.recentValue }}</VChip></td>
              <td v-if="activeIndicators.adx">{{ item.adx }}</td>
              <td v-if="activeIndicators.ama">{{ item.atr }}</td>
              <td v-if="activeIndicators.adx">{{ item.pdi }}</td>
              <td v-if="activeIndicators.adx">{{ item.ndi }}</td>
              <td v-if="activeIndicators.macd" :class="item.macd < 0 ? 'text-error' : ''">{{ item.macd }}</td>
              <td v-if="activeIndicators.bb">{{ item.bb_up }}</td>
              <td v-if="activeIndicators.bb">{{ item.bb_mid }}</td>
              <td v-if="activeIndicators.bb">{{ item.bb_low }}</td>
              <td v-if="activeIndicators.rsi">{{ item.rsi }}</td>
              <td v-if="activeIndicators.stoch">{{ item.slowK }}</td>
              <td v-if="activeIndicators.stoch">{{ item.slowD }}</td>
              <td>{{ item.sk }}</td>
            </tr>
          </tbody>
        </VTable>
      </div>

      <!-- Pagination -->
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4">
        <div class="d-flex align-center gap-1">
          <VBtn icon variant="text" size="x-small" :disabled="currentPage === 1" @click="currentPage--">
            <VIcon icon="tabler-chevron-left" size="14" />
          </VBtn>
          <VBtn v-for="page in Math.min(totalPages, 8)" :key="page" :color="currentPage === page ? 'primary' : 'default'" :variant="currentPage === page ? 'flat' : 'text'" size="x-small" min-width="24" @click="currentPage = page">{{ page }}</VBtn>
          <span v-if="totalPages > 8" class="mx-1">...</span>
          <VBtn v-if="totalPages > 8" :color="currentPage === totalPages ? 'primary' : 'default'" :variant="currentPage === totalPages ? 'flat' : 'text'" size="x-small" min-width="24" @click="currentPage = totalPages">{{ totalPages }}</VBtn>
          <VBtn icon variant="text" size="x-small" :disabled="currentPage === totalPages" @click="currentPage++">
            <VIcon icon="tabler-chevron-right" size="14" />
          </VBtn>
        </div>
        <div class="d-flex align-center gap-2">
          <VSelect v-model="itemsPerPage" :items="[10, 20, 50]" density="compact" hide-details style="width: 60px" />
          <span class="text-caption text-medium-emphasis">Displaying 1 - 20 of {{ totalItems }} Records</span>
        </div>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.indicators-table th { font-size: 9px !important; font-weight: 600; white-space: nowrap; background-color: rgb(var(--v-theme-surface)); }
.indicators-table td { font-size: 10px !important; white-space: nowrap; padding: 6px 8px !important; }
.table-responsive { overflow-x: auto; }
.indicators-table { min-width: 1400px; }
</style>
