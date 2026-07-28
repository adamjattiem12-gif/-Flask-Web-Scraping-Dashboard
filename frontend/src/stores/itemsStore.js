import { defineStore } from 'pinia'

/**
 * itemsStore - Manages all product/crypto items
 * Used by: Dashboard, DataTable, Watchlist, TopMovers
 * 
 * MOCK DATA NOTE: Week 1 uses hardcoded data. 
 * Week 2 will replace this with real API calls.
 */
export const useItemsStore = defineStore('items', {
  state: () => ({
    items: [],           // All items from both markets
    filteredItems: [],   // Items after search/filter applied
    loading: false,      // True when data is being fetched
    error: null          // Error message if something fails
  }),

  getters: {
    /**
     * getRetailItems - Filters items to only Retail Goods
     * Used by: Dashboard market cards
     */
    getRetailItems: (state) => {
      return state.items.filter(item => item.market === 'Retail Goods')
    },
    
    /**
     * getCryptoItems - Filters items to only Digital Assets
     * Used by: Dashboard market cards
     */
    getCryptoItems: (state) => {
      return state.items.filter(item => item.market === 'Digital Assets')
    },

    /**
     * getTopMovers - Returns top 5 items by price change
     * Used by: TopMovers component (Rushin)
     */
    getTopMovers: (state) => {
      const itemsWithChange = state.items.filter(item => 
        item.extra?.change_24h !== undefined || item.change !== undefined
      )
      
      const sorted = [...itemsWithChange].sort((a, b) => {
        const changeA = a.extra?.change_24h ?? a.change ?? 0
        const changeB = b.extra?.change_24h ?? b.change ?? 0
        return Math.abs(changeB) - Math.abs(changeA)
      })
      
      return sorted.slice(0, 5).map((item, index) => ({
        rank: index + 1,
        symbol: item.symbol || item.name,
        name: item.name,
        change: item.extra?.change_24h ?? item.change ?? 0,
        price: item.price,
        market: item.market
      }))
    },

    /**
     * getItemById - Returns a single item by ID
     * Used by: Watchlist component (Chad)
     */
    getItemById: (state) => (id) => {
      return state.items.find(item => item.id === id)
    }
  },

  actions: {
    /**
     * fetchItems - Gets all items from the API
     * 
     * Week 1: Returns mock data (20 items)
     * Week 2: Will call the real backend API
     * 
     * Used by: App.vue on page load
     */
    async fetchItems() {
      this.loading = true
      this.error = null

      // Simulate network delay (remove this in Week 2)
      await new Promise(resolve => setTimeout(resolve, 500))

      try {
        // ⚠️ WEEK 1: MOCK DATA - 20 items (10 Retail + 10 Crypto)
        // Week 2: Replace this with: const response = await fetch('/api/items')
        this.items = [
          // ===== RETAIL GOODS (10 items) =====
          {
            id: 1,
            name: 'Asus VivoBook X441NA-GA190',
            price: 295.99,
            price_display: '$295.99',
            currency: 'USD',
            source: 'WebScraper.io E-Commerce',
            market: 'Retail Goods',
            scraped_at: '2026-07-20T14:30:00',
            extra: { rating: 4.5, review_count: 14 }
          },
          {
            id: 2,
            name: 'Apple iPhone 13 Pro Max 256GB',
            price: 1099.00,
            price_display: '$1,099.00',
            currency: 'USD',
            source: 'WebScraper.io E-Commerce',
            market: 'Retail Goods',
            scraped_at: '2026-07-20T14:30:00',
            extra: { rating: 4.8, review_count: 42 }
          },
          {
            id: 3,
            name: 'Samsung Galaxy S22 Ultra 512GB',
            price: 1199.00,
            price_display: '$1,199.00',
            currency: 'USD',
            source: 'WebScraper.io E-Commerce',
            market: 'Retail Goods',
            scraped_at: '2026-07-20T14:30:00',
            extra: { rating: 4.7, review_count: 38 }
          },
          {
            id: 4,
            name: 'Sony WH-1000XM4 Headphones',
            price: 348.00,
            price_display: '$348.00',
            currency: 'USD',
            source: 'WebScraper.io E-Commerce',
            market: 'Retail Goods',
            scraped_at: '2026-07-20T14:30:00',
            extra: { rating: 4.9, review_count: 56 }
          },
          {
            id: 5,
            name: 'Dell XPS 13 9310 Laptop',
            price: 1299.99,
            price_display: '$1,299.99',
            currency: 'USD',
            source: 'WebScraper.io E-Commerce',
            market: 'Retail Goods',
            scraped_at: '2026-07-20T14:30:00',
            extra: { rating: 4.6, review_count: 23 }
          },
          {
            id: 6,
            name: 'iPad Pro 12.9-inch 2022',
            price: 1099.00,
            price_display: '$1,099.00',
            currency: 'USD',
            source: 'WebScraper.io E-Commerce',
            market: 'Retail Goods',
            scraped_at: '2026-07-20T14:30:00',
            extra: { rating: 4.8, review_count: 31 }
          },
          {
            id: 7,
            name: 'Nintendo Switch OLED',
            price: 349.99,
            price_display: '$349.99',
            currency: 'USD',
            source: 'WebScraper.io E-Commerce',
            market: 'Retail Goods',
            scraped_at: '2026-07-20T14:30:00',
            extra: { rating: 4.7, review_count: 89 }
          },
          {
            id: 8,
            name: 'GoPro Hero 11 Black',
            price: 399.99,
            price_display: '$399.99',
            currency: 'USD',
            source: 'WebScraper.io E-Commerce',
            market: 'Retail Goods',
            scraped_at: '2026-07-20T14:30:00',
            extra: { rating: 4.4, review_count: 17 }
          },
          {
            id: 9,
            name: 'Kindle Paperwhite Signature',
            price: 189.99,
            price_display: '$189.99',
            currency: 'USD',
            source: 'WebScraper.io E-Commerce',
            market: 'Retail Goods',
            scraped_at: '2026-07-20T14:30:00',
            extra: { rating: 4.6, review_count: 45 }
          },
          {
            id: 10,
            name: 'Ring Video Doorbell Pro 2',
            price: 249.99,
            price_display: '$249.99',
            currency: 'USD',
            source: 'WebScraper.io E-Commerce',
            market: 'Retail Goods',
            scraped_at: '2026-07-20T14:30:00',
            extra: { rating: 4.3, review_count: 28 }
          },

          // ===== DIGITAL ASSETS (10 items) =====
          {
            id: 11,
            name: 'Bitcoin (BTC)',
            symbol: 'BTC',
            price: 29345.00,
            price_display: '$29,345.00',
            currency: 'USD',
            source: 'CoinGecko',
            market: 'Digital Assets',
            scraped_at: '2026-07-20T14:30:00',
            extra: { change_24h: 2.5, volume: 15000000000 }
          },
          {
            id: 12,
            name: 'Ethereum (ETH)',
            symbol: 'ETH',
            price: 1823.00,
            price_display: '$1,823.00',
            currency: 'USD',
            source: 'CoinGecko',
            market: 'Digital Assets',
            scraped_at: '2026-07-20T14:30:00',
            extra: { change_24h: -1.2, volume: 8000000000 }
          },
          {
            id: 13,
            name: 'Binance Coin (BNB)',
            symbol: 'BNB',
            price: 245.00,
            price_display: '$245.00',
            currency: 'USD',
            source: 'CoinGecko',
            market: 'Digital Assets',
            scraped_at: '2026-07-20T14:30:00',
            extra: { change_24h: 0.8, volume: 1200000000 }
          },
          {
            id: 14,
            name: 'Solana (SOL)',
            symbol: 'SOL',
            price: 24.50,
            price_display: '$24.50',
            currency: 'USD',
            source: 'CoinGecko',
            market: 'Digital Assets',
            scraped_at: '2026-07-20T14:30:00',
            extra: { change_24h: 5.3, volume: 450000000 }
          },
          {
            id: 15,
            name: 'Cardano (ADA)',
            symbol: 'ADA',
            price: 0.34,
            price_display: '$0.34',
            currency: 'USD',
            source: 'CoinGecko',
            market: 'Digital Assets',
            scraped_at: '2026-07-20T14:30:00',
            extra: { change_24h: -0.5, volume: 280000000 }
          },
          {
            id: 16,
            name: 'Dogecoin (DOGE)',
            symbol: 'DOGE',
            price: 0.08,
            price_display: '$0.08',
            currency: 'USD',
            source: 'CoinGecko',
            market: 'Digital Assets',
            scraped_at: '2026-07-20T14:30:00',
            extra: { change_24h: 3.2, volume: 350000000 }
          },
          {
            id: 17,
            name: 'Polkadot (DOT)',
            symbol: 'DOT',
            price: 5.67,
            price_display: '$5.67',
            currency: 'USD',
            source: 'CoinGecko',
            market: 'Digital Assets',
            scraped_at: '2026-07-20T14:30:00',
            extra: { change_24h: -2.1, volume: 180000000 }
          },
          {
            id: 18,
            name: 'Chainlink (LINK)',
            symbol: 'LINK',
            price: 12.34,
            price_display: '$12.34',
            currency: 'USD',
            source: 'CoinGecko',
            market: 'Digital Assets',
            scraped_at: '2026-07-20T14:30:00',
            extra: { change_24h: 1.7, volume: 220000000 }
          },
          {
            id: 19,
            name: 'Avalanche (AVAX)',
            symbol: 'AVAX',
            price: 18.90,
            price_display: '$18.90',
            currency: 'USD',
            source: 'CoinGecko',
            market: 'Digital Assets',
            scraped_at: '2026-07-20T14:30:00',
            extra: { change_24h: 4.1, volume: 160000000 }
          },
          {
            id: 20,
            name: 'Polygon (MATIC)',
            symbol: 'MATIC',
            price: 0.76,
            price_display: '$0.76',
            currency: 'USD',
            source: 'CoinGecko',
            market: 'Digital Assets',
            scraped_at: '2026-07-20T14:30:00',
            extra: { change_24h: -0.9, volume: 200000000 }
          }
        ]

        // Update filtered items to show everything initially
        this.filteredItems = this.items
        this.loading = false
        return this.items
      } catch (error) {
        // If anything fails, show error message
        this.error = 'Failed to load items'
        this.loading = false
        throw error
      }
    },

    /**
     * searchItems - Filters items by name
     * @param {string} query - The search term
     * Used by: SearchBar component (Rushin)
     */
    searchItems(query) {
      // If search is empty, show all items
      if (!query || query.trim() === '') {
        this.filteredItems = this.items
        return
      }

      // Filter items where name contains the search term (case insensitive)
      const searchTerm = query.toLowerCase().trim()
      this.filteredItems = this.items.filter(item =>
        item.name.toLowerCase().includes(searchTerm)
      )
    },

    /**
     * filterByMarket - Filters items by market type
     * @param {string} market - 'Retail Goods', 'Digital Assets', or 'All'
     * Used by: FilterPanel component (Rushin)
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
     * addItem - Adds a new item to the store
     * @param {Object} item - The item to add
     * Used by: Scraper after successful scrape
     */
    addItem(item) {
      this.items.push({
        ...item,
        scraped_at: new Date().toISOString()
      })
      this.filteredItems = this.items
    },

    /**
     * updateItem - Updates an existing item
     * @param {number} id - The item ID
     * @param {Object} updates - The fields to update
     * Used by: Scraper after successful scrape
     */
    updateItem(id, updates) {
      const index = this.items.findIndex(item => item.id === id)
      if (index !== -1) {
        this.items[index] = {
          ...this.items[index],
          ...updates,
          scraped_at: new Date().toISOString()
        }
        this.filteredItems = this.items
      }
    },

    /**
     * updateItemsAfterScrape - Updates all items with fresh data and timestamps
     * @param {Array} newItems - The fresh items from the API
     * Used by: Dashboard after scrape completes
     */
    updateItemsAfterScrape(newItems = null) {
      if (newItems) {
        // If new items provided, replace all items
        this.items = newItems.map(item => ({
          ...item,
          scraped_at: new Date().toISOString()
        }))
      } else {
        // Otherwise just update timestamps on existing items
        this.items = this.items.map(item => ({
          ...item,
          scraped_at: new Date().toISOString()
        }))
      }
      this.filteredItems = this.items
      return this.items
    },

    /**
     * resetItems - Resets items to default (empty)
     * Used by: Testing
     */
    resetItems() {
      this.items = []
      this.filteredItems = []
      this.error = null
    }
  }
})