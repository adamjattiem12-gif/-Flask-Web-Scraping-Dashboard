<template>
  <div class="watchlist">
    <div class="watchlist-header">
      <h3 class="section-title">⭐ Watchlist</h3>
      <span class="item-count">{{ watchedItems.length }} items</span>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading watchlist...</p>
    </div>
    
    <!-- Empty State -->
    <div v-else-if="watchedItems.length === 0" class="empty-state">
      <p>📭 No items in watchlist</p>
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
// const watchlistStore = useWatchlistStore()  // ❌ Remove this
// const itemsStore = useItemsStore()          // ❌ Remove this

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
  background: #FFFFFF;
  border: 1px solid #E5E2DD;
  border-radius: 12px;
  padding: 20px 24px;
  min-height: 200px;
}

.watchlist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-title {
  color: #2D2A3E;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.item-count {
  color: #9E9BB0;
  font-size: 13px;
  background: #F7F5F2;
  padding: 2px 12px;
  border-radius: 20px;
}

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
  background: #F7F5F2;
  font-size: 14px;
}

.watch-rank {
  color: #9E9BB0;
  font-weight: 600;
  width: 28px;
}

.watch-name {
  flex: 1;
  font-weight: 500;
  color: #2D2A3E;
}

.watch-price {
  color: #5C5A6B;
  font-weight: 500;
}

.watch-change {
  font-weight: 600;
  min-width: 60px;
  text-align: right;
}

.watch-change.positive {
  color: #5B8C5A;
}

.watch-change.negative {
  color: #C1666B;
}

.remove-btn {
  background: none;
  border: none;
  color: #C1666B;
  cursor: pointer;
  font-size: 16px;
  padding: 0 4px;
  transition: all 0.2s;
}

.remove-btn:hover {
  color: #A85257;
  transform: scale(1.2);
}

.loading-state {
  text-align: center;
  padding: 30px 0;
  color: #9E9BB0;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #F7F5F2;
  border-top: 3px solid #5B8C5A;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 12px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 30px 0;
  color: #9E9BB0;
}

.empty-state p {
  margin: 0;
  font-size: 15px;
}

.hint {
  font-size: 13px !important;
  margin-top: 4px !important;
  color: #C5C5D0 !important;
}
</style>