<template>
  <aside class="sidebar" :class="{ open: isOpen }">
    <div class="sidebar-header">
      <h1 class="logo">Market Pulse</h1>
      <p class="subtitle">PRICE MONITOR</p>
    </div>
    
    <button class="sidebar-close" @click="$emit('close')" aria-label="Close menu">
      ✕
    </button>
    
    <nav class="sidebar-nav">
      <p class="nav-label">NAVIGATION</p>
      <router-link 
        v-for="item in navItems" 
        :key="item.path"
        :to="item.path" 
        class="nav-link"
        active-class="active"
        exact
        @click="$emit('close')"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup>
defineProps({
  isOpen: { type: Boolean, default: false }
})

defineEmits(['close'])

const navItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/retail-goods', label: 'Retail Goods', icon: '🛍️' },
  { path: '/digital-assets', label: 'Digital Assets', icon: '₿' },
  { path: '/watchlist', label: 'Watchlist', icon: '⭐' },
  { path: '/history', label: 'History', icon: '📜' },
  { path: '/websites', label: 'Websites', icon: '🌐' }
]
</script>

<style scoped>
.sidebar {
  width: 240px;
  min-height: 100vh;
  background: #2D2A3E;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  padding: 32px 0;
  display: flex;
  flex-direction: column;
  z-index: 100;
  transition: transform 0.3s ease;
}

.sidebar-header {
  padding: 0 24px 32px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 24px;
}

.logo {
  color: #FFFFFF;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.subtitle {
  color: #9E9BB0;
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 4px;
}

.sidebar-nav {
  flex: 1;
  padding: 0 12px;
}

.nav-label {
  color: #9E9BB0;
  font-size: 11px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 0 12px 12px 12px;
  font-weight: 600;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  color: #9E9BB0;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 2px;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #FFFFFF;
}

.nav-link.active {
  color: #FFFFFF;
  background: rgba(255, 255, 255, 0.08);
  border-left: 3px solid #5B8C5A;
  border-radius: 8px 0 0 8px;
}

.nav-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.sidebar-close {
  display: none;
  position: absolute;
  top: 16px;
  right: 16px;
  background: none;
  border: none;
  color: #9E9BB0;
  font-size: 24px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.sidebar-close:hover {
  color: #FFFFFF;
  background: rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    width: 280px;
  }
  .sidebar.open {
    transform: translateX(0);
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.2);
  }
  .sidebar-close {
    display: block;
  }
}
</style>