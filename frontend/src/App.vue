<!-- ============================================================ -->
<!-- FILE: frontend/src/App.vue -->
<!-- ============================================================ -->
<!-- Sidebar can be collapsed on desktop via a toggle button in Sidebar.vue -->
<template>
  <div class="app-container">
    <div v-if="!connectivity.isOnline" class="connectivity-banner" role="alert">
      ⏳ Waiting to connect to server...
    </div>

    <!-- Hamburger button (mobile) -->
    <button
      class="hamburger-btn"
      @click="toggleSidebar"
      :class="{ active: sidebarOpen }"
      :aria-expanded="sidebarOpen"
      aria-label="Toggle menu"
    >
      <span></span>
      <span></span>
      <span></span>
    </button>

    <div
      class="sidebar-overlay"
      v-if="sidebarOpen"
      @click="closeSidebar"
    ></div>

    <Sidebar
      :is-open="sidebarOpen"
      :is-collapsed="sidebarCollapsed"
      @close="closeSidebar"
      @toggle-collapse="toggleCollapse"
    />

    <main class="main-content" :class="{
      'sidebar-open': sidebarOpen,
      'has-banner': !connectivity.isOnline,
      'sidebar-collapsed': sidebarCollapsed
    }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import { useThemeStore } from '@/stores/themeStore'
import { useConnectivityStore } from '@/stores/connectivityStore'

const theme = useThemeStore()
const connectivity = useConnectivityStore()

theme.init()
connectivity.init()

const sidebarOpen = ref(false)
const sidebarCollapsed = ref(false)

// Load collapsed state from localStorage
onMounted(() => {
  const saved = localStorage.getItem('sidebar-collapsed')
  if (saved !== null) {
    sidebarCollapsed.value = saved === 'true'
  }
})

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
  document.body.style.overflow = sidebarOpen.value ? 'hidden' : ''
}

const closeSidebar = () => {
  sidebarOpen.value = false
  document.body.style.overflow = ''
}

const toggleCollapse = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
  localStorage.setItem('sidebar-collapsed', String(sidebarCollapsed.value))
}

const handleEscape = (event) => {
  if (event.key === 'Escape' && sidebarOpen.value) {
    closeSidebar()
  }
}

const handleResize = () => {
  if (window.innerWidth > 768 && sidebarOpen.value) {
    closeSidebar()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
  window.removeEventListener('resize', handleResize)
  document.body.style.overflow = ''
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--color-bg);
  color: var(--color-text);
  transition: background 0.2s ease, color 0.2s ease;
}

.app-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  margin-left: 240px;
  min-height: 100vh;
  transition: margin-left 0.3s ease;
}

.main-content.sidebar-collapsed {
  margin-left: 64px;
}

.main-content.has-banner {
  padding-top: 44px;
}

.connectivity-banner {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 200;
  background: #B3261E;
  color: #ffffff;
  padding: 10px 16px;
  text-align: center;
  font-size: 0.9rem;
  font-weight: 600;
}

/* ── HAMBURGER BUTTON ── */
.hamburger-btn {
  display: none;
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 1000;
  background: #2D2A3E;
  border: none;
  border-radius: 8px;
  padding: 10px 12px;
  cursor: pointer;
  flex-direction: column;
  gap: 5px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.hamburger-btn:hover {
  background: #3D3A4E;
  transform: scale(1.05);
}

.hamburger-btn:active {
  transform: scale(0.95);
}

.hamburger-btn span {
  display: block;
  width: 24px;
  height: 2.5px;
  background: white;
  border-radius: 2px;
  transition: all 0.3s ease;
  transform-origin: center;
}

/* ✅ FIX: Hide hamburger button when sidebar is open (no X overlap) */
.hamburger-btn.active {
  display: none;
}

.sidebar-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
  .hamburger-btn {
    display: flex;
  }

  .sidebar-overlay {
    display: block;
  }

  .main-content {
    margin-left: 0;
    padding-top: 60px;
  }

  .main-content.sidebar-open {
    overflow: hidden;
  }

  .main-content.sidebar-collapsed {
    margin-left: 0;
  }

  .dashboard-header-bar {
    padding-left: 70px !important;
  }

  .dashboard-header-bar .header-left {
    padding-left: 4px;
  }
}
</style>