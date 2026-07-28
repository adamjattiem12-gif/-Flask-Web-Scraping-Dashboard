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
          <span class="refresh-icon">⟳</span>
          {{ isRefreshing ? 'Refreshing...' : 'Refresh' }}
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

// CHAD'S COMPONENTS
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

// MOCK DATA FOR MARKET CARDS
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

// TOP MOVERS DATA
const topMoversData = ref([
  { rank: 1, symbol: 'SOL', change: 8.7, price: 178.45, market: 'Digital' },
  { rank: 2, symbol: 'DOGE', change: 7.2, price: 0.1600, market: 'Digital' },
  { rank: 3, symbol: 'AVAX', change: -6.3, price: 38.91, market: 'Digital' },
  { rank: 4, symbol: 'LINK', change: 5.6, price: 18.47, market: 'Digital' },
  { rank: 5, name: 'HP Pavilion 15.6" FHD Laptop', change: -5.1, price: 529.99, market: 'Retail' }
])

// DATA TABLE ITEMS
const tableItems = ref([
  {
    id: 1,
    name: 'BTC - Bitcoin',
    source: 'CoinGecko',
    price: 67234.50,
    change: 3.2,
    market: 'Digital',
    rating: null,
    scrapedAt: 'Jul 20, 02:30 PM'
  },
  {
    id: 2,
    name: 'ETH - Ethereum',
    source: 'CoinGecko',
    price: 3412.80,
    change: 2.4,
    market: 'Digital',
    rating: null,
    scrapedAt: 'Jul 20, 02:30 PM'
  },
  {
    id: 3,
    name: 'Samsung 65" Crystal 4K UHD TV',
    source: 'WebScraper.io',
    price: 897.99,
    change: 0.8,
    market: 'Retail',
    rating: 4.5,
    scrapedAt: 'Jul 20, 02:31 PM'
  },
  {
    id: 4,
    name: 'Samsung Galaxy Tab S8+',
    source: 'WebScraper.io',
    price: 699.99,
    change: 1.5,
    market: 'Retail',
    rating: 4.3,
    scrapedAt: 'Jul 20, 02:33 PM'
  },
  {
    id: 5,
    name: 'Canon EOS Rebel SL3 DSLR',
    source: 'WebScraper.io',
    price: 649.00,
    change: -0.5,
    market: 'Retail',
    rating: 4.7,
    scrapedAt: 'Jul 20, 02:32 PM'
  },
  {
    id: 6,
    name: 'iPad Air 10.9-inch (2022)',
    source: 'WebScraper.io',
    price: 599.00,
    change: 2.1,
    market: 'Retail',
    rating: 4.6,
    scrapedAt: 'Jul 20, 02:31 PM'
  }
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
.dashboard-page {
  min-height: 100vh;
  background: #F7F5F2;
  padding: 0;
}

/* HEADER BAR */
.dashboard-header-bar {
  background: #FFFFFF;
  padding: 24px 40px;
  margin: 0;
  border-bottom: 1px solid #E5E2DD;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.dashboard-header-bar h1 {
  color: #2D2A3E;
  font-size: 28px;
  font-weight: 600;
  margin: 0;
}

.last-updated {
  color: #9E9BB0;
  font-size: 13px;
  font-weight: 400;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* ✅ REFRESH BUTTON - GREEN LIKE SCRAPE BUTTON */
.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  background: #5B8C5A;
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(91, 140, 90, 0.2);
}

.refresh-btn:hover:not(:disabled) {
  background: #4A7349;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(91, 140, 90, 0.35);
}

.refresh-btn:active:not(:disabled) {
  transform: scale(0.97);
}

.refresh-btn:disabled {
  background: #9E9BB0;
  cursor: not-allowed;
  opacity: 0.7;
  transform: none;
  box-shadow: none;
}

.refresh-icon {
  display: inline-block;
  font-size: 18px;
  transition: transform 0.6s ease;
}

.refresh-btn:hover:not(:disabled) .refresh-icon {
  transform: rotate(180deg);
}

.refresh-btn:disabled .refresh-icon {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* CONTENT */
.dashboard-content {
  padding: 32px 40px 40px 40px;
  max-width: 100%;
}

/* LOADING STATE */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #E5E2DD;
  border-top-color: #5B8C5A;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-state p {
  color: #9E9BB0;
  font-size: 14px;
}

/* STATS GRID */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

/* SECTION HEADER */
.section-header {
  margin-bottom: 20px;
  margin-top: 8px;
}

.section-header h2 {
  color: #2D2A3E;
  font-size: 20px;
  font-weight: 600;
}

.section-subtitle {
  color: #9E9BB0;
  font-size: 14px;
  display: block;
  margin-top: 4px;
}

/* MARKETS GRID */
.markets-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 32px;
}

/* TOP MOVERS & WATCHLIST ROW */
.row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 32px;
}

/* ACTION BAR */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  margin-bottom: 32px;
  border-top: 1px solid #E5E2DD;
  border-bottom: 1px solid #E5E2DD;
}

.source-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #5C5A6B;
  font-size: 14px;
  font-weight: 500;
}

.badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #5B8C5A;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

/* RESPONSIVE */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 992px) {
  .markets-grid {
    grid-template-columns: 1fr;
  }
  .row-2col {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-header-bar {
    padding: 16px 20px;
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-left {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .last-updated {
    font-size: 12px;
  }
  
  .dashboard-content {
    padding: 20px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  
  .dashboard-header-bar h1 {
    font-size: 24px;
  }
  
  .action-bar {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .refresh-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 375px) {
  .dashboard-header-bar {
    padding: 12px 16px;
  }
  
  .dashboard-content {
    padding: 16px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-header-bar h1 {
    font-size: 20px;
  }
}
</style>