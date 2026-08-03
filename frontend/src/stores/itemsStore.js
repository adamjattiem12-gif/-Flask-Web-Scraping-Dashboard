import { defineStore } from 'pinia'
import api from '../services/api'

/**
 * itemsStore - Manages all product/crypto items
 * Used by: Dashboard, DataTable, Watchlist, TopMovers
 * 
 * REAL API: Uses CoinPaprika for crypto data with real change calculations
 */
export const useItemsStore = defineStore('items', {
  state: () => ({
    items: [],           // All items from both markets
    loading: false,      // True when data is being fetched
    error: null,         // Error message if something fails
    previousItems: [],   // Store previous scrape data for change calculation
    itemHistory: {},     // Cache of historical prices per item ID
    // ✅ Search & filter state — kept together so all three criteria
    // (name search, source, price range) combine instead of one
    // overwriting the results of another.
    filters: {
      search: '',
      source: null,
      minPrice: null,
      maxPrice: null
    },
    // ✅ ADDED: Stats for 3D chart and summary
    stats: {
      total_items: 0,
      markets: {
        "Retail Goods": {
          item_count: 0,
          avg_price: 0
        },
        "Digital Assets": {
          item_count: 0,
          avg_price: 0
        }
      }
    }
  }),

  getters: {
    /**
     * getRetailItems - Filters items to only Retail Goods
     */
    getRetailItems: (state) => {
      return state.items.filter(item => item.market === 'Retail Goods')
    },
    
    /**
     * getCryptoItems - Filters items to only Digital Assets
     */
    getCryptoItems: (state) => {
      return state.items.filter(item => item.market === 'Digital Assets')
    },

    /**
     * getTopMovers - Returns top 5 items by price change magnitude
     */
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

    /**
     * getItemById - Returns a single item by ID
     */
    getItemById: (state) => (id) => {
      return state.items.find(item => item.id === id)
    },

    /**
     * filteredItems - Applies the current search text, source, and price
     * range filters together (rather than any one overwriting the others).
     * This is what the Dashboard's DataTable and pagination should read
     * from, so search/filter actions actually affect what's displayed.
     */
    filteredItems: (state) => {
      const { search, source, minPrice, maxPrice } = state.filters

      return state.items.filter(item => {
        if (search && !item.name.toLowerCase().includes(search.toLowerCase())) {
          return false
        }
        if (source && item.source !== source) {
          return false
        }
        if (minPrice !== null && minPrice !== undefined && minPrice !== '' && item.price < minPrice) {
          return false
        }
        if (maxPrice !== null && maxPrice !== undefined && maxPrice !== '' && item.price > maxPrice) {
          return false
        }
        return true
      })
    }
  },

  actions: {
    /**
     * fetchItems - Gets all items from REAL APIs
     * - Retail: WebScraper.io E-Commerce Sandbox
     * - Crypto: CoinPaprika API
     */
    async fetchItems() {
  this.loading = true
  this.error = null

  try {

      const response = await api.get('/api/display-items')

      const allItems = response.data
        
        // Store previous items before updating
        this.previousItems = [...this.items]
        
        // Process items with change calculation
        this.items = this.calculateChanges(allItems)
        
        // ✅ UPDATE STATS after items are loaded
        this.updateStats()
        
        this.loading = false
        
        return this.items
      } catch (error) {
        this.error = `Failed to load items: ${error.error || error.message}`
        this.loading = false
        throw error
      }
    },

    /**
     * calculateChanges - Calculates percentage changes for all items
     * @param {Array} newItems - Fresh items from API
     * @returns {Array} Items with change percentages
     */
    calculateChanges(newItems) {
      return newItems.map(item => {
        // Find previous price for this item
        const previousItem = this.findPreviousItem(item.id)
        const previousPrice = previousItem?.price ?? null
        
        // Calculate change percentage
        let change = 0
        if (previousPrice && previousPrice > 0) {
          change = ((item.price - previousPrice) / previousPrice) * 100
          // Round to 1 decimal place
          change = Math.round(change * 10) / 10
        }
        
        // If CoinPaprika provides 24h change, use that (it's more accurate)
        if (item.extra?.change_24h !== undefined && item.market === 'Digital Assets') {
          change = item.extra.change_24h
        }
        
        // If no previous data and no API change, keep as 0
        return {
          ...item,
          change: change,
          previous_price: previousPrice,
          scraped_at: new Date().toISOString()
        }
      })
    },

    /**
     * findPreviousItem - Finds an item from previous scrape data
     */
    findPreviousItem(id) {
      return this.previousItems.find(item => item.id === id) || null
    },

    /**
/**
 * updateItemsAfterScrape - Updates items after a scrape
 */
async updateItemsAfterScrape(newItems = null) {

  try {

    let freshItems = newItems

    // If nothing was passed in, load the current display items
    if (!freshItems) {

      const response = await api.get('/api/display-items')

      freshItems = response.data

    }

    // Store previous items for change calculation
    this.previousItems = [...this.items]

    // Update table
    this.items = this.calculateChanges(freshItems)

    // Update chart statistics
    this.updateStats()

    return this.items

  } catch (error) {

    this.error = `Failed to update items: ${error.message}`

    throw error

  }

},

    /**
     * ✅ updateStats - Calculates and updates stats for the 3D chart
     * Used by: fetchItems, updateItemsAfterScrape
     */
    updateStats() {
      const retailItems = this.getRetailItems || []
      const cryptoItems = this.getCryptoItems || []
      
      // Calculate retail stats
      let retailAvg = 0
      if (retailItems.length > 0) {
        const sum = retailItems.reduce((acc, item) => acc + (item.price || 0), 0)
        retailAvg = sum / retailItems.length
      }
      
      // Calculate crypto stats
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
      
      console.log('📊 Stats updated:', this.stats)
    },

    /**
     * setSearchQuery - Updates the name-search text.
     * Combines with any active source/price filters (via the
     * filteredItems getter) instead of overwriting them.
     */
    setSearchQuery(query) {
      this.filters.search = (query || '').trim()
    },

    /**
     * setFilters - Updates source/price-range filters from FilterPanel.
     * Combines with the active search text (via the filteredItems
     * getter) instead of overwriting it.
     */
    setFilters({ source = null, minPrice = null, maxPrice = null } = {}) {
      this.filters.source = source || null
      this.filters.minPrice = minPrice !== '' ? minPrice : null
      this.filters.maxPrice = maxPrice !== '' ? maxPrice : null
    },

    /**
     * clearFilters - Resets search text and source/price filters.
     */
    clearFilters() {
      this.filters = { search: '', source: null, minPrice: null, maxPrice: null }
    },

    /**
     * resetItems - Resets items to default
     */
    resetItems() {
      this.items = []
      this.previousItems = []
      this.itemHistory = {}
      this.filters = { search: '', source: null, minPrice: null, maxPrice: null }
      this.stats = {
        total_items: 0,
        markets: {
          "Retail Goods": { item_count: 0, avg_price: 0 },
          "Digital Assets": { item_count: 0, avg_price: 0 }
        }
      }
      this.error = null
    }
  }
})
