<script setup>
const lastRefreshTime = ref('2026-01-02 16:10:53')

// Filters
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']
const openTrades = ref(true)
const nonCurated = ref(false)
const curated = ref(true)
const supercurated = ref(true)
const autoRefresh = ref(false)

// Search & Pagination
const searchQuery = ref('')
const selectedTrades = ref([])
const currentPage = ref(1)
const itemsPerPage = ref(10)
const totalItems = ref(25)

// Trades data
const tradesData = ref([
  { id: 1, strategy: 'POSITIONAL-1', timeplay: 'POSITIONAL', symbol: 'RELIANCE', recentValue: 2485.50, alert: 'LONG', signalDt: '2026-01-02 15:04:32', status: 'ACTIVE', entry: 2450, t1: 2520, t2: 2590, t3: 2660, sl: 2380, trade: 'OPEN', exit: 0 },
  { id: 2, strategy: 'POSITIONAL-1', timeplay: 'POSITIONAL', symbol: 'TCS', recentValue: 3890.25, alert: 'LONG', signalDt: '2026-01-02 15:04:32', status: 'T1 HIT', entry: 3750, t1: 3850, t2: 3950, t3: 4050, sl: 3650, trade: 'OPEN', exit: 0 },
  { id: 3, strategy: 'SWING-1', timeplay: 'POSITIONAL', symbol: 'HDFCBANK', recentValue: 1685.80, alert: 'LONG', signalDt: '2025-12-28 15:04:46', status: 'T2 HIT', entry: 1620, t1: 1660, t2: 1700, t3: 1740, sl: 1580, trade: 'OPEN', exit: 0 },
  { id: 4, strategy: 'POSITIONAL-2', timeplay: 'POSITIONAL', symbol: 'INFY', recentValue: 1545.60, alert: 'SHORT', signalDt: '2025-12-25 15:04:33', status: 'SL HIT', entry: 1580, t1: 1550, t2: 1520, t3: 1490, sl: 1610, trade: 'CLOSED', exit: 1612.50 },
  { id: 5, strategy: 'SWING-2', timeplay: 'POSITIONAL', symbol: 'ICICIBANK', recentValue: 1125.40, alert: 'LONG', signalDt: '2025-12-22 15:04:33', status: 'T3 HIT', entry: 1050, t1: 1080, t2: 1110, t3: 1140, sl: 1020, trade: 'CLOSED', exit: 1142.30 },
  { id: 6, strategy: 'POSITIONAL-1', timeplay: 'POSITIONAL', symbol: 'SBIN', recentValue: 812.35, alert: 'LONG', signalDt: '2025-12-20 15:04:31', status: 'ACTIVE', entry: 790, t1: 820, t2: 850, t3: 880, sl: 760, trade: 'OPEN', exit: 0 },
  { id: 7, strategy: 'SWING-1', timeplay: 'POSITIONAL', symbol: 'BHARTIARTL', recentValue: 1678.90, alert: 'LONG', signalDt: '2025-12-18 15:04:34', status: 'T1 HIT', entry: 1620, t1: 1670, t2: 1720, t3: 1770, sl: 1570, trade: 'OPEN', exit: 0 },
  { id: 8, strategy: 'POSITIONAL-2', timeplay: 'POSITIONAL', symbol: 'KOTAKBANK', recentValue: 1845.20, alert: 'SHORT', signalDt: '2025-12-15 15:04:36', status: 'ACTIVE', entry: 1880, t1: 1840, t2: 1800, t3: 1760, sl: 1920, trade: 'OPEN', exit: 0 },
])

const getStatusColor = (status) => {
  switch(status) {
    case 'T1 HIT': case 'T2 HIT': case 'T3 HIT': return 'success'
    case 'ACTIVE': return 'info'
    case 'SL HIT': return 'error'
    default: return 'secondary'
  }
}

const filteredTrades = computed(() => {
  if (!searchQuery.value) return tradesData.value
  return tradesData.value.filter(t => t.symbol.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Positional Trades</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-medium-emphasis">Positional Trades</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">New trades generate everyday between 3 - 3:30pm.</p>
        </div>
      </VCardText>
    </VCard>

    <!-- Trade Type Info -->
    <VCard class="mb-4">
      <VCardText class="py-3">
        <VRow>
          <VCol cols="12" md="6">
            <p class="text-caption text-medium-emphasis mb-1">Type</p>
            <p class="text-body-1 font-weight-bold mb-0">Positional</p>
          </VCol>
          <VCol cols="12" md="6">
            <p class="text-caption text-warning mb-1">Max Trade Duration</p>
            <p class="text-body-1 font-weight-bold mb-0">15 - 30 Days</p>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Select your preferred index from the filters</p>
            <p class="mb-1">2. Monitor positional trade signals for swing trading</p>
            <p class="mb-1">3. Track targets (T1, T2, T3) and stop loss levels</p>
            <p class="mb-0">4. Hold positions for 15-30 days as per trade signals</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Filters -->
    <VCard class="mb-4">
      <VCardTitle class="py-2">Positional Trades Filter</VCardTitle>
      <VCardText>
        <div class="d-flex align-center justify-end flex-wrap gap-4">
          <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 140px" />
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Open Trades</span>
            <VSwitch v-model="openTrades" hide-details density="compact" color="primary" />
          </div>
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Non Curated</span>
            <VSwitch v-model="nonCurated" hide-details density="compact" />
          </div>
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Curated</span>
            <VSwitch v-model="curated" hide-details density="compact" color="info" />
          </div>
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Supercurated</span>
            <VSwitch v-model="supercurated" hide-details density="compact" color="success" />
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Results -->
    <VCard>
      <VCardTitle class="d-flex align-center justify-space-between py-2 flex-wrap gap-2">
        <span class="text-body-1 font-weight-medium">Positional Trades Results</span>
        <div class="d-flex align-center gap-1 flex-wrap">
          <VBtn color="error" variant="flat" size="x-small">CASH</VBtn>
          <VBtn color="error" variant="flat" size="x-small">FNO</VBtn>
          <VBtn color="warning" variant="outlined" size="x-small">CASH</VBtn>
          <VBtn color="success" variant="flat" size="x-small">FNO</VBtn>
          <VBtn variant="outlined" size="x-small">CASH</VBtn>
          <VBtn variant="outlined" size="x-small">F&O</VBtn>
          <VBtn color="info" variant="flat" size="x-small">CASH</VBtn>
          <VBtn color="primary" variant="flat" size="x-small">FO</VBtn>
        </div>
      </VCardTitle>
      <VCardText>
        <div class="d-flex align-center justify-space-between flex-wrap gap-4 mb-4">
          <VTextField v-model="searchQuery" placeholder="Search..." density="compact" hide-details prepend-inner-icon="tabler-search" style="width: 150px" />
          <div class="d-flex align-center gap-2 flex-wrap">
            <span class="text-caption">Auto Refresh</span>
            <VSwitch v-model="autoRefresh" hide-details density="compact" color="primary" />
            <VBtn color="primary" variant="outlined" size="small">Trading View Charts</VBtn>
            <VBtn color="info" variant="outlined" size="small">Watchlist</VBtn>
            <VBtn color="warning" variant="outlined" size="small">Add to My Trades</VBtn>
          </div>
        </div>

        <div class="table-responsive">
          <VTable density="compact" class="trades-table">
            <thead>
              <tr>
                <th style="width: 30px"><VCheckbox hide-details density="compact" /></th>
                <th>STRATEGY</th>
                <th>TIMEPLAY</th>
                <th>SYMBOL</th>
                <th>RECENT VALUE</th>
                <th>ALERT</th>
                <th>SIGNAL DT <VIcon icon="tabler-arrow-down" size="10" /></th>
                <th>STATUS</th>
                <th>ENTRY</th>
                <th>T1</th>
                <th>T2</th>
                <th>T3</th>
                <th>SL</th>
                <th>TRADE</th>
                <th>EXIT</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trade in filteredTrades" :key="trade.id">
                <td><VCheckbox v-model="selectedTrades" :value="trade.id" hide-details density="compact" /></td>
                <td>{{ trade.strategy }}</td>
                <td>{{ trade.timeplay }}</td>
                <td><a href="#" class="text-warning font-weight-medium">{{ trade.symbol }}</a></td>
                <td><VChip color="info" size="x-small" variant="flat">{{ trade.recentValue }}</VChip></td>
                <td><span :class="trade.alert === 'LONG' ? 'text-info' : 'text-error'" class="font-weight-medium">{{ trade.alert }}</span></td>
                <td class="text-caption">{{ trade.signalDt }}</td>
                <td><span :class="getStatusColor(trade.status) === 'success' ? 'text-success' : getStatusColor(trade.status) === 'error' ? 'text-error' : 'text-info'">{{ trade.status }}</span></td>
                <td>{{ trade.entry }}</td>
                <td>{{ trade.t1 }}</td>
                <td>{{ trade.t2 }}</td>
                <td>{{ trade.t3 }}</td>
                <td>{{ trade.sl }}</td>
                <td><span :class="trade.trade === 'OPEN' ? 'text-success' : ''">{{ trade.trade }}</span></td>
                <td :class="trade.exit > 0 ? 'text-error' : ''">{{ trade.exit || 0 }}</td>
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
            <VBtn v-for="page in totalPages" :key="page" :color="currentPage === page ? 'primary' : 'default'" :variant="currentPage === page ? 'flat' : 'text'" size="x-small" min-width="24" @click="currentPage = page">{{ page }}</VBtn>
            <VBtn icon variant="text" size="x-small" :disabled="currentPage === totalPages" @click="currentPage++">
              <VIcon icon="tabler-chevron-right" size="14" />
            </VBtn>
          </div>
          <div class="d-flex align-center gap-2">
            <VSelect v-model="itemsPerPage" :items="[10, 20, 50]" density="compact" hide-details style="width: 60px" />
            <span class="text-caption text-medium-emphasis">Displaying 1 - 10 of {{ totalItems }} records</span>
          </div>
        </div>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.trades-table th { font-size: 9px !important; font-weight: 600; white-space: nowrap; background-color: rgb(var(--v-theme-surface)); }
.trades-table td { font-size: 10px !important; white-space: nowrap; padding: 6px 4px !important; }
.table-responsive { overflow-x: auto; }
.trades-table { min-width: 1200px; }
</style>
