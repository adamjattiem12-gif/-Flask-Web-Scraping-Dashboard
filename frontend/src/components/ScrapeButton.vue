<template>
  <div class="scrape-button-wrapper">
    <button 
      @click="handleScrape" 
      :disabled="isLoading"
      :class="['scrape-btn', buttonClass]"
    >
      <span v-if="isLoading" class="spinner">⟳</span>
      <span v-else-if="status === 'success'">✓</span>
      <span v-else-if="status === 'error'">✗</span>
      {{ buttonText }}
    </button>
    
    <p v-if="message" :class="messageClass" class="status-message">
      {{ message }}
    </p>
    
    <p v-if="lastScrapeTime" class="last-scrape">
      Last scrape: {{ lastScrapeTime }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useScrapeStore } from '@/stores/scrapeStore'

// ✅ Initialize store INSIDE setup
const scrapeStore = useScrapeStore()

// Local state
const isLoading = ref(false)
const status = ref('idle') // idle | loading | success | error
const message = ref('')
const lastScrapeTime = ref('')

const buttonText = computed(() => {
  switch(status.value) {
    case 'loading': return 'Scraping...'
    case 'success': return 'Done!'
    case 'error': return 'Try Again'
    default: return '🔍 Scrape Now'
  }
})

const buttonClass = computed(() => {
  switch(status.value) {
    case 'loading': return 'btn-loading'
    case 'success': return 'btn-success'
    case 'error': return 'btn-error'
    default: return 'btn-idle'
  }
})

const messageClass = computed(() => {
  switch(status.value) {
    case 'success': return 'msg-success'
    case 'error': return 'msg-error'
    default: return 'msg-info'
  }
})

const emit = defineEmits(['scrape'])

const handleScrape = async () => {
  if (isLoading.value) return
  
  status.value = 'loading'
  isLoading.value = true
  message.value = 'Scraping in progress...'
  
  try {
    await scrapeStore.triggerScrape()
    status.value = 'success'
    message.value = 'Scrape completed successfully!'
    lastScrapeTime.value = new Date().toLocaleString()
    emit('scrape')
  } catch (error) {
    status.value = 'error'
    message.value = error.message || 'Scrape failed. Please try again.'
  } finally {
    isLoading.value = false
    
    // Auto-reset after 5 seconds
    setTimeout(() => {
      if (status.value !== 'loading') {
        status.value = 'idle'
        message.value = ''
      }
    }, 5000)
  }
}

onMounted(() => {
  // Load last scrape time from store if available
  if (scrapeStore.lastScrape) {
    lastScrapeTime.value = new Date(scrapeStore.lastScrape).toLocaleString()
  }
})
</script>

<style scoped>
.scrape-button-wrapper {
  padding: 0;
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
  background: #5B8C5A;
  color: white;
}

.btn-idle:hover {
  background: #4A7349;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(91, 140, 90, 0.3);
}

.btn-loading {
  background: #5B8C5A;
  color: white;
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-success {
  background: #5B8C5A;
  color: white;
}

.btn-error {
  background: #C1666B;
  color: white;
}

.btn-error:hover {
  background: #A85257;
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
  color: #5B8C5A;
}

.msg-error {
  color: #C1666B;
}

.msg-info {
  color: #4A8C8C;
}

.last-scrape {
  margin: 4px 0 0;
  font-size: 13px;
  color: #9E9BB0;
}
</style>