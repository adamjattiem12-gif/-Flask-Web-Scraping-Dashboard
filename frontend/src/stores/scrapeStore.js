import { defineStore } from 'pinia'

export const useScrapeStore = defineStore('scrape', {
  state: () => ({
    status: 'idle',        // idle | loading | success | error
    message: '',
    lastScrape: null,
    error: null,
    scrapeHistory: []
  }),

  actions: {
  
    async triggerScrape() {
      this.status = 'loading'
      this.message = 'Scraping in progress...'
      this.error = null

      await new Promise(resolve => setTimeout(resolve, 2000))

      const success = Math.random() > 0.2

      if (success) {
        const itemsFound = Math.floor(Math.random() * 15) + 10
        this.status = 'success'
        this.message = `✓ Successfully scraped ${itemsFound} items!`
        this.lastScrape = new Date()
        
        this.scrapeHistory.unshift({
          timestamp: new Date(),
          market: 'All',
          target: 'All Markets',
          items_found: itemsFound,
          success: true
        })
      } else {
        this.status = 'error'
        this.error = 'Scrape failed: Connection timeout'
        this.message = '✗ Scrape failed - try again'
        
        this.scrapeHistory.unshift({
          timestamp: new Date(),
          market: 'All',
          target: 'All Markets',
          items_found: 0,
          success: false
        })
      }
    },

    resetStatus() {
      this.status = 'idle'
      this.message = ''
      this.error = null
    },

    generateMockHistory() {
      // Only generate if history is empty
      if (this.scrapeHistory.length > 0) {
        return
      }
      
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
            : 'CoinGecko',
          items_found: success ? Math.floor(Math.random() * 15) + 5 : 0,
          success: success
        })
      }
    },

    async fetchHistory() {
      // Week 2: Replace with real API call
      // const response = await fetch('/api/history')
      // this.scrapeHistory = await response.json()
      console.log('Week 2: Real history will be fetched from API')
    }
  }
})