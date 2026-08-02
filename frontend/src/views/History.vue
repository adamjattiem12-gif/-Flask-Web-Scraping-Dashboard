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

    <!-- ✅ NEW: Scrape Button - auto-refreshes history when scrape completes -->
    <div class="scrape-section">
      <ScrapeButton @scrape-complete="refreshHistory" />
    </div>

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
// ✅ NEW: Import ScrapeButton to add auto-refresh functionality
import ScrapeButton from '../components/ScrapeButton.vue'

const scrapeStore = useScrapeStore()
const history = ref([])
const loading = ref(false)

// ✅ NEW: This function now gets called by both the Refresh button AND scrape-complete event
const refreshHistory = async () => {
  loading.value = true
  try {
    // Pull the authoritative record from the backend (history.json) so the
    // page never shows stale or duplicate entries after a scrape.
    await scrapeStore.fetchHistory()
  } finally {
    history.value = scrapeStore.scrapeHistory
    loading.value = false
  }
}

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

onMounted(async () => {
  loading.value = true
  try {
    await scrapeStore.fetchHistory()
  } finally {
    history.value = scrapeStore.scrapeHistory
    loading.value = false
  }
})
</script>

<style scoped>
.history {
  padding: 24px;
  background: var(--color-bg);
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
  color: var(--color-text);
  margin-bottom: 4px;
}

.subtitle {
  color: var(--color-text-secondary);
  margin-top: 0;
  margin-bottom: 16px;
}

/* ✅ NEW: Spacing for ScrapeButton section */
.scrape-section {
  margin: 16px 0 24px 0;
}

.refresh-btn {
  background: var(--color-success);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.refresh-btn:hover {
  background: var(--color-success-strong);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.table-container {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th {
  background: var(--color-bg);
  color: var(--color-text);
  font-weight: 600;
  padding: 12px 16px;
  text-align: left;
  border-bottom: 2px solid var(--color-border);
}

td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-bg);
}

tr:hover td {
  background: var(--color-border-subtle);
}

.badge {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.badge-retail {
  background: var(--color-warning);
  color: white;
}

.badge-crypto {
  background: var(--color-info);
  color: white;
}

.status-success {
  color: var(--color-success);
  font-weight: 500;
}

.status-error {
  color: var(--color-danger);
  font-weight: 500;
}

.loading-state {
  text-align: center;
  padding: 40px;
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

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

.empty-state p {
  font-size: 18px;
  color: var(--color-text);
  margin: 0;
}

.empty-sub {
  color: var(--color-text-muted) !important;
  font-size: 14px !important;
  margin-top: 8px !important;
}

.week1-note {
  margin-top: 32px;
  padding: 16px 20px;
  background: var(--color-warning-bg);
  border: 1px solid var(--color-warning-strong);
  border-radius: 8px;
  color: var(--color-text-secondary);
  font-size: 14px;
}
</style>