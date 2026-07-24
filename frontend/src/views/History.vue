<template>
  <div class="history">
    <!-- PAGE HEADER -->
    <div class="history-header">
      <h2>📜 Scrape History</h2>
      <button 
        @click="refreshHistory" 
        class="refresh-btn"
        :disabled="loading"
      >
        🔄 Refresh
      </button>
    </div>
    <p class="subtitle">Log of all past scraping runs</p>

    <!-- LOADING STATE -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading history...</p>
    </div>

    <!-- EMPTY STATE -->
    <div v-else-if="history.length === 0" class="empty-state">
      <p>📭 No history yet</p>
      <p class="empty-sub">Run a scrape to see results here</p>
    </div>

    <!-- HISTORY TABLE -->
    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Date & Time</th>
            <th>Market</th>
            <th>Target</th>
            <th>Items Found</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in history" :key="record.timestamp">
            <td>{{ formatDate(record.timestamp) }}</td>
            <td>
              <span 
                class="badge" 
                :class="record.market === 'Retail Goods' ? 'badge-retail' : 'badge-crypto'"
              >
                {{ record.market }}
              </span>
            </td>
            <td>{{ record.target }}</td>
            <td>{{ record.items_found }}</td>
            <td>
              <span :class="record.success ? 'status-success' : 'status-error'">
                {{ record.success ? '✅ Success' : '❌ Failed' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useScrapeStore } from '../stores/scrapeStore'

const scrapeStore = useScrapeStore()
const history = ref([])
const loading = ref(false)

/**
 * refreshHistory - Loads history from the store
 */
const refreshHistory = async () => {
  loading.value = true
  await new Promise(resolve => setTimeout(resolve, 300))
  history.value = scrapeStore.scrapeHistory
  loading.value = false
}

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

onMounted(() => {
  // Only generate if history is empty
  if (scrapeStore.scrapeHistory.length === 0) {
    scrapeStore.generateMockHistory()
  }
  history.value = scrapeStore.scrapeHistory
})
</script>

<style scoped>
.history {
  padding: 24px;
  background: #F7F5F2;
  min-height: 100vh;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
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

.refresh-btn {
  background: #5B8C5A;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.refresh-btn:hover {
  background: #4A7349;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.table-container {
  background: white;
  border: 1px solid #E5E2DD;
  border-radius: 8px;
  overflow: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th {
  background: #F7F5F2;
  color: #2D2A3E;
  font-weight: 600;
  padding: 12px 16px;
  text-align: left;
  border-bottom: 2px solid #E5E2DD;
}

td {
  padding: 12px 16px;
  border-bottom: 1px solid #F7F5F2;
}

tr:hover td {
  background: #FAF9F7;
}

.badge {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.badge-retail {
  background: #D4914A;
  color: white;
}

.badge-crypto {
  background: #4A8C8C;
  color: white;
}

.status-success {
  color: #5B8C5A;
  font-weight: 500;
}

.status-error {
  color: #C1666B;
  font-weight: 500;
}

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

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border: 1px solid #E5E2DD;
  border-radius: 8px;
}

.empty-state p {
  font-size: 18px;
  color: #2D2A3E;
  margin: 0;
}

.empty-sub {
  color: #9E9BB0 !important;
  font-size: 14px !important;
  margin-top: 8px !important;
}

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