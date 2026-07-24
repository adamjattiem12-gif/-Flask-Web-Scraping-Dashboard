<template>
  <div class="page-container">
    <h1>⭐ Watchlist</h1>
    <p>Save the products and assets you want to monitor here.</p>
    
    <!-- Loading State -->
    <div v-if="itemsStore.loading" class="loading">
      Loading watchlist...
    </div>
    
    <!-- Empty State -->
    <div v-else-if="watchedItems.length === 0" class="empty">
      <p>📭 No items in watchlist</p>
      <p class="hint">Click the ⭐ on items in the table to add them</p>
    </div>
    
    <!-- Watchlist Items -->
    <div v-else class="items-grid">
      <div v-for="item in watchedItems" :key="item.id" class="item-card">
        <h3>{{ item.name }}</h3>
        <p class="price">${{ item.price }}</p>
        <span class="badge" :class="item.market === 'Retail Goods' ? 'retail' : 'crypto'">
          {{ item.market }}
        </span>
        <button @click="watchlistStore.toggleWatch(item.id)" class="remove-btn">
          ✕ Remove
        </button>
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

const watchedItems = computed(() => {
  return watchlistStore.getWatchedItems(itemsStore)
})

onMounted(() => {
  itemsStore.fetchItems()
})
</script>

<style scoped>
.page-container {
  padding: 24px;
  background: #F7F5F2;
  min-height: 100vh;
}

h1 {
  color: #2D2A3E;
  margin-bottom: 4px;
}

p {
  color: #5C5A6B;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.item-card {
  background: white;
  border: 1px solid #E5E2DD;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-card h3 {
  margin: 0;
  color: #2D2A3E;
}

.price {
  font-size: 20px;
  font-weight: bold;
  color: #2D2A3E;
}

.badge {
  display: inline-block;
  padding: 2px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  width: fit-content;
}

.badge.retail {
  background: #D4914A;
  color: white;
}

.badge.crypto {
  background: #4A8C8C;
  color: white;
}

.remove-btn {
  background: #C1666B;
  color: white;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 8px;
}

.remove-btn:hover {
  background: #A85257;
}

.loading, .empty {
  text-align: center;
  padding: 40px;
  color: #9E9BB0;
}

.hint {
  font-size: 14px;
  margin-top: 4px;
}
</style>