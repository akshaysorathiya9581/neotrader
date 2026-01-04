<script setup>
import { useRealTimeStock } from '@/composables/useRealTimeStock'

// Real-time stock data from WebSocket
const { stocks, indices, isConnected, isLoading, error, lastUpdate } = useRealTimeStock()

const searchQuery = ref('')
const selectedSector = ref('ALL SECTORS')
const selectedChange = ref('LAST MIN CHANGE')
const selectedIndex = ref('NIFTY FNO')

const sectorOptions = ['ALL SECTORS', 'AUTO', 'BANK', 'CEMENT', 'CONSUMER GOODS', 'ENERGY', 'FINANCIAL SERVICES', 'FMCG', 'INDUSTRIAL MANUFACTURING', 'IT', 'METALS', 'PHARMA', 'REALTY', 'TELECOM', 'HEALTHCARE', 'INFRASTRUCTURE']
const changeOptions = ['LAST MIN CHANGE', 'DAY CHANGE', '5 MIN CHANGE', '15 MIN CHANGE']
const indexOptions = ['NIFTY FNO', 'NIFTY 50', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']

// Format stock data from WebSocket
const stockData = computed(() => {
  return stocks.value.map(s => ({
    symbol: s.symbol,
    value: s.price,
    sector: s.sector || 'OTHER',
    dayClose: s.change_percent || 0,
    dayOpen: ((s.open - s.prev_close) / s.prev_close * 100) || 0,
    lastMin: (Math.random() - 0.5) * 0.4, // Simulated for now
  }))
})

// Last refresh time
const lastRefreshTime = computed(() => {
  if (lastUpdate.value) {
    return lastUpdate.value.toLocaleString()
  }
  return new Date().toLocaleString()
})

// Filtered data
const filteredStocks = computed(() => {
  let data = stockData.value
  if (searchQuery.value) {
    data = data.filter(s => s.symbol.toLowerCase().includes(searchQuery.value.toLowerCase()))
  }
  if (selectedSector.value !== 'ALL SECTORS') {
    data = data.filter(s => s.sector === selectedSector.value)
  }
  return data
})

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)
const totalItems = computed(() => filteredStocks.value.length)
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))
const paginatedStocks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredStocks.value.slice(start, start + itemsPerPage.value)
})

const refresh = () => {
  // WebSocket auto-refreshes, this is just for manual trigger if needed
  window.location.reload()
}
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Query Window</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-primary text-caption">Query Window</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">New signals appear every 15 seconds</p>
        </div>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Use the search box to find specific stocks by symbol name</p>
            <p class="mb-1">2. Filter by sector using the dropdown to narrow down results</p>
            <p class="mb-0">3. Data refreshes automatically every 15 seconds with real-time price updates</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Query Table -->
    <VCard>
      <VCardTitle class="d-flex align-center justify-space-between py-2 flex-wrap gap-2">
        <span class="text-body-1">Query Table</span>
        <div class="text-caption text-medium-emphasis">
          Datetime = Any:2025/04/Ma Stock Acting Observe on: Open Date, Yesterday = Any:2025/03 Marker Exp. Gain Date
        </div>
      </VCardTitle>
      <VCardText>
        <!-- Filters -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-4 mb-4">
          <VTextField v-model="searchQuery" placeholder="Symbol Name" density="compact" hide-details prepend-inner-icon="tabler-search" style="width: 180px" />
          <div class="d-flex align-center gap-2 flex-wrap">
            <VSelect v-model="selectedSector" :items="sectorOptions" density="compact" hide-details style="width: 140px" />
            <VSelect v-model="selectedChange" :items="changeOptions" density="compact" hide-details style="width: 160px" />
            <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 120px" />
            <VBtn color="info" size="small" @click="refresh">Refresh</VBtn>
            <VBtn color="primary" variant="outlined" size="small">Trading View Charts</VBtn>
            <VBtn color="info" variant="outlined" size="small">Watchlist</VBtn>
          </div>
        </div>

        <!-- Table -->
        <div class="table-responsive">
          <VTable density="compact" class="query-table">
            <thead>
              <tr>
                <th><VCheckbox hide-details density="compact" /></th>
                <th class="text-warning">SYMBOL</th>
                <th>RECENT VALUE</th>
                <th>SECTOR</th>
                <th>DAY CLOSE CHG(%)</th>
                <th>DAY OPEN CHG(%)</th>
                <th>LAST 1 MIN CHG(%)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="stock in paginatedStocks" :key="stock.symbol">
                <td><VCheckbox hide-details density="compact" /></td>
                <td><a href="#" class="text-warning font-weight-medium">{{ stock.symbol }}</a></td>
                <td>{{ stock.value.toFixed(2) }}</td>
                <td><span class="text-info">{{ stock.sector }}</span></td>
                <td :class="stock.dayClose >= 0 ? 'text-success' : 'text-error'">{{ stock.dayClose >= 0 ? '' : '' }}{{ stock.dayClose.toFixed(2) }}%</td>
                <td :class="stock.dayOpen >= 0 ? 'text-success' : 'text-error'">{{ stock.dayOpen.toFixed(2) }}%</td>
                <td :class="stock.lastMin >= 0 ? 'text-success' : 'text-error'">{{ stock.lastMin.toFixed(2) }}%</td>
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
            <VBtn v-for="page in Math.min(totalPages, 6)" :key="page" :color="currentPage === page ? 'primary' : 'default'" :variant="currentPage === page ? 'flat' : 'text'" size="x-small" min-width="24" @click="currentPage = page">{{ page }}</VBtn>
            <span v-if="totalPages > 6" class="mx-1">...</span>
            <VBtn icon variant="text" size="x-small" :disabled="currentPage === totalPages" @click="currentPage++">
              <VIcon icon="tabler-chevron-right" size="14" />
            </VBtn>
          </div>
          <div class="d-flex align-center gap-2">
            <VSelect v-model="itemsPerPage" :items="[10, 20, 50]" density="compact" hide-details style="width: 60px" />
            <span class="text-caption text-medium-emphasis">Displaying {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage, totalItems) }} of {{ totalItems }} records</span>
          </div>
        </div>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.query-table th { font-size: 10px !important; font-weight: 600; white-space: nowrap; }
.query-table td { font-size: 11px !important; white-space: nowrap; padding: 8px 10px !important; }
.table-responsive { overflow-x: auto; }
</style>
