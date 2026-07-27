<template>
  <div class="dashboard-page">
    <!-- WHITE HEADER BAR -->
    <div class="dashboard-header-bar">
      <div class="header-left">
        <h1>Dashboard</h1>
        <span v-if="lastUpdated" class="last-updated">
          🕐 Updated: {{ lastUpdated }}
        </span>
      </div>
      <div class="header-right">
        <button class="refresh-btn" @click="refreshData" :disabled="isRefreshing">
          {{ isRefreshing ? '⟳ Refreshing...' : '⟳ Refresh' }}
        </button>
      </div>
    </div>

    <!-- CONTENT -->
    <div class="dashboard-content">
      <!-- LOADING STATE -->
      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading dashboard data...</p>
      </div>

      <!-- ACTUAL CONTENT -->
      <template v-else>
        <!-- STAT CARDS -->
        <div class="stats-grid">
          <StatCard
            icon="📦"
            label="Total Items"
            :value="stats.totalItems"
            subtitle="across 2 markets"
          />
          <StatCard
            icon="🌐"
            label="Active Sources"
            :value="stats.activeSources"
            subtitle="WebScraper.io · CoinGecko"
          />
          <StatCard
            icon="✅"
            label="Success Rate"
            :value="stats.successRate"
            subtitle="last 7 days"
          />
          <StatCard
            icon="🕐"
            label="Last Scrape"
            :value="stats.lastScrape"
            subtitle="Jul 20, 2026"
          />
        </div>

        <!-- PRICE SNAPSHOT -->
        <div class="section-header">
          <h2>Price Snapshot</h2>
          <span class="section-subtitle">Market Overview · Updated from your latest scrape</span>
        </div>

        <!-- MARKET OVERVIEW -->
        <div class="markets-grid">
          <MarketOverviewCard
            title="Retail Goods"
            accent-color="#D4914A"
            :avg-price="473.99"
            :items-count="12"
            :recent-items="retailRecentItems"
          />
          <MarketOverviewCard
            title="Digital Assets"
            accent-color="#4A8C8C"
            :avg-price="5942.24"
            :items-count="12"
            :recent-items="cryptoRecentItems"
          />
        </div>

        <!-- TOP MOVERS & WATCHLIST -->
        <div class="row-2col">
          <TopMovers :items="topMoversData" />
          <Watchlist />
        </div>

        <!-- SCRAPE BUTTON -->
        <div class="action-bar">
          <div class="source-badge">
            <span class="badge-dot"></span>
            WebScraper.io · CoinGecko
          </div>
          <ScrapeButton @scrape="handleScrape" />
        </div>

        <!-- DATA TABLE -->
        <DataTable 
          :items="tableItems" 
          :loading="tableLoading"
          :error="errorMessage"
          :current-page="currentPage"
          :total-pages="totalPages"
          @page-change="handlePageChange"
          @retry="refreshData"
        />
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// YOUR COMPONENTS
import StatCard from '@/components/StatCard.vue'
import MarketOverviewCard from '@/components/MarketOverviewCard.vue'

// RUSHIN'S COMPONENTS
import TopMovers from '@/components/TopMovers.vue'
import DataTable from '@/components/DataTable.vue'

// ✅ CHAD'S COMPONENTS (Now fixed!)
import Watchlist from '@/components/Watchlist.vue'
import ScrapeButton from '@/components/ScrapeButton.vue'

// STATE
const isLoading = ref(true)
const isRefreshing = ref(false)
const tableLoading = ref(false)
const lastUpdated = ref('')
const errorMessage = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
let refreshInterval = null

// STATS DATA
const stats = ref({
  totalItems: 24,
  activeSources: 2,
  successRate: '96.5%',
  lastScrape: '02:33 PM'
})

// MOCK DATA
const retailRecentItems = [
  { name: 'HP Pavilion 15.6" FHD Laptop', change: -5.1 },
  { name: 'Bose QuietComfort 45 Wireless', change: -4.2 },
  { name: 'Asus VivoBook X441NA-GA190', change: -3.8 }
]

const cryptoRecentItems = [
  { name: 'SOL - Solana', change: 8.7 },
  { name: 'DOGE - Dogecoin', change: 7.2 },
  { name: 'AVAX - Avalanche', change: -6.3 }
]

const topMoversData = ref([
  { rank: 1, symbol: 'SOL', change: 8.7, price: 178.45, market: 'Digital' },
  { rank: 2, symbol: 'DOGE', change: 7.2, price: 0.1600, market: 'Digital' },
  { rank: 3, symbol: 'AVAX', change: -6.3, price: 38.91, market: 'Digital' },
  { rank: 4, symbol: 'LINK', change: 5.6, price: 18.47, market: 'Digital' },
  { rank: 5, name: 'HP Pavilion 15.6" FHD Laptop', change: -5.1, price: 529.99, market: 'Retail' }
])

const tableItems = ref([
  // ... your items here
])

// METHODS
const updateTimestamp = () => {
  const now = new Date()
  lastUpdated.value = now.toLocaleTimeString() + ' · ' + now.toLocaleDateString()
}

const refreshData = async () => {
  isRefreshing.value = true
  tableLoading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1500))
    updateTimestamp()
    totalPages.value = Math.ceil(tableItems.value.length / 10)
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = error.message || 'Failed to load data'
  } finally {
    isRefreshing.value = false
    tableLoading.value = false
  }
}

const handleScrape = async () => {
  console.log('Scrape triggered')
  await refreshData()
}

const handlePageChange = (page) => {
  currentPage.value = page
  console.log('Page changed to:', page)
}

// LIFECYCLE
onMounted(async () => {
  try {
    await refreshData()
    refreshInterval = setInterval(refreshData, 60000)
  } catch (error) {
    console.error('Error loading dashboard:', error)
  } finally {
    isLoading.value = false
  }
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
/* ... your existing styles ... */
</style>