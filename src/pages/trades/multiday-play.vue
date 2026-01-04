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
const totalItems = ref(17)

// Trades data
const tradesData = ref([
  { id: 1, strategy: 'MOMENTUM-1', timeplay: 'MULTIDAY', symbol: 'NIFTY ***', recentValue: 26336.6, alert: 'LONG', signalDt: '2026-01-02 15:04:32', status: 'ACTIVE', entry: 26292, t1: 26768.3, t2: 26188.6, t3: 26085.5, sl: 26569.7, trade: 'OPEN', exit: 0 },
  { id: 2, strategy: 'MOMENTUM-1', timeplay: 'MULTIDAY', symbol: 'BANKNIFTY ***', recentValue: 60176.2, alert: 'LONG', signalDt: '2026-01-02 15:04:32', status: 'ACTIVE', entry: 60583.3, t1: 61039.4, t2: 61479.7, t3: 61675.2, sl: 58943.4, trade: 'OPEN', exit: 0 },
  { id: 3, strategy: 'REVERSAL-1', timeplay: 'MULTIDAY', symbol: 'HINDZINC ***', recentValue: 657.8, alert: 'SHORT', signalDt: '2026-01-01 15:04:46', status: 'ACTIVE', entry: 614, t1: 600.2, t2: 578.5, t3: 576.5, sl: 641.5, trade: 'CLOSED', exit: 0 },
  { id: 4, strategy: 'MOMENTUM-1', timeplay: 'MULTIDAY', symbol: 'BSE', recentValue: 2868, alert: 'SHORT', signalDt: '2025-12-30 15:04:33', status: 'ACTIVE', entry: 2599.8, t1: 2844, t2: 2497.3, t3: 2399, sl: 2745, trade: 'OPEN', exit: 0 },
  { id: 5, strategy: 'MOMENTUM-1', timeplay: 'MULTIDAY', symbol: 'INOXWIND ***', recentValue: 127.03, alert: 'SHORT', signalDt: '2025-12-30 15:04:33', status: 'ACTIVE', entry: 122, t1: 119.5, t2: 117.6, t3: 105.2, sl: 129.3, trade: 'OPEN', exit: 0 },
  { id: 6, strategy: 'MOMENTUM-1', timeplay: 'MULTIDAY', symbol: 'IFL ***', recentValue: 542.8, alert: 'LONG', signalDt: '2025-12-24 15:04:31', status: 'T2 HIT', entry: 502.6, t1: 511.5, t2: 521.4, t3: 552.8, sl: 538.2, trade: 'CLOSED', exit: 524.4 },
  { id: 7, strategy: 'MOMENTUM-1', timeplay: 'MULTIDAY', symbol: 'PNBHOUSING ***', recentValue: 958.25, alert: 'LONG', signalDt: '2025-12-24 15:04:34', status: 'T2 HIT', entry: 955.4, t1: 952.8, t2: 1050.2, t3: 1019.7, sl: 911, trade: 'CLOSED', exit: 11003.2 },
  { id: 8, strategy: 'MOMENTUM+', timeplay: 'MULTIDAY', symbol: 'CHOLAHFIN ***', recentValue: 1779.9, alert: 'SHORT', signalDt: '2025-12-22 15:04:36', status: 'SL HIT', entry: 1678.6, t1: 1559.2, t2: 1521.8, t3: 1488.9, sl: 1673.3, trade: 'CLOSED', exit: 1673.8 },
  { id: 9, strategy: 'MOMENTUM-1', timeplay: 'MULTIDAY', symbol: 'DIXON', recentValue: 1950, alert: 'SHORT', signalDt: '2025-12-22 15:04:36', status: 'T3 HIT', entry: 11066, t1: 12634.4, t2: 12432.8, t3: 11801.1, sl: 13636, trade: 'CLOSED', exit: 11803.1 },
  { id: 10, strategy: 'MOMENTUM+', timeplay: 'MULTIDAY', symbol: 'MCX ***', recentValue: 3990, alert: 'LONG', signalDt: '2025-12-22 15:04:36', status: 'T2 HIT', entry: 10681, t1: 11055.8, t2: 11096.5, t3: 10471.2, sl: 10508.8, trade: 'CLOSED', exit: 11090.2 },
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
          <VChip color="primary" variant="flat" size="small">Multiday Trades</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-medium-emphasis">Multiday Trades</span>
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
            <p class="text-body-1 font-weight-bold mb-0">Multiday</p>
          </VCol>
          <VCol cols="12" md="6">
            <p class="text-caption text-warning mb-1">Max Trade Duration</p>
            <p class="text-body-1 font-weight-bold mb-0">5 Days</p>
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
            <p class="mb-1">2. Monitor multiday trade signals with entry and exit points</p>
            <p class="mb-1">3. Track targets (T1, T2, T3) and stop loss levels</p>
            <p class="mb-0">4. Hold positions for up to 5 days as per trade signals</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Filters -->
    <VCard class="mb-4">
      <VCardTitle class="py-2">Multiday Trades Filter</VCardTitle>
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
        <span class="text-body-1 font-weight-medium">Multiday Trades Results</span>
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
        <p class="text-caption text-medium-emphasis mb-3">*** Symbols marked with *** stock charts appear on a separate modal via a pop through toggle week or Charts</p>
        
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
