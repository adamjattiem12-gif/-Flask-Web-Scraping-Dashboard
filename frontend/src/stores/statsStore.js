import { defineStore } from 'pinia'
import { fetchStatistics } from '../services/api'  // ✅ ADDED: Import real API function

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
     * fetchStats - Gets statistics for the dashboard
     * 
     * ✅ Week 2: Now calls REAL backend API
     * Falls back to mock data if API fails
     */
    async fetchStats() {
      this.loading = true
      this.error = null

      try {
        // 🟢 REAL API CALL - Get stats from backend
        const response = await fetchStatistics()
        this.stats = response
      } catch (error) {
        console.error('Stats API Error:', error)
        this.error = error.error || 'Failed to load statistics'
        
        // 🔄 FALLBACK: Use mock stats if API fails
        await this.loadMockStats()
      } finally {
        this.loading = false
      }
    },

    /**
     * loadMockStats - Fallback mock stats if API is down
     */
    async loadMockStats() {
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
    }
  }
})