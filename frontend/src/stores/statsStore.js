import { defineStore } from 'pinia'
import api from '@/services/api'

export const useStatsStore = defineStore('stats', {
  state: () => ({
    stats: {
      total_items: 0,
      active_sites: 0,
      success_rate: 0,
      last_scrape: null,
      markets: {}
    },
    loading: false,
    error: null
  }),

  actions: {
    /**
     * fetchStats - Gets statistics from REAL API
     */
    async fetchStats() {
      this.loading = true
      this.error = null

      try {
        // ✅ REAL API CALL
        const response = await api.stats.getStats()
        this.stats = response
        this.loading = false
        return this.stats
      } catch (error) {
        this.error = `Failed to load stats: ${error.message}`
        this.loading = false
        throw error
      }
    },

    /**
     * updateLastScrape - Updates the last scrape timestamp
     */
    updateLastScrape(timestamp = null) {
      const now = timestamp || new Date().toISOString()
      this.stats.last_scrape = now
      
      if (this.stats.markets) {
        Object.keys(this.stats.markets).forEach(key => {
          if (this.stats.markets[key]) {
            this.stats.markets[key].last_updated = now
          }
        })
      }
    },

    /**
     * resetStats - Resets stats to default
     */
    resetStats() {
      this.stats = {
        total_items: 0,
        active_sites: 0,
        success_rate: 0,
        last_scrape: null,
        markets: {}
      }
      this.error = null
    }
  },

  getters: {
    getTotalItems: (state) => state.stats.total_items || 0,
    getActiveSites: (state) => state.stats.active_sites || 0,
    getSuccessRate: (state) => {
      const rate = state.stats.success_rate || 0
      return typeof rate === 'number' ? rate + '%' : rate
    },
    getLastScrape: (state) => {
      const timestamp = state.stats.last_scrape
      if (!timestamp) return 'Never'
      try {
        const date = new Date(timestamp)
        if (isNaN(date.getTime())) return 'Never'
        return date.toLocaleString()
      } catch {
        return 'Never'
      }
    },
    getMarketStats: (state) => (marketName) => {
      return state.stats.markets?.[marketName] || {
        item_count: 0,
        avg_price: 0,
        last_updated: null
      }
    },
    getRetailStats: (state) => {
      return state.stats.markets?.['Retail Goods'] || {
        item_count: 0,
        avg_price: 0,
        last_updated: null
      }
    },
    getCryptoStats: (state) => {
      return state.stats.markets?.['Digital Assets'] || {
        item_count: 0,
        avg_price: 0,
        last_updated: null
      }
    }
  }
})