<script setup>
const lastRefreshTime = ref(new Date().toLocaleString('en-GB', { 
  year: 'numeric', month: '2-digit', day: '2-digit', 
  hour: '2-digit', minute: '2-digit', second: '2-digit' 
}))

// Search
const searchQuery = ref('')

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(20)
const totalItems = ref(200)

// Selected stocks
const selectedStocks = ref([])

// Time slots for the table
const timeSlots = ['9:45', '10:15', '10:45', '11:15', '11:45', '12:15', '12:45', '1:15', '1:45', '2:15', '2:45', '3:15']

// Bullish stocks
const bullishStocks = ref([
  { symbol: 'KALYANKJIL', change: 1.47 }
])

// Bearish stocks
const bearishStocks = ref([])

// Stock data with trend arrows
const stocksData = ref([
  { symbol: '360ONE', recentValue: 1047, trends: ['right', 'right', 'right', 'right', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right'] },
  { symbol: 'ABB', recentValue: 5738, trends: ['right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'] },
  { symbol: 'ABCAPITAL', recentValue: 203, trends: ['up', 'right', 'down', 'right', 'right', 'right', 'right', 'right', 'down', 'right', 'right', 'up'] },
  { symbol: 'ADANIENSOL', recentValue: 1067, trends: ['right', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'down', 'right', 'right', 'right'] },
  { symbol: 'ADANIENT', recentValue: 2578, trends: ['up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'] },
  { symbol: 'ADANIGREEN', recentValue: 1068, trends: ['right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'up', 'right', 'right'] },
  { symbol: 'ADANIPORTS', recentValue: 1405, trends: ['up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'] },
  { symbol: 'ATGL', recentValue: 642, trends: ['right', 'right', 'right', 'right', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right'] },
  { symbol: 'AWL', recentValue: 315, trends: ['right', 'up', 'right', 'right', 'right', 'right', 'right', 'down', 'right', 'right', 'right', 'right'] },
  { symbol: 'ABFRL', recentValue: 287, trends: ['right', 'right', 'right', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'up', 'right'] },
])

// Get trend icon and color
const getTrendIcon = (trend) => {
  switch(trend) {
    case 'up': return 'tabler-arrow-up'
    case 'down': return 'tabler-arrow-down'
    default: return 'tabler-arrows-right-left'
  }
}

const getTrendColor = (trend) => {
  switch(trend) {
    case 'up': return 'success'
    case 'down': return 'error'
    default: return 'secondary'
  }
}

// Filtered stocks based on search
const filteredStocks = computed(() => {
  if (!searchQuery.value) return stocksData.value
  return stocksData.value.filter(stock => 
    stock.symbol.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Pagination info
const paginationInfo = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value + 1
  const end = Math.min(currentPage.value * itemsPerPage.value, totalItems.value)
  return `Displaying ${start} - ${end} of ${totalItems.value} records`
})

const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <h4 class="text-h5 font-weight-bold">Intraday Stock Trends</h4>
          <VIcon icon="tabler-home" size="18" />
          <VBreadcrumbs :items="[{ title: 'Intraday Stock Trends', disabled: true }]" class="pa-0" />
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">New signals appear every 30 minutes.</p>
        </div>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle class="bg-primary text-white">
            <span>How To Use</span>
          </VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Monitor stock trends throughout the trading day</p>
            <p class="mb-1">2. Green arrows indicate bullish movement, Red arrows indicate bearish movement</p>
            <p class="mb-1">3. Horizontal arrows indicate sideways/neutral movement</p>
            <p class="mb-0">4. Click on stock symbols to view detailed charts</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Bullish / Bearish Cards -->
    <VRow class="mb-4">
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="text-success py-2">Bullish</VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-2">
              <VChip
                v-for="stock in bullishStocks"
                :key="stock.symbol"
                color="success"
                variant="flat"
                size="small"
              >
                {{ stock.symbol }}
                <VIcon icon="tabler-arrow-up" size="14" class="ms-1" />
                {{ stock.change }}%
              </VChip>
              <span v-if="bullishStocks.length === 0" class="text-medium-emphasis">—</span>
            </div>
          </VCardText>
        </VCard>
      </VCol>
      <VCol cols="12" md="6">
        <VCard>
          <VCardTitle class="text-error py-2">Bearish</VCardTitle>
          <VCardText>
            <div class="d-flex flex-wrap gap-2">
              <VChip
                v-for="stock in bearishStocks"
                :key="stock.symbol"
                color="error"
                variant="flat"
                size="small"
              >
                {{ stock.symbol }}
                <VIcon icon="tabler-arrow-down" size="14" class="ms-1" />
                {{ stock.change }}%
              </VChip>
              <span v-if="bearishStocks.length === 0" class="text-medium-emphasis">—</span>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>

    <!-- Stock Trends Table -->
    <VCard>
      <VCardText>
        <!-- Search and Actions -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-4 mb-4">
          <div class="d-flex align-center gap-2">
            <VIcon icon="tabler-search" size="18" />
            <VTextField
              v-model="searchQuery"
              placeholder="Search..."
              density="compact"
              hide-details
              style="width: 200px"
            />
          </div>
          <div class="d-flex gap-2">
            <VBtn color="primary" variant="outlined" size="small">
              <VIcon icon="tabler-chart-line" size="16" class="me-1" />
              Trading View Charts
            </VBtn>
            <VBtn color="info" variant="outlined" size="small">
              <VIcon icon="tabler-star" size="16" class="me-1" />
              Watchlist
            </VBtn>
          </div>
        </div>

        <!-- Data Table -->
        <div class="table-responsive">
          <VTable class="trends-table" density="compact">
            <thead>
              <tr>
                <th style="width: 40px">
                  <VCheckbox hide-details density="compact" />
                </th>
                <th class="text-left">SYMBOL</th>
                <th class="text-left">RECENT VALUE</th>
                <th v-for="time in timeSlots" :key="time" class="text-center time-header">{{ time }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="stock in filteredStocks" :key="stock.symbol">
                <td>
                  <VCheckbox v-model="selectedStocks" :value="stock.symbol" hide-details density="compact" />
                </td>
                <td>
                  <a href="#" class="text-primary font-weight-medium">{{ stock.symbol }}</a>
                </td>
                <td>
                  <VChip size="small" color="info" variant="flat">{{ stock.recentValue }}</VChip>
                </td>
                <td v-for="(trend, index) in stock.trends" :key="index" class="text-center">
                  <VIcon :icon="getTrendIcon(trend)" :color="getTrendColor(trend)" size="20" />
                </td>
              </tr>
            </tbody>
          </VTable>
        </div>

        <!-- Pagination -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-4 mt-4">
          <div class="d-flex align-center gap-1">
            <VBtn icon variant="text" size="small" :disabled="currentPage === 1" @click="currentPage--">
              <VIcon icon="tabler-chevron-left" />
            </VBtn>
            <VBtn
              v-for="page in Math.min(6, totalPages)"
              :key="page"
              :color="currentPage === page ? 'primary' : 'default'"
              :variant="currentPage === page ? 'flat' : 'text'"
              size="small"
              min-width="32"
              @click="currentPage = page"
            >
              {{ page }}
            </VBtn>
            <span v-if="totalPages > 6" class="mx-1">...</span>
            <VBtn
              v-if="totalPages > 6"
              :color="currentPage === totalPages ? 'primary' : 'default'"
              :variant="currentPage === totalPages ? 'flat' : 'text'"
              size="small"
              min-width="32"
              @click="currentPage = totalPages"
            >
              {{ totalPages }}
            </VBtn>
            <VBtn icon variant="text" size="small" :disabled="currentPage === totalPages" @click="currentPage++">
              <VIcon icon="tabler-chevron-right" />
            </VBtn>
          </div>
          <div class="d-flex align-center gap-2">
            <VSelect
              v-model="itemsPerPage"
              :items="[10, 20, 50, 100]"
              density="compact"
              hide-details
              style="width: 70px"
            />
            <span class="text-caption text-medium-emphasis">{{ paginationInfo }}</span>
          </div>
        </div>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.trends-table th {
  background-color: rgb(var(--v-theme-surface));
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.trends-table td {
  font-size: 12px;
  padding: 8px 6px !important;
}

.time-header {
  min-width: 50px;
  font-size: 10px !important;
}

.table-responsive {
  overflow-x: auto;
}

.trends-table {
  min-width: 1200px;
}
</style>
