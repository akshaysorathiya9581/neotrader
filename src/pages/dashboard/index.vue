<script setup>
import VueApexCharts from 'vue3-apexcharts'

const lastRefreshTime = ref(new Date().toLocaleString('en-GB', { 
  year: 'numeric', month: '2-digit', day: '2-digit', 
  hour: '2-digit', minute: '2-digit', second: '2-digit' 
}))
const refreshInterval = ref(null)

// Dashboard tabs
const activeTab = ref('heatmap')

// Active Stocks tabs
const activeStockTab = ref('all')
const stockTabs = [
  { value: 'all', label: 'All Stocks' },
  { value: 'fno', label: 'FNO Stocks' },
  { value: 'cash', label: 'Cash Stocks' },
  { value: 'indices', label: 'Indices/Index' },
  { value: 'midcap', label: 'Midcap/Amber' },
]

// Sort options
const sortBy = ref('AGING')
const sortOptions = ['AGING', 'CHANGE', 'VOLUME']
const timeFrame = ref('Day')
const timeFrameOptions = ['Day', '1 Min', '5 Min', '15 Min']
const ageMovement = ref(true)
const curated = ref(false)

// Market Indices Data
const indicesData = ref({
  series: [{
    name: 'Change %',
    data: [1.2, 1.0, 0.9, 0.8, 0.7, 0.5, 0.3, 0.2]
  }],
  categories: ['NIFTY', 'NIFTY MIDCAP 100', 'NIFTY FIN SVC', 'BANKNIFTY', 'NIFTY IT', 'NIFTY FMCG', 'SENSEX', 'NIFTY PSE']
})

const indicesChartOptions = computed(() => ({
  chart: { type: 'bar', toolbar: { show: false }, height: 250 },
  plotOptions: { bar: { horizontal: true, barHeight: '60%', distributed: true } },
  colors: indicesData.value.series[0].data.map(val => val >= 0 ? '#00C896' : '#FF6B6B'),
  dataLabels: { enabled: false },
  xaxis: { categories: indicesData.value.categories },
  yaxis: { labels: { style: { fontSize: '10px' } } },
  legend: { show: false },
  grid: { borderColor: '#f1f1f1' }
}))

// Sector Performance Data
const sectorData = ref({
  series: [{
    name: 'Change %',
    data: [1.5, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, -0.1, -0.2, -0.4, -0.6]
  }],
  categories: ['NIFTY AUTO', 'NIFTY FMCG', 'NIFTY INFRA', 'NIFTY PSU BANK', 'NIFTY IT', 'NIFTY METAL', 'NIFTY PHARMA', 'NIFTY REALTY', 'NIFTY MEDIA', 'NIFTY CPSE', 'NIFTY PSE', 'NIFTY DEFENCE']
})

const sectorChartOptions = computed(() => ({
  chart: { type: 'bar', toolbar: { show: false }, height: 250 },
  plotOptions: { bar: { horizontal: true, barHeight: '50%', distributed: true } },
  colors: sectorData.value.series[0].data.map(val => val >= 0 ? '#00C896' : '#FF6B6B'),
  dataLabels: { enabled: false },
  xaxis: { categories: sectorData.value.categories },
  yaxis: { labels: { style: { fontSize: '9px' } } },
  legend: { show: false },
  grid: { borderColor: '#f1f1f1' }
}))

// Advance/Decline Data
const advanceDeclineData = ref({
  series: [892, 412, 196],
  labels: ['Advance', 'Decline', 'Unchanged']
})

const advanceDeclineOptions = computed(() => ({
  chart: { type: 'donut', height: 250 },
  labels: advanceDeclineData.value.labels,
  colors: ['#00C896', '#FF6B6B', '#FFC107'],
  legend: { position: 'right', fontSize: '11px' },
  plotOptions: {
    pie: {
      donut: {
        size: '65%',
        labels: { show: true, total: { show: true, label: 'Total', formatter: () => '1500' } }
      }
    }
  },
  dataLabels: { enabled: false }
}))

// Active Stocks Data
const activeStocks = ref([
  { symbol: 'HUDCO', rank: 5, change: 1.72, rating: 4, positive: true },
  { symbol: 'GODREJCP', rank: 7, change: -0.5, rating: 3, positive: false },
  { symbol: 'HINDALCO', rank: 7, change: 0.5, rating: 3, positive: true },
  { symbol: 'NTPC', rank: 8, change: 0.04, rating: 3, positive: true },
  { symbol: 'ADANIENT', rank: 8, change: 1.08, rating: 4, positive: true },
  { symbol: 'SHRIRAMFIN', rank: 5, change: 0.05, rating: 3, positive: true },
  { symbol: 'INDIAMART', rank: 4, change: 0.55, rating: 4, positive: true },
  { symbol: 'ASHOKEY', rank: 4, change: 1.05, rating: 3, positive: true },
  { symbol: 'JSWSTEEL', rank: 4, change: 1.02, rating: 3, positive: true },
  { symbol: 'IRCTC', rank: 4, change: 0.07, rating: 3, positive: true },
  { symbol: 'ICICIPRULI', rank: 4, change: 0.65, rating: 3, positive: true },
  { symbol: 'TATASTEEL', rank: 6, change: 0.5, rating: 4, positive: true },
  { symbol: 'SAIL', rank: 1, change: -0.76, rating: 2, positive: false },
  { symbol: 'NHPC', rank: 3, change: 0.35, rating: 3, positive: true },
  { symbol: 'IEL', rank: 3, change: 0.8, rating: 4, positive: true },
  { symbol: 'CHOLAFIN', rank: 5, change: 0.24, rating: 4, positive: true },
  { symbol: 'UNIONBK', rank: 3, change: 2.74, rating: 3, positive: true },
  { symbol: 'UNIONBANK', rank: 5, change: 2.2, rating: 4, positive: true },
  { symbol: 'SBIN', rank: 5, change: 2.12, rating: 4, positive: true },
  { symbol: 'BANKBARODA', rank: 3, change: 1.78, rating: 3, positive: true },
  { symbol: 'HEROMOTOCO', rank: 5, change: 1.02, rating: 3, positive: true },
  { symbol: 'MRF', rank: 8, change: 1.48, rating: 3, positive: true },
  { symbol: 'MARUTI', rank: 3, change: 1.47, rating: 3, positive: true },
  { symbol: 'MHINDRA', rank: 3, change: 1.06, rating: 4, positive: true },
  { symbol: 'HINDALIVE', rank: 3, change: 0.85, rating: 3, positive: true },
  { symbol: 'MSUMI', rank: 3, change: 1.08, rating: 4, positive: true },
  { symbol: 'PETRONET', rank: 3, change: 1.68, rating: 3, positive: true },
  { symbol: 'BANKBEES', rank: 5, change: 0.78, rating: 3, positive: true },
  { symbol: 'LTI', rank: 3, change: 0.92, rating: 4, positive: true },
  { symbol: 'CUMMINS', rank: 3, change: 0.38, rating: 3, positive: true },
])

// Heatmap Stocks Data
const heatmapStocks = ref([
  { symbol: 'BOSCHLTD', change: 8.24, positive: true },
  { symbol: 'COALINDIA', change: 7.71, positive: true },
  { symbol: 'TORNTPOWER', change: 5.57, positive: true },
  { symbol: 'NRDA', change: 5.48, positive: true },
  { symbol: 'NHPC', change: 5.19, positive: true },
  { symbol: 'DABUR', change: 5.04, positive: true },
  { symbol: 'PPLPHARMA', change: 4.82, positive: true },
  { symbol: 'NATIONALAM', change: 4.74, positive: true },
  { symbol: 'NTPC', change: 4.84, positive: true },
  { symbol: 'INOXWIND', change: 4.65, positive: true },
  { symbol: 'PGEL', change: 3.94, positive: true },
  { symbol: 'YESBANK', change: 3.91, positive: true },
  { symbol: 'RECLTD', change: 3.89, positive: true },
  { symbol: 'PAYTM', change: 3.80, positive: true },
  { symbol: 'IFL', change: 3.60, positive: true },
  { symbol: 'INDIAGRN', change: 3.58, positive: true },
  { symbol: 'HINDALCO', change: 3.50, positive: true },
  { symbol: 'SUZLON', change: 3.49, positive: true },
  { symbol: 'PFC', change: 3.48, positive: true },
  { symbol: 'VOLTAS', change: 3.28, positive: true },
  { symbol: 'CHOLAFIN', change: 3.24, positive: true },
  { symbol: 'TATACHEM', change: 3.07, positive: true },
  { symbol: 'GAIL', change: 2.96, positive: true },
  { symbol: 'BHEL', change: 2.76, positive: true },
  { symbol: 'UNIONBRA', change: 2.74, positive: true },
  { symbol: 'SBIMANICAP', change: 2.74, positive: true },
  { symbol: 'TATAPOWER', change: 2.72, positive: true },
  { symbol: 'GODREJAGRO', change: 2.65, positive: true },
  { symbol: 'SONACOMS', change: 2.60, positive: true },
  { symbol: 'MINDTEC', change: 2.59, positive: true },
  { symbol: 'NMMT', change: 2.48, positive: true },
  { symbol: 'VRAJ', change: 2.33, positive: true },
  { symbol: 'KALYAN', change: 2.33, positive: true },
  { symbol: 'SBIN', change: 2.12, positive: true },
  { symbol: 'BANKBARODA', change: 1.78, positive: true },
  { symbol: 'PNB', change: 1.65, positive: true },
  { symbol: 'CANBK', change: 1.52, positive: true },
  { symbol: 'IOB', change: 1.48, positive: true },
  { symbol: 'INDIANB', change: 1.45, positive: true },
  { symbol: 'UCOBANK', change: 1.42, positive: true },
  { symbol: 'CENTRALBK', change: 1.38, positive: true },
  { symbol: 'BANDHANBNK', change: 1.35, positive: true },
  { symbol: 'IDFCFIRSTB', change: 1.32, positive: true },
  { symbol: 'FEDERALBNK', change: 1.28, positive: true },
  { symbol: 'HEROMOTOCO', change: 1.25, positive: true },
  { symbol: 'BAJAJ-AUTO', change: 1.22, positive: true },
  { symbol: 'EICHERMOT', change: 1.18, positive: true },
  { symbol: 'TVSMOTOR', change: 1.15, positive: true },
  { symbol: 'ASHOKLEY', change: 1.12, positive: true },
  { symbol: 'BHARATFORG', change: 1.08, positive: true },
  { symbol: 'MOTHERSON', change: 1.05, positive: true },
  { symbol: 'BALKRISIND', change: 1.02, positive: true },
  { symbol: 'EXIDEIND', change: 0.98, positive: true },
  { symbol: 'AMARAJABAT', change: 0.95, positive: true },
  { symbol: 'APOLLOTYRE', change: 0.92, positive: true },
  { symbol: 'RELIANCE', change: 0.85, positive: true },
  { symbol: 'TCS', change: 0.78, positive: true },
  { symbol: 'INFY', change: 0.72, positive: true },
  { symbol: 'HDFCBANK', change: 0.65, positive: true },
  { symbol: 'ICICIBANK', change: 0.58, positive: true },
  { symbol: 'KOTAKBANK', change: 0.52, positive: true },
  { symbol: 'WIPRO', change: 0.45, positive: true },
  { symbol: 'HCLTECH', change: 0.38, positive: true },
  { symbol: 'TECHM', change: 0.32, positive: true },
  { symbol: 'LT', change: 0.25, positive: true },
  { symbol: 'AXISBANK', change: 0.18, positive: true },
  { symbol: 'ADANIGREEN', change: -0.15, positive: false },
  { symbol: 'ADANIPORTS', change: -0.22, positive: false },
  { symbol: 'ADANIENT', change: -0.28, positive: false },
  { symbol: 'AMBUJACEM', change: -0.35, positive: false },
  { symbol: 'ACC', change: -0.42, positive: false },
  { symbol: 'ULTRACEMCO', change: -0.48, positive: false },
  { symbol: 'SHREECEM', change: -0.55, positive: false },
  { symbol: 'GRASIM', change: -0.62, positive: false },
  { symbol: 'AUROPHARMA', change: -0.68, positive: false },
  { symbol: 'CIPLA', change: -0.75, positive: false },
  { symbol: 'DRREDDY', change: -0.82, positive: false },
  { symbol: 'SUNPHARMA', change: -0.88, positive: false },
  { symbol: 'DIVISLAB', change: -0.95, positive: false },
  { symbol: 'BIOCON', change: -1.02, positive: false },
  { symbol: 'LUPIN', change: -1.08, positive: false },
  { symbol: 'ALKEM', change: -1.15, positive: false },
  { symbol: 'TORNTPHARMA', change: -1.22, positive: false },
  { symbol: 'ZYDUSLIFE', change: -1.28, positive: false },
  { symbol: 'GLENMARK', change: -1.35, positive: false },
  { symbol: 'IPCALAB', change: -1.42, positive: false },
  { symbol: 'NATCOPHARM', change: -1.48, positive: false },
  { symbol: 'LAURUSLABS', change: -1.55, positive: false },
])

// Refresh data function
const refreshData = () => {
  lastRefreshTime.value = new Date().toLocaleString('en-GB', { 
    year: 'numeric', month: '2-digit', day: '2-digit', 
    hour: '2-digit', minute: '2-digit', second: '2-digit' 
  })
}

onMounted(() => {
  refreshInterval.value = setInterval(refreshData, 15000)
})

onUnmounted(() => {
  if (refreshInterval.value) clearInterval(refreshInterval.value)
})

// Dashboard Universe
const selectedIndex = ref('NIFTY 100')
const indexOptions = ['NIFTY 50', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']
const selectedTimeframe = ref('Close')
const timeframeOptions = ['Close', '1 Min', '5 Min', '15 Min']
</script>

<template>
  <div>
    <!-- Dashboard Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div>
          <h4 class="text-h5 font-weight-bold mb-2">Dashboard</h4>
          <div class="d-flex gap-2">
            <VChip :color="activeTab === 'heatmap' ? 'primary' : 'default'" :variant="activeTab === 'heatmap' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'heatmap'">Heatmap</VChip>
            <VChip :color="activeTab === 'market' ? 'primary' : 'default'" :variant="activeTab === 'market' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'market'">Market View</VChip>
            <VChip :color="activeTab === 'nifty' ? 'primary' : 'default'" :variant="activeTab === 'nifty' ? 'flat' : 'outlined'" size="small" @click="activeTab = 'nifty'">Nifty Tour</VChip>
          </div>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">Using realtime data. Page refreshes every 15 seconds.</p>
        </div>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Select your preferred index from Dashboard Universe</p>
            <p class="mb-1">2. Choose timeframe for analysis</p>
            <p class="mb-1">3. Monitor real-time market data through charts</p>
            <p class="mb-0">4. Click on stock cards to view detailed analysis</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Dashboard Universe -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center gap-4 flex-wrap">
          <div class="d-flex align-center gap-2">
            <VIcon icon="tabler-chart-bar" size="20" />
            <span class="font-weight-medium">Dashboard Universe</span>
          </div>
          <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 120px" />
          <VSelect v-model="selectedTimeframe" :items="timeframeOptions" density="compact" hide-details style="width: 100px" />
          <VSpacer />
          <div class="text-caption">
            <span class="text-success">Advance = NIFTY 100 based on Cash Data</span> | 
            <span class="text-warning">Advance = NIFTYEW based on Cash Data</span>
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Charts Row -->
    <VRow class="mb-4">
      <VCol cols="12" md="4">
        <VCard>
          <VCardTitle class="text-body-1 font-weight-medium py-2">Broad Market Indices</VCardTitle>
          <VCardText class="pa-2">
            <VueApexCharts type="bar" height="220" :options="indicesChartOptions" :series="indicesData.series" />
          </VCardText>
        </VCard>
      </VCol>
      <VCol cols="12" md="4">
        <VCard>
          <VCardTitle class="text-body-1 font-weight-medium py-2">Sector Performance</VCardTitle>
          <VCardText class="pa-2">
            <VueApexCharts type="bar" height="220" :options="sectorChartOptions" :series="sectorData.series" />
          </VCardText>
        </VCard>
      </VCol>
      <VCol cols="12" md="4">
        <VCard>
          <VCardTitle class="text-body-1 font-weight-medium py-2">Advance/Decline</VCardTitle>
          <VCardText class="pa-2">
            <VueApexCharts type="donut" height="220" :options="advanceDeclineOptions" :series="advanceDeclineData.series" />
          </VCardText>
        </VCard>
      </VCol>
    </VRow>

    <!-- Active Stocks Section -->
    <VCard class="mb-4">
      <VCardTitle class="d-flex align-center justify-space-between py-2 flex-wrap gap-2">
        <div class="d-flex align-center gap-2">
          <span class="text-body-1 font-weight-medium">Active Stocks</span>
          <VIcon icon="tabler-info-circle" size="16" color="primary" />
          <span class="text-caption text-primary">Filter to show only Cash and F&O components of Nifty index</span>
        </div>
      </VCardTitle>
      <VCardText class="py-2">
        <!-- Stock Tabs -->
        <div class="d-flex align-center gap-2 mb-3 flex-wrap">
          <VChip v-for="tab in stockTabs" :key="tab.value" :color="activeStockTab === tab.value ? 'success' : 'default'" :variant="activeStockTab === tab.value ? 'flat' : 'outlined'" size="small" @click="activeStockTab = tab.value">{{ tab.label }}</VChip>
          <VSpacer />
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Sort by:</span>
            <VSelect v-model="sortBy" :items="sortOptions" density="compact" hide-details style="width: 90px" />
            <span class="text-caption">Time frame</span>
            <VSelect v-model="timeFrame" :items="timeFrameOptions" density="compact" hide-details style="width: 80px" />
            <VChip :color="ageMovement ? 'primary' : 'default'" :variant="ageMovement ? 'flat' : 'outlined'" size="small" @click="ageMovement = !ageMovement">Age Movement</VChip>
            <VChip :color="curated ? 'primary' : 'default'" :variant="curated ? 'flat' : 'outlined'" size="small" @click="curated = !curated">Curated</VChip>
          </div>
        </div>

        <!-- Active Stocks Grid -->
        <div class="stock-grid">
          <div v-for="stock in activeStocks" :key="stock.symbol" class="stock-card-wrapper">
            <div :class="['stock-card-item', stock.positive ? 'bg-success' : 'bg-error']">
              <div class="d-flex align-center justify-center gap-1">
                <span class="text-white font-weight-bold stock-symbol">{{ stock.symbol }}</span>
                <span class="text-white stock-rank">{{ stock.rank }}</span>
                <VIcon icon="tabler-caret-right-filled" size="10" color="white" />
              </div>
              <VIcon icon="tabler-chart-bar" size="14" color="white" />
              <div class="text-white stock-change">{{ stock.change }}%</div>
              <div class="d-flex justify-center gap-0">
                <VIcon v-for="n in stock.rating" :key="n" icon="tabler-star-filled" size="8" color="warning" />
              </div>
            </div>
          </div>
        </div>
        <div class="text-caption text-medium-emphasis mt-2">Note :- Last Refresh Date Time: {{ lastRefreshTime }}</div>
      </VCardText>
    </VCard>

    <!-- Heatmap Section -->
    <VCard class="mb-4">
      <VCardTitle class="d-flex align-center justify-space-between py-2">
        <span class="text-body-1 font-weight-medium">Heatmap</span>
        <div class="d-flex align-center gap-2">
          <VIcon icon="tabler-chart-bar" size="16" />
          <span class="text-caption text-primary">** click the icon to view charts /</span>
        </div>
      </VCardTitle>
      <VCardText class="pa-2">
        <div class="heatmap-grid">
          <div v-for="stock in heatmapStocks" :key="stock.symbol" class="heatmap-card-wrapper">
            <div :class="['heatmap-card-item', stock.positive ? 'bg-success' : 'bg-error']">
              <div class="d-flex align-center justify-center gap-1">
                <span class="text-white font-weight-bold heatmap-symbol">{{ stock.symbol }}</span>
                <VIcon icon="tabler-caret-right-filled" size="8" color="white" />
              </div>
              <VIcon icon="tabler-chart-bar" size="12" color="white" />
              <div class="text-white heatmap-change">{{ stock.change }}%</div>
            </div>
          </div>
        </div>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.stock-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 6px;
}

.heatmap-grid {
  display: grid;
  grid-template-columns: repeat(11, 1fr);
  gap: 4px;
}

@media (max-width: 1400px) {
  .stock-grid { grid-template-columns: repeat(8, 1fr); }
  .heatmap-grid { grid-template-columns: repeat(8, 1fr); }
}

@media (max-width: 1200px) {
  .stock-grid { grid-template-columns: repeat(6, 1fr); }
  .heatmap-grid { grid-template-columns: repeat(6, 1fr); }
}

@media (max-width: 900px) {
  .stock-grid { grid-template-columns: repeat(4, 1fr); }
  .heatmap-grid { grid-template-columns: repeat(4, 1fr); }
}

@media (max-width: 600px) {
  .stock-grid { grid-template-columns: repeat(3, 1fr); }
  .heatmap-grid { grid-template-columns: repeat(3, 1fr); }
}

.stock-card-item {
  border-radius: 4px;
  padding: 6px 3px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1px;
  cursor: pointer;
  transition: transform 0.2s;
}

.stock-card-item:hover { transform: scale(1.02); }

.heatmap-card-item {
  border-radius: 3px;
  padding: 4px 2px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1px;
  cursor: pointer;
  transition: transform 0.2s;
}

.heatmap-card-item:hover { transform: scale(1.02); }

.stock-symbol { font-size: 9px; line-height: 1; }
.stock-rank { font-size: 8px; }
.stock-change { font-size: 9px; line-height: 1; }
.heatmap-symbol { font-size: 8px; line-height: 1; }
.heatmap-change { font-size: 8px; line-height: 1; }

.bg-success { background-color: #00C896 !important; }
.bg-error { background-color: #FF6B6B !important; }
</style>
