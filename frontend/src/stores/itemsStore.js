import { defineStore } from 'pinia'

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
    itemHistory: {}      // Cache of historical prices per item ID
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
        // Fetch retail data from backend
        const retailResponse = await fetch('/api/items/retail')
        if (!retailResponse.ok) {
          throw new Error(`Retail API error: ${retailResponse.status}`)
        }
        const retailItems = await retailResponse.json()

        // Fetch crypto data from CoinPaprika via backend
        const cryptoResponse = await fetch('/api/items/crypto')
        if (!cryptoResponse.ok) {
          throw new Error(`Crypto API error: ${cryptoResponse.status}`)
        }
        const cryptoItems = await cryptoResponse.json()

        // Combine both datasets
        const allItems = [...retailItems, ...cryptoItems]
        
        // Store previous items before updating
        this.previousItems = [...this.items]
        
        // Process items with change calculation
        this.items = this.calculateChanges(allItems)
        this.filteredItems = this.items
        this.loading = false
        
        return this.items
      } catch (error) {
        this.error = `Failed to load items: ${error.message}`
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
            fetch('/api/items/retail'),
            fetch('/api/items/crypto')
          ])
          
          if (!retailRes.ok || !cryptoRes.ok) {
            throw new Error('Failed to fetch fresh data')
          }
          
          const retailItems = await retailRes.json()
          const cryptoItems = await cryptoRes.json()
          freshItems = [...retailItems, ...cryptoItems]
        }
        
        // Store previous items for change calculation
        this.previousItems = [...this.items]
        
        // Calculate changes and update
        this.items = this.calculateChanges(freshItems)
        this.filteredItems = this.items
        
        return this.items
      } catch (error) {
        this.error = `Failed to update items: ${error.message}`
        throw error
      }
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
      this.error = null
    }
  }
})