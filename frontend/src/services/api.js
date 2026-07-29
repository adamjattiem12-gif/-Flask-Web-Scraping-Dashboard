// API client configuration will live here.
import axios from 'axios'

// Axios instance pointed at the Flask backend
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor — simple logging so we can see every outgoing call
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`, config.params || config.data || '')
    return config
  },
  (error) => {
    console.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor — normalize all errors into a consistent shape
// { error: 'message', status: code }
api.interceptors.response.use(
  (response) => response,
  (error) => {
    let normalized

    if (error.response) {
      // Server responded with a non-2xx status
      normalized = {
        error: error.response.data?.error || error.response.statusText || 'Request failed',
        status: error.response.status,
      }
    } else if (error.request) {
      // Request was made but no response received (server down, network issue, etc)
      normalized = {
        error: 'No response from server. Is the Flask API running?',
        status: 0,
      }
    } else {
      // Something went wrong setting up the request
      normalized = {
        error: error.message || 'Unexpected request error',
        status: 0,
      }
    }

    console.error('[API] Response error:', normalized)
    return Promise.reject(normalized)
  }
)

/**
 * GET /api/items
 * Supports pagination via page and per_page query params
 */
export function fetchItems(page = 1, perPage = 20) {
  return api.get('/api/items', { params: { page, per_page: perPage } })
    .then((res) => res.data.items)
}

/**
 * GET /api/statistics
 */
export function fetchStatistics() {
  return api.get('/api/statistics')
    .then((res) => res.data)
}

/**
 * POST /api/scrape
 * target is optional — omit to scrape both sources
 */
export function triggerScrape(target = null) {
  const body = target ? { target } : {}
  return api.post('/api/scrape', body)
    .then((res) => res.data)
}

/**
 * GET /api/history
 * limit is optional
 */
export function fetchHistory(limit = null) {
  const params = limit ? { limit } : {}
  return api.get('/api/history', { params })
    .then((res) => res.data)
}

/**
 * GET /api/search?q=
 * source is optional — filter to 'books' or 'crypto'
 */
export function searchItems(query, source = null) {
  const params = source ? { q: query, source } : { q: query }
  return api.get('/api/search', { params })
    .then((res) => res.data)
}

/**
 * GET /api/websites
 */
export function fetchWebsites() {
  return api.get('/api/websites')
    .then((res) => res.data)
}

/**
 * POST /api/websites
 * site = { name, url }
 */
export function addWebsite(site) {
  return api.post('/api/websites', site)
    .then((res) => res.data)
}

export default api