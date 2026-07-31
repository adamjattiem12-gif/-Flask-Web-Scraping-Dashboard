import { defineStore } from 'pinia'

/**
 * watchlistStore - Manages the user's watchlist (favorited items)
 * Used by: Watchlist component, DataTable (for star button)
 * 
 * This store works the same in Week 1 and Week 2
 */
export const useWatchlistStore = defineStore('watchlist', {
  state: () => ({
    watchedIds: loadWatchedIds()   // Array of item IDs that the user has favorited
  }),

  getters: {
    /**
     * isWatched - Checks if an item is in the watchlist
     * @param {number} id - The item ID
     * Used by: DataTable star button
     */
    isWatched: (state) => (id) => {
      return state.watchedIds.includes(id)
    },

    /**
     * watchCount - Returns how many items are in the watchlist
     * Used by: Watchlist header
     */
    watchCount: (state) => {
      return state.watchedIds.length
    },

    /**
     * getWatchedItems - Gets full item objects for all watched items
     * @param {object} itemsStore - The itemsStore instance
     * Used by: Watchlist component
     */
    getWatchedItems: (state) => {
      return (itemsStore) => {
        return itemsStore.items.filter(item => 
          state.watchedIds.includes(item.id)
        )
      }
    }
  },

  actions: {
    /**
     * toggleWatch - Adds or removes an item from the watchlist
     * @param {number} itemId - The item ID to toggle
     * Used by: DataTable star button, Watchlist remove button
     */
    toggleWatch(itemId) {
      const index = this.watchedIds.indexOf(itemId)
      if (index > -1) {
        // Already in watchlist → remove it
        this.watchedIds.splice(index, 1)
      } else {
        // Not in watchlist → add it
        this.watchedIds.push(itemId)
      }
      persistWatchedIds(this.watchedIds)
    },

    clearWatchlist() {
      this.watchedIds = []
      persistWatchedIds(this.watchedIds)
    }
  }
})

function loadWatchedIds() {
  if (typeof window === 'undefined') return []
  try {
    const stored = window.localStorage.getItem('dashboard-watchlist')
    return stored ? JSON.parse(stored) : []
  } catch {
    return []
  }
}

function persistWatchedIds(ids) {
  if (typeof window === 'undefined') return
  window.localStorage.setItem('dashboard-watchlist', JSON.stringify(ids))
}
