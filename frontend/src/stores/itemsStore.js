import { defineStore } from 'pinia'
import { fetchItems } from '../services/api'

export const useItemsStore = defineStore('items', {
  state: () => ({
    items: [],
    filteredItems: [],
    loading: false,
    error: null
  }),

  getters: {
    getRetailItems: (state) => {
      return state.items.filter(item => item.market === 'Retail Goods')
    },
    getCryptoItems: (state) => {
      return state.items.filter(item => item.market === 'Digital Assets')
    }
  },

  actions: {
    /**
     * fetchItems - Gets all items from the API
     * ✅ Week 2: Now calls REAL backend API
     * 🔄 Falls back to mock data if API fails (Caleb's DataTable support)
     */
    async fetchItems() {
      this.loading = true
      this.error = null

      try {
        // ✅ REAL API CALL - Get items from backend
        const response = await fetchItems()
        this.items = response.items || response
        this.filteredItems = this.items
      } catch (error) {
        console.error('Items API Error:', error)
        this.error = error.error || 'Failed to load items'
        
        // 🔄 FALLBACK: Use mock data if API fails
        await this.loadMockData()
      } finally {
        this.loading = false
      }
    },

    /**
     * loadMockData - Fallback mock data if API is down
     * Used for development and testing
     * Includes Caleb's DataTable pagination support
     */
    async loadMockData() {
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
          price: 0.76,
          price_display: '$0.76',
          currency: 'USD',
          source: 'CoinGecko',
          market: 'Digital Assets',
          scraped_at: '2026-07-20T14:30:00',
          extra: { change_24h: -0.9, volume: 200000000 }
        }
      ]
      this.filteredItems = this.items
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
    }
  }
})