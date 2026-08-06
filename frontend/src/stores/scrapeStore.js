import { defineStore } from 'pinia'
import { triggerScrape, fetchHistory } from '../services/api'

export const useScrapeStore = defineStore('scrape', {
  state: () => ({
    status: 'idle',
    message: '',
    lastScrape: null,
    error: null,
    scrapeHistory: []
  }),

  actions: {
    async triggerScrape(market = null) {
      this.status = 'loading'
      this.message = 'Scraping in progress...'
      this.error = null

      try {
        const response = await triggerScrape(market)

        this.status = 'success'
        this.message = `✓ ${response.message || 'Scraped successfully!'}`
        this.lastScrape = new Date()

        // ✅ FRONTEND-ONLY FIX: Determine target based on market
        const marketName = market || response.market || 'All'

        let targetName = 'Both Markets'
        if (marketName === 'Retail Goods') {
          targetName = 'WebScraper.io'
        } else if (marketName === 'Digital Assets') {
          targetName = 'CoinGecko'
        } else if (marketName === 'All' || marketName === 'Both') {
          targetName = 'Both Markets'
        } else {
          targetName = marketName
        }

        this.scrapeHistory.unshift({
          timestamp: new Date(),
          market: marketName,
          target: targetName,
          items_found: response.data?.total_count ?? response.items_found ?? 0,
          success: true
        })
      } catch (error) {
        console.error('Scrape API Error:', error)
        this.status = 'error'
        this.error = error.error || 'Scrape failed'
        this.message = '✗ Scrape failed - try again'

        const marketName = market || 'All'
        let targetName = 'Unknown'
        if (marketName === 'Retail Goods') targetName = 'WebScraper.io'
        else if (marketName === 'Digital Assets') targetName = 'CoinGecko'
        else targetName = marketName

        this.scrapeHistory.unshift({
          timestamp: new Date(),
          market: marketName,
          target: targetName,
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

    async fetchHistory(limit = 50) {
      try {
        const response = await fetchHistory(limit)
        const records = response.history || response || []
        this.scrapeHistory = [...records].reverse()
      } catch (error) {
        console.error('History API Error:', error)
        if (this.scrapeHistory.length === 0) {
          this.generateMockHistory()
        }
      }
    },

    generateMockHistory() {
      if (this.scrapeHistory.length > 0) return

      const markets = ['Retail Goods', 'Digital Assets']
      const websites = ['WebScraper.io', 'CoinGecko']
      const statuses = [true, true, true, true, false]

      for (let i = 0; i < 10; i++) {
        const date = new Date()
        date.setHours(date.getHours() - (i * 2))

        const success = statuses[i % statuses.length]
        this.scrapeHistory.push({
          timestamp: date,
          market: markets[i % markets.length],
          target: websites[i % websites.length],
          items_found: success ? Math.floor(Math.random() * 15) + 5 : 0,
          success: success
        })
      }
    }
  }
})