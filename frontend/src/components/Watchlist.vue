<template>
  <div class="watchlist">
    <div class="watchlist-header">
      <h3 class="section-title">Watchlist</h3>
      <span class="item-count">{{ watchedItems.length }} items</span>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading watchlist...</p>
    </div>
    
    <!-- Empty State -->
    <div v-else-if="watchedItems.length === 0" class="empty-state">
      <p>No items in watchlist</p>
      <p class="hint">Click the ⭐ on items in the table to add them</p>
    </div>
    
    <!-- Watchlist Items -->
    <div v-else class="watchlist-items">
      <div v-for="(item, index) in watchedItems" :key="item.id" class="watchlist-item">
        <span class="watch-rank">{{ String(index + 1).padStart(2, '0') }}</span>
        <span class="watch-name">{{ item.name }}</span>
        <span class="watch-price">${{ item.price.toFixed(2) }}</span>
        <span class="watch-change" :class="item.change >= 0 ? 'positive' : 'negative'">
          {{ item.change >= 0 ? '+' : '' }}{{ item.change }}%
        </span>
        <button @click="removeFromWatchlist(item.id)" class="remove-btn" title="Remove from watchlist">
          ✕
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useWatchlistStore } from '@/stores/watchlistStore'
import { useItemsStore } from '@/stores/itemsStore'

// ✅ Call stores INSIDE functions, not at top level
const loading = ref(false)

// ✅ Computed property calls store INSIDE the function
const watchedItems = computed(() => {
  const watchlistStore = useWatchlistStore()
  const itemsStore = useItemsStore()
  return watchlistStore.getWatchedItems(itemsStore)
})

// ✅ Method calls store INSIDE the function
const removeFromWatchlist = (id) => {
  const watchlistStore = useWatchlistStore()
  watchlistStore.toggleWatch(id)
}

// ✅ Load data on mount
onMounted(() => {
  loading.value = true
  const itemsStore = useItemsStore()
  itemsStore.fetchItems()
  loading.value = false
})
</script>

<style scoped>
.watchlist {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 20px 24px;
  min-height: 200px;
}

.watchlist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  color: var(--color-text);
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.item-count {
  color: var(--color-text-muted);
  font-size: 13px;
  background: var(--color-bg);
  padding: 2px 12px;
  border-radius: 20px;
}

/* ✅ EMPTY STATE - MATCHES RIGHT SIDE */
.empty-state {
  text-align: center;
  padding: 20px 0;
  color: var(--color-text-secondary);
}

.empty-state p {
  margin: 0;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.hint {
  font-size: 13px !important;
  margin-top: 4px !important;
  color: var(--color-text-muted) !important;
}

/* ✅ WATCHLIST ITEMS */
.watchlist-items {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.watchlist-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 8px;
  background: var(--color-bg);
  font-size: 14px;
}

.watch-rank {
  color: var(--color-text-muted);
  font-weight: 600;
  width: 28px;
  font-size: 13px;
}

.watch-name {
  flex: 1;
  font-weight: 500;
  color: var(--color-text);
  font-size: 14px;
}

.watch-price {
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 14px;
}

.watch-change {
  font-weight: 600;
  min-width: 60px;
  text-align: right;
  font-size: 14px;
}

.watch-change.positive {
  color: var(--color-success);
}

.watch-change.negative {
  color: var(--color-danger);
}

.remove-btn {
  background: none;
  border: none;
  color: var(--color-danger);
  cursor: pointer;
  font-size: 14px;
  padding: 0 4px;
  transition: all 0.2s;
  opacity: 0.6;
}

.remove-btn:hover {
  opacity: 1;
  color: var(--color-danger-strong);
  transform: scale(1.2);
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 30px 0;
  color: var(--color-text-muted);
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid var(--color-bg);
  border-top: 3px solid var(--color-success);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 12px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>