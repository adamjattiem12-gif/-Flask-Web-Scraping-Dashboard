import { defineStore } from 'pinia'

const STORAGE_KEY = 'market-pulse-theme'

function getInitialTheme() {
  const saved = window.localStorage.getItem(STORAGE_KEY)
  if (saved === 'dark' || saved === 'light') return saved
  // Respect the OS-level preference on first visit
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light'
}

/**
 * themeStore - Light/dark theme toggle.
 *
 * Applies a `data-theme` attribute to <html>, which the CSS variables in
 * style.css key off of. Persisted to localStorage so it survives reloads.
 */
export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme: 'light',
  }),

  actions: {
    init() {
      this.theme = getInitialTheme()
      this.apply()
    },

    toggle() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark'
      window.localStorage.setItem(STORAGE_KEY, this.theme)
      this.apply()
    },

    apply() {
      document.documentElement.setAttribute('data-theme', this.theme)
    },
  },
})
