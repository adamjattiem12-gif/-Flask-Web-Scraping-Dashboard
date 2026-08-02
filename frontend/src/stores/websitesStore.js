import { defineStore } from 'pinia'
import { fetchWebsites, createWebsite, deleteWebsite } from '../services/api'

export const useWebsitesStore = defineStore('websites', {
  state: () => ({
    websites: [],
    loading: false,
    error: null,
    // Separate flags so the "add" form and the list-loading spinner don't
    // fight over the same loading state.
    saving: false,
    saveError: null,
    deletingId: null,
  }),

  actions: {
    /**
     * fetchWebsites - Gets the list of websites being scraped
     */
    async fetchWebsites() {
      this.loading = true
      this.error = null

      try {
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
     * addWebsite - Registers a new target website via POST /api/websites
     * and appends it to local state on success.
     */
    async addWebsite({ name, url, market, pathKeywords = null }) {
      this.saving = true
      this.saveError = null

      try {
        const newSite = await createWebsite({ name, url, market, pathKeywords })
        this.websites.push(newSite)
        return newSite
      } catch (error) {
        this.saveError = error.error || 'Failed to add website'
        throw error
      } finally {
        this.saving = false
      }
    },

    /**
     * removeWebsite - Deletes a website via DELETE /api/websites/<id>
     * and removes it from local state on success.
     */
    async removeWebsite(id) {
      this.deletingId = id
      this.error = null

      try {
        await deleteWebsite(id)
        this.websites = this.websites.filter((w) => w.id !== id)
      } catch (error) {
        this.error = error.error || 'Failed to remove website'
        throw error
      } finally {
        this.deletingId = null
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
