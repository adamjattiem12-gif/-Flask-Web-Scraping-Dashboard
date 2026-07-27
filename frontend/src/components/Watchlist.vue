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

// ✅ CORRECT: Import the store function, but don't call it at the top level
import { useWatchlistStore } from '@/stores/watchlistStore'
import { useItemsStore } from '@/stores/itemsStore'

// ✅ CORRECT: Call useStore() INSIDE a function that runs after Pinia is installed
// Option 1: Inside a computed property
const watchedItems = computed(() => {
  const watchlistStore = useWatchlistStore()
  const itemsStore = useItemsStore()
  return watchlistStore.getWatchedItems(itemsStore)
})

// Option 2: Inside a method
const removeFromWatchlist = (id) => {
  const watchlistStore = useWatchlistStore()
  watchlistStore.toggleWatch(id)
}

// Option 3: Inside onMounted lifecycle hook
onMounted(() => {
  const itemsStore = useItemsStore()
  itemsStore.fetchItems()
})

// Loading state
const loading = ref(false)
</script>

<style scoped>
/* ... your existing styles ... */
</style>