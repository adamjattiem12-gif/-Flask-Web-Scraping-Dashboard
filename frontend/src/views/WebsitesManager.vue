<!-- ============================================================ -->
<!-- FILE: frontend/src/views/WebsitesManager.vue -->
<!-- ============================================================ -->
<template>
  <div class="websites-manager">
    <h2>Monitored Websites</h2>
    <p class="subtitle">Websites that are currently being scraped for price data</p>

    <!-- Demo notice - clear and simple -->
    <div class="demo-notice">
      <p class="demo-title">DEMO VERSION</p>
      <p class="demo-description">
        Adding a website here will save it to the list, but it will not be scraped for data.
        This feature is for preview purposes only and does not affect the live scraping process.
      </p>
    </div>

    <form class="add-website-form" @submit.prevent="handleAdd">
      <h3>Add a website</h3>
      <div class="form-grid">
        <label>
          Name
          <input v-model.trim="form.name" type="text" placeholder="e.g. My News Source" required />
        </label>
        <label>
          Market
          <select v-model="form.market" required>
            <option disabled value="">Choose a market</option>
            <option value="Retail Goods">Retail Goods</option>
            <option value="Digital Assets">Digital Assets</option>
          </select>
        </label>
        <label class="url-field">
          URL
          <input v-model.trim="form.url" type="url" placeholder="https://example.com/target-page" required />
        </label>
      </div>
      <p v-if="websitesStore.saveError" class="form-error">{{ websitesStore.saveError }}</p>
      <button type="submit" class="add-btn" :disabled="websitesStore.saving">
        {{ websitesStore.saving ? 'Adding…' : 'Add Website' }}
      </button>
    </form>

    <div v-if="websitesStore.loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading websites...</p>
    </div>

    <div v-else-if="websitesStore.error" class="error-state">
      <p>{{ websitesStore.error }}</p>
      <button @click="websitesStore.fetchWebsites()">Retry</button>
    </div>

    <div v-else class="websites-grid">
      <p v-if="websitesStore.websites.length === 0" class="empty-state">
        No websites registered yet — add one above.
      </p>
      <div
        v-for="site in websitesStore.websites"
        :key="site.id"
        class="website-card"
        :class="{ 'demo-card': site.isDemo }"
      >
        <div class="website-header">
          <h3>{{ site.name }}</h3>
          <span
            class="badge"
            :class="site.market === 'Retail Goods' ? 'badge-retail' : 'badge-crypto'"
          >
            {{ site.market }}
          </span>
        </div>
        <div class="website-details">
          <p class="url">{{ site.url }}</p>
          <span class="status status-active">● Active</span>
          <!-- Demo badge on cards added via the form -->
          <span v-if="site.isDemo" class="demo-card-badge">Demo only</span>
        </div>
        <div class="website-footer">
          <span class="last-scraped">Last scraped: {{ formatDate() }}</span>
          <button
            class="remove-btn"
            :disabled="websitesStore.deletingId === site.id"
            @click="handleRemove(site)"
          >
            {{ websitesStore.deletingId === site.id ? 'Removing…' : 'Remove' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue'
import { useWebsitesStore } from '../stores/websitesStore'

const websitesStore = useWebsitesStore()

const form = reactive({
  name: '',
  url: '',
  market: ''
})

const formatDate = () => {
  return new Date().toLocaleString()
}

const handleAdd = async () => {
  try {
    await websitesStore.addWebsite({
      name: form.name,
      url: form.url,
      market: form.market,
      isDemo: true
    })
    form.name = ''
    form.url = ''
    form.market = ''
  } catch {
    // saveError is already set on the store
  }
}

const handleRemove = async (site) => {
  if (!window.confirm(`Remove "${site.name}" from monitored websites?`)) return
  try {
    await websitesStore.removeWebsite(site.id)
  } catch {
    // error is already set on the store
  }
}

onMounted(() => {
  websitesStore.fetchWebsites()
})
</script>

<style scoped>
.websites-manager {
  padding: 24px;
  background: var(--color-bg);
  min-height: 100vh;
}

h2 {
  color: var(--color-text);
  margin-bottom: 4px;
}

.subtitle {
  color: var(--color-text-muted);
  margin-bottom: 8px;
}

.demo-notice {
  background: var(--color-warning-bg);
  border-left: 4px solid var(--color-warning);
  padding: 12px 16px;
  margin-bottom: 24px;
  border-radius: 4px;
}

.demo-title {
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 2px 0;
  font-size: 14px;
}

.demo-description {
  color: var(--color-text-secondary);
  font-size: 13px;
  margin: 0;
  line-height: 1.5;
}

.demo-card-badge {
  display: inline-block;
  background: var(--color-warning-bg);
  color: var(--color-warning);
  font-size: 11px;
  padding: 2px 10px;
  border-radius: 12px;
  margin-left: 8px;
  font-weight: 500;
}

.demo-card {
  border: 1px solid var(--color-warning);
}

.empty-state {
  color: var(--color-text-muted);
  padding: 24px;
}

.add-website-form {
  background: var(--color-surface);
  border: 1px solid var(--color-border-subtle);
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 28px;
}

.add-website-form h3 {
  margin: 0 0 16px;
  font-size: 16px;
  color: var(--color-text);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-grid label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.url-field {
  grid-column: 1 / -1;
}

.form-grid input,
.form-grid select {
  padding: 10px 12px;
  border: 1px solid var(--color-border-subtle);
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  background: var(--color-surface);
  color: var(--color-text);
}

.form-error {
  color: var(--color-danger);
  font-size: 13px;
  margin: 12px 0 0;
}

.add-btn {
  margin-top: 16px;
  background: var(--color-success);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
}

.add-btn:hover:not(:disabled) {
  background: var(--color-success-strong);
}

.add-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.websites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.website-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border-subtle);
  border-radius: 12px;
  padding: 20px;
}

.website-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.website-header h3 {
  margin: 0;
  font-size: 15px;
  color: var(--color-text);
}

.badge {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 12px;
  white-space: nowrap;
}

.badge-retail {
  background: var(--color-success-bg);
  color: var(--color-success-strong);
}

.badge-crypto {
  background: var(--color-info-bg);
  color: var(--color-info-strong);
}

.website-details {
  margin: 8px 0;
}

.url {
  color: var(--color-text-secondary);
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
  color: var(--color-success);
}

.website-footer {
  border-top: 1px solid var(--color-bg);
  padding-top: 12px;
  font-size: 13px;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.remove-btn {
  background: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text-muted);
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-btn:hover:not(:disabled) {
  background: var(--color-danger-bg);
  border-color: var(--color-danger);
  color: var(--color-danger);
}

.remove-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

.error-state {
  text-align: center;
  padding: 40px;
  color: var(--color-danger);
}

.error-state button {
  background: var(--color-success);
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 12px;
}

.error-state button:hover {
  background: var(--color-success-strong);
}
</style>