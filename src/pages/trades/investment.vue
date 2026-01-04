<script setup>
const lastRefreshTime = ref('2026-01-02 16:16:01')

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
const totalItems = ref(42)

// Trades data
const tradesData = ref([
  { id: 1, strategy: 'INVEST-1', timeplay: 'INVEST', symbol: 'WIPRO', recentValue: 268.75, alert: 'LONG', signalDt: '2026-01-02 15:06:18', status: 'ACTIVE', entry: 268.7, t1: 288.6, t2: 300.3, t3: 304.7, sl: 543.1, trade: 'OPEN', exit: 0 },
  { id: 2, strategy: 'INVEST-1', timeplay: 'INVEST', symbol: 'MARICO', recentValue: 757, alert: 'LONG', signalDt: '2026-01-02 15:10:16', status: 'ACTIVE', entry: 756.6, t1: 812.3, t2: 849.4, t3: 842.4, sl: 688.6, trade: 'OPEN', exit: 0 },
  { id: 3, strategy: 'INVEST-1', timeplay: 'INVEST', symbol: 'IRIG ***', recentValue: 190.5, alert: 'LONG', signalDt: '2025-12-30 15:00:14', status: 'ACTIVE', entry: 193.1, t1: 147, t2: 18.9, t3: 185.8, sl: 185.4, trade: 'OPEN', exit: 0 },
  { id: 4, strategy: 'INVEST-1', timeplay: 'INVEST', symbol: 'RVNL ***', recentValue: 305.85, alert: 'LONG', signalDt: '2025-12-26 15:10:14', status: 'ACTIVE', entry: 305.2, t1: 414.1, t2: 418, t3: 472.8, sl: 227.5, trade: 'OPEN', exit: 0 },
  { id: 5, strategy: 'INVEST-1', timeplay: 'INVEST', symbol: 'NHMO ***', recentValue: 84.46, alert: 'LONG', signalDt: '2025-12-26 15:00:14', status: 'ACTIVE', entry: 82.6, t1: 68.6, t2: 95, t3: 26.8, sl: 72.4, trade: 'OPEN', exit: 0 },
  { id: 6, strategy: 'INVEST-1', timeplay: 'INVEST', symbol: 'TCS ***', recentValue: 3252.7, alert: 'LONG', signalDt: '2025-12-19 15:10:15', status: 'ACTIVE', entry: 3291.4, t1: 8538.3, t2: 3706.2, t3: 3709.2, sl: 2995.1, trade: 'OPEN', exit: 0 },
  { id: 7, strategy: 'INVEST-1', timeplay: 'INVEST', symbol: 'HINDZINC', recentValue: 637.8, alert: 'LONG', signalDt: '2025-12-12 15:10:17', status: 'T2 HIT', entry: 585, t1: 607.3, t2: 649.7, t3: 666.9, sl: 487.9, trade: 'OPEN', exit: 0 },
  { id: 8, strategy: 'INVEST-1', timeplay: 'INVEST', symbol: 'ICICIPRU ***', recentValue: 678, alert: 'LONG', signalDt: '2025-12-12 15:10:17', status: 'ACTIVE', entry: 647.1, t1: 685.6, t2: 742.2, t3: 742.2, sl: 575.2, trade: 'OPEN', exit: 0 },
  { id: 9, strategy: 'INVEST-1', timeplay: 'INVEST', symbol: 'MOTHERSON ***', recentValue: 122, alert: 'LONG', signalDt: '2025-11-28 15:10:28', status: 'ACTIVE', entry: 185.1, t1: 124.8, t2: 133.1, t3: 136.3, sl: 88.3, trade: 'OPEN', exit: 0 },
  { id: 10, strategy: 'INVEST-1', timeplay: 'INVEST', symbol: 'LTM ***', recentValue: 6072, alert: 'LONG', signalDt: '2025-11-28 15:10:28', status: 'ACTIVE', entry: 6832.5, t1: 6508.7, t2: 6984.9, t3: 7075.7, sl: 5313.1, trade: 'OPEN', exit: 0 },
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
          <VChip color="primary" variant="flat" size="small">Investments</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-medium-emphasis">Investments</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">New trades generate every Friday between 3 - 3:30pm.</p>
        </div>
      </VCardText>
    </VCard>

    <!-- Trade Type Info -->
    <VCard class="mb-4">
      <VCardText class="py-3">
        <VRow>
          <VCol cols="12" md="6">
            <p class="text-caption text-medium-emphasis mb-1">Type</p>
            <p class="text-body-1 font-weight-bold mb-0">Investment</p>
          </VCol>
          <VCol cols="12" md="6">
            <p class="text-caption text-warning mb-1">Max Trade Duration</p>
            <p class="text-body-1 font-weight-bold mb-0">12 Weeks</p>
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
            <p class="mb-1">2. Monitor investment signals for long-term holdings</p>
            <p class="mb-1">3. Track targets (T1, T2, T3) and stop loss levels</p>
            <p class="mb-0">4. Hold positions for up to 12 weeks as per investment signals</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Filters -->
    <VCard class="mb-4">
      <VCardTitle class="py-2">Investment Trades Filter</VCardTitle>
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
        <span class="text-body-1 font-weight-medium">Investments Trades Results</span>
        <div class="d-flex align-center gap-1 flex-wrap">
          <VBtn color="error" variant="flat" size="x-small">CASH</VBtn>
          <VBtn color="error" variant="flat" size="x-small">FNO</VBtn>
          <VBtn color="warning" variant="outlined" size="x-small">CASH</VBtn>
          <VBtn color="success" variant="flat" size="x-small">FNO</VBtn>
          <VBtn variant="outlined" size="x-small">T CASH</VBtn>
          <VBtn variant="outlined" size="x-small">T FNO</VBtn>
          <VBtn color="info" variant="flat" size="x-small">CASH</VBtn>
          <VBtn color="primary" variant="flat" size="x-small">FNO</VBtn>
        </div>
      </VCardTitle>
      <VCardText>
        <p class="text-caption text-medium-emphasis mb-3">*** Symbols marked in blue with 3 stars denote super curated trades which go through higher level of filtration</p>
        
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
                <td><span class="text-info font-weight-medium">{{ trade.alert }}</span></td>
                <td class="text-caption">{{ trade.signalDt }}</td>
                <td><span :class="getStatusColor(trade.status) === 'success' ? 'text-success' : getStatusColor(trade.status) === 'error' ? 'text-error' : 'text-info'">{{ trade.status }}</span></td>
                <td>{{ trade.entry }}</td>
                <td>{{ trade.t1 }}</td>
                <td>{{ trade.t2 }}</td>
                <td>{{ trade.t3 }}</td>
                <td>{{ trade.sl }}</td>
                <td><span class="text-success">{{ trade.trade }}</span></td>
                <td>{{ trade.exit || 0 }}</td>
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
