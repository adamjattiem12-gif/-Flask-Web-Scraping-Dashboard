import axios from 'axios'

// Base URL comes from the environment so the app doesn't break the moment
// it's deployed somewhere other than localhost. Falls back to the local
// Flask dev server default if VITE_API_URL isn't set.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Simple pub/sub so any part of the app (e.g. a connectivity banner) can
// react to the backend becoming unreachable/reachable without every store
// having to duplicate that logic.
const connectivityListeners = new Set()

export function onConnectivityChange(callback) {
  connectivityListeners.add(callback)
  return () => connectivityListeners.delete(callback)
}

function notifyConnectivity(isOnline) {
  connectivityListeners.forEach((cb) => cb(isOnline))
}

api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => {
    notifyConnectivity(true)
    return response
  },
  (error) => {
    let normalized
    if (error.response) {
      // Server responded, so the backend itself is reachable — this is an
      // application-level error (400/404/500), not a connectivity issue.
      notifyConnectivity(true)
      normalized = {
        error: error.response.data?.error || error.response.statusText,
        status: error.response.status,
      }
    } else if (error.request) {
      // Request was sent but no response came back — the backend is down
      // or unreachable.
      notifyConnectivity(false)
      normalized = {
        error: 'Waiting to connect to server...',
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
// EXPORT ALL FUNCTIONS
// ============================================================

export function fetchItems(page = 1, perPage = 20) {
  return api.get('/api/items', { params: { page, per_page: perPage } })
    .then((res) => res.data)
}

export function fetchStatistics() {
  return api.get('/api/statistics')
    .then((res) => res.data)
}

export function triggerScrape(market = null) {
  const body = market ? { market } : {}
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

export function createWebsite({ name, url, market, pathKeywords = null }) {
  const body = { name, url, market }
  if (pathKeywords) body.path_keywords = pathKeywords
  return api.post('/api/websites', body)
    .then((res) => res.data)
}

export function deleteWebsite(id) {
  return api.delete(`/api/websites/${id}`)
    .then((res) => res.data)
}

// Default export for convenience
export default api