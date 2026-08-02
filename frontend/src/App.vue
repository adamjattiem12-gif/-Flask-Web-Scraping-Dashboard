<template>
  <div class="app-container">
    <div v-if="!connectivity.isOnline" class="connectivity-banner" role="alert">
      ⚠️ Can't reach the Flask server. Is the backend running?
    </div>

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

    <Sidebar :is-open="sidebarOpen" @close="closeSidebar" />
    
    <main class="main-content" :class="{ 'sidebar-open': sidebarOpen, 'has-banner': !connectivity.isOnline }">
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

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
  document.body.style.overflow = sidebarOpen.value ? 'hidden' : ''
}

const closeSidebar = () => {
  sidebarOpen.value = false
  document.body.style.overflow = ''
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

.main-content.has-banner {
  padding-top: 44px;
}

.connectivity-banner {
  position: fixed;
  top: 0;
  left: 240px;
  right: 0;
  z-index: 200;
  background: #B3261E;
  color: #ffffff;
  padding: 10px 16px;
  text-align: center;
  font-size: 0.9rem;
  font-weight: 600;
}

@media (max-width: 768px) {
  .connectivity-banner {
    left: 0;
  }
}

.hamburger-btn {
  display: none;
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 1000;
  background: var(--color-sidebar);
  border: none;
  border-radius: 8px;
  padding: 10px 12px;
  cursor: pointer;
  flex-direction: column;
  gap: 5px;
  transition: all 0.3s ease;
}

.hamburger-btn:hover {
  background: var(--color-sidebar);
  opacity: 0.85;
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

.hamburger-btn.active span:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.hamburger-btn.active span:nth-child(2) {
  opacity: 0;
  transform: scaleX(0);
}

.hamburger-btn.active span:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

.sidebar-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgb(0 0 0 / 50%);
  z-index: 99;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

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
}
</style>