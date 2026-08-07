<!-- ============================================================ -->
<!-- FILE: frontend/src/views/Dashboard.vue -->
<!-- ============================================================ -->
<!-- Chart stays visible on refresh — bars animate to 0 then grow -->
<template>
  <div class="dashboard-page">
    <!-- STICKY HEADER — lower z-index so burger menu sits above it -->
    <div class="dashboard-header-bar">
      <div class="header-left">
        <h1>Dashboard</h1>
        <span v-if="lastUpdated" class="last-updated">
          Updated: {{ lastUpdated }}
        </span>
      </div>
      <div class="header-right">
        <ScrapeButton @scrape-complete="handleScrapeComplete" />
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
        <div class="source-badge-container">
          <div class="source-badge">
            <span class="badge-dot"></span>
            WebScraper.io · CoinPaprika
          </div>
        </div>

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
            icon="📈"
            label="Success Rate"
            :value="statsStore.stats?.success_rate ?? '0%'"
            subtitle="last 7 days"
          />
        </div>

        <div class="section-header">
          <h2>Price Snapshot</h2>
          <span class="section-subtitle">Market Overview · Updated from your latest scrape</span>
        </div>

        <div class="markets-grid">
          <MarketOverviewCard
            title="Retail Goods"
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

        <div class="row-2col">
          <TopMovers :items="topMoversData" />
          <Watchlist />
        </div>

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

        <ThreeDBarChart ref="chartRef" />
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { useItemsStore } from '@/stores/itemsStore'
import { useStatsStore } from '@/stores/statsStore'
import StatCard from '@/components/StatCard.vue'
import MarketOverviewCard from '@/components/MarketOverviewCard.vue'
import TopMovers from '@/components/TopMovers.vue'
import DataTable from '@/components/DataTable.vue'
import Watchlist from '@/components/Watchlist.vue'
import ScrapeButton from '@/components/ScrapeButton.vue'
import ThreeDBarChart from '@/components/ThreeDBarChart.vue'

const itemsStore = useItemsStore()
const statsStore = useStatsStore()
const chartRef = ref(null)

const isLoading = ref(true)
const isRefreshing = ref(false)
const tableLoading = ref(false)
const lastUpdated = ref('')
const errorMessage = ref('')
const currentPage = ref(1)
const totalPages = computed(() => Math.max(1, Math.ceil((itemsStore.filteredItems ?? []).length / 10)))
let refreshInterval = null

const tableItems = computed(() => itemsStore.filteredItems ?? [])

const retailRecentItems = computed(() => {
  const items = itemsStore.getRetailItems ?? []
  return items.slice(0, 3).map(item => ({
    name: item.name,
    price: item.price,
    change: null
  }))
})

// ✅ FIX: Added price to cryptoRecentItems so MarketOverviewCard can show it
const cryptoRecentItems = computed(() => {
  const items = itemsStore.getCryptoItems ?? []
  return items.slice(0, 3).map(item => ({
    name: item.name,
    price: item.price,
    change: item.change ?? item.extra?.change_24h ?? null
  }))
})

const topMoversData = computed(() => itemsStore.getTopMovers)

const clearSearchFilter = () => {
  try {
    if (itemsStore.searchQuery !== undefined) {
      itemsStore.searchQuery = ''
    }
    currentPage.value = 1
  } catch (error) {
    console.warn('Could not clear search filter:', error)
  }
}

const updateTimestamp = () => {
  const now = new Date()
  lastUpdated.value = now.toLocaleTimeString() + ' · ' + now.toLocaleDateString()
}

const loadDashboard = async () => {
  isLoading.value = true
  try {
    clearSearchFilter()
    await itemsStore.fetchItems()
    await statsStore.fetchStats()
    chartRef.value?.reset()
    updateTimestamp()
    currentPage.value = 1
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = error.message || 'Failed to load dashboard'
  } finally {
    isLoading.value = false
  }
}

// ============================================================
// ✅ REFRESH — Fixed: reset stats store before fetching
// ============================================================
const refreshAllData = async () => {
  isRefreshing.value = true
  tableLoading.value = true
  try {
    await axios.post('/api/clear-all')
    itemsStore.clearItems()
    statsStore.resetStats()           // ✅ This is the fix
    await statsStore.fetchStats()
    chartRef.value?.reset()
    updateTimestamp()
    currentPage.value = 1
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = error.message || 'Failed to load data'
  } finally {
    isRefreshing.value = false
    tableLoading.value = false
  }
}

const handleScrapeComplete = async () => {
  await itemsStore.updateItemsAfterScrape()
  await statsStore.fetchStats()
  await new Promise(resolve => requestAnimationFrame(resolve))
  chartRef.value?.reset()
  statsStore.updateLastScrape()
  updateTimestamp()
  totalPages.value = Math.ceil((itemsStore.items ?? []).length / 10)
  errorMessage.value = ''
}

const handlePageChange = (page) => {
  currentPage.value = page
}

onMounted(async () => {
  try {
    await loadDashboard()
    refreshInterval = setInterval(loadDashboard, 60000)
  } catch (error) {
    console.error('Error loading dashboard:', error)
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

/* ── HEADER ── */
.dashboard-header-bar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: var(--color-surface);
  padding: 16px 40px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
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
  color: #9E9BB0;
  font-size: 13px;
  font-weight: 400;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.header-right :deep(.scrape-button-wrapper) {
  padding: 0;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  height: 42px;
  border: none;
  border-radius: 8px;
  background: #5B8C5A;
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(91, 140, 90, 0.2);
  white-space: nowrap;
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

/* ── CONTENT ── */
.dashboard-content {
  padding: 24px 40px 40px 40px;
}

.source-badge-container {
  padding: 8px 0 16px 0;
}

.source-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #5C5A6B;
  font-size: 14px;
  font-weight: 500;
  background: #FFFFFF;
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid #E5E2DD;
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

/* ── GRIDS ── */
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

.table-section {
  margin-top: 8px;
}

/* ── MEDIA QUERIES ── */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 992px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .markets-grid {
    grid-template-columns: 1fr;
  }
  .row-2col {
    grid-template-columns: 1fr;
  }
  .dashboard-content {
    padding: 20px 20px 32px 20px;
  }
}

@media (max-width: 768px) {
  /* ✅ FIX: Use dynamic viewport height so the page doesn't "zoom"
     when the mobile browser's address bar shows/hides as the body's
     overflow is toggled by the burger menu. 100vh on mobile refers to
     the large viewport and doesn't shrink with the visible area,
     causing the sticky header + content to reflow awkwardly. */
  .dashboard-page {
    min-height: 100dvh;
  }

  .dashboard-header-bar {
    padding: 12px 16px;
    flex-direction: column;
    align-items: flex-start;
  }

  .header-left {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
    width: 100%;
  }

  .dashboard-header-bar h1 {
    font-size: 24px;
  }

  .last-updated {
    font-size: 12px;
  }

  .header-right {
    width: 100%;
    justify-content: flex-start;
    gap: 8px;
  }

  .header-right :deep(.scrape-button-wrapper) {
    flex: 1;
  }

  .header-right :deep(.scrape-btn) {
    width: 100%;
    justify-content: center;
  }

  .refresh-btn {
    flex: 1;
    justify-content: center;
    padding: 10px 16px;
    height: 42px;
    font-size: 14px;
  }

  .dashboard-content {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .stats-grid :deep(.stat-card) {
    padding: 16px;
  }

  .stats-grid :deep(.stat-value) {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .dashboard-page {
    min-height: 100dvh;
  }

  .dashboard-header-bar {
    padding: 10px 12px;
  }

  .dashboard-header-bar h1 {
    font-size: 20px;
  }

  .last-updated {
    font-size: 11px;
  }

  .header-left {
    flex-direction: column;
    align-items: flex-start;
    gap: 2px;
  }

  .header-right {
    flex-direction: column;
    width: 100%;
  }

  .header-right :deep(.scrape-button-wrapper) {
    width: 100%;
  }

  .refresh-btn {
    width: 100%;
    justify-content: center;
    padding: 10px 16px;
    height: 42px;
    font-size: 14px;
  }

  .dashboard-content {
    padding: 12px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .stats-grid :deep(.stat-card) {
    padding: 14px;
  }

  .stats-grid :deep(.stat-value) {
    font-size: 18px;
  }

  .source-badge {
    font-size: 12px;
    padding: 4px 12px;
  }

  .section-header h2 {
    font-size: 17px;
  }

  .section-subtitle {
    font-size: 12px;
  }
}
</style>