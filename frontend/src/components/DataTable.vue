<template>
  <div class="data-table-wrapper">
    <!-- Error state -->
    <div v-if="error" class="table-message error-message">
      <p>{{ error }}</p>
      <button class="retry-btn" @click="$emit('retry')">Retry</button>
    </div>

    <!-- Table -->
    <table v-else class="data-table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" @click="col.sortable !== false && sortBy(col.key)">
            {{ col.label }}
            <span v-if="sortKey === col.key" class="sort-arrow">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <!-- Skeleton rows while loading -->
        <template v-if="loading">
          <tr v-for="n in 5" :key="'skeleton-' + n" class="skeleton-row">
            <td v-for="col in columns" :key="col.key">
              <div class="skeleton-cell"></div>
            </td>
          </tr>
        </template>

        <!-- Empty state -->
        <tr v-else-if="sortedItems.length === 0">
          <td :colspan="columns.length" class="empty-state">
            <p class="empty-title">No results found</p>
            <p class="empty-subtitle">Try adjusting your search or filters</p>
          </td>
        </tr>

        <!-- Real data -->
        <tr v-else v-for="item in paginatedItems" :key="item.id ?? item.name + (item.scraped_at || item.scrapedAt)">
          <td>{{ item.name }}</td>
          <td>{{ formatCurrency(item.price, item.currency) }}</td>
          <td>{{ item.currency || 'USD' }}</td>
          <td>
            <span class="source-badge" :class="getSourceClass(item.source)">
              {{ item.source }}
            </span>
          </td>
          <td>{{ getScrapedTime(item) }}</td>
          <td class="watchlist-cell">
            <button
              class="watch-btn"
              :class="{ watched: watchlistStore.isWatched(item.id) }"
              :aria-label="watchlistStore.isWatched(item.id) ? 'Remove from watchlist' : 'Add to watchlist'"
              @click="watchlistStore.toggleWatch(item.id)"
            >
              {{ watchlistStore.isWatched(item.id) ? '★' : '☆' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div v-if="!error && !loading && totalPages > 1" class="pagination">
      <button
        class="page-btn"
        :disabled="currentPage <= 1"
        @click="goToPage(currentPage - 1)"
      >
        Previous
      </button>

      <button
        v-for="page in pageNumbers"
        :key="page"
        class="page-btn"
        :class="{ active: page === currentPage }"
        @click="goToPage(page)"
      >
        {{ page }}
      </button>

      <button
        class="page-btn"
        :disabled="currentPage >= totalPages"
        @click="goToPage(currentPage + 1)"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useWatchlistStore } from '@/stores/watchlistStore'

const watchlistStore = useWatchlistStore()

const props = defineProps({
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
  currentPage: { type: Number, default: 1 },
  totalPages: { type: Number, default: 1 },
  onPageChange: { type: Function, default: null },
})

const emit = defineEmits(['retry', 'page-change'])

const columns = [
  { key: 'name', label: 'Name' },
  { key: 'price', label: 'Price' },
  { key: 'currency', label: 'Currency' },
  { key: 'source', label: 'Source' },
  { key: 'scraped_at', label: 'Scraped At' },
  { key: 'watchlist', label: 'Watch', sortable: false },
]

const pageSize = 10

const sortKey = ref('')
const sortOrder = ref('asc')

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

const sortedItems = computed(() => {
  if (!sortKey.value) return props.items

  const key = sortKey.value
  const dir = sortOrder.value === 'asc' ? 1 : -1

  return [...props.items].sort((a, b) => {
    let valA = a[key]
    let valB = b[key]

    if (key === 'price') {
      return (Number(valA) - Number(valB)) * dir
    }

    if (key === 'scraped_at') {
      const dateA = new Date(getScrapedTimeRaw(a))
      const dateB = new Date(getScrapedTimeRaw(b))
      return (dateA - dateB) * dir
    }

    valA = String(valA ?? '').toLowerCase()
    valB = String(valB ?? '').toLowerCase()
    if (valA < valB) return -1 * dir
    if (valA > valB) return 1 * dir
    return 0
  })
})

const paginatedItems = computed(() => {
  const start = (props.currentPage - 1) * pageSize
  return sortedItems.value.slice(start, start + pageSize)
})

const pageNumbers = computed(() => {
  const pages = []
  for (let i = 1; i <= props.totalPages; i++) pages.push(i)
  return pages
})

const getSourceClass = (source) => {
  if (source === 'WebScraper.io' || source === 'WebScraper.io E-Commerce') return 'source-retail'
  if (source === 'CoinPaprika') return 'source-crypto'
  return 'source-default'
}

const getScrapedTimeRaw = (item) => {
  return item.scraped_at || item.scrapedAt || item.last_scrape || item.updated_at || null
}

const getScrapedTime = (item) => {
  const timestamp = getScrapedTimeRaw(item)
  if (!timestamp) return '—'
  try {
    const date = new Date(timestamp)
    if (isNaN(date.getTime())) return '—'
    return date.toLocaleString()
  } catch {
    return '—'
  }
}

const goToPage = (page) => {
  if (page < 1 || page > props.totalPages || page === props.currentPage) return
  if (props.onPageChange) props.onPageChange(page)
  emit('page-change', page)
}

const formatCurrency = (price, currency) => {
  if (price === null || price === undefined) return '—'
  try {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: currency || 'USD',
    }).format(price)
  } catch {
    return `${currency || 'USD'} ${Number(price).toFixed(2)}`
  }
}
</script>

<style scoped>
.data-table-wrapper {
  width: 100%;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  overflow: hidden;
}

.data-table th {
  text-align: left;
  padding: 12px 16px;
  background: var(--color-border-subtle);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
  cursor: pointer;
  user-select: none;
  border-bottom: 1px solid var(--color-border);
}

.data-table th:hover {
  color: var(--color-success);
}

.sort-arrow {
  font-size: 10px;
  margin-left: 4px;
}

.data-table td {
  padding: 12px 16px;
  font-size: 14px;
  color: var(--color-text);
  border-bottom: 1px solid var(--color-border-subtle);
}

.watchlist-cell {
  text-align: center;
  width: 70px;
}

.watch-btn {
  border: 0;
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  font-size: 22px;
  line-height: 1;
  padding: 2px 6px;
}

.watch-btn:hover,
.watch-btn.watched {
  color: var(--color-warning);
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

.source-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.source-retail {
  background: var(--color-success-bg);
  color: var(--color-success-strong);
}

.source-crypto {
  background: var(--color-info-bg);
  color: var(--color-info-strong);
}

.source-default {
  background: var(--color-border-subtle);
  color: var(--color-text-secondary);
}

.skeleton-cell {
  height: 14px;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--color-border-subtle) 25%, var(--color-border) 50%, var(--color-border-subtle) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

@keyframes shimmer {
  from { background-position: 200% 0; }
  to { background-position: -200% 0; }
}

.empty-state {
  text-align: center;
  padding: 40px 16px;
}

.empty-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin: 0 0 4px;
}

.empty-subtitle {
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
}

.table-message.error-message {
  text-align: center;
  padding: 32px 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  color: var(--color-danger);
}

.retry-btn {
  margin-top: 12px;
  padding: 8px 20px;
  border: none;
  border-radius: 6px;
  background: var(--color-danger);
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.retry-btn:hover {
  background: var(--color-danger-strong);
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-top: 16px;
}

.page-btn {
  padding: 6px 12px;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  color: var(--color-text-secondary);
}

.page-btn:hover:not(:disabled) {
  border-color: var(--color-success);
  color: var(--color-success);
}

.page-btn.active {
  background: var(--color-success);
  border-color: var(--color-success);
  color: white;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
