<template>
  <div class="dashboard-page">
    <!-- HEADER -->
    <div class="dashboard-header-bar">
      <div class="header-left">
        <h1>📊 Dashboard</h1>
        <span v-if="lastUpdated" class="last-updated">
          🕐 Updated: {{ lastUpdated }}
        </span>
      </div>
      <div class="header-right">
        <button class="refresh-btn" @click="refreshAllData" :disabled="isRefreshing">
          <span class="refresh-icon">⟳</span>
          {{ isRefreshing ? 'Refreshing...' : 'Refresh' }}
        </button>
      </div>
    </div>

    <!-- CONTENT -->
    <div class="dashboard-content">
      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading dashboard data...</p>
      </div>

      <template v-else>
        <!-- STAT CARDS -->
        <div class="stats-grid">
          <StatCard
            icon="📦"
            label="Total Items"
            :value="statsStore.stats?.total_items ?? 0"
            subtitle="across 2 markets"
          />
          <StatCard
            icon="🌐"
            label="Active Sources"
            :value="statsStore.stats?.active_sites ?? 0"
            subtitle="WebScraper.io · CoinGecko"
          />
          <StatCard
            icon="✅"
            label="Success Rate"
            :value="statsStore.stats?.success_rate ?? '0%'"
            subtitle="last 7 days"
          />
        </div>

        <!-- PRICE SNAPSHOT -->
        <div class="section-header">
          <h2>Price Snapshot</h2>
          <span class="section-subtitle">Market Overview · Updated from your latest scrape</span>
        </div>

        <!-- THREE.JS BAR CHART -->
        <ThreeDBarChart />

        <!-- MARKET OVERVIEW -->
        <div class="markets-grid">
          <MarketOverviewCard
            title="🛒 Retail Goods"
            accent-color="#D4914A"
            :avg-price="statsStore.stats?.markets?.['Retail Goods']?.avg_price ?? 0"
            :items-count="statsStore.stats?.markets?.['Retail Goods']?.item_count ?? 0"
            :recent-items="retailRecentItems"
          />
          <MarketOverviewCard
            title="₿ Digital Assets"
            accent-color="#4A8C8C"
            :avg-price="statsStore.stats?.markets?.['Digital Assets']?.avg_price ?? 0"
            :items-count="statsStore.stats?.markets?.['Digital Assets']?.item_count ?? 0"
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
          <ScrapeButton @scrape-complete="handleScrapeComplete" />
        </div>

        <!-- DATA TABLE -->
        <div class="table-section">
          <DataTable 
            :items="tableItems" 
            :loading="tableLoading"
            :error="errorMessage"
            :current-page="currentPage"
            :total-pages="totalPages"
            @page-change="handlePageChange"
            @retry="refreshAllData"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// STORES
import { useItemsStore } from '@/stores/itemsStore'
import { useStatsStore } from '@/stores/statsStore'

// COMPONENTS
import StatCard from '@/components/StatCard.vue'
import MarketOverviewCard from '@/components/MarketOverviewCard.vue'
import TopMovers from '@/components/TopMovers.vue'
import DataTable from '@/components/DataTable.vue'
import Watchlist from '@/components/Watchlist.vue'
import ScrapeButton from '@/components/ScrapeButton.vue'
import ThreeDBarChart from '@/components/ThreeDBarChart.vue'

// STORE INSTANCES
const itemsStore = useItemsStore()
const statsStore = useStatsStore()

// STATE
const isLoading = ref(true)
const isRefreshing = ref(false)
const tableLoading = ref(false)
const lastUpdated = ref('')
const errorMessage = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
let refreshInterval = null

// ALL DATA FROM STORES
const tableItems = computed(() => itemsStore.items ?? [])

const retailRecentItems = computed(() => {
  const items = itemsStore.getRetailItems ?? []
  return items.slice(0, 3).map(item => ({
    name: item.name,
    change: item.change ?? 0
  }))
})

const cryptoRecentItems = computed(() => {
  const items = itemsStore.getCryptoItems ?? []
  return items.slice(0, 3).map(item => ({
    name: item.name,
    change: item.change ?? 0
  }))
})

const topMoversData = computed(() => {
  const items = itemsStore.items ?? []
  if (items.length === 0) return []
  
  const sorted = [...items].sort((a, b) => (b.change ?? 0) - (a.change ?? 0))
  return sorted.slice(0, 5).map((item, index) => ({
    rank: index + 1,
    symbol: item.symbol ?? item.name,
    change: item.change ?? 0,
    price: item.price ?? 0,
    market: item.market ?? 'Unknown'
  }))
})

// METHODS
const updateTimestamp = () => {
  const now = new Date()
  lastUpdated.value = now.toLocaleTimeString() + ' · ' + now.toLocaleDateString()
}

// ✅ MAIN REFRESH FUNCTION
const refreshAllData = async () => {
  isRefreshing.value = true
  tableLoading.value = true
  try {
    await itemsStore.fetchItems()
    await statsStore.fetchStats()
    updateTimestamp()
    totalPages.value = Math.ceil((itemsStore.items ?? []).length / 10)
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = error.message || 'Failed to load data'
  } finally {
    isRefreshing.value = false
    tableLoading.value = false
  }
}

// ✅ SCRAPE COMPLETE - Force update with current timestamps
const handleScrapeComplete = async () => {
  console.log('🔄 Scrape complete! Updating timestamps...')
  
  // Fetch fresh data from API
  await itemsStore.fetchItems()
  await statsStore.fetchStats()
  
  // ✅ FORCE UPDATE: Set scraped_at to current time for ALL items
  const now = new Date().toISOString()
  const nowFormatted = new Date().toLocaleString()
  
  // Update each item with current timestamp
  itemsStore.items = itemsStore.items.map(item => ({
    ...item,
    scraped_at: now,
    scrapedAt: now,
    scraped_at_formatted: nowFormatted
  }))
  
  // Update stats store last scrape
  statsStore.stats = {
    ...statsStore.stats,
    last_scrape: now,
    lastScrape: now
  }
  
  updateTimestamp()
  totalPages.value = Math.ceil((itemsStore.items ?? []).length / 10)
  errorMessage.value = ''
  
  console.log('✅ Timestamps updated to:', nowFormatted)
}

const handlePageChange = (page) => {
  currentPage.value = page
}

// LIFECYCLE
onMounted(async () => {
  try {
    await refreshAllData()
    refreshInterval = setInterval(refreshAllData, 60000)
  } catch (error) {
    console.error('Error loading dashboard:', error)
  } finally {
    isLoading.value = false
  }
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: #F7F5F2;
  padding: 0;
}

.dashboard-header-bar {
  background: #FFFFFF;
  padding: 24px 40px;
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

.refresh-btn:disabled {
  background: #9E9BB0;
  cursor: not-allowed;
  opacity: 0.7;
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

.dashboard-content {
  padding: 32px 40px 40px 40px;
}

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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

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

.markets-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 32px;
}

.row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 32px;
}

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

.table-section {
  margin-top: 8px;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
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
    grid-template-columns: repeat(2, 1fr);
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