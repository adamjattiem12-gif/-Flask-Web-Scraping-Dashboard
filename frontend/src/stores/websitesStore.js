import { defineStore } from 'pinia'
import { fetchWebsites } from '../services/api'  // ✅ ADDED: Import real API function

export const useWebsitesStore = defineStore('websites', {
  state: () => ({
    websites: [],
    loading: false,
    error: null
  }),

  actions: {
    /**
     * fetchWebsites - Gets the list of websites being scraped
     * 
     * ✅ Week 2: Now calls REAL backend API
     * Falls back to mock if API fails
     */
    async fetchWebsites() {
      this.loading = true
      this.error = null

      try {
        // 🟢 REAL API CALL - Get websites from backend
        const response = await fetchWebsites()
        this.websites = response.websites || response
      } catch (error) {
        console.error('Websites API Error:', error)
        this.error = error.error || 'Failed to load websites'
        
        // 🔄 FALLBACK: Use mock websites if API fails
        await this.loadMockWebsites()
      } finally {
        this.loading = false
      }
    },

    /**
     * loadMockWebsites - Fallback mock websites if API is down
     */
    async loadMockWebsites() {
      this.websites = [
        {
          id: 1,
          name: 'WebScraper.io E-Commerce Sandbox',
          url: 'https://webscraper.io/test-sites/e-commerce/static',
          market: 'Retail Goods',
          status: 'active'
        },
        {
          id: 2,
          name: 'CoinGecko API',
          url: 'https://api.coingecko.com/api/v3',
          market: 'Digital Assets',
          status: 'active'
        }
      ]
    }
  }
})