<script setup>
const lastRefreshTime = ref('2026-01-02 15:32:21')

// Filters
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']
const openTrades = ref(false)
const autoRefresh = ref(false)

// Search & Pagination
const searchQuery = ref('')
const selectedTrades = ref([])
const currentPage = ref(1)
const itemsPerPage = ref(10)
const totalItems = ref(89)

// Trades data
const tradesData = ref([
  { id: 1, strategy: 'DWAN', timeplay: 'INTRADAY', symbol: 'COFPM', recentValue: 2634, alert: 'SHORT', entry: 2632.6, signalDt: '2026-01-02 12:29:09', sl: 2654, status: 'EQT', t1: 2608, t2: 2603.1, t3: 2597.3, trade: 'CLOSED', exit: 2081.4, updateDt: '2026-01-02 14:16:31', summary: 'success' },
  { id: 2, strategy: 'REVERSAL-4', timeplay: 'INTRADAY', symbol: 'MAXHEALTH', recentValue: 1062.8, alert: 'LONG', entry: 1050.9, signalDt: '2026-01-02 10:03:21', sl: 1041.8, status: 'EQT', t1: 1070.9, t2: 1081.5, t3: 1092.1, trade: 'CLOSED', exit: 10621, updateDt: '2026-01-02 14:45:31', summary: 'success' },
  { id: 3, strategy: 'REVERSAL-3', timeplay: 'OVERNIGHT', symbol: 'IIH', recentValue: 672.8, alert: 'SHORT', entry: 635.2, signalDt: '2026-01-02 INTRA01', sl: 673.8, status: 'SL HIT', t1: 628, t2: 623.3, t3: 621.4, trade: 'CLOSED', exit: 643.8, updateDt: '2026-01-02 12:10:03', summary: 'error' },
  { id: 4, strategy: 'BREAKOUT-1', timeplay: 'INTRADAY', symbol: 'HEROMOTOCO', recentValue: 5890, alert: 'LONG', entry: 5964, signalDt: '2026-01-02 10:42:06', sl: 5876, status: 'EQT', t1: 6002.8, t2: 6055.5, t3: 6115.2, trade: 'CLOSED', exit: 5928, updateDt: '2026-01-02 14:45:31', summary: 'neutral' },
  { id: 5, strategy: 'BREAKOUT-1', timeplay: 'INTRADAY', symbol: 'JSWENERGY', recentValue: 510.6, alert: 'LONG', entry: 506.5, signalDt: '2026-01-02 10:37:31', sl: 504.5, status: 'T1 HIT', t1: 513.6, t2: 517.4, t3: 522.4, trade: 'CLOSED', exit: 513.5, updateDt: '2026-01-02 11:23:52', summary: 'success' },
  { id: 6, strategy: 'REVERSAL-4', timeplay: 'INTRADAY', symbol: 'PPLPHARMA', recentValue: 178.05, alert: 'LONG', entry: 171.8, signalDt: '2026-01-02 10:32:07', sl: 168.2, status: 'T3 HIT', t1: 173.6, t2: 175.3, t3: 177, trade: 'CLOSED', exit: 177, updateDt: '2026-01-02 11:56:15', summary: 'success' },
  { id: 7, strategy: 'REVERSAL-4', timeplay: 'INTRADAY', symbol: 'PAYTM', recentValue: 1338.2, alert: 'LONG', entry: 1308.7, signalDt: '2026-01-02 09:53:46', sl: 1281.6, status: 'T2 HIT', t1: 1321.8, t2: 1334.9, t3: 1348, trade: 'CLOSED', exit: 1334.9, updateDt: '2026-01-02 13:40:52', summary: 'success' },
  { id: 8, strategy: 'REVERSAL-4', timeplay: 'INTRADAY', symbol: 'SAIL', recentValue: 147.35, alert: 'SHORT', entry: 147, signalDt: '2026-01-02 08:29:10', sl: 151.5, status: 'EQT', t1: 145.5, t2: 144.1, t3: 142.6, trade: 'CLOSED', exit: 147.5, updateDt: '2026-01-02 14:45:31', summary: 'neutral' },
])

const getStatusColor = (status) => {
  switch(status) {
    case 'T1 HIT': case 'T2 HIT': case 'T3 HIT': return 'success'
    case 'EQT': return 'info'
    case 'SL HIT': return 'error'
    default: return 'secondary'
  }
}

const getAlertColor = (alert) => alert === 'LONG' ? 'info' : 'error'

const getSummaryColor = (summary) => {
  switch(summary) {
    case 'success': return 'success'
    case 'error': return 'error'
    default: return 'grey'
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
          <h4 class="text-h5 font-weight-bold">Intraday Trades</h4>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-warning">Intraday Trader</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">Using realtime data</p>
          <p class="text-caption text-medium-emphasis mb-0">To get insights of all strategy used here please refer HOW TO USE section below.</p>
        </div>
      </VCardText>
    </VCard>

    <!-- Trade Type Info -->
    <VCard class="mb-4">
      <VCardText class="py-3">
        <VRow>
          <VCol cols="12" md="6">
            <p class="text-caption text-medium-emphasis mb-1">Type</p>
            <p class="text-error text-body-1 font-weight-bold mb-0">Intraday/Overnight</p>
          </VCol>
          <VCol cols="12" md="6">
            <p class="text-caption text-warning mb-1">Max Trade Duration</p>
            <p class="text-body-1 font-weight-bold mb-0">2.5/5 Hours</p>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle class="text-error">How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Select your preferred index from the filters</p>
            <p class="mb-1">2. Monitor intraday trade signals with entry and exit points</p>
            <p class="mb-1">3. Track targets (T1, T2, T3) and stop loss levels</p>
            <p class="mb-0">4. Square off all positions before market close</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Filters -->
    <VCard class="mb-4">
      <VCardTitle class="py-2">Intraday Trades Filters</VCardTitle>
      <VCardText>
        <div class="d-flex align-center justify-end flex-wrap gap-4">
          <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 140px" />
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Open Trades</span>
            <VSwitch v-model="openTrades" hide-details density="compact" color="primary" />
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Results -->
    <VCard>
      <VCardTitle class="d-flex align-center justify-space-between py-2 flex-wrap gap-2">
        <span class="text-body-1 font-weight-medium">Intraday Trades Results</span>
        <div class="d-flex align-center gap-1 flex-wrap">
          <VBtn color="error" variant="flat" size="x-small">CASH</VBtn>
          <VBtn color="error" variant="flat" size="x-small">FNO</VBtn>
          <VBtn color="warning" variant="outlined" size="x-small">LONG</VBtn>
          <VBtn color="success" variant="flat" size="x-small">PRT</VBtn>
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
                <th>ENTRY</th>
                <th>SIGNAL DT <VIcon icon="tabler-arrow-down" size="10" /></th>
                <th>SL</th>
                <th>STATUS</th>
                <th>T1</th>
                <th>T2</th>
                <th>T3</th>
                <th>TRADE</th>
                <th>EXIT</th>
                <th>UPDATE DT</th>
                <th>SUMMARY 30MIN/1224</th>
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
                <td>{{ trade.entry }}</td>
                <td class="text-caption">{{ trade.signalDt }}</td>
                <td>{{ trade.sl }}</td>
                <td><span :class="getStatusColor(trade.status) === 'success' ? 'text-success' : getStatusColor(trade.status) === 'error' ? 'text-error' : 'text-info'">{{ trade.status }}</span></td>
                <td>{{ trade.t1 }}</td>
                <td>{{ trade.t2 }}</td>
                <td>{{ trade.t3 }}</td>
                <td>{{ trade.trade }}</td>
                <td>{{ trade.exit }}</td>
                <td class="text-error text-caption">{{ trade.updateDt }}</td>
                <td class="text-center">
                  <div class="d-flex gap-1 justify-center">
                    <VIcon :icon="trade.summary === 'success' ? 'tabler-circle-filled' : 'tabler-circle'" :color="getSummaryColor(trade.summary)" size="10" />
                    <VIcon icon="tabler-circle" color="grey" size="10" />
                    <VIcon icon="tabler-circle-filled" color="success" size="10" />
                  </div>
                </td>
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
            <VBtn v-for="page in Math.min(6, totalPages)" :key="page" :color="currentPage === page ? 'primary' : 'default'" :variant="currentPage === page ? 'flat' : 'text'" size="x-small" min-width="24" @click="currentPage = page">{{ page }}</VBtn>
            <span v-if="totalPages > 6" class="mx-1">...</span>
            <VBtn v-if="totalPages > 6" variant="text" size="x-small" min-width="24" @click="currentPage = totalPages">{{ totalPages }}</VBtn>
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
.trades-table { min-width: 1400px; }
</style>
