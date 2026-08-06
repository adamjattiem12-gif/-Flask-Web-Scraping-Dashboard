<template>
  <div class="page-container">
    <h1> Retail Goods</h1>
    <p class="subtitle">Track prices, availability, and changes for your retail sources here.</p>

    <!-- Scrape Button with auto-refresh -->
    <div class="scrape-section">
      <ScrapeButton @scrape-complete="refreshRetailItems" />
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
          <!-- ✅ STAR ICON REMOVED -->
          <!-- <span class="badge">⭐ {{ item.extra?.rating || 'N/A' }}</span> -->
        </div>
        <p class="price">${{ item.price }}</p>
        <p class="source">{{ item.source }}</p>
        <p class="review-count">{{ item.extra?.review_count || 0 }} reviews</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useItemsStore } from '../stores/itemsStore'
import ScrapeButton from '../components/ScrapeButton.vue'

const itemsStore = useItemsStore()
const retailItems = computed(() => itemsStore.getRetailItems)

// Refresh retail items when scrape completes
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
  flex: 1;
}

/* ✅ Badge removed - no longer needed */
/* .badge {
  display: inline-block;
  background: #D4914A;
  color: white;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  white-space: nowrap;
} */

.price {
  font-size: 24px;
  font-weight: bold;
  color: #D4914A;
  margin: 8px 0 4px 0;
}

.source {
  color: #5C5A6B;
  font-size: 14px;
  margin: 4px 0;
}

.review-count {
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
  border-top: 3px solid #D4914A;
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

/* ✅ Responsive */
@media (max-width: 768px) {
  .page-container {
    padding: 16px;
  }
  
  h1 {
    font-size: 24px;
  }
  
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }
  
  .item-card {
    padding: 16px;
  }
  
  .price {
    font-size: 20px;
  }
}

@media (max-width: 375px) {
  .page-container {
    padding: 12px;
  }
  
  h1 {
    font-size: 20px;
  }
  
  .items-grid {
    grid-template-columns: 1fr;
  }
}
</style>