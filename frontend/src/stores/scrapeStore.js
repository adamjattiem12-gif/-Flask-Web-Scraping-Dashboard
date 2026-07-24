import { defineStore } from 'pinia'

/**
 * scrapeStore - Manages scraping status and history
 * Used by: ScrapeButton, History page
 * 
 * MOCK DATA NOTE: Week 1 simulates scraping with random success/fail.
 * Week 2 will call the real POST /api/scrape endpoint.
 */
export const useScrapeStore = defineStore('scrape', {
  state: () => ({
    status: 'idle',        // Possible: idle | loading | success | error
    message: '',           // Status message to show user
    lastScrape: null,      // When the last scrape happened
    error: null,           // Error message if scrape fails
    scrapeHistory: []      // List of all past scrapes (for History page)
  }),

  actions: {
    /**
     * triggerScrape - Runs the scraping process
     * 
     * Week 1: Simulates scraping (2 second delay, random success)
     * Week 2: Will POST to /api/scrape
     * 
     * Used by: ScrapeButton.vue when clicked
     */
    async triggerScrape() {
      // 1. Set state to loading
      this.status = 'loading'
      this.message = 'Scraping in progress...'
      this.error = null

      // 2. Simulate scraping delay (remove in Week 2)
      await new Promise(resolve => setTimeout(resolve, 2000))

      // 3. Simulate success/failure (80% success rate)
      // Week 2: Replace with real API call
      const success = Math.random() > 0.2

      if (success) {
        // ✅ SUCCESS
        const itemsFound = Math.floor(Math.random() * 15) + 10
        this.status = 'success'
        this.message = `✓ Successfully scraped ${itemsFound} items!`
        this.lastScrape = new Date()
        
        // Add to history
        this.scrapeHistory.unshift({
          timestamp: new Date(),
          market: 'All',
          target: 'All Markets',
          items_found: itemsFound,
          success: true
        })
      } else {
        // ❌ FAILURE
        this.status = 'error'
        this.error = 'Scrape failed: Connection timeout'
        this.message = '✗ Scrape failed - try again'
        
        // Add to history
        this.scrapeHistory.unshift({
          timestamp: new Date(),
          market: 'All',
          target: 'All Markets',
          items_found: 0,
          success: false
        })
      }
    },

    /**
     * resetStatus - Resets button to idle state
     * Used by: ScrapeButton after 5 seconds (auto-reset)
     */
    resetStatus() {
      this.status = 'idle'
      this.message = ''
      this.error = null
    },

    /**
     * generateMockHistory - Creates sample history for display
     * Used by: History.vue on page load (Week 1 only)
     * 
     * Week 2: This will be replaced with real data from /api/history
     */
    generateMockHistory() {
      const markets = ['Retail Goods', 'Digital Assets']
      const statuses = [true, true, true, true, false] // 80% success rate
      
      // Generate 10 history entries
      for (let i = 0; i < 10; i++) {
        const date = new Date()
        date.setHours(date.getHours() - (i * 2)) // Each entry 2 hours apart
        
        const success = statuses[i % statuses.length]
        this.scrapeHistory.push({
          timestamp: date,
          market: markets[i % markets.length],
          target: markets[i % markets.length] === 'Retail Goods' 
            ? 'WebScraper.io' 
            : 'CoinGecko',
          items_found: success ? Math.floor(Math.random() * 15) + 5 : 0,
          success: success
        })
      }
    }
  }
})