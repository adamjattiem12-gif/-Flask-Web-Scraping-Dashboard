<template>
  <div class="page-container">
    <h1>₿ Digital Assets</h1>
    <p class="subtitle">Track digital-asset prices and market movements here.</p>

    <!-- Scrape Button with auto-refresh -->
    <div class="scrape-section">
      <ScrapeButton @scrape-complete="refreshCryptoItems" />
    </div>

    <!-- Loading State -->
    <div v-if="itemsStore.loading" class="loading">
      <div class="spinner"></div>
      <p>Loading digital assets...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="itemsStore.error" class="error">
      :x: {{ itemsStore.error }}
    </div>

    <!-- Items Grid -->
    <div v-else class="items-grid">
      <div v-for="item in cryptoItems" :key="item.id" class="item-card">
        <div class="item-header">
          <h3>{{ item.name }}</h3>
          <span class="badge">{{ item.source }}</span>
        </div>
        <p class="price">${{ item.price.toLocaleString() }}</p>
        <p class="change" :class="item.extra?.change_24h >= 0 ? 'up' : 'down'">
          {{ item.extra?.change_24h >= 0 ? '▲' : '▼' }} {{ Math.abs(item.extra?.change_24h || 0) }}% (24h)
        </p>
        <p class="volume">Volume: ${{ (item.extra?.volume || 0).toLocaleString() }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useItemsStore } from '../stores/itemsStore'
import ScrapeButton from '../components/ScrapeButton.vue'

const itemsStore = useItemsStore()
const cryptoItems = computed(() => itemsStore.getCryptoItems)

// :white_check_mark: NEW: Refresh crypto items when scrape completes
const refreshCryptoItems = async () => {
  await itemsStore.fetchItems()
}

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
  font-size: 28px;
  margin-bottom: 4px;
}

.subtitle {
  color: #5C5A6B;
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
  background: white;
  border: 1px solid #E5E2DD;
  border-radius: 8px;
  padding: 24px;
  transition: all 0.2s ease;
  border-top: 4px solid #4A8C8C;
}

.item-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
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
  color: #2D2A3E;
  font-size: 16px;
  font-weight: 600;
}

.badge {
  display: inline-block;
  background: #4A8C8C;
  color: white;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
  white-space: nowrap;
}

.price {
  font-size: 24px;
  font-weight: bold;
  color: #4A8C8C;
  margin: 8px 0 4px 0;
}

.change {
  font-size: 16px;
  font-weight: 600;
  margin: 4px 0;
}

.change.up {
  color: #5B8C5A;
}

.change.down {
  color: #C1666B;
}

.volume {
  color: #9E9BB0;
  font-size: 13px;
  margin: 4px 0 0 0;
}

.loading {
  text-align: center;
  padding: 60px 20px;
  color: #5C5A6B;
}

.spinner {
  border: 3px solid #F7F5F2;
  border-top: 3px solid #4A8C8C;
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
  color: #C1666B;
}
</style>