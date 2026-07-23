<template>
  <div class="watchlist">
    <!-- HEADER -->
    <div class="watchlist-header">
      <h3>⭐ Watchlist</h3>
      <span class="count">{{ watchedItems.length }} items</span>
    </div>

    <!-- LOADING STATE -->
    <div v-if="itemsStore.loading" class="loading">
      Loading watchlist...
    </div>

    <!-- EMPTY STATE - No items in watchlist -->
    <div v-else-if="watchedItems.length === 0" class="empty-state">
      <p>No items in watchlist</p>
      <p class="hint">Click the ⭐ on items in the table to add them</p>
    </div>

    <!-- WATCHLIST ITEMS -->
    <div v-else class="watchlist-items">
      <div 
        v-for="item in watchedItems" 
        :key="item.id" 
        class="watchlist-item"
      >
        <div class="item-info">
          <div class="item-name">{{ item.name }}</div>
          <div class="item-market">
            <span 
              class="market-badge"
              :class="item.market === 'Retail Goods' ? 'badge-retail' : 'badge-crypto'"
            >
              {{ item.market }}
            </span>
          </div>
        </div>
        
        <div class="item-price-info">
          <span class="item-price">${{ item.price }}</span>
          <!-- Price change with arrow (mock data) -->
          <span 
            class="price-change" 
            :class="getPriceChange(item).direction"
          >
            {{ getPriceChange(item).arrow }} {{ getPriceChange(item).percent }}%
          </span>
          <!-- Remove button -->
          <button 
            @click="watchlistStore.toggleWatch(item.id)" 
            class="remove-btn"
            title="Remove from watchlist"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useWatchlistStore } from '../stores/watchlistStore'
import { useItemsStore } from '../stores/itemsStore'

const watchlistStore = useWatchlistStore()
const itemsStore = useItemsStore()

/**
 * watchedItems - Gets full item objects for all watched items
 * Used by: Template to display watchlist items
 */
const watchedItems = computed(() => {
  return itemsStore.items.filter(item => 
    watchlistStore.isWatched(item.id)
  )
})

/**
 * getPriceChange - Generates random price change for demo
 * ⚠️ Week 1: Random values for demonstration
 * Week 2: Will use real price change data from API
 */
const getPriceChange = (item) => {
  // Generate random price change between -15% and +15%
  const percent = (Math.random() * 30) - 15
  const direction = percent >= 0 ? 'up' : 'down'
  return {
    direction: direction,
    arrow: percent >= 0 ? '↑' : '↓',
    percent: Math.abs(percent).toFixed(1)
  }
}

// Add default items to watchlist on load (for demo)
onMounted(() => {
  if (watchlistStore.watchedIds.length === 0) {
    watchlistStore.toggleWatch(1)   // Asus VivoBook
    watchlistStore.toggleWatch(11)  // Bitcoin
  }
})
</script>

<style scoped>
.watchlist {
  background: white;
  border: 1px solid #E5E2DD;
  border-radius: 8px;
  padding: 20px;
  min-height: 200px;
}

.watchlist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #F7F5F2;
}

.watchlist-header h3 {
  margin: 0;
  color: #2D2A3E;
  font-size: 16px;
}

.count {
  background: #F7F5F2;
  padding: 2px 12px;
  border-radius: 12px;
  font-size: 13px;
  color: #5C5A6B;
}

.watchlist-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.watchlist-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: #FAF9F7;
  border-radius: 6px;
  transition: background 0.2s;
}

.watchlist-item:hover {
  background: #F7F5F2;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 14px;
  color: #2D2A3E;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-market {
  margin-top: 2px;
}

.market-badge {
  font-size: 11px;
  padding: 2px 10px;
  border-radius: 3px;
  font-weight: 600;
}

.badge-retail {
  background: #D4914A;
  color: white;
}

.badge-crypto {
  background: #4A8C8C;
  color: white;
}

.item-price-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.item-price {
  font-size: 15px;
  font-weight: 600;
  color: #2D2A3E;
}

.price-change {
  font-size: 13px;
  font-weight: 500;
  min-width: 60px;
  text-align: right;
}

.price-change.up {
  color: #5B8C5A;
}

.price-change.down {
  color: #C1666B;
}

.remove-btn {
  background: none;
  border: none;
  color: #9E9BB0;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: #F7F5F2;
  color: #C1666B;
}

.empty-state {
  text-align: center;
  padding: 30px 20px;
  color: #9E9BB0;
}

.empty-state p {
  margin: 0;
}

.empty-state .hint {
  font-size: 13px;
  margin-top: 4px;
}

.loading {
  text-align: center;
  padding: 30px;
  color: #9E9BB0;
}
</style>