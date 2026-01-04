<script setup>
import VueApexCharts from 'vue3-apexcharts'

const lastRefreshTime = ref(new Date().toLocaleString('en-GB', { 
  year: 'numeric', month: '2-digit', day: '2-digit', 
  hour: '2-digit', minute: '2-digit', second: '2-digit' 
}))

// View tabs
const activeView = ref('sector-analysis')
const viewTabs = [
  { value: 'sector-analysis', label: 'Sector Analysis' },
  { value: 'sector-view', label: 'Sector View' },
  { value: 'market-stats', label: 'Market Stats' },
  { value: 'market-display', label: 'Market Display' },
]

// Timeframe
const timeframe = ref('Day')
const timeframeOptions = ['Day', '1 Min', '5 Min', '15 Min']
const sectorData = ref('Sector Data')

// Sector Performance Data
const sectorPerformance = ref({
  series: [{
    name: 'Change %',
    data: [3.13, 2.24, 2.47, 1.90, 1.69, 1.42, 1.56, 1.31, 1.06, 0.69, 0.81, 0.42, 0.35, 0.37, -0.47, -2.66]
  }],
  categories: ['CPSE', 'PSE', 'ENERGY', 'PSU BANK', 'COMMODITIES', 'REALTY', 'METAL', 'AUTO', 'MEDIA', 'INFRA', 'FIN SERV', 'PHARMA', 'IT', 'PVT BANK', 'CONSUMPTION', 'FMCG']
})

const sectorChartOptions = computed(() => ({
  chart: { type: 'bar', toolbar: { show: false }, height: 400 },
  plotOptions: { bar: { horizontal: true, barHeight: '70%', distributed: true } },
  colors: sectorPerformance.value.series[0].data.map(val => val >= 0 ? '#00C896' : '#FF6B6B'),
  dataLabels: { enabled: true, formatter: (val) => val.toFixed(2), style: { fontSize: '10px' } },
  xaxis: { categories: sectorPerformance.value.categories, labels: { formatter: (val) => val.toFixed(1) } },
  yaxis: { labels: { style: { fontSize: '10px' } } },
  legend: { show: false },
  grid: { borderColor: '#f1f1f1', xaxis: { lines: { show: true } } },
  tooltip: { y: { formatter: (val) => val.toFixed(2) + '%' } }
}))

// Sector tabs for stocks
const activeSector = ref('AUTO')
const sectorTabs = ['Nifty 500', 'Mid-cap', 'Nifty Total Mkt', 'Mid-Cap Select', 'Nifty 100', 'Mid-cap 100', 'Nifty 50', 'Cash Stks']

// Auto Stocks data
const autoStocks = ref([
  { symbol: 'ASHOKLEY', change: 1.85 },
  { symbol: 'BAJAJ-AUTO', change: -0.61 },
  { symbol: 'BALKRISIND', change: 2.02 },
  { symbol: 'BHARATFORG', change: 0.97 },
  { symbol: 'BOSCHLTD', change: 8.34 },
  { symbol: 'EICHERMOT', change: -0.04 },
  { symbol: 'HEROMOTOCO', change: 1.52 },
  { symbol: 'MRF', change: -0.59 },
])

// Search
const searchQuery = ref('')

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)
const totalItems = ref(15)

const filteredStocks = computed(() => {
  if (!searchQuery.value) return autoStocks.value
  return autoStocks.value.filter(s => s.symbol.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Sector View</VChip>
          <VIcon icon="tabler-home" size="18" />
          <VBreadcrumbs :items="[{ title: 'Sector Views' }, { title: 'Dashboard' }]" class="pa-0" />
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time:</p>
          <p class="text-primary text-caption mb-0">Using realtime data. Page refreshes in every 15 seconds.</p>
        </div>
      </VCardText>
    </VCard>

    <!-- View Tabs -->
    <div class="d-flex align-center justify-space-between flex-wrap gap-4 mb-4">
      <div class="d-flex gap-2">
        <VChip
          v-for="tab in viewTabs"
          :key="tab.value"
          :color="activeView === tab.value ? 'primary' : 'default'"
          :variant="activeView === tab.value ? 'flat' : 'outlined'"
          size="small"
          @click="activeView = tab.value"
        >{{ tab.label }}</VChip>
      </div>
    </div>

    <!-- Sector Performance Card -->
    <VCard class="mb-4">
      <VCardTitle class="d-flex align-center justify-space-between py-2">
        <span class="text-body-1 font-weight-medium">Sector Performance</span>
        <div class="d-flex align-center gap-2">
          <VSelect v-model="timeframe" :items="timeframeOptions" density="compact" hide-details style="width: 80px" />
          <VSelect v-model="sectorData" :items="['Sector Data']" density="compact" hide-details style="width: 120px" />
        </div>
      </VCardTitle>
      <VCardText>
        <VRow>
          <!-- Sector Chart -->
          <VCol cols="12" md="7">
            <div class="d-flex flex-wrap gap-1 mb-2">
              <VChip v-for="tab in sectorTabs" :key="tab" size="x-small" variant="text" class="text-caption">{{ tab }}</VChip>
            </div>
            <VueApexCharts type="bar" height="400" :options="sectorChartOptions" :series="sectorPerformance.series" />
          </VCol>
          
          <!-- Auto Stocks Table -->
          <VCol cols="12" md="5">
            <VCard variant="outlined">
              <VCardTitle class="bg-info text-white py-2 text-center">
                <span class="text-body-1 font-weight-bold">AUTO STOCKS</span>
              </VCardTitle>
              <VCardText class="pa-2">
                <VTextField
                  v-model="searchQuery"
                  placeholder="Search..."
                  density="compact"
                  hide-details
                  prepend-inner-icon="tabler-search"
                  class="mb-2"
                />
                <VTable density="compact">
                  <thead>
                    <tr class="bg-grey-lighten-4">
                      <th class="text-left">Symbol</th>
                      <th class="text-right">Change percentage(%)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="stock in filteredStocks" :key="stock.symbol">
                      <td>
                        <a href="#" class="text-primary">{{ stock.symbol }}</a>
                      </td>
                      <td class="text-right">
                        <span :class="stock.change >= 0 ? 'text-success' : 'text-error'">
                          {{ stock.change >= 0 ? '+' : '' }}{{ stock.change.toFixed(2) }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </VTable>
                
                <!-- Pagination -->
                <div class="d-flex align-center justify-space-between mt-2">
                  <div class="d-flex align-center gap-1">
                    <VBtn icon variant="text" size="x-small" :disabled="currentPage === 1" @click="currentPage--">
                      <VIcon icon="tabler-chevron-left" size="14" />
                    </VBtn>
                    <VBtn
                      v-for="page in totalPages"
                      :key="page"
                      :color="currentPage === page ? 'primary' : 'default'"
                      :variant="currentPage === page ? 'flat' : 'text'"
                      size="x-small"
                      min-width="24"
                      @click="currentPage = page"
                    >{{ page }}</VBtn>
                    <VBtn icon variant="text" size="x-small" :disabled="currentPage === totalPages" @click="currentPage++">
                      <VIcon icon="tabler-chevron-right" size="14" />
                    </VBtn>
                  </div>
                  <div class="d-flex align-center gap-1">
                    <VSelect v-model="itemsPerPage" :items="[5, 10, 20]" density="compact" hide-details style="width: 60px" />
                    <span class="text-caption">10 of 15 records</span>
                  </div>
                </div>
              </VCardText>
            </VCard>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.v-table th {
  font-size: 11px !important;
  font-weight: 600;
}
.v-table td {
  font-size: 12px !important;
}
</style>
