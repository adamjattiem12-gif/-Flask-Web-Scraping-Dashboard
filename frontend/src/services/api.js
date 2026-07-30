import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    let normalized
    if (error.response) {
      normalized = {
        error: error.response.data?.error || error.response.statusText,
        status: error.response.status,
      }
    } else if (error.request) {
      normalized = {
        error: 'No response from server. Is Flask running?',
        status: 0,
      }
    } else {
      normalized = {
        error: error.message,
        status: 0,
      }
    }
    console.error('[API] Error:', normalized)
    return Promise.reject(normalized)
  }
)

// ============================================================
// :white_check_mark: EXPORT ALL FUNCTIONS
// ============================================================

export function fetchItems(page = 1, perPage = 20) {
  return api.get('/api/items', { params: { page, per_page: perPage } })
    .then((res) => res.data)
}

export function fetchStatistics() {
  return api.get('/api/statistics')
    .then((res) => res.data)
}

export function triggerScrape(target = null) {
  const body = target ? { target } : {}
  return api.post('/api/scrape', body)
    .then((res) => res.data)
}

export function fetchHistory(limit = null) {
  const params = limit ? { limit } : {}
  return api.get('/api/history', { params })
    .then((res) => res.data)
}

export function searchItems(query, market = null) {
  const params = market ? { q: query, market } : { q: query }
  return api.get('/api/search', { params })
    .then((res) => res.data)
}

export function fetchWebsites() {
  return api.get('/api/websites')
    .then((res) => res.data)
}

// Default export for convenience
export default api