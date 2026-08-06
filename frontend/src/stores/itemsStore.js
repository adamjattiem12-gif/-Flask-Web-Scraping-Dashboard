// ============================================================
// FILE: frontend/src/stores/itemsStore.js
// ============================================================
// No fallback data — shows empty when no data exists
// Added clearItems() method for Refresh button
import { defineStore } from 'pinia'
import api from '../services/api'
export const useItemsStore = defineStore('items', {
state: () => ({
items: [],
loading: false,
error: null,
previousItems: [],
itemHistory: {},
filters: {
search: '',
source: null,
minPrice: null,
maxPrice: null
},
stats: {
total_items: 0,
markets: {
"Retail Goods": { item_count: 0, avg_price: 0 },
"Digital Assets": { item_count: 0, avg_price: 0 }
}
}
}),
getters: {
getRetailItems: (state) => {
return state.items.filter(item => item.market === 'Retail Goods')
},
getCryptoItems: (state) => {
return state.items.filter(item => item.market === 'Digital Assets')
},
getTopMovers: (state) => {
const itemsWithChange = state.items.filter(item =>
item.change !== undefined && item.change !== 0
)
const sorted = [...itemsWithChange].sort((a, b) => {
return Math.abs(b.change) - Math.abs(a.change)
})
return sorted.slice(0, 5).map((item, index) => ({
rank: index + 1,
symbol: item.symbol || item.name,
name: item.name,
change: item.change,
price: item.price,
market: item.market
}))
},
getItemById: (state) => (id) => {
return state.items.find(item => item.id === id)
},
filteredItems: (state) => {
const { search, source, minPrice, maxPrice } = state.filters
return state.items.filter(item => {
if (search && !item.name.toLowerCase().includes(search.toLowerCase())) {
return false
}
if (source && item.source !== source) {
return false
}
if (minPrice !== null && minPrice !== undefined && minPrice !== '' && item.price <
minPrice) {
return false
}
if (maxPrice !== null && maxPrice !== undefined && maxPrice !== '' && item.price >
maxPrice) {
return false
}
return true
})
}
},
actions: {
/**
* fetchItems - Gets all items from REAL APIs
* No fallback data — shows empty when API fails
*/
async fetchItems(keepFilters = false) {
this.loading = true
this.error = null
try {
if (!keepFilters) {
this.clearFilters()
console.log(' Filters cleared before fetch')
}
const [retailResponse, cryptoResponse] = await Promise.all([
api.get('/api/items', { params: { market: 'Retail Goods', per_page: 100 } }),
api.get('/api/items', { params: { market: 'Digital Assets', per_page: 100 } })
])
const retailItems = retailResponse.data.items || []
const cryptoItems = cryptoResponse.data.items || []
const allItems = [...retailItems, ...cryptoItems]
this.previousItems = [...this.items]
this.items = this.calculateChanges(allItems)
this.updateStats()
this.loading = false
return this.items
} catch (error) {
this.error = `Failed to load items: ${error.error || error.message}`
this.loading = false
// No fallback — keep empty
this.items = []
return this.items
}
},
/**
* calculateChanges - Calculates percentage changes for all items
*/
calculateChanges(newItems) {
return newItems.map(item => {
const previousItem = this.findPreviousItem(item.id)
const previousPrice = previousItem?.price ?? null
let change = 0
if (previousPrice && previousPrice > 0) {
change = ((item.price - previousPrice) / previousPrice) * 100
change = Math.round(change * 10) / 10
}
if (item.extra?.change_24h !== undefined && item.market === 'Digital Assets') {
change = item.extra.change_24h
}
return {
...item,
change: change,
previous_price: previousPrice,
scraped_at: new Date().toISOString()
}
})
},
findPreviousItem(id) {
return this.previousItems.find(item => item.id === id) || null
},
/**
* updateItemsAfterScrape - Updates items after a scrape
*/
async updateItemsAfterScrape(newItems = null) {
try {
let freshItems = newItems
if (!freshItems) {
const [retailRes, cryptoRes] = await Promise.all([
api.get('/api/items', { params: { market: 'Retail Goods', per_page: 100 } }),
api.get('/api/items', { params: { market: 'Digital Assets', per_page: 100 } })
])
freshItems = [...(retailRes.data.items || []), ...(cryptoRes.data.items || [])]
}
this.previousItems = [...this.items]
this.items = this.calculateChanges(freshItems)
this.updateStats()
this.clearFilters()
console.log(' Filters cleared after scrape')
return this.items
} catch (error) {
this.error = `Failed to update items: ${error.message}`
throw error
}
},
/**
* clearItems - Clears all items without fetching new ones
* Used by: Refresh button to show empty state
*/
clearItems() {
this.items = []
this.previousItems = []
this.stats = {
total_items: 0,
markets: {
"Retail Goods": { item_count: 0, avg_price: 0 },
"Digital Assets": { item_count: 0, avg_price: 0 }
}
}
this.error = null
console.log(' All items cleared (refresh)')
},
updateStats() {
const retailItems = this.getRetailItems || []
const cryptoItems = this.getCryptoItems || []
let retailAvg = 0
if (retailItems.length > 0) {
const sum = retailItems.reduce((acc, item) => acc + (item.price || 0), 0)
retailAvg = sum / retailItems.length
}
let cryptoAvg = 0
if (cryptoItems.length > 0) {
const sum = cryptoItems.reduce((acc, item) => acc + (item.price || 0), 0)
cryptoAvg = sum / cryptoItems.length
}
this.stats = {
total_items: this.items.length,
markets: {
"Retail Goods": {
item_count: retailItems.length,
avg_price: Math.round(retailAvg * 100) / 100
},
"Digital Assets": {
item_count: cryptoItems.length,
avg_price: Math.round(cryptoAvg * 100) / 100
}
}
}
console.log(' Stats updated:', this.stats)
},
setSearchQuery(query) {
this.filters.search = (query || '').trim()
console.log(' Search set to:', this.filters.search)
},
setFilters({ source = null, minPrice = null, maxPrice = null } = {}) {
this.filters.source = source || null
this.filters.minPrice = minPrice !== '' ? minPrice : null
this.filters.maxPrice = maxPrice !== '' ? maxPrice : null
console.log(' Filters set to:', this.filters)
},
clearFilters() {
this.filters = {
search: '',
source: null,
minPrice: null,
maxPrice: null
}
console.log(' All filters cleared')
},
resetItems() {
this.items = []
this.previousItems = []
this.itemHistory = {}
this.filters = {
search: '',
source: null,
minPrice: null,
maxPrice: null
}
this.stats = {
total_items: 0,
markets: {
"Retail Goods": { item_count: 0, avg_price: 0 },
"Digital Assets": { item_count: 0, avg_price: 0 }
}
}
this.error = null
console.log(' All items reset')
},
async refreshWithClearFilters() {
console.log(' Refreshing with filters cleared...')
this.clearFilters()
await this.fetchItems(true)
console.log(' Refresh complete')
}
}
})