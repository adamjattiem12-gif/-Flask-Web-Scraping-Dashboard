<template>
  <div class="websites-manager">
    <!-- PAGE HEADER -->
    <h2>📡 Monitored Websites</h2>
    <p class="subtitle">Websites that are currently being scraped for price data</p>

    <!-- LOADING STATE -->
    <div v-if="websitesStore.loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading websites...</p>
    </div>

    <!-- ERROR STATE -->
    <div v-else-if="websitesStore.error" class="error-state">
      <p>❌ {{ websitesStore.error }}</p>
      <button @click="websitesStore.fetchWebsites()">Retry</button>
    </div>

    <!-- WEBSITES GRID - Shows all monitored websites -->
    <div v-else class="websites-grid">
      <div 
        v-for="site in websitesStore.websites" 
        :key="site.id" 
        class="website-card"
      >
        <div class="website-header">
          <h3>{{ site.name }}</h3>
          <!-- Market badge - changes color based on market type -->
          <span 
            class="badge" 
            :class="site.market === 'Retail Goods' ? 'badge-retail' : 'badge-crypto'"
          >
            {{ site.market }}
          </span>
        </div>
        
        <div class="website-details">
          <p class="url">🔗 {{ site.url }}</p>
          <!-- Green dot shows website is active -->
          <span class="status status-active">● Active</span>
        </div>

        <div class="website-footer">
          <span class="last-scraped">Last scraped: {{ formatDate() }}</span>
        </div>
      </div>
    </div> 
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useWebsitesStore } from '../stores/websitesStore'

const websitesStore = useWebsitesStore()

// Helper function to format the current date
const formatDate = () => {
  return new Date().toLocaleString()
}

// Load websites when page loads
onMounted(() => {
  websitesStore.fetchWebsites()
})
</script>

<style scoped>
.websites-manager {
  padding: 24px;
  background: #F7F5F2;
  min-height: 100vh;
}

/* Page title styles */
h2 {
  color: #2D2A3E;
  margin-bottom: 4px;
}

.subtitle {
  color: #5C5A6B;
  margin-top: 0;
  margin-bottom: 32px;
}

/* Website cards grid - responsive layout */
.websites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

/* Individual website card */
.website-card {
  background: white;
  border: 1px solid #E5E2DD;
  border-radius: 8px;
  padding: 24px;
  transition: box-shadow 0.2s;
}

.website-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.website-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.website-header h3 {
  margin: 0;
  color: #2D2A3E;
  font-size: 16px;
}

/* Market badges */
.badge {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  white-space: nowrap;
}

.badge-retail {
  background: #D4914A;
  color: white;
}

.badge-crypto {
  background: #4A8C8C;
  color: white;
}

.website-details {
  margin-bottom: 16px;
}

.url {
  color: #5C5A6B;
  font-size: 14px;
  word-break: break-all;
  margin: 8px 0;
}

.status {
  font-size: 13px;
  padding: 2px 8px;
  border-radius: 12px;
}

.status-active {
  color: #5B8C5A;
}

.website-footer {
  border-top: 1px solid #F7F5F2;
  padding-top: 12px;
  font-size: 13px;
  color: #9E9BB0;
}

/* Loading state */
.loading-state {
  text-align: center;
  padding: 40px;
  color: #5C5A6B;
}

.spinner {
  border: 3px solid #F7F5F2;
  border-top: 3px solid #5B8C5A;
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

/* Error state */
.error-state {
  text-align: center;
  padding: 40px;
  color: #C1666B;
}

.error-state button {
  background: #5B8C5A;
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 12px;
}

.error-state button:hover {
  background: #4A7349;
}

/* Week 1 notice */
.week1-note {
  margin-top: 32px;
  padding: 16px 20px;
  background: #FFF8E7;
  border: 1px solid #F0E6D0;
  border-radius: 8px;
  color: #5C5A6B;
  font-size: 14px;
}
</style>