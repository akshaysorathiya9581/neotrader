<script setup>
const lastRefreshTime = ref('2026-01-02 15:32:39')
const activePattern = ref('hammer')
const selectedTimeframe = ref('30Min')
const timeframes = ['5Min', '15Min', '30Min', '1Hour', '4Hour', 'Daily']

const patterns = [
  { id: 'hammer', name: 'HAMMER', color: 'success' },
  { id: 'shootingstar', name: 'SHOOTING STAR', color: 'error' },
  { id: 'spinningtop', name: 'SPINNING TOP', color: 'warning' },
  { id: 'doji', name: 'DOJI', color: 'info' },
  { id: 'engulfing', name: 'ENGULFING', color: 'primary' },
  { id: 'longline', name: 'LONGLINE', color: 'success' },
  { id: 'dragonfly', name: 'DRAGONFLY AUCTION', color: 'warning' },
  { id: 'shortreversal', name: 'SHORT EXHAUSTION', color: 'error' },
]

const patternDescriptions = {
  hammer: 'HAMMER: A hammer is a single candle bullish reversal candlestick pattern. It appears at the end of a decline. The candle formation looks like a hammer, as it has a long lower wick and a short body at the top of the candlestick with little or no upper wick.',
  shootingstar: 'SHOOTING STAR: A shooting star is a bearish candlestick with a long upper shadow, little or no lower shadow, and a small real body near the low of the day.',
  spinningtop: 'SPINNING TOP: A spinning top is a candlestick pattern with a short real body that is vertically centered between long upper and lower shadows.',
  doji: 'DOJI: A doji is a candlestick pattern where the open and close prices are virtually equal.',
  engulfing: 'ENGULFING: An engulfing pattern is a two-candle reversal pattern where the second candle completely engulfs the first candle.',
  longline: 'LONGLINE: A long line candle has a long real body compared to other candles in the chart.',
  dragonfly: 'DRAGONFLY: A dragonfly doji is a candlestick pattern that signals a possible price reversal.',
  shortreversal: 'SHORT REVERSAL: A short-term reversal pattern indicating exhaustion of the current trend.',
}

// Trending Up data
const trendingUp = ref([
  { symbol: 'COALINDIA', score: 96, consec: 8 },
  { symbol: 'GLENMARK', score: 82, consec: 2 },
  { symbol: 'NTPC', score: 68, consec: 5 },
  { symbol: 'BOSCHLTD', score: 46, consec: 0 },
  { symbol: 'DIVISLAB', score: 45, consec: 1 },
])

// Trending Down data
const trendingDown = ref([
  { symbol: 'EPIGHEALTH', score: -56, consec: 0 },
  { symbol: 'KOTAKBANK', score: -20, consec: 1 },
  { symbol: 'MANAPURAM', score: -53, consec: 1 },
  { symbol: 'NESTLEIND', score: -27, consec: 0 },
  { symbol: 'PRISMJOHNS', score: -27, consec: 0 },
])

// Stats data
const stats = ref({
  trendingUp: { count: 96, name: 'Trending Up' },
  trendingDown: { count: 8, name: 'Trending Down' },
  hammer: { count: 0, name: 'Hammer' },
  shootingStar: { count: 0, name: 'Shooting Star' },
  longReversal: { count: 1, name: 'Long Reversal' },
  spinningTop: { count: 0, name: 'Spinning Top' },
  doji: { count: 6, name: 'Doji' },
  engulfing: { count: 0, name: 'Engulfing' },
  longline: { count: 33, name: 'Longline' },
  shortReversal: { count: 3, name: 'Short Reversal' },
})
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Candlestick Dashboard</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-medium-emphasis">Candlestick Dashboard</span>
        </div>
        <div class="text-right">
          <p class="text-body-2 mb-0">Last Refresh Date Time: <strong>{{ lastRefreshTime }}</strong></p>
          <p class="text-primary text-caption mb-0">New signals appear every 30 minutes.</p>
          <p class="text-caption text-medium-emphasis mb-0">Watchlist ~ NIFTY 200 / Cash Market AllCap</p>
        </div>
      </VCardText>
    </VCard>

    <!-- Pattern Tabs -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <div class="d-flex align-center gap-2 flex-wrap">
          <VBtn 
            v-for="pattern in patterns" 
            :key="pattern.id" 
            :color="activePattern === pattern.id ? pattern.color : 'default'" 
            :variant="activePattern === pattern.id ? 'flat' : 'outlined'" 
            size="small" 
            @click="activePattern = pattern.id"
          >{{ pattern.name }}</VBtn>
        </div>
      </VCardText>
    </VCard>

    <!-- Pattern Description -->
    <VCard class="mb-4">
      <VCardText>
        <p class="text-primary text-body-2 mb-0 font-italic">{{ patternDescriptions[activePattern] }}</p>
      </VCardText>
    </VCard>

    <!-- How To Use -->
    <VCard class="mb-4">
      <VExpansionPanels variant="accordion">
        <VExpansionPanel>
          <VExpansionPanelTitle>How To Use</VExpansionPanelTitle>
          <VExpansionPanelText>
            <p class="mb-1">1. Select a candlestick pattern to view stocks showing that pattern</p>
            <p class="mb-1">2. Trending Up shows bullish patterns, Trending Down shows bearish patterns</p>
            <p class="mb-0">3. Use Stats to see the count of each pattern type</p>
          </VExpansionPanelText>
        </VExpansionPanel>
      </VExpansionPanels>
    </VCard>

    <!-- Timeframe selector -->
    <VCard class="mb-4">
      <VCardText class="py-2">
        <VChip color="info" variant="flat" size="small">{{ selectedTimeframe }}</VChip>
      </VCardText>
    </VCard>

    <!-- Data Grid -->
    <VRow>
      <!-- Trending Up -->
      <VCol cols="12" md="4">
        <VCard>
          <VCardTitle class="py-2">Trending Up</VCardTitle>
          <VTable density="compact">
            <thead>
              <tr>
                <th class="text-info text-caption">Symbol</th>
                <th class="text-info text-caption">Score</th>
                <th class="text-info text-caption">Consec</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in trendingUp" :key="item.symbol">
                <td><a href="#" class="text-info font-weight-medium">{{ item.symbol }}</a></td>
                <td>{{ item.score }}</td>
                <td>{{ item.consec }}</td>
              </tr>
            </tbody>
          </VTable>
        </VCard>
      </VCol>

      <!-- Trending Down -->
      <VCol cols="12" md="4">
        <VCard>
          <VCardTitle class="py-2">Trending Down</VCardTitle>
          <VTable density="compact">
            <thead>
              <tr>
                <th class="text-info text-caption">Symbol</th>
                <th class="text-info text-caption">Score</th>
                <th class="text-info text-caption">Consec</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in trendingDown" :key="item.symbol">
                <td><a href="#" class="text-error font-weight-medium">{{ item.symbol }}</a></td>
                <td class="text-error">{{ item.score }}</td>
                <td>{{ item.consec }}</td>
              </tr>
            </tbody>
          </VTable>
        </VCard>
      </VCol>

      <!-- Stats -->
      <VCol cols="12" md="4">
        <VCard>
          <VCardTitle class="py-2">Stats</VCardTitle>
          <VCardText>
            <VRow dense>
              <VCol cols="6">
                <div class="d-flex justify-space-between mb-2">
                  <span class="text-caption text-info">Name</span>
                  <span class="text-caption text-info">Count</span>
                </div>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Trending Up</span>
                  <span class="text-caption text-success">{{ stats.trendingUp.count }}</span>
                </div>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Trending Down</span>
                  <span class="text-caption text-error">{{ stats.trendingDown.count }}</span>
                </div>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Hammer</span>
                  <span class="text-caption">{{ stats.hammer.count }}</span>
                </div>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Shooting Star</span>
                  <span class="text-caption">{{ stats.shootingStar.count }}</span>
                </div>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Long Reversal</span>
                  <span class="text-caption text-primary">{{ stats.longReversal.count }}</span>
                </div>
              </VCol>
              <VCol cols="6">
                <div class="d-flex justify-space-between mb-2">
                  <span class="text-caption text-info">Name</span>
                  <span class="text-caption text-info">Count</span>
                </div>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Spinning Top</span>
                  <span class="text-caption">{{ stats.spinningTop.count }}</span>
                </div>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Doji</span>
                  <span class="text-caption text-warning">{{ stats.doji.count }}</span>
                </div>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Engulfing</span>
                  <span class="text-caption">{{ stats.engulfing.count }}</span>
                </div>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Longline</span>
                  <span class="text-caption text-success">{{ stats.longline.count }}</span>
                </div>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Short Reversal</span>
                  <span class="text-caption text-error">{{ stats.shortReversal.count }}</span>
                </div>
              </VCol>
            </VRow>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </div>
</template>
