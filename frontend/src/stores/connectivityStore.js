import { defineStore } from 'pinia'
import { onConnectivityChange } from '../services/api'

/**
 * connectivityStore - Tracks whether the Flask backend is reachable.
 *
 * api.js emits connectivity events on every request based on whether a
 * response came back at all (not just whether it was a 2xx). This store
 * subscribes once and exposes a simple `isOnline` flag the UI can use to
 * show a "can't reach the server" banner instead of silently failing.
 */
export const useConnectivityStore = defineStore('connectivity', {
  state: () => ({
    isOnline: true,
    subscribed: false,
  }),

  actions: {
    init() {
      if (this.subscribed) return
      this.subscribed = true
      onConnectivityChange((online) => {
        this.isOnline = online
      })
    },
  },
})
