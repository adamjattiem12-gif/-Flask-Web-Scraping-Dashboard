/**
 * api.js - API service for all backend calls
 * Handles: Items, Statistics, Scraping, Websites
 * Crypto data sourced from CoinPaprika
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

/**
 * fetchWithError - Helper for API calls with error handling
 */
async function fetchWithError(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  })
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.message || `API Error: ${response.status}`)
  }
  
  return response.json()
}

/**
 * Items API - Retail + CoinPaprika Crypto
 */
export const itemsApi = {
  /**
   * getAll - Gets all items (retail + crypto)
   */
  async getAll() {
    return fetchWithError('/api/items')
  },
  
  /**
   * getRetail - Gets retail items from WebScraper.io
   */
  async getRetail() {
    return fetchWithError('/api/items/retail')
  },
  
  /**
   * getCrypto - Gets crypto items from CoinPaprika
   * CoinPaprika tickers: BTC, ETH, BNB, SOL, ADA, DOGE, DOT, LINK, AVAX, MATIC
   */
  async getCrypto() {
    return fetchWithError('/api/items/crypto')
  },
  
  /**
   * getItem - Gets a single item by ID
   */
  async getItem(id) {
    return fetchWithError(`/api/items/${id}`)
  },
  
  /**
   * getHistory - Gets price history for an item
   */
  async getHistory(id) {
    return fetchWithError(`/api/items/${id}/history`)
  },
  
  /**
   * getChanges - Gets items with calculated changes
   */
  async getChanges() {
    return fetchWithError('/api/items/changes')
  }
}

/**
 * Statistics API
 */
export const statsApi = {
  async getStats() {
    return fetchWithError('/api/statistics')
  }
}

/**
 * Scrape API
 */
export const scrapeApi = {
  async triggerScrape() {
    return fetchWithError('/api/scrape', { method: 'POST' })
  },
  
  async getHistory(params = {}) {
    const query = new URLSearchParams(params).toString()
    return fetchWithError(`/api/history?${query}`)
  }
}

/**
 * Websites API
 */
export const websitesApi = {
  async getAll() {
    return fetchWithError('/api/websites')
  }
}

export default {
  items: itemsApi,
  stats: statsApi,
  scrape: scrapeApi,
  websites: websitesApi
}