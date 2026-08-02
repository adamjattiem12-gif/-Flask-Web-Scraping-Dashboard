<template>
  <div class="scrape-button-wrapper">
    <button 
      @click="handleScrape" 
      :disabled="scrapeStore.status === 'loading'"
      :class="['scrape-btn', buttonClass]"
    >
      <span v-if="scrapeStore.status === 'loading'" class="spinner">⟳</span>
      <span v-else-if="scrapeStore.status === 'success'">✓</span>
      <span v-else-if="scrapeStore.status === 'error'">✗</span>
      {{ buttonText }}
    </button>
    
    <p v-if="scrapeStore.message" :class="messageClass" class="status-message">
      {{ scrapeStore.message }}
    </p>
    
    <p v-if="scrapeStore.lastScrape" class="last-scrape">
      Last scrape: {{ formatTime(scrapeStore.lastScrape) }}
    </p>
  </div>
</template>

<script setup>
import { computed, defineEmits, defineProps } from 'vue'
import { useScrapeStore } from '../stores/scrapeStore'

// ✅ NEW: Emit event so parent components know when scrape is complete
// Used by: Dashboard, History, RetailGoods, DigitalAssets to auto-refresh
const emit = defineEmits(['scrape-complete'])

// Optional: pass market="Retail Goods" or market="Digital Assets" to scrape
// only that market. Omit (or pass null) to scrape both, as before.
const props = defineProps({
  market: {
    type: String,
    default: null
  }
})

const scrapeStore = useScrapeStore()

const buttonText = computed(() => {
  switch(scrapeStore.status) {
    case 'loading': return 'Scraping...'
    case 'success': return 'Done!'
    case 'error': return 'Try Again'
    default: return '🔍 Scrape Now'
  }
})

const buttonClass = computed(() => {
  switch(scrapeStore.status) {
    case 'loading': return 'btn-loading'
    case 'success': return 'btn-success'
    case 'error': return 'btn-error'
    default: return 'btn-idle'
  }
})

const messageClass = computed(() => {
  switch(scrapeStore.status) {
    case 'success': return 'msg-success'
    case 'error': return 'msg-error'
    default: return 'msg-info'
  }
})

const handleScrape = async () => {
  await scrapeStore.triggerScrape(props.market)
  
  // ✅ NEW: After successful scrape, tell parent to refresh its data
  if (scrapeStore.status === 'success') {
    emit('scrape-complete')
  }
  
  if (scrapeStore.status === 'success' || scrapeStore.status === 'error') {
    setTimeout(() => {
      scrapeStore.resetStatus()
    }, 5000)
  }
}

const formatTime = (date) => {
  return new Date(date).toLocaleString()
}
</script>

<style scoped>
.scrape-button-wrapper {
  padding: 16px 0;
}

.scrape-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 32px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 180px;
  justify-content: center;
}

.btn-idle {
  background: var(--color-success);
  color: white;
}

.btn-idle:hover {
  background: var(--color-success-strong);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(91, 140, 90, 0.3);
}

.btn-loading {
  background: var(--color-success);
  color: white;
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-success {
  background: var(--color-success);
  color: white;
}

.btn-error {
  background: var(--color-danger);
  color: white;
}

.btn-error:hover {
  background: var(--color-danger-strong);
}

.spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
  font-size: 20px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.status-message {
  margin: 8px 0 0;
  font-size: 14px;
  font-weight: 500;
}

.msg-success {
  color: var(--color-success);
}

.msg-error {
  color: var(--color-danger);
}

.msg-info {
  color: var(--color-info);
}

.last-scrape {
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--color-text-muted);
}
</style>