<template>
  <div class="data-table">
    <div class="data-table__header">
      <h3 class="data-table__title">Recent Items</h3>
      <span class="data-table__count" v-if="!loading && !error">
        {{ totalCount }} item{{ totalCount === 1 ? '' : 's' }}
      </span>
    </div>

    <!-- Loading state: 5 skeleton rows -->
    <div v-if="loading" class="data-table__skeleton">
      <div class="skeleton-row" v-for="n in 5" :key="n">
        <div class="skeleton-cell" v-for="c in 5" :key="c"></div>
      </div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="data-table__state data-table__state--error">
      <p>Couldn't load items.</p>
      <span class="data-table__error-detail">{{ error }}</span>
      <button class="retry-btn" @click="$emit('retry')">Try again</button>
    </div>

    <!-- Empty state -->
    <div v-else-if="!sortedItems.length" class="data-table__state">
      <p>No items to show.</p>
      <span class="data-table__error-detail">Run a scrape or adjust your filters.</span>
    </div>

    <!-- Populated state -->
    <table v-else class="data-table__table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" @click="toggleSort(col)" :class="{ sortable: col.sortable }">
            {{ col.label }}
            <span v-if="col.sortable" class="sort-arrow" :class="{ active: sortKey === col.key }">
              {{ sortKey === col.key ? (sortDir === 'asc' ? '▲' : '▼') : '↕' }}
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in pagedItems" :key="item.id">
          <td>{{ item.name }}</td>
          <td>{{ item.price_display }}</td>
          <td>
            <span class="market-badge" :class="marketClass(item.market)">{{ item.market }}</span>
          </td>
          <td>{{ item.source }}</td>
          <td>{{ formatDate(item.scraped_at) }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div v-if="!loading && !error && sortedItems.length" class="data-table__pagination">
      <button :disabled="page === 1" @click="page--">Prev</button>
      <span>Page {{ page }} of {{ totalPages }}</span>
      <button :disabled="page === totalPages" @click="page++">Next</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
  pageSize: { type: Number, default: 10 },
})

defineEmits(['retry'])

const columns = [
  { key: 'name', label: 'Name', sortable: true },
  { key: 'price', label: 'Price', sortable: true },
  { key: 'market', label: 'Market', sortable: false },
  { key: 'source', label: 'Source', sortable: false },
  { key: 'scraped_at', label: 'Scraped', sortable: false },
]

const sortKey = ref('')
const sortDir = ref('asc')
const page = ref(1)

function toggleSort(col) {
  if (!col.sortable) return
  if (sortKey.value === col.key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = col.key
    sortDir.value = 'asc'
  }
}

const sortedItems = computed(() => {
  const list = [...props.items]
  if (!sortKey.value) return list
  return list.sort((a, b) => {
    let av = a[sortKey.value]
    let bv = b[sortKey.value]
    if (sortKey.value === 'name') {
      av = av.toLowerCase()
      bv = bv.toLowerCase()
    }
    if (av < bv) return sortDir.value === 'asc' ? -1 : 1
    if (av > bv) return sortDir.value === 'asc' ? 1 : -1
    return 0
  })
})

const totalCount = computed(() => sortedItems.value.length)
const totalPages = computed(() => Math.max(1, Math.ceil(totalCount.value / props.pageSize)))

const pagedItems = computed(() => {
  const start = (page.value - 1) * props.pageSize
  return sortedItems.value.slice(start, start + props.pageSize)
})

// Reset to page 1 whenever the underlying item set changes (new search/filter/scrape)
watch(() => props.items, () => { page.value = 1 })

function marketClass(market) {
  return market === 'Retail Goods' ? 'market-badge--retail' : 'market-badge--digital'
}

function formatDate(iso) {
  const d = new Date(iso)
  return d.toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.data-table {
  background: #FFFFFF;
  border: 1px solid #E5E2DD;
  border-radius: 8px;
  padding: 24px;
}

.data-table__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.data-table__title {
  color: #2D2A3E;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.data-table__count {
  color: #5C5A6B;
  font-size: 13px;
}

.data-table__table {
  width: 100%;
  border-collapse: collapse;
}

.data-table__table th {
  text-align: left;
  color: #5C5A6B;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  padding: 10px 12px;
  border-bottom: 1px solid #E5E2DD;
  user-select: none;
}

.data-table__table th.sortable {
  cursor: pointer;
}

.sort-arrow {
  font-size: 10px;
  color: #9E9BB0;
  margin-left: 4px;
}

.sort-arrow.active {
  color: #5B8C5A;
}

.data-table__table td {
  padding: 12px;
  border-bottom: 1px solid #F7F5F2;
  color: #2D2A3E;
  font-size: 14px;
}

.market-badge {
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  color: #FFFFFF;
}

.market-badge--retail { background: #D4914A; }
.market-badge--digital { background: #4A8C8C; }

.data-table__pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
  color: #5C5A6B;
  font-size: 13px;
}

.data-table__pagination button {
  background: #5B8C5A;
  color: #FFFFFF;
  border: none;
  border-radius: 6px;
  padding: 6px 12px;
  cursor: pointer;
}

.data-table__pagination button:hover { background: #4A7349; }
.data-table__pagination button:disabled {
  background: #E5E2DD;
  color: #9E9BB0;
  cursor: not-allowed;
}

.data-table__state {
  text-align: center;
  padding: 40px 20px;
  color: #5C5A6B;
}

.data-table__state--error { color: #C1666B; }

.data-table__error-detail {
  display: block;
  font-size: 13px;
  color: #9E9BB0;
  margin-top: 4px;
}

.retry-btn {
  margin-top: 12px;
  background: #5B8C5A;
  color: #FFFFFF;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  cursor: pointer;
}

.retry-btn:hover { background: #4A7349; }

/* Skeleton loading rows */
.data-table__skeleton {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton-row {
  display: flex;
  gap: 12px;
}

.skeleton-cell {
  height: 16px;
  flex: 1;
  border-radius: 4px;
  background: linear-gradient(90deg, #F7F5F2 25%, #E5E2DD 50%, #F7F5F2 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
