<!-- ============================================================ -->
<!-- FILE: frontend/src/components/Sidebar.vue                     -->
<!-- ============================================================ -->
<!-- All outline SVG icons — no emojis, no filled icons           -->
<template>
  <aside class="sidebar" :class="{ open: isOpen, collapsed: isCollapsed }">
    <div class="sidebar-header">
      <h1 class="logo">Market Pulse</h1>
      <p class="subtitle">PRICE MONITOR</p>
    </div>

    <!-- ✅ REMOVED: sidebar-close button entirely -->

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
        <span class="nav-icon" v-html="item.icon"></span>
        <span>{{ item.label }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <button class="sidebar-btn theme-toggle" @click="themeStore.toggle()">
        <span class="nav-icon" v-html="themeStore.theme === 'dark' ? sunIcon : moonIcon"></span>
        <span>{{ themeStore.theme === 'dark' ? 'Light' : 'Dark' }}</span>
      </button>
      <button class="sidebar-btn collapse-toggle" @click="handleCollapseToggle">
        <span class="nav-icon" v-html="isCollapsed ? expandIcon : collapseIcon"></span>
        <span>{{ isCollapsed ? 'Expand' : 'Collapse' }}</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useThemeStore } from '@/stores/themeStore'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  isCollapsed: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'toggle-collapse'])

const themeStore = useThemeStore()

const handleCollapseToggle = () => {
  if (window.innerWidth <= 768 && props.isOpen) {
    emit('close')
  }
  emit('toggle-collapse')
}

// ── ICONS ──
const dashboardIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>`

const retailIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>`

const digitalIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>`

const watchlistIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`

const historyIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`

const websitesIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`

const sunIcon = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`

const moonIcon = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`

const collapseIcon = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>`

const expandIcon = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>`

const navItems = [
  { path: '/', label: 'Dashboard', icon: dashboardIcon },
  { path: '/retail-goods', label: 'Retail Goods', icon: retailIcon },
  { path: '/digital-assets', label: 'Digital Assets', icon: digitalIcon },
  { path: '/watchlist', label: 'Watchlist', icon: watchlistIcon },
  { path: '/history', label: 'History', icon: historyIcon },
  { path: '/websites', label: 'Websites', icon: websitesIcon }
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
  transition: transform 0.3s ease, width 0.3s ease;
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar.collapsed .logo,
.sidebar.collapsed .subtitle,
.sidebar.collapsed .nav-label,
.sidebar.collapsed .nav-link span:last-child,
.sidebar.collapsed .sidebar-btn span:last-child {
  display: none;
}

.sidebar.collapsed .nav-link {
  justify-content: center;
  padding: 10px;
}

.sidebar.collapsed .nav-icon {
  width: auto;
}

.sidebar.collapsed .nav-icon svg {
  width: 24px;
  height: 24px;
}

.sidebar.collapsed .sidebar-header {
  padding: 0 16px 32px 16px;
}

.sidebar.collapsed .sidebar-footer {
  padding: 0 16px;
}

.sidebar.collapsed .sidebar-btn {
  justify-content: center;
  padding: 10px;
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

.nav-link.active .nav-icon {
  color: #FFFFFF;
}

.nav-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  color: #9E9BB0;
  flex-shrink: 0;
  transition: color 0.2s;
}

.nav-link:hover .nav-icon {
  color: #FFFFFF;
}

.nav-link.active .nav-icon {
  color: #FFFFFF;
}

.nav-icon svg {
  width: 20px;
  height: 20px;
  stroke: currentColor;
}

.sidebar-footer {
  padding: 0 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sidebar-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #9E9BB0;
  font-size: 14px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
}

.sidebar-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #FFFFFF;
  border-color: rgba(255, 255, 255, 0.2);
}

.sidebar-btn:hover .nav-icon {
  color: #FFFFFF;
}

/* ✅ NO sidebar-close styles anywhere */

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    width: 280px;
  }
  .sidebar.open {
    transform: translateX(0);
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.2);
  }
  .sidebar.collapsed {
    width: 280px;
  }
  .sidebar.collapsed .logo,
  .sidebar.collapsed .subtitle,
  .sidebar.collapsed .nav-label,
  .sidebar.collapsed .nav-link span:last-child,
  .sidebar.collapsed .sidebar-btn span:last-child {
    display: block;
  }
  .sidebar.collapsed .nav-link {
    justify-content: flex-start;
    padding: 10px 12px;
  }
  .sidebar.collapsed .nav-icon svg {
    width: 20px;
    height: 20px;
  }
  .sidebar.collapsed .sidebar-header {
    padding: 0 24px 32px 24px;
  }
  .sidebar.collapsed .sidebar-footer {
    padding: 0 12px;
  }
  .sidebar.collapsed .sidebar-btn {
    justify-content: flex-start;
    padding: 10px 12px;
  }
}
</style>