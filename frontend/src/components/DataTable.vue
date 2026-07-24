<template>
  <div class="data-table-wrapper">
    <!-- Error state -->
    <div v-if="error" class="table-message error-message">
      <p>{{ error }}</p>
      <button class="retry-btn" @click="$emit('retry')">Retry</button>
    </div>

    <!-- Loading state -->
    <table v-else class="data-table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" @click="sortBy(col.key)">
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
        <tr v-else v-for="item in sortedItems" :key="item.id ?? item.name + item.scraped_at">
          <td>{{ item.name }}</td>
          <td>{{ formatCurrency(item.price, item.currency) }}</td>
          <td>{{ item.currency }}</td>
          <td>
            <span class="source-badge" :class="'source-' + item.source">{{ item.source }}</span>
          </td>
          <td>{{ formatTimestamp(item.scraped_at) }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination controls -->
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
]

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

    // Numeric sort for price
    if (key === 'price') {
      return (Number(valA) - Number(valB)) * dir
    }

    // Date sort for scraped_at
    if (key === 'scraped_at') {
      return (new Date(valA) - new Date(valB)) * dir
    }

    // Alphabetical sort for everything else (name, currency, source)
    valA = String(valA ?? '').toLowerCase()
    valB = String(valB ?? '').toLowerCase()
    if (valA < valB) return -1 * dir
    if (valA > valB) return 1 * dir
    return 0
  })
})

const pageNumbers = computed(() => {
  const pages = []
  for (let i = 1; i <= props.totalPages; i++) pages.push(i)
  return pages
})

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
      currency: currency || 'GBP',
    }).format(price)
  } catch {
    // Fall back if currency code isn't recognized
    return `${currency ?? ''} ${Number(price).toFixed(2)}`
  }
}

const formatTimestamp = (date) => {
  if (!date) return '—'
  return new Date(date).toLocaleString()
}
</script>

<style scoped>
.data-table-wrapper {
  width: 100%;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border: 1px solid #E0DEEB;
  border-radius: 6px;
  overflow: hidden;
}

.data-table th {
  text-align: left;
  padding: 12px 16px;
  background: #F7F6FB;
  font-size: 13px;
  font-weight: 600;
  color: #4A4762;
  cursor: pointer;
  user-select: none;
  border-bottom: 1px solid #E0DEEB;
}

.data-table th:hover {
  color: #5B8C5A;
}

.sort-arrow {
  font-size: 10px;
  margin-left: 4px;
}

.data-table td {
  padding: 12px 16px;
  font-size: 14px;
  color: #333;
  border-bottom: 1px solid #F0EFF5;
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

.source-books {
  background: #EAF2EA;
  color: #4A7349;
}

.source-crypto {
  background: #E6F1F1;
  color: #2F6363;
}

/* Skeleton loading state */
.skeleton-cell {
  height: 14px;
  border-radius: 4px;
  background: linear-gradient(90deg, #F0EFF5 25%, #E4E2ED 50%, #F0EFF5 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

@keyframes shimmer {
  from { background-position: 200% 0; }
  to { background-position: -200% 0; }
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 40px 16px;
}

.empty-title {
  font-size: 15px;
  font-weight: 600;
  color: #4A4762;
  margin: 0 0 4px;
}

.empty-subtitle {
  font-size: 13px;
  color: #9E9BB0;
  margin: 0;
}

/* Error state */
.table-message.error-message {
  text-align: center;
  padding: 32px 16px;
  background: white;
  border: 1px solid #E0DEEB;
  border-radius: 6px;
  color: #C1666B;
}

.retry-btn {
  margin-top: 12px;
  padding: 8px 20px;
  border: none;
  border-radius: 6px;
  background: #C1666B;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.retry-btn:hover {
  background: #A85257;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-top: 16px;
}

.page-btn {
  padding: 6px 12px;
  border: 1px solid #E0DEEB;
  background: white;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  color: #4A4762;
}

.page-btn:hover:not(:disabled) {
  border-color: #5B8C5A;
  color: #5B8C5A;
}

.page-btn.active {
  background: #5B8C5A;
  border-color: #5B8C5A;
  color: white;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
