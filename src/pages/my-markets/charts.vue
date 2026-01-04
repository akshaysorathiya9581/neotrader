<script setup>
import VueApexCharts from 'vue3-apexcharts'

const selectedSymbol = ref('NIFTY')
const selectedInterval = ref('1h')
const symbols = [
  { title: 'NIFTY 50', value: 'NIFTY', price: 26328.5 },
  { title: 'NIFTY BANK', value: 'NIFTYBANK', price: 48756.3 },
  { title: 'RELIANCE', value: 'RELIANCE', price: 2987.5 },
  { title: 'TCS', value: 'TCS', price: 4123.5 },
  { title: 'HDFCBANK', value: 'HDFCBANK', price: 1678.9 },
  { title: 'INFY', value: 'INFY', price: 1567.8 },
  { title: 'ICICIBANK', value: 'ICICIBANK', price: 1234.5 },
  { title: 'SBIN', value: 'SBIN', price: 765.4 },
  { title: 'BHARTIARTL', value: 'BHARTIARTL', price: 1654.3 },
  { title: 'ITC', value: 'ITC', price: 456.7 },
]
const intervals = [
  { label: '1m', value: '1m' },
  { label: '5m', value: '5m' },
  { label: '15m', value: '15m' },
  { label: '30m', value: '30m' },
  { label: '1h', value: '1h' },
  { label: '4h', value: '4h' },
  { label: '1D', value: '1D' },
  { label: '1W', value: '1W' },
]

// Generate candlestick data
const generateCandlestickData = (basePrice, count = 100) => {
  const data = []
  let price = basePrice
  const now = new Date()
  
  for (let i = count; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60 * 60 * 1000)
    const volatility = basePrice * 0.02
    const open = price
    const close = price + (Math.random() - 0.48) * volatility
    const high = Math.max(open, close) + Math.random() * volatility * 0.5
    const low = Math.min(open, close) - Math.random() * volatility * 0.5
    
    data.push({
      x: time,
      y: [+open.toFixed(2), +high.toFixed(2), +low.toFixed(2), +close.toFixed(2)]
    })
    price = close
  }
  return data
}

// Generate volume data
const generateVolumeData = (count = 100) => {
  const data = []
  const now = new Date()
  
  for (let i = count; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60 * 60 * 1000)
    data.push({
      x: time,
      y: Math.floor(Math.random() * 1000000) + 500000
    })
  }
  return data
}

const currentSymbol = computed(() => symbols.find(s => s.value === selectedSymbol.value))
const candlestickData = ref([])
const volumeData = ref([])

const updateChartData = () => {
  const basePrice = currentSymbol.value?.price || 25000
  candlestickData.value = generateCandlestickData(basePrice)
  volumeData.value = generateVolumeData()
}

// Chart options
const candlestickOptions = computed(() => ({
  chart: {
    type: 'candlestick',
    height: 400,
    id: 'candles',
    toolbar: { autoSelected: 'pan', show: true },
    zoom: { enabled: true },
    animations: { enabled: false },
  },
  title: {
    text: `${currentSymbol.value?.title || 'NIFTY 50'} - ${selectedInterval.value}`,
    align: 'left',
    style: { fontSize: '14px', fontWeight: 600 }
  },
  xaxis: { type: 'datetime', labels: { datetimeUTC: false } },
  yaxis: {
    tooltip: { enabled: true },
    labels: { formatter: (val) => val?.toFixed(2) }
  },
  plotOptions: {
    candlestick: {
      colors: { upward: '#26a69a', downward: '#ef5350' }
    }
  },
  grid: { borderColor: '#e0e0e0' },
}))

const volumeOptions = computed(() => ({
  chart: {
    type: 'bar',
    height: 150,
    id: 'volume',
    brush: { enabled: true, target: 'candles' },
    selection: { enabled: true, xaxis: {} },
    animations: { enabled: false },
  },
  dataLabels: { enabled: false },
  xaxis: { type: 'datetime', labels: { datetimeUTC: false } },
  yaxis: {
    labels: { formatter: (val) => (val / 1000000).toFixed(1) + 'M' }
  },
  colors: ['#26a69a'],
  grid: { borderColor: '#e0e0e0' },
}))

const candlestickSeries = computed(() => [{ data: candlestickData.value }])
const volumeSeries = computed(() => [{ name: 'Volume', data: volumeData.value }])

// Real-time update simulation
const updateInterval = ref(null)
onMounted(() => {
  updateChartData()
  updateInterval.value = setInterval(() => {
    if (candlestickData.value.length > 0) {
      const lastCandle = candlestickData.value[candlestickData.value.length - 1]
      const price = lastCandle.y[3]
      const volatility = price * 0.001
      const newClose = price + (Math.random() - 0.5) * volatility
      lastCandle.y[3] = +newClose.toFixed(2)
      lastCandle.y[1] = Math.max(lastCandle.y[1], newClose)
      lastCandle.y[2] = Math.min(lastCandle.y[2], newClose)
    }
  }, 2000)
})

onUnmounted(() => {
  if (updateInterval.value) clearInterval(updateInterval.value)
})

watch([selectedSymbol, selectedInterval], () => {
  updateChartData()
})
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Realtime Charts</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-primary text-caption">Realtime Charts</span>
        </div>
        <VBtn color="info" size="small">Charts</VBtn>
      </VCardText>
    </VCard>

    <!-- Chart Card -->
    <VCard>
      <VCardTitle class="d-flex align-center justify-space-between py-2">
        <span class="text-body-1">Realtime Charts</span>
      </VCardTitle>
      <VCardText>
        <!-- Symbol and Interval Selectors -->
        <div class="d-flex align-center gap-2 mb-4 flex-wrap">
          <VSelect
            v-model="selectedSymbol"
            :items="symbols"
            item-title="title"
            item-value="value"
            density="compact"
            hide-details
            style="width: 160px"
            label="Symbol"
          />
          <div class="d-flex align-center gap-1">
            <VBtn
              v-for="int in intervals"
              :key="int.value"
              :color="selectedInterval === int.value ? 'info' : 'default'"
              :variant="selectedInterval === int.value ? 'flat' : 'outlined'"
              size="x-small"
              @click="selectedInterval = int.value"
            >
              {{ int.label }}
            </VBtn>
          </div>
        </div>

        <!-- Candlestick Chart -->
        <div class="chart-container">
          <VueApexCharts
            type="candlestick"
            height="400"
            :options="candlestickOptions"
            :series="candlestickSeries"
          />
          <VueApexCharts
            type="bar"
            height="150"
            :options="volumeOptions"
            :series="volumeSeries"
          />
        </div>

        <!-- Source Attribution -->
        <div class="mt-2 d-flex align-center justify-space-between">
          <span class="text-caption text-medium-emphasis">Source: NeoTrader Real-time Data</span>
          <span class="text-caption text-success">● Live - Updates every 2 seconds</span>
        </div>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 4px;
  padding: 8px;
}
</style>
