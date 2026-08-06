<!-- ============================================================ -->
<!-- FILE: frontend/src/views/History.vue -->
<!-- ============================================================ -->
<!-- Clean button styling, subtle pagination -->
<template>
<div class="history">
<div class="history-header">
<h2> Scrape History</h2>
<div class="header-actions">
<button
@click="exportCSV"
class="action-btn export-btn"
:disabled="!history.length || loading"
>
Export CSV
</button>
<button
@click="refreshHistory"
class="action-btn refresh-btn"
:disabled="loading"
>
⟳ Refresh
</button>
</div>
</div>
<p class="subtitle">Log of all past scraping runs</p>
<div class="scrape-section">
<ScrapeButton @scrape-complete="refreshHistory" />
</div>
<div v-if="loading" class="loading-state">
<div class="spinner"></div>
<p>Loading history...</p>
</div>
<div v-else-if="history.length === 0" class="empty-state">
<p> No history yet</p>
<p class="empty-sub">Run a scrape to see results here</p>
</div>
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
<tr v-for="record in paginatedHistory" :key="record.timestamp+ record.id">
<td>{{ formatDate(record.timestamp)}}</td>
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
{{ record.success ? ' Success' : ' Failed' }}
</span>
</td>
</tr>
</tbody>
</table>
</div>
<div v-if="totalPages > 1" class="pagination">
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
<div v-if="history.length > 0" class="pagination-info">
{{ ((currentPage - 1) * pageSize) + 1 }} – {{ Math.min(currentPage * pageSize, history.length) }}
of {{ history.length }}
</div>
</div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useScrapeStore } from '../stores/scrapeStore'
import ScrapeButton from '../components/ScrapeButton.vue'
import { exportToCSV } from '../utils/export'
const scrapeStore = useScrapeStore()
const history = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = 10
const totalPages = computed(() => Math.ceil(history.value.length / pageSize))
const pageNumbers = computed(() => {
const pages = []
for (let i = 1; i <= totalPages.value; i++) pages.push(i)
return pages
})
const paginatedHistory = computed(() => {
const start = (currentPage.value - 1) * pageSize
const end = start + pageSize
return history.value.slice(start, end)
})
const refreshHistory = async () => {
loading.value = true
try {
await scrapeStore.fetchHistory()
history.value = scrapeStore.scrapeHistory
currentPage.value = 1
} finally {
loading.value = false
}
}
const goToPage = (page) => {
if (page < 1 || page > totalPages.value) return
currentPage.value = page
}
const formatDate = (timestamp) => {
return new Date(timestamp).toLocaleString()
}
const exportCSV = () => {
if (!history.value.length) return
const rows = history.value.map(record => ({
'Date & Time': formatDate(record.timestamp),
'Market': record.market || 'N/A',
'Target': record.target || 'N/A',
'Items Found': record.items_found || 0,
'Status': record.success ? 'Success' : 'Failed'
}))
exportToCSV(rows, 'scrape-history')
}
onMounted(async () => {
loading.value = true
try {
await scrapeStore.fetchHistory()
history.value = scrapeStore.scrapeHistory
} finally {
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
.header-actions {
display: flex;
gap: 8px;
align-items: center;
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
.scrape-section {
margin: 16px 0 24px 0;
}
.action-btn {
padding: 8px 18px;
border: 1px solid var(--color-border);
border-radius: 6px;
background: var(--color-surface);
color: var(--color-text-secondary);
font-size: 13px;
font-weight: 500;
cursor: pointer;
font-family: inherit;
transition: all 0.2s;
}
.action-btn:hover:not(:disabled) {
background: var(--color-bg);
border-color: var(--color-border);
}
.action-btn:disabled {
opacity: 0.5;
cursor: not-allowed;
}
.export-btn {
border-color: var(--color-info);
color: var(--color-info);
}
.export-btn:hover:not(:disabled) {
background: var(--color-info-bg);
border-color: var(--color-info-strong);
color: var(--color-info-strong);
}
.refresh-btn:hover:not(:disabled) {
background: var(--color-border-subtle);
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
background: var(--color-warning-bg);
color: var(--color-warning-strong);
}
.badge-crypto {
background: var(--color-info-bg);
color: var(--color-info-strong);
}
.status-success {
color: var(--color-success);
font-weight: 500;
}
.status-error {
color: var(--color-danger);
font-weight: 500;
}
.pagination {
display: flex;
justify-content: center;
gap: 4px;
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
font-family: inherit;
transition: all 0.2s;
}
.page-btn:hover:not(:disabled) {
background: var(--color-bg);
border-color: var(--color-border);
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
.pagination-info {
text-align: center;
color: var(--color-text-muted);
font-size: 13px;
margin-top: 6px;
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
</style>
