<script setup>
const lastRefreshTime = ref('2026-01-02 15:32:39')
const selectedTimeframe = ref('30Min')
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']
const timeframes = ['5Min', '15Min', '30Min', '1Hour', '4Hour', 'Daily']
const autoRefresh = ref(false)
const searchQuery = ref('')

// Filter toggles
const filters = ref({
  smallBody: true,
  longBody: true,
  moderateBody: true,
  confirmedTrend: true,
  continueTrend: true,
  newTrend: true,
  reverseTrend: true,
})

// New Trend stocks (Bullish)
const newTrendBullish = ref([
  { symbol: 'BAJFINANCE', trend: 'up' },
  { symbol: 'BEL', trend: 'up' },
  { symbol: 'HDFCBANK', trend: 'up' },
  { symbol: 'JSWSTEEL', trend: 'up' },
  { symbol: 'COFORGE', trend: 'up' },
])

// Reverse Trend
const reverseTrend = ref({ bullish: 0, bearish: 1 })

// Continue Trend stocks (Bullish)
const continueTrend = ref([
  { symbol: 'DIVISLAB', trend: 'up' },
])

// Confirmed Trend
const confirmedTrend = ref({ bullish: 3, bearish: 1 })

// Table data
const tableData = ref([
  { symbol: 'ADANIENT', value: 2279.5, col1: 0, col2: 0, col3: 0, col4: 0, col5: 0, col6: 0, col7: 0, timeframe: '30Min', datetime: '2026-01-02 15:32:16' },
  { symbol: 'APOLLOHOSP', value: 7152.5, col1: 0, col2: 5, col3: 1, col4: 0, col5: 0, col6: 0, col7: 0, timeframe: '30Min', datetime: '2026-01-02 15:32:16' },
  { symbol: 'ASIANPAINT', value: 2774.6, col1: 0, col2: 1, col3: 0, col4: 0, col5: 0, col6: 0, col7: 0, timeframe: '30Min', datetime: '2026-01-02 15:32:16' },
  { symbol: 'BAJFINANCE', value: 540.5, col1: 0, col2: 1, col3: 0, col4: 0, col5: 0, col6: 1, col7: 0, timeframe: '30Min', datetime: '2026-01-02 15:32:16' },
  { symbol: 'BEL', value: 403.25, col1: 0, col2: 1, col3: 0, col4: 0, col5: 0, col6: 0, col7: 0, timeframe: '30Min', datetime: '2026-01-02 15:32:16' },
  { symbol: 'HDFCLIFE', value: 763.3, col1: 0, col2: 0, col3: -1, col4: 0, col5: 0, col6: 0, col7: 0, timeframe: '30Min', datetime: '2026-01-02 15:32:16' },
  { symbol: 'CIPLA', value: 1510.9, col1: 0, col2: 0, col3: 1, col4: 0, col5: 0, col6: 0, col7: 0, timeframe: '30Min', datetime: '2026-01-02 15:32:16' },
  { symbol: 'DRREDDY', value: 1267.5, col1: 0, col2: 0, col3: 1, col4: 0, col5: 0, col6: 0, col7: 0, timeframe: '30Min', datetime: '2026-01-02 15:32:16' },
  { symbol: 'EICHERMOT', value: 7345, col1: -1, col2: 0, col3: 0, col4: 0, col5: 0, col6: 0, col7: 0, timeframe: '30Min', datetime: '2026-01-02 15:32:16' },
  { symbol: 'GRASIM', value: 2803.8, col1: 0, col2: 0, col3: 0, col4: 0, col5: 0, col6: 0, col7: 0, timeframe: '30Min', datetime: '2026-01-02 15:32:16' },
])

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(20)
const totalItems = ref(216)
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Candlestick Dashboard (Using Heikin-Ashi candles)</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-primary text-caption">Candlestick Dashboard (Using Heikin-Ashi candles)</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">New signals appear in every 30 minutes.</p>
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
            <p class="mb-1">1. Heikin-Ashi candles smooth price data for clearer trend identification</p>
            <p class="mb-1">2. New Trend shows stocks starting a new trend direction</p>
            <p class="mb-0">3. Continue Trend shows stocks maintaining their current trend</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Timeframe -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <VChip color="info" variant="flat" size="small">{{ selectedTimeframe }}</VChip>
        <VIcon icon="tabler-chevron-down" size="14" class="ms-1" />
      </VCardText>
    </VCard>

    <!-- Trend Cards -->
    <VRow class="mb-4">
      <!-- New Trend -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">NEW TREND</span>
            <div class="d-flex align-center gap-2">
              <span class="text-caption text-success">Bullish: 5</span>
              <span class="text-caption text-error">Bearish: 2</span>
              <span class="text-caption text-info">Watchlist</span>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="d-flex gap-2 flex-wrap">
              <div v-for="stock in newTrendBullish" :key="stock.symbol" class="stock-chip bullish">
                <span class="font-weight-bold">{{ stock.symbol }}</span>
                <VIcon icon="tabler-trending-up" size="12" class="ms-1" />
              </div>
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Confirmed Trend -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">CONFIRMED TREND</span>
            <div class="d-flex align-center gap-2">
              <span class="text-caption text-success">Bullish: {{ confirmedTrend.bullish }}</span>
              <span class="text-caption text-error">Bearish: {{ confirmedTrend.bearish }}</span>
            </div>
          </VCardTitle>
        </VCard>
      </VCol>
    </VRow>

    <VRow class="mb-4">
      <!-- Reverse Trend -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">REVERSE TREND</span>
            <div class="d-flex align-center gap-2">
              <span class="text-caption text-success">Bullish: {{ reverseTrend.bullish }}</span>
              <span class="text-caption text-error">Bearish: {{ reverseTrend.bearish }}</span>
            </div>
          </VCardTitle>
        </VCard>
      </VCol>

      <!-- Continue Trend -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="d-flex align-center justify-space-between py-2">
            <span class="text-body-1">CONTINUE TREND</span>
            <div class="d-flex align-center gap-2">
              <span class="text-caption text-success">Bullish: 1</span>
              <span class="text-caption text-error">Bearish: 1</span>
              <span class="text-caption text-info">Watchlist</span>
            </div>
          </VCardTitle>
          <VCardText>
            <div class="d-flex gap-2 flex-wrap">
              <div v-for="stock in continueTrend" :key="stock.symbol" class="stock-chip continue">
                <span class="font-weight-bold">{{ stock.symbol }}</span>
                <VIcon icon="tabler-trending-up" size="12" class="ms-1" />
              </div>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>

    <!-- Filters -->
    <VCard class="mb-4">
      <VCardText>
        <div class="d-flex align-center gap-4 mb-4">
          <span class="text-body-2 font-weight-medium">Filters</span>
          <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 120px" />
          <VSelect v-model="selectedTimeframe" :items="timeframes" density="compact" hide-details style="width: 100px" />
        </div>
        <div class="d-flex align-center gap-3 flex-wrap">
          <div class="d-flex align-center gap-1">
            <span class="text-caption">SMALL BODY</span>
            <VSwitch v-model="filters.smallBody" hide-details density="compact" color="info" />
          </div>
          <div class="d-flex align-center gap-1">
            <span class="text-caption">LONG BODY</span>
            <VSwitch v-model="filters.longBody" hide-details density="compact" color="info" />
          </div>
          <div class="d-flex align-center gap-1">
            <span class="text-caption">MODERATE BODY</span>
            <VSwitch v-model="filters.moderateBody" hide-details density="compact" color="info" />
          </div>
          <div class="d-flex align-center gap-1">
            <span class="text-caption">CONFIRMED TREND</span>
            <VSwitch v-model="filters.confirmedTrend" hide-details density="compact" color="info" />
          </div>
          <div class="d-flex align-center gap-1">
            <span class="text-caption">CONTINUE TREND</span>
            <VSwitch v-model="filters.continueTrend" hide-details density="compact" color="info" />
          </div>
          <div class="d-flex align-center gap-1">
            <span class="text-caption">NEW TREND</span>
            <VSwitch v-model="filters.newTrend" hide-details density="compact" color="info" />
          </div>
          <div class="d-flex align-center gap-1">
            <span class="text-caption">REVERSE TREND</span>
            <VSwitch v-model="filters.reverseTrend" hide-details density="compact" color="info" />
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Data Table -->
    <VCard>
      <VCardText>
        <div class="d-flex align-center justify-space-between flex-wrap gap-4 mb-4">
          <VTextField v-model="searchQuery" placeholder="Search" density="compact" hide-details prepend-inner-icon="tabler-search" style="width: 150px" />
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Auto Refresh</span>
            <VSwitch v-model="autoRefresh" hide-details density="compact" />
            <VBtn color="primary" variant="outlined" size="small">Trading View Charts</VBtn>
            <VBtn color="info" variant="outlined" size="small">Watchlist</VBtn>
          </div>
        </div>

        <div class="table-responsive">
          <VTable density="compact" class="ha-table">
            <thead>
              <tr>
                <th><VCheckbox hide-details density="compact" /></th>
                <th class="text-warning">SYMBOL</th>
                <th>VALUE</th>
                <th>COL1</th>
                <th>COL2</th>
                <th>COL3</th>
                <th>COL4</th>
                <th>COL5</th>
                <th>COL6</th>
                <th>COL7</th>
                <th>TIMEFRAME</th>
                <th>DATETIME</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in tableData" :key="item.symbol">
                <td><VCheckbox hide-details density="compact" /></td>
                <td><a href="#" class="text-warning font-weight-medium">{{ item.symbol }}</a></td>
                <td>{{ item.value }}</td>
                <td :class="item.col1 < 0 ? 'text-error' : item.col1 > 0 ? 'text-success' : ''">{{ item.col1 }}</td>
                <td :class="item.col2 < 0 ? 'text-error' : item.col2 > 0 ? 'text-success' : ''">{{ item.col2 }}</td>
                <td :class="item.col3 < 0 ? 'text-error' : item.col3 > 0 ? 'text-success' : ''">{{ item.col3 }}</td>
                <td :class="item.col4 < 0 ? 'text-error' : item.col4 > 0 ? 'text-success' : ''">{{ item.col4 }}</td>
                <td :class="item.col5 < 0 ? 'text-error' : item.col5 > 0 ? 'text-success' : ''">{{ item.col5 }}</td>
                <td :class="item.col6 < 0 ? 'text-error' : item.col6 > 0 ? 'text-success' : ''">{{ item.col6 }}</td>
                <td :class="item.col7 < 0 ? 'text-error' : item.col7 > 0 ? 'text-success' : ''">{{ item.col7 }}</td>
                <td>{{ item.timeframe }}</td>
                <td class="text-info">{{ item.datetime }}</td>
              </tr>
            </tbody>
          </VTable>
        </div>

        <!-- Pagination -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-4 mt-4">
          <div class="d-flex align-center gap-1">
            <VBtn icon variant="text" size="x-small" :disabled="currentPage === 1" @click="currentPage--">
              <VIcon icon="tabler-chevron-left" size="14" />
            </VBtn>
            <VBtn v-for="page in Math.min(totalPages, 7)" :key="page" :color="currentPage === page ? 'primary' : 'default'" :variant="currentPage === page ? 'flat' : 'text'" size="x-small" min-width="24" @click="currentPage = page">{{ page }}</VBtn>
            <span v-if="totalPages > 7" class="mx-1">...</span>
            <VBtn v-if="totalPages > 7" :color="currentPage === totalPages ? 'primary' : 'default'" :variant="currentPage === totalPages ? 'flat' : 'text'" size="x-small" min-width="24" @click="currentPage = totalPages">{{ totalPages }}</VBtn>
            <VBtn icon variant="text" size="x-small" :disabled="currentPage === totalPages" @click="currentPage++">
              <VIcon icon="tabler-chevron-right" size="14" />
            </VBtn>
          </div>
          <div class="d-flex align-center gap-2">
            <VSelect v-model="itemsPerPage" :items="[10, 20, 50]" density="compact" hide-details style="width: 60px" />
            <span class="text-caption text-medium-emphasis">Displaying 1 - 20 of {{ totalItems }} records</span>
          </div>
        </div>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.stock-chip {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 10px;
  color: white;
}

.stock-chip.bullish {
  background-color: rgb(var(--v-theme-success));
}

.stock-chip.continue {
  background-color: rgb(var(--v-theme-info));
}

.ha-table th { font-size: 9px !important; font-weight: 600; white-space: nowrap; }
.ha-table td { font-size: 10px !important; white-space: nowrap; padding: 6px 8px !important; }
.table-responsive { overflow-x: auto; }
</style>
