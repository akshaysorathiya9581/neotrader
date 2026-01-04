<script setup>
const lastRefreshTime = ref('2026-01-02 15:32:39')
const autoRefresh = ref(false)
const searchQuery = ref('')
const selectedIndex = ref('NIFTY FNO')
const indexOptions = ['NIFTY FNO', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500']
const selectedTimeframe = ref('All')
const timeframeOptions = ['All', '30Min', '60Min', '1Day', '1Week']
const fromDate = ref('')
const toDate = ref('')

// Filter chips
const activeFilters = ref(['30Min', '60Min', '1Day', '1Week'])

// Signal filters
const bullishSignals = ref({
  closeXCloud: true,
  tkCrossedKijun: false,
  tsKsBullishCross: false,
  tsKsTkBullishCross: false,
  csBullish: false,
  kumoTwistBullish: true,
})

const bearishSignals = ref({
  closeXCloud: true,
  csBearishCloud: false,
  tsKsBearishCross: false,
  tsKsBearishRecentCross: false,
  csBearish: false,
  kumoTwistBearish: false,
})

const generalFilters = ref({
  flatCloud: false,
  priceInsideCloud: false,
  narrowCloud: false,
  tkFsLine: false,
  flatTsLine: false,
})

const bullishFilter = ref({
  closeAboveCloud: false,
  tenkanAboveKijun: false,
  csAboveCloud: false,
  tenkanKs: false,
  tsKsAboveCloud: false,
  futureCloudBullish: false,
})

const bearishFilter = ref({
  closeBelowCloud: false,
  csTsBelowKsAsDx: false,
  csBelowCloud: false,
  tsKsBelowCloud: false,
  futureCloudBearish: false,
})

// Table data
const tableData = ref([
  { symbol: 'ADANIENT', value: 2279.5, timeframe: '30Min', bullScore: 37, bearScore: 7, tenkanSen: 2279, kijunSen: 2264.2, senkouSpanA: 2226.05, senkouSpanB: 2322.55, chikouSpan: 2378.5 },
  { symbol: 'ADANIENT', value: 2279.5, timeframe: '60Min', bullScore: 70, bearScore: 7, tenkanSen: 2320, kijunSen: 2340.2, senkouSpanA: 2227.1, senkouSpanB: 2254.5, chikouSpan: 2276.0 },
  { symbol: 'ADANIENT', value: 2279.5, timeframe: '1Day', bullScore: 14, bearScore: 28, tenkanSen: 2241, kijunSen: 2251.6, senkouSpanA: 2382.775, senkouSpanB: 2477.15, chikouSpan: 2378.8 },
  { symbol: 'ADANIENT', value: 2279.5, timeframe: '1Week', bullScore: 7, bearScore: 35, tenkanSen: 2825, kijunSen: 2856.75, senkouSpanA: 2831.3, senkouSpanB: 2560.0, chikouSpan: 2278.8 },
  { symbol: 'APOLLOHOSP', value: 7152.5, timeframe: '30Min', bullScore: 57, bearScore: 7, tenkanSen: 717, kijunSen: 7012.35, senkouSpanA: 7015, senkouSpanB: 7068.5, chikouSpan: 7135.8 },
  { symbol: 'APOLLOHOSP', value: 7132.5, timeframe: '60Min', bullScore: 43, bearScore: 7, tenkanSen: 7115, kijunSen: 7064, senkouSpanA: 7063.875, senkouSpanB: 7045.26, chikouSpan: 7125.5 },
  { symbol: 'APOLLOHOSP', value: 7132.5, timeframe: '1Day', bullScore: 0, bearScore: 35, tenkanSen: 7073, kijunSen: 7108.5, senkouSpanA: 7056.26, senkouSpanB: 7704, chikouSpan: 7125.5 },
  { symbol: 'APOLLOHOSP', value: 7132.5, timeframe: '1Week', bullScore: 21, bearScore: 21, tenkanSen: 7586, kijunSen: 7450.25, senkouSpanA: 5959.875, senkouSpanB: 5809.75, chikouSpan: 7135.5 },
  { symbol: 'ASIANPAINT', value: 2774.6, timeframe: '30Min', bullScore: 0, bearScore: 14, tenkanSen: 2768, kijunSen: 2772.55, senkouSpanA: 2774.375, senkouSpanB: 2755.9, chikouSpan: 2771.6 },
  { symbol: 'ASIANPAINT', value: 2774.6, timeframe: '60Min', bullScore: 7, bearScore: 28, tenkanSen: 2772, kijunSen: 2770, senkouSpanA: 2772.125, senkouSpanB: 2776.85, chikouSpan: 2771.6 },
])

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(20)
const totalItems = ref(890)
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Ichimoku Dashboard</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-primary text-caption">Ichimoku Dashboard</span>
        </div>
        <div class="d-flex align-center gap-4">
          <div class="text-right">
            <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
            <p class="text-primary text-caption mb-0">New signals appear every 30 minutes.</p>
            <p class="text-caption text-medium-emphasis mb-0">Watchlist ~ NIFTY 200 / Cash Market AllCap</p>
          </div>
          <div class="d-flex align-center gap-2">
            <span class="text-caption">Auto refresh</span>
            <VSwitch v-model="autoRefresh" hide-details density="compact" />
            <VBtn icon variant="text" size="small">
              <VIcon icon="tabler-refresh" />
            </VBtn>
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Ichimoku Cloud helps identify trend direction, support/resistance, and momentum</p>
            <p class="mb-1">2. Bullish signals indicate potential buying opportunities</p>
            <p class="mb-0">3. Bearish signals indicate potential selling opportunities</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Timeframe Chips -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center gap-4 flex-wrap">
          <VSelect v-model="selectedTimeframe" label="TIMEFRAME" :items="timeframeOptions" density="compact" hide-details style="width: 120px" />
          <div class="d-flex align-center gap-2">
            <VChip v-for="tf in activeFilters" :key="tf" color="info" variant="flat" size="small" closable>{{ tf }}</VChip>
          </div>
        </div>
      </VCardText>
    </VCard>

    <!-- Signal Filters -->
    <VCard class="mb-4">
      <VCardText>
        <VRow>
          <!-- Bullish Signal -->
          <VCol cols="12" md="2">
            <h6 class="text-body-1 font-weight-bold mb-2">BULLISH SIGNAL</h6>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish"></div>
              <VCheckbox v-model="bullishSignals.closeXCloud" label="CLOSE CROSSED CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish"></div>
              <VCheckbox v-model="bullishSignals.tkCrossedKijun" label="TK CROSSED KIJUN" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish"></div>
              <VCheckbox v-model="bullishSignals.tsKsBullishCross" label="TS & KS BULLISH CROSS" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish"></div>
              <VCheckbox v-model="bullishSignals.tsKsTkBullishCross" label="TS KS TK BULLISH RECENT CROSS" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish"></div>
              <VCheckbox v-model="bullishSignals.csBullish" label="CS BULLISH" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish"></div>
              <VCheckbox v-model="bullishSignals.kumoTwistBullish" label="KUMO TWIST BULLISH" hide-details density="compact" class="signal-checkbox" />
            </div>
          </VCol>

          <!-- Bearish Signal -->
          <VCol cols="12" md="2">
            <h6 class="text-body-1 font-weight-bold mb-2">BEARISH SIGNAL</h6>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bearish"></div>
              <VCheckbox v-model="bearishSignals.closeXCloud" label="CLOSE CROSSED CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bearish"></div>
              <VCheckbox v-model="bearishSignals.csBearishCloud" label="CS BEARISH CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bearish"></div>
              <VCheckbox v-model="bearishSignals.tsKsBearishCross" label="TS & KS BEARISH CROSS" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bearish"></div>
              <VCheckbox v-model="bearishSignals.tsKsBearishRecentCross" label="TS KS BEARISH RECENT CROSS" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bearish"></div>
              <VCheckbox v-model="bearishSignals.csBearish" label="CS BEARISH" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bearish"></div>
              <VCheckbox v-model="bearishSignals.kumoTwistBearish" label="KUMO TWIST BEARISH" hide-details density="compact" class="signal-checkbox" />
            </div>
          </VCol>

          <!-- General Filters -->
          <VCol cols="12" md="2">
            <h6 class="text-body-1 font-weight-bold mb-2">General Filters</h6>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot neutral"></div>
              <VCheckbox v-model="generalFilters.flatCloud" label="FLAT CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot neutral"></div>
              <VCheckbox v-model="generalFilters.priceInsideCloud" label="PRICE INSIDE CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot neutral"></div>
              <VCheckbox v-model="generalFilters.narrowCloud" label="NARROW CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot neutral"></div>
              <VCheckbox v-model="generalFilters.tkFsLine" label="TK FS LINE" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot neutral"></div>
              <VCheckbox v-model="generalFilters.flatTsLine" label="FLAT TS LINE" hide-details density="compact" class="signal-checkbox" />
            </div>
          </VCol>

          <!-- Bullish Filter -->
          <VCol cols="12" md="3">
            <h6 class="text-body-1 font-weight-bold mb-2">BULLISH FILTER</h6>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish-light"></div>
              <VCheckbox v-model="bullishFilter.closeAboveCloud" label="CLOSE ABOVE CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish-light"></div>
              <VCheckbox v-model="bullishFilter.tenkanAboveKijun" label="TENKAN ABOVE KIJUN" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish-light"></div>
              <VCheckbox v-model="bullishFilter.csAboveCloud" label="CS ABOVE CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish-light"></div>
              <VCheckbox v-model="bullishFilter.tenkanKs" label="TENKAN KS" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish-light"></div>
              <VCheckbox v-model="bullishFilter.tsKsAboveCloud" label="TS & KS ABOVE CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bullish-light"></div>
              <VCheckbox v-model="bullishFilter.futureCloudBullish" label="FUTURE CLOUD BULLISH" hide-details density="compact" class="signal-checkbox" />
            </div>
          </VCol>

          <!-- Bearish Filter -->
          <VCol cols="12" md="3">
            <h6 class="text-body-1 font-weight-bold mb-2">BEARISH FILTER</h6>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bearish-light"></div>
              <VCheckbox v-model="bearishFilter.closeBelowCloud" label="CLOSE BELOW CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bearish-light"></div>
              <VCheckbox v-model="bearishFilter.csTsBelowKsAsDx" label="CS TS BELOW KS AS DX" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bearish-light"></div>
              <VCheckbox v-model="bearishFilter.csBelowCloud" label="CS BELOW CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bearish-light"></div>
              <VCheckbox v-model="bearishFilter.tsKsBelowCloud" label="TS & KS BELOW CLOUD" hide-details density="compact" class="signal-checkbox" />
            </div>
            <div class="d-flex align-items-center gap-1 mb-1">
              <div class="signal-dot bearish-light"></div>
              <VCheckbox v-model="bearishFilter.futureCloudBearish" label="FUTURE CLOUD BEARISH" hide-details density="compact" class="signal-checkbox" />
            </div>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- Data Table -->
    <VCard>
      <VCardText>
        <div class="d-flex align-center justify-space-between flex-wrap gap-4 mb-4">
          <div class="d-flex align-center gap-2">
            <VTextField v-model="searchQuery" placeholder="Search" density="compact" hide-details prepend-inner-icon="tabler-search" style="width: 150px" />
            <VSelect v-model="selectedIndex" :items="indexOptions" density="compact" hide-details style="width: 120px" />
          </div>
          <div class="d-flex align-center gap-2">
            <span class="text-caption">From:</span>
            <VTextField v-model="fromDate" type="date" density="compact" hide-details style="width: 130px" />
            <span class="text-caption">To:</span>
            <VTextField v-model="toDate" type="date" density="compact" hide-details style="width: 130px" />
            <VBtn color="primary" variant="outlined" size="small">Trading View Charts</VBtn>
            <VBtn color="info" variant="outlined" size="small">Watchlist</VBtn>
          </div>
        </div>

        <div class="table-responsive">
          <VTable density="compact" class="ichi-table">
            <thead>
              <tr>
                <th><VCheckbox hide-details density="compact" /></th>
                <th class="text-warning">SYMBOL</th>
                <th>RECENT VALUE</th>
                <th>TIMEFRAME</th>
                <th>BULL_SCORE</th>
                <th>BEAR_SCORE</th>
                <th class="text-info">Tenkan_Sen</th>
                <th class="text-info">Kijun_Sen</th>
                <th class="text-success">Senkou_Span_A</th>
                <th class="text-error">Senkou_Span_B</th>
                <th class="text-primary">Chikou_Span</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in tableData" :key="idx">
                <td><VCheckbox hide-details density="compact" /></td>
                <td><a href="#" class="text-warning font-weight-medium">{{ item.symbol }}</a></td>
                <td>{{ item.value }}</td>
                <td><VChip :color="item.timeframe === '30Min' ? 'info' : item.timeframe === '60Min' ? 'success' : item.timeframe === '1Day' ? 'warning' : 'error'" size="x-small" variant="flat">{{ item.timeframe }}</VChip></td>
                <td>{{ item.bullScore }}</td>
                <td>{{ item.bearScore }}</td>
                <td class="text-info">{{ item.tenkanSen }}</td>
                <td class="text-info">{{ item.kijunSen }}</td>
                <td class="text-success">{{ item.senkouSpanA }}</td>
                <td class="text-error">{{ item.senkouSpanB }}</td>
                <td class="text-primary">{{ item.chikouSpan }}</td>
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
            <VBtn v-if="totalPages > 6" :color="currentPage === totalPages ? 'primary' : 'default'" :variant="currentPage === totalPages ? 'flat' : 'text'" size="x-small" min-width="24" @click="currentPage = totalPages">{{ totalPages }}</VBtn>
            <VBtn icon variant="text" size="x-small" :disabled="currentPage === totalPages" @click="currentPage++">
              <VIcon icon="tabler-chevron-right" size="14" />
            </VBtn>
          </div>
          <div class="d-flex align-center gap-2">
            <VSelect v-model="itemsPerPage" :items="[10, 20, 50]" density="compact" hide-details style="width: 60px" />
            <span class="text-caption text-medium-emphasis">Displaying 1 - 20 of {{ totalItems }} records</span>
          </div>
        </div>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.signal-dot {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  flex-shrink: 0;
}

.signal-dot.bullish { background-color: #4caf50; }
.signal-dot.bearish { background-color: #f44336; }
.signal-dot.neutral { background-color: #9e9e9e; }
.signal-dot.bullish-light { background-color: #81c784; }
.signal-dot.bearish-light { background-color: #e57373; }

.signal-checkbox :deep(.v-label) { font-size: 9px !important; }

.ichi-table th { font-size: 9px !important; font-weight: 600; white-space: nowrap; }
.ichi-table td { font-size: 10px !important; white-space: nowrap; padding: 6px 8px !important; }
.table-responsive { overflow-x: auto; }
</style>
