<script setup>
const lastRefreshTime = ref('2026-01-02 15:32:21')

// Filters
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'BANKNIFTY', 'FINNIFTY', 'MIDCPNIFTY']
const openTrades = ref(true)
const curated = ref(true)

// Action buttons
const autoRefresh = ref(false)

// Search
const searchQuery = ref('')

// Selected trades
const selectedTrades = ref([])

// Trades data
const tradesData = ref([
  { id: 1, strategy: 'IDX-OPT', symbol: 'NIFTY 29 JAN 06 26250 CE', alert: 'LONG', signalDt: '2025-01-02 10:02:02', status: 'TARGET', entry: 104.1, t1: 130.12, t2: 156.15, t3: 182.18, sl: 52.05, target: 'OPEN', exit: 0, updateDt: '2025-01-02 15:31:30' },
  { id: 2, strategy: 'IDX-OPT', symbol: 'NIFTY 29 JAN 06 26200 CE', alert: 'LONG', signalDt: '2025-01-02 12:33:03', status: 'LIVE', entry: 78.15, t1: 95.19, t2: 114.23, t3: 133.26, sl: 38.08, target: 'OPEN', exit: 0, updateDt: '2026-01-02 15:31:33' },
  { id: 3, strategy: 'IDX-OPT', symbol: 'BANKNIFTY 26 JAN 27 00100 CE', alert: 'LONG', signalDt: '2025-01-02 12:02:06', status: 'ACTIVE', entry: 185.05, t1: 305.31, t2: 1047.57, t3: 1536.44, sl: 102.43, target: 'OPEN', exit: 0, updateDt: '2026-01-02 12:17:05' },
  { id: 4, strategy: 'IDX-OPT', symbol: 'NIFTY 29 JAN 06 26250 CE', alert: 'LONG', signalDt: '2025-01-02 10:02:03', status: 'LIVE', entry: 90.85, t1: 113.56, t2: 136.28, t3: 158.99, sl: 45.43, target: 'OPEN', exit: 0, updateDt: '2026-01-02 12:46:51' },
])

// Get status color
const getStatusColor = (status) => {
  switch(status) {
    case 'TARGET': return 'success'
    case 'LIVE': return 'info'
    case 'ACTIVE': return 'warning'
    case 'SL HIT': return 'error'
    default: return 'secondary'
  }
}

// Filtered trades
const filteredTrades = computed(() => {
  if (!searchQuery.value) return tradesData.value
  return tradesData.value.filter(t => 
    t.symbol.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    t.strategy.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <h4 class="text-h5 font-weight-bold">Option Trades</h4>
          <VIcon icon="tabler-home" size="18" />
          <VBreadcrumbs :items="[{ title: 'Option Trades', disabled: true }]" class="pa-0" />
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">New trades generated every 30 minutes.</p>
        </div>
      </VCardText>
    </VCard>

    <!-- Trade Type Info -->
    <VCard class="mb-4">
      <VCardText class="py-3">
        <VRow>
          <VCol cols="12" md="6">
            <p class="text-caption text-medium-emphasis mb-1">Type</p>
            <p class="text-body-1 font-weight-bold mb-0">Intraday/Overnight</p>
          </VCol>
          <VCol cols="12" md="6">
            <p class="text-caption text-warning mb-1">Max Trade Duration</p>
            <p class="text-body-1 font-weight-bold mb-0">3 - 5 Days</p>
          </VCol>
        </VRow>
        <p class="text-caption text-medium-emphasis mt-2 mb-0">
          ** Note: All option trades are valid for 3 - 5 days from date of generation to final targets (T3 MT/SL HIT). It can be exited intraday if targets or stop loss levels are hit on the same day itself.
        </p>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Select your preferred index from the filters</p>
            <p class="mb-1">2. Monitor trade signals and their status</p>
            <p class="mb-1">3. Track entry, targets (T1, T2, T3) and stop loss levels</p>
            <p class="mb-0">4. Add trades to watchlist or execute via broker</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Options Trades Filters -->
    <VCard class="mb-4">
      <VCardTitle class="py-2">
        <span class="text-body-1 font-weight-medium">Options Trades Filters</span>
      </VCardTitle>
      <VCardText>
        <div class="d-flex align-center justify-end flex-wrap gap-4">
          <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 140px" />
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Open Trades</span>
            <VSwitch v-model="openTrades" hide-details density="compact" color="primary" />
          </div>
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Curated</span>
            <VSwitch v-model="curated" hide-details density="compact" color="success" />
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Options Trades Results -->
    <VCard>
      <VCardTitle class="d-flex align-center justify-space-between py-2 flex-wrap gap-2">
        <span class="text-body-1 font-weight-medium">Options Trades Results</span>
        <div class="d-flex align-center gap-2">
          <VBtn color="error" variant="flat" size="small">
            <VIcon icon="tabler-brand-telegram" size="16" class="me-1" />
            TG
          </VBtn>
          <VBtn color="success" variant="flat" size="small">FNO</VBtn>
          <VBtn color="info" variant="outlined" size="small">T'View</VBtn>
          <VBtn color="primary" variant="flat" size="small">
            <VIcon icon="tabler-brand-telegram" size="16" class="me-1" />
            TG
          </VBtn>
        </div>
      </VCardTitle>
      <VCardText>
        <!-- Search and Actions -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-4 mb-4">
          <VTextField
            v-model="searchQuery"
            placeholder="Search..."
            density="compact"
            hide-details
            prepend-inner-icon="tabler-search"
            style="width: 200px"
          />
          <div class="d-flex align-center gap-2">
            <div class="d-flex align-center gap-1">
              <span class="text-caption">Auto Refresh</span>
              <VSwitch v-model="autoRefresh" hide-details density="compact" color="primary" />
            </div>
            <VBtn color="primary" variant="outlined" size="small">Trading View Charts</VBtn>
            <VBtn color="info" variant="outlined" size="small">Watchlist</VBtn>
            <VBtn color="warning" variant="outlined" size="small">Add to My Trades</VBtn>
          </div>
        </div>

        <!-- Data Table -->
        <div class="table-responsive">
          <VTable density="compact" class="trades-table">
            <thead>
              <tr>
                <th style="width: 40px"><VCheckbox hide-details density="compact" /></th>
                <th>STRATEGY</th>
                <th>SYMBOL</th>
                <th>ALERT</th>
                <th>SIGNAL DT</th>
                <th>STATUS</th>
                <th>ENTRY</th>
                <th>T1</th>
                <th>T2</th>
                <th>T3</th>
                <th>SL</th>
                <th>TARGET</th>
                <th>EXIT</th>
                <th>UPDATE DT</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trade in filteredTrades" :key="trade.id">
                <td><VCheckbox v-model="selectedTrades" :value="trade.id" hide-details density="compact" /></td>
                <td>{{ trade.strategy }}</td>
                <td><a href="#" class="text-primary">{{ trade.symbol }}</a></td>
                <td><span class="text-info font-weight-medium">{{ trade.alert }}</span></td>
                <td class="text-caption">{{ trade.signalDt }}</td>
                <td><VChip :color="getStatusColor(trade.status)" size="x-small" variant="flat">{{ trade.status }}</VChip></td>
                <td>{{ trade.entry }}</td>
                <td>{{ trade.t1 }}</td>
                <td>{{ trade.t2 }}</td>
                <td>{{ trade.t3 }}</td>
                <td class="text-error">{{ trade.sl }}</td>
                <td><span class="text-success">{{ trade.target }}</span></td>
                <td>{{ trade.exit }}</td>
                <td class="text-caption">{{ trade.updateDt }}</td>
              </tr>
            </tbody>
          </VTable>
        </div>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.trades-table th {
  font-size: 10px !important;
  font-weight: 600;
  white-space: nowrap;
  background-color: rgb(var(--v-theme-surface));
}
.trades-table td {
  font-size: 11px !important;
  white-space: nowrap;
}
.table-responsive {
  overflow-x: auto;
}
</style>
