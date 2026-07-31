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
    filteredItems: [],   // Items after search/filter applied
    loading: false,      // True when data is being fetched
    error: null,         // Error message if something fails
    previousItems: [],   // Store previous scrape data for change calculation
    itemHistory: {},     // Cache of historical prices per item ID
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
        const [retailResponse, cryptoResponse] = await Promise.all([
          api.get('/api/items', { params: { market: 'Retail Goods', per_page: 100 } }),
          api.get('/api/items', { params: { market: 'Digital Assets', per_page: 100 } })
        ])
        const retailItems = retailResponse.data.items
        const cryptoItems = cryptoResponse.data.items

        // Combine both datasets
        const allItems = [...retailItems, ...cryptoItems]
        
        // Store previous items before updating
        this.previousItems = [...this.items]
        
        // Process items with change calculation
        this.items = this.calculateChanges(allItems)
        this.filteredItems = this.items
        
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
     * updateItemsAfterScrape - Updates items after a scrape
     */
    async updateItemsAfterScrape(newItems = null) {
      try {
        let freshItems = newItems
        
        if (!freshItems) {
          // Fetch fresh data from both APIs
          const [retailRes, cryptoRes] = await Promise.all([
            api.get('/api/items', { params: { market: 'Retail Goods', per_page: 100 } }),
            api.get('/api/items', { params: { market: 'Digital Assets', per_page: 100 } })
          ])

          const retailItems = retailRes.data.items
          const cryptoItems = cryptoRes.data.items
          freshItems = [...retailItems, ...cryptoItems]
        }
        
        // Store previous items for change calculation
        this.previousItems = [...this.items]
        
        // Calculate changes and update
        this.items = this.calculateChanges(freshItems)
        this.filteredItems = this.items
        
        // ✅ UPDATE STATS after items are updated
        this.updateStats()
        
        return this.items
      } catch (error) {
        this.error = `Failed to update items: ${error.error || error.message}`
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
     * searchItems - Filters items by name
     */
    searchItems(query) {
      if (!query || query.trim() === '') {
        this.filteredItems = this.items
        return
      }

      const searchTerm = query.toLowerCase().trim()
      this.filteredItems = this.items.filter(item =>
        item.name.toLowerCase().includes(searchTerm)
      )
    },

    /**
     * filterByMarket - Filters items by market type
     */
    filterByMarket(market) {
      if (!market || market === 'All') {
        this.filteredItems = this.items
      } else {
        this.filteredItems = this.items.filter(item =>
          item.market === market
        )
      }
    },

    /**
     * resetItems - Resets items to default
     */
    resetItems() {
      this.items = []
      this.filteredItems = []
      this.previousItems = []
      this.itemHistory = {}
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
