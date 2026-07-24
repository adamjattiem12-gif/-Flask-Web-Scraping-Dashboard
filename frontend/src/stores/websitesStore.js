import { defineStore } from 'pinia'

/**
 * websitesStore - Manages the list of monitored websites
 * Used by: WebsitesManager page
 * 
 * MOCK DATA NOTE: Week 1 uses hardcoded websites.
 * Week 2 will fetch from /api/websites
 */
export const useWebsitesStore = defineStore('websites', {
  state: () => ({
    websites: [],    // List of all monitored websites
    loading: false,
    error: null
  }),

  actions: {
    /**
     * fetchWebsites - Gets the list of websites being scraped
     * 
     * Week 1: Returns mock websites
     * Week 2: Will call /api/websites
     * 
     * Used by: WebsitesManager.vue on page load
     */
    async fetchWebsites() {
      this.loading = true
      this.error = null

      // Simulate network delay (remove in Week 2)
      await new Promise(resolve => setTimeout(resolve, 200))

      try {
        // ⚠️ WEEK 1: MOCK WEBSITES
        // Week 2: Replace with: const response = await fetch('/api/websites')
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
        this.loading = false
      } catch (error) {
        this.error = 'Failed to load websites'
        this.loading = false
      }
    }
  }
})