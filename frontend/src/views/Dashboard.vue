<template>
  <div class="dashboard">
    <h2>:bar_chart: Dashboard</h2>
    <p class="subtitle">Real-time market monitoring overview</p>

    <!-- Stat Cards -->
    <div class="stats-grid">
      <StatCard
        icon=":package:"
        label="TOTAL ITEMS"
        :value="statsStore.stats.total_items"
        sub="across 2 markets"
      />
      <StatCard
        icon=":globe_with_meridians:"
        label="ACTIVE SOURCES"
        :value="statsStore.stats.active_sites"
        sub="All active"
      />
      <StatCard
        icon=":white_check_mark:"
        label="SUCCESS RATE"
        :value="statsStore.stats.success_rate + '%'"
        sub="last 7 days"
      />
      <StatCard
        icon="⏱"
        label="LAST SCRAPE"
        value="02:33 PM"
        sub="Jul 20, 2026"
      />
    </div>

    <!-- Market Cards -->
    <div class="markets-grid">
      <MarketOverviewCard
        title=":shopping_trolley: Retail Goods"
        :itemCount="statsStore.stats.markets['Retail Goods']?.item_count || 0"
        :avgPrice="statsStore.stats.markets['Retail Goods']?.avg_price || 0"
        source="WebScraper.io"
        sourceItems="15"
        market="retail"
      />
      <MarketOverviewCard
        title="₿ Digital Assets"
        :itemCount="statsStore.stats.markets['Digital Assets']?.item_count || 0"
        :avgPrice="statsStore.stats.markets['Digital Assets']?.avg_price || 0"
        source="CoinGecko"
        sourceItems="10"
        market="crypto"
      />
    </div>

    <!-- Watchlist -->
    <div class="watchlist-section">
      <Watchlist />
    </div>

    <!-- Scrape Button with auto-refresh -->
    <div class="scrape-section">
      <ScrapeButton @scrape-complete="refreshAllData" />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useItemsStore } from '../stores/itemsStore'
import { useStatsStore } from '../stores/statsStore'
import StatCard from '../components/StatCard.vue'
import MarketOverviewCard from '../components/MarketOverviewCard.vue'
import Watchlist from '../components/Watchlist.vue'
import ScrapeButton from '../components/ScrapeButton.vue'

const itemsStore = useItemsStore()
const statsStore = useStatsStore()

// :white_check_mark: NEW: Refresh all data when scrape completes
const refreshAllData = async () => {
  await itemsStore.fetchItems()
  await statsStore.fetchStats()
}

onMounted(() => {
  itemsStore.fetchItems()
  statsStore.fetchStats()
})
</script>

<style scoped>
.dashboard {
  padding: 24px;
  background: #F7F5F2;
  min-height: 100vh;
}

h2 {
  color: #2D2A3E;
  margin-bottom: 4px;
}

.subtitle {
  color: #5C5A6B;
  margin-top: 0;
  margin-bottom: 32px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.markets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.watchlist-section {
  margin-bottom: 20px;
}

.scrape-section {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .markets-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>