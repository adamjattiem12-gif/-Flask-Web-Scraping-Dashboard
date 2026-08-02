import { defineStore } from 'pinia'
import { triggerScrape, fetchHistory } from '../services/api'  // ✅ ADDED: Import real API functions

export const useScrapeStore = defineStore('scrape', {
  state: () => ({
    status: 'idle',        // idle | loading | success | error
    message: '',
    lastScrape: null,
    error: null,
    scrapeHistory: []
  }),

  actions: {
    /**
     * triggerScrape - Runs the scraping process
     * 
     * ✅ Week 2: Now calls REAL backend API
     * Falls back to mock if API fails
     */
    async triggerScrape(market = null) {
      this.status = 'loading'
      this.message = 'Scraping in progress...'
      this.error = null

      try {
        // 🟢 REAL API CALL - Trigger scrape on backend
        // Passing `market` scrapes only that market (Retail Goods /
        // Digital Assets); omitting it scrapes both, as before.
        const response = await triggerScrape(market)

        this.status = 'success'
        this.message = `✓ ${response.message || 'Scraped successfully!'}`
        this.lastScrape = new Date()

        // Add a local entry immediately for instant UI feedback, then
        // sync with the backend's authoritative record via fetchHistory()
        // (called by the view after scrape-complete) so the two never
        // drift apart.
        this.scrapeHistory.unshift({
          timestamp: new Date(),
          market: market || response.market || 'All',
          target: response.target || market || 'All Markets',
          items_found: response.data?.total_count ?? response.items_found ?? 0,
          success: true
        })
      } catch (error) {
        console.error('Scrape API Error:', error)
        this.status = 'error'
        this.error = error.error || 'Scrape failed'
        this.message = '✗ Scrape failed - try again'

        this.scrapeHistory.unshift({
          timestamp: new Date(),
          market: market || 'All',
          target: market || 'All Markets',
          items_found: 0,
          success: false
        })
      }
    },

    /**
     * resetStatus - Resets button to idle state
     */
    resetStatus() {
      this.status = 'idle'
      this.message = ''
      this.error = null
    },

    /**
     * fetchHistory - Gets scrape history from API
     * 
     * ✅ Week 2: Now calls REAL backend API
     * Falls back to mock if API fails
     */
    async fetchHistory(limit = 50) {
      try {
        // 🟢 REAL API CALL - Get history from backend
        const response = await fetchHistory(limit)
        const records = response.history || response || []
        // Backend stores/returns records oldest-first; the rest of the UI
        // (and the optimistic entries added via unshift() in
        // triggerScrape) expect newest-first, so reverse here.
        this.scrapeHistory = [...records].reverse()
      } catch (error) {
        console.error('History API Error:', error)
        // 🔄 FALLBACK: Use mock history if API fails
        if (this.scrapeHistory.length === 0) {
          this.generateMockHistory()
        }
      }
    },

    /**
     * generateMockHistory - Fallback mock history if API is down
     */
    generateMockHistory() {
      if (this.scrapeHistory.length > 0) return
      
      const markets = ['Retail Goods', 'Digital Assets']
      const statuses = [true, true, true, true, false]
      
      for (let i = 0; i < 10; i++) {
        const date = new Date()
        date.setHours(date.getHours() - (i * 2))
        
        const success = statuses[i % statuses.length]
        this.scrapeHistory.push({
          timestamp: date,
          market: markets[i % markets.length],
          target: markets[i % markets.length] === 'Retail Goods' 
            ? 'WebScraper.io' 
            : 'CoinPaprika',
          items_found: success ? Math.floor(Math.random() * 15) + 5 : 0,
          success: success
        })
      }
    }
  }
})