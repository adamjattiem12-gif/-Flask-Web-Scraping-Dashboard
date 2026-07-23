import { defineStore } from 'pinia'

/**
 * statsStore - Manages dashboard statistics
 * Used by: Dashboard stat cards and market cards
 * 
 * MOCK DATA NOTE: Week 1 uses hardcoded stats.
 * Week 2 will calculate from real API data.
 */
export const useStatsStore = defineStore('stats', {
  state: () => ({
    stats: {
      total_items: 0,      // Total items across all markets
      active_sites: 0,     // Number of active scraping sources
      success_rate: 0,     // Percentage of successful scrapes
      last_scrape: null,   // Timestamp of last scrape
      markets: {}          // Breakdown by market (Retail, Crypto)
    },
    loading: false,
    error: null
  }),

  actions: {
    /**
     * fetchStats - Gets statistics for the dashboard
     * 
     * Week 1: Returns mock stats
     * Week 2: Will call /api/statistics
     * 
     * Used by: Dashboard.vue on page load
     */
    async fetchStats() {
      this.loading = true
      this.error = null

      // Simulate network delay (remove in Week 2)
      await new Promise(resolve => setTimeout(resolve, 300))

      try {
        // ⚠️ WEEK 1: MOCK STATS
        // Week 2: Replace with: const response = await fetch('/api/statistics')
        this.stats = {
          total_items: 20,
          active_sites: 2,
          success_rate: 96.5,
          last_scrape: '2026-07-20T14:30:00',
          markets: {
            'Retail Goods': {
              item_count: 10,
              avg_price: 683.19,
              last_updated: '2026-07-20T14:30:00'
            },
            'Digital Assets': {
              item_count: 10,
              avg_price: 3152.45,
              last_updated: '2026-07-20T14:30:00'
            }
          }
        }
        this.loading = false
      } catch (error) {
        this.error = 'Failed to load stats'
        this.loading = false
      }
    }
  }
})
