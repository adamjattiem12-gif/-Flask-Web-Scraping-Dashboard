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
            subtitle="WebScraper.io · CoinPaprika"
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
            WebScraper.io · CoinPaprika
          </div>
          <ScrapeButton @scrape-complete="handleScrapeComplete" />
        </div>

        <div class="three-chart-wrapper">
          <ThreeDBarChart />
        </div>

        <!-- DATA TABLE -->
        <div class="table-section">
          <div class="table-controls">
            <SearchBar @search="handleSearch" />
            <FilterPanel @filter="handleFilter" />
          </div>
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
  <!-- ✅ THREE.JS 3D BAR CHART -->
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
import SearchBar from '@/components/SearchBar.vue'
import FilterPanel from '@/components/FilterPanel.vue'

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
const pageSize = 10
let refreshInterval = null

// ALL DATA FROM STORES
// ✅ Uses the filteredItems getter (search + source + price range) instead
// of the raw, unfiltered items list, so Search/Filter actually affect the
// table and pagination reflects the filtered result count.
const tableItems = computed(() => itemsStore.filteredItems ?? [])
const totalPages = computed(() => Math.max(1, Math.ceil(tableItems.value.length / pageSize)))

// ✅ RETAIL RECENT ITEMS - Uses store data with calculated changes
const retailRecentItems = computed(() => {
  const items = itemsStore.getRetailItems ?? []
  return items.slice(0, 3).map(item => ({
    name: item.name,
    change: item.change ?? 0
  }))
})

// ✅ CRYPTO RECENT ITEMS - Uses store data with calculated changes
const cryptoRecentItems = computed(() => {
  const items = itemsStore.getCryptoItems ?? []
  return items.slice(0, 3).map(item => ({
    name: item.name,
    change: item.change ?? 0
  }))
})

// ✅ TOP MOVERS - Uses store getter (cleaner)
const topMoversData = computed(() => itemsStore.getTopMovers)

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
    if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = error.message || 'Failed to load data'
  } finally {
    isRefreshing.value = false
    tableLoading.value = false
  }
}

// ✅ SCRAPE COMPLETE - Store handles everything
const handleScrapeComplete = async () => {
  console.log('🔄 Scrape complete! Updating data...')
  
  // Store handles change calculation and timestamp updates
  await itemsStore.updateItemsAfterScrape()
  await statsStore.fetchStats()
  statsStore.updateLastScrape()
  
  updateTimestamp()
  if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
  errorMessage.value = ''
  
  console.log('✅ Data updated with real changes')
}

const handlePageChange = (page) => {
  currentPage.value = page
}

// ✅ SEARCH & FILTER - Update store filters and jump back to page 1 so
// users don't land on a now-empty/out-of-range page after filtering.
const handleSearch = (query) => {
  itemsStore.setSearchQuery(query)
  currentPage.value = 1
}

const handleFilter = (filters) => {
  itemsStore.setFilters(filters)
  currentPage.value = 1
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
  background: var(--color-bg);
  padding: 0;
}

.dashboard-header-bar {
  background: var(--color-surface);
  padding: 24px 40px;
  border-bottom: 1px solid var(--color-border);
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
  color: var(--color-text);
  font-size: 28px;
  font-weight: 600;
  margin: 0;
}

.last-updated {
  color: var(--color-text-muted);
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
  background: var(--color-success);
  color: var(--color-surface);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(91, 140, 90, 0.2);
}

.refresh-btn:hover:not(:disabled) {
  background: var(--color-success-strong);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(91, 140, 90, 0.35);
}

.refresh-btn:disabled {
  background: var(--color-text-muted);
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
  border: 3px solid var(--color-border);
  border-top-color: var(--color-success);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-state p {
  color: var(--color-text-muted);
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
  color: var(--color-text);
  font-size: 20px;
  font-weight: 600;
}

.section-subtitle {
  color: var(--color-text-muted);
  font-size: 14px;
  display: block;
  margin-top: 4px;
}

/* ✅ 3D CHART WRAPPER - Add some spacing */
.three-chart-wrapper {
  margin-bottom: 32px;
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
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.source-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 500;
}

.badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-success);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.table-section {
  margin-top: 8px;
}

.table-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
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
