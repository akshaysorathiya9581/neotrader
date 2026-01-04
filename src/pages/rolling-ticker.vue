<script setup>
// Filter checkboxes
const filters = ref({
  camarilla: true,
  pricePlay: true,
  heikinAshiPatterns: true,
  rsi: false,
  priceGapper: false,
  cpr: false,
  technical: true,
  bollingerBand: false,
  dawn: false,
  priceAndVolumeConfirm: false,
})

// Dropdown filters
const indexFilter = ref('NIFTY 500')
const timeframeFilter = ref('INTRADAY')
const filterType = ref('All')

const indexOptions = ['NIFTY 500', 'NIFTY 50', 'NIFTY 100', 'NIFTY 200', 'BANK NIFTY', 'FNO']
const timeframeOptions = ['INTRADAY', 'DAILY', 'WEEKLY', 'MONTHLY']
const typeOptions = ['All', 'Bullish', 'Bearish']

// Search
const search = ref('')

// Auto refresh
const selectAll = ref(false)
const removeAll = ref(false)
const autoRefresh = ref(false)

// View mode
const viewMode = ref('watchlist')

// Ticker data
const tickerData = ref([
  { symbol: 'DIVISLAB', message: 'FIB PIVOT ABOVE R1', recentValue: 6327.5, timestamp: '2026-01-02 15:03:1', dayHigh: 5095, dayLow: 6332.6, type: 'bullish' },
  { symbol: 'ICICIBANK', message: 'FIB PIVOT ABOVE R3', recentValue: 1354.5, timestamp: '2026-01-02 15:03:1', dayHigh: 859.2, dayLow: 1383.3, type: 'bullish' },
  { symbol: 'KOTAKBANK', message: 'FIB PIVOT BELOW S1', recentValue: 2144.4, timestamp: '2026-01-02 15:03:1', dayHigh: 2273, dayLow: 219.3, type: 'bearish' },
  { symbol: 'ALKEM', message: 'FIB PIVOT ABOVE R3', recentValue: 5527, timestamp: '2026-01-02 15:05:30', dayHigh: 5508.2, dayLow: 5448.6, type: 'normal' },
  { symbol: 'CGPOWER', message: 'FIB PIVOT ABOVE R1', recentValue: 847.8, timestamp: '2026-01-02 15:05:15', dayHigh: 848.5, dayLow: 888, type: 'normal' },
  { symbol: 'ADANIENT', message: 'FIB PIVOT ABOVE R1', recentValue: 2392, timestamp: '2026-01-03 14:48:40', dayHigh: 2491.1, dayLow: 2159, type: 'normal' },
  { symbol: 'HUDCO', message: 'FIB PIVOT ABOVE R1', recentValue: 258.88, timestamp: '2026-01-02 14:43:34', dayHigh: 256.75, dayLow: 225.8, type: 'normal' },
  { symbol: 'LTIM', message: 'FIB PIVOT BELOW S1', recentValue: 'N/M', timestamp: '2026-01-03 14:41:05', dayHigh: 81.75, dayLow: 'N/N', type: 'normal' },
  { symbol: 'SYNGENE', message: 'FIB PIVOT ABOVE R3', recentValue: 890.45, timestamp: '2026-01-02 14:35:11', dayHigh: 883.85, dayLow: 847.55, type: 'normal' },
  { symbol: 'BAJAJFINSV', message: 'FIB PIVOT BELOW S1', recentValue: 2029, timestamp: '2026-01-02 14:35:11', dayHigh: 2050, dayLow: 2025.8, type: 'normal' },
])

const headers = [
  { title: '', key: 'checkbox', width: '40px', sortable: false },
  { title: 'SYMBOL', key: 'symbol' },
  { title: 'MESSAGE', key: 'message' },
  { title: 'RECENT VALUE', key: 'recentValue' },
  { title: 'TIMESTAMP', key: 'timestamp' },
  { title: 'DAY_HIGH', key: 'dayHigh' },
  { title: 'DAY_LOW', key: 'dayLow' },
]

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)
const totalItems = ref(200)

const handleSelectAll = () => {
  Object.keys(filters.value).forEach(key => {
    filters.value[key] = true
  })
}

const handleRemoveAll = () => {
  Object.keys(filters.value).forEach(key => {
    filters.value[key] = false
  })
}

const getRowClass = (item) => {
  if (item.type === 'bullish') return 'row-bullish'
  if (item.type === 'bearish') return 'row-bearish'
  return ''
}
</script>

<template>
  <div class="rolling-ticker-page">
    <!-- Page Header -->
    <div class="d-flex justify-space-between align-center mb-4">
      <div class="d-flex align-center gap-2">
        <h5 class="text-h5 font-weight-bold">Rolling Ticker</h5>
        <VIcon icon="tabler-home" size="18" />
        <span class="text-caption">Rolling Ticker</span>
      </div>
    </div>

    <!-- How To Use Section -->
    <VExpansionPanels class="mb-4">
      <VExpansionPanel title="How To Use" color="warning">
        <template #text>
          <p>Rolling Ticker shows real-time alerts based on technical indicators.</p>
        </template>
      </VExpansionPanel>
    </VExpansionPanels>

    <!-- Rolling Ticker Filters -->
    <VCard class="mb-4">
      <VCardTitle class="d-flex justify-space-between align-center">
        <span>Rolling Ticker Filters</span>
        <div class="d-flex align-center gap-2">
          <VBtn size="small" variant="outlined" @click="handleSelectAll">Select All</VBtn>
          <VBtn size="small" variant="outlined" @click="handleRemoveAll">Remove All</VBtn>
          <div class="d-flex align-center gap-1">
            <span class="text-caption">Auto Refresh</span>
            <VSwitch v-model="autoRefresh" density="compact" hide-details color="primary" />
          </div>
        </div>
      </VCardTitle>
      <VCardText>
        <!-- Filter Checkboxes -->
        <VRow class="mb-4">
          <VCol cols="6" sm="3">
            <VCheckbox v-model="filters.camarilla" label="CAMARILLA" density="compact" hide-details color="primary" />
            <VCheckbox v-model="filters.pricePlay" label="PRICE PLAY" density="compact" hide-details color="primary" />
            <VCheckbox v-model="filters.heikinAshiPatterns" label="HEIKIN ASHI PATTERNS" density="compact" hide-details color="primary" />
          </VCol>
          <VCol cols="6" sm="3">
            <VCheckbox v-model="filters.rsi" label="RSI" density="compact" hide-details color="success" />
            <VCheckbox v-model="filters.priceGapper" label="PRICE GAPPER" density="compact" hide-details color="primary" />
            <VCheckbox v-model="filters.cpr" label="CPR" density="compact" hide-details color="primary" />
          </VCol>
          <VCol cols="6" sm="3">
            <VCheckbox v-model="filters.technical" label="TECHNICAL" density="compact" hide-details color="success" />
            <VCheckbox v-model="filters.bollingerBand" label="BOLLINGER BAND" density="compact" hide-details color="primary" />
          </VCol>
          <VCol cols="6" sm="3">
            <VCheckbox v-model="filters.dawn" label="DAWN" density="compact" hide-details color="primary" />
            <VCheckbox v-model="filters.priceAndVolumeConfirm" label="PRICE AND VOLUME CONFIRM" density="compact" hide-details color="primary" />
          </VCol>
        </VRow>

        <!-- Dropdown Filters -->
        <VRow>
          <VCol cols="12" sm="4">
            <VSelect
              v-model="indexFilter"
              :items="indexOptions"
              density="compact"
              hide-details
              variant="outlined"
            />
          </VCol>
          <VCol cols="12" sm="4">
            <VSelect
              v-model="timeframeFilter"
              :items="timeframeOptions"
              density="compact"
              hide-details
              variant="outlined"
            />
          </VCol>
          <VCol cols="12" sm="4">
            <VSelect
              v-model="filterType"
              :items="typeOptions"
              density="compact"
              hide-details
              variant="outlined"
            />
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- Data Table Card -->
    <VCard>
      <VCardText>
        <!-- Search and View Toggle -->
        <div class="d-flex justify-space-between align-center mb-4">
          <VTextField
            v-model="search"
            placeholder="Search"
            prepend-inner-icon="tabler-search"
            density="compact"
            hide-details
            variant="outlined"
            style="max-width: 200px;"
          />
          <VBtnToggle v-model="viewMode" mandatory density="compact" color="primary">
            <VBtn value="watchlist" size="small">Existing Watchlists</VBtn>
            <VBtn value="watchlist2" size="small">Watchlist</VBtn>
          </VBtnToggle>
        </div>

        <!-- Data Table -->
        <VDataTable
          :headers="headers"
          :items="tickerData"
          :search="search"
          :items-per-page="itemsPerPage"
          class="rolling-ticker-table"
        >
          <template #item.checkbox="{ item }">
            <VCheckbox density="compact" hide-details />
          </template>
          <template #item.symbol="{ item }">
            <span :class="{ 'text-success': item.type === 'bullish', 'text-error': item.type === 'bearish' }" class="font-weight-medium">
              {{ item.symbol }}
            </span>
          </template>
          <template #item.message="{ item }">
            <span :class="{ 'text-success': item.message.includes('ABOVE'), 'text-error': item.message.includes('BELOW') }">
              {{ item.message }}
            </span>
          </template>
          <template #item.recentValue="{ item }">
            {{ typeof item.recentValue === 'number' ? item.recentValue.toFixed(2) : item.recentValue }}
          </template>
          <template #item.dayHigh="{ item }">
            <span class="text-success">{{ item.dayHigh }}</span>
          </template>
          <template #item.dayLow="{ item }">
            <span class="text-error">{{ item.dayLow }}</span>
          </template>
          <template #bottom>
            <div class="d-flex justify-space-between align-center pa-4">
              <VPagination
                v-model="currentPage"
                :length="Math.ceil(totalItems / itemsPerPage)"
                :total-visible="7"
                density="compact"
              />
              <div class="text-caption">
                <VSelect
                  v-model="itemsPerPage"
                  :items="[10, 25, 50, 100]"
                  density="compact"
                  hide-details
                  variant="outlined"
                  style="width: 80px; display: inline-block;"
                />
                <span class="ms-2">Displaying 1 - 10 of {{ totalItems }} records</span>
              </div>
            </div>
          </template>
        </VDataTable>
      </VCardText>
    </VCard>
  </div>
</template>

<style lang="scss">
.rolling-ticker-table {
  .v-data-table__tr {
    &.row-bullish {
      background-color: rgba(0, 200, 150, 0.15) !important;
    }
    &.row-bearish {
      background-color: rgba(0, 200, 200, 0.15) !important;
    }
  }
  
  // Style for bullish/bearish rows based on data
  tbody tr:nth-child(1),
  tbody tr:nth-child(2) {
    background-color: rgba(0, 200, 150, 0.12) !important;
  }
  
  tbody tr:nth-child(3) {
    background-color: rgba(0, 200, 200, 0.12) !important;
  }
}
</style>
