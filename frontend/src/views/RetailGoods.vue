<template>
  <div class="page-container">
    <h1>🛒 Retail Goods</h1>
    <p class="subtitle">Track prices, availability, and changes for your retail sources here.</p>

    <!-- Scrape Button - scoped to Retail Goods only -->
    <div class="scrape-section">
      <ScrapeButton market="Retail Goods" @scrape-complete="refreshRetailItems" />
    </div>

    <!-- Loading State -->
    <div v-if="itemsStore.loading" class="loading">
      <div class="spinner"></div>
      <p>Loading retail items...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="itemsStore.error" class="error">
      ❌ {{ itemsStore.error }}
    </div>
    
    <!-- Items Grid -->
    <div v-else class="items-grid">
      <div v-for="item in retailItems" :key="item.id" class="item-card">
        <div class="item-header">
          <h3>{{ item.name }}</h3>
        </div>
        <p class="price">${{ item.price }}</p>
        <p class="source">{{ item.source }}</p>
        <p class="review-count">{{ item.extra?.review_count || 0 }} reviews</p>
        <button class="watch-btn" :class="{ watched: watchlistStore.isWatched(item.id) }" @click="watchlistStore.toggleWatch(item.id)">
          {{ watchlistStore.isWatched(item.id) ? '★ In Watchlist' : '☆ Add to Watchlist' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useItemsStore } from '../stores/itemsStore'
import { useWatchlistStore } from '../stores/watchlistStore'
import ScrapeButton from '../components/ScrapeButton.vue'

const itemsStore = useItemsStore()
const watchlistStore = useWatchlistStore()
const retailItems = computed(() => itemsStore.getRetailItems)

const refreshRetailItems = async () => {
  await itemsStore.fetchItems()
}

onMounted(() => {
  itemsStore.fetchItems()
})
</script>

<style scoped>
.page-container {
  padding: 24px;
  background: var(--color-bg);
  min-height: 100vh;
}

h1 {
  color: var(--color-text);
  font-size: 28px;
  margin-bottom: 4px;
}

.subtitle {
  color: var(--color-text-secondary);
  font-size: 16px;
  margin-top: 0;
  margin-bottom: 32px;
}

.scrape-section {
  margin: 16px 0 24px 0;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.item-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 24px;
  transition: all 0.2s ease;
}

.item-card:hover {
  box-shadow: 0 4px 12px var(--color-shadow);
  transform: translateY(-2px);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.item-header h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 16px;
  font-weight: 600;
}

.badge {
  display: inline-block;
  background: var(--color-warning);
  color: white;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  white-space: nowrap;
}

.price {
  font-size: 24px;
  font-weight: bold;
  color: var(--color-warning);
  margin: 8px 0 4px 0;
}

.source {
  color: var(--color-text-secondary);
  font-size: 14px;
  margin: 4px 0;
}

.review-count {
  color: var(--color-text-muted);
  font-size: 13px;
  margin: 4px 0 0 0;
}

.watch-btn {
  margin-top: 14px;
  padding: 8px 12px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
}
.watch-btn.watched { color: var(--color-warning); border-color: var(--color-warning); }

.loading {
  text-align: center;
  padding: 60px 20px;
  color: var(--color-text-secondary);
}

.spinner {
  border: 3px solid var(--color-bg);
  border-top: 3px solid var(--color-success);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 40px;
  color: var(--color-danger);
}
</style>
